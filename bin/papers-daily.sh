#!/usr/bin/env bash
# papers-daily.sh — Jornal de papers do Hugging Face em duas passadas.
#
# Passada 1 — geração, cron 22:00 BRT (também manual):
#   bash ~/papers-journal/bin/papers-daily.sh "$(date +%F)"
#   Gera a edição do dia com snapshot de IDs+upvotes no front-matter.
#   Edição já existente só é regenerada em mudança material (diff de IDs ou
#   delta absoluto >= 5 upvotes desde a última versão publicada); sem mudança,
#   silêncio.
# Passada 2 — reconciliação, cron 07:00 BRT (sem argumento):
#   bash ~/papers-journal/bin/papers-daily.sh
#   Diferencia a janela D-1..D-3 contra a última versão publicada: regenera o
#   que mudou materialmente, faz backfill do que falta e silencia no dia comum.
#
# Exit codes vindos de journal.py:
#   0 jornal escrito/reconciliado | 1 config | 2 rede/API | 3 asserção de sanidade
#   4 sem publicação no dia ou janela vazia (fim de semana) — não é falha, não notifica
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$(readlink -f "$0")")/.." && pwd)"
export PAPERS_HOME="${PAPERS_HOME:-${PROJECT_ROOT}}"
DATA_DIR="${PAPERS_DATA_DIR:-${PAPERS_HOME}}"

LOG_FILE="${DATA_DIR}/papers.log"
JOURNAL_BIN="${PROJECT_ROOT}/src/journal.py"

# Segredos ficam fora do versionamento: um topico ntfy e protegido apenas por
# ser dificil de adivinhar, entao publica-lo equivaleria a torna-lo aberto.
if [ -f "${PROJECT_ROOT}/.env" ]; then
  set -a; . "${PROJECT_ROOT}/.env"; set +a
fi
NTFY_TOPIC="${PAPERS_NTFY_TOPIC:-}"
PAGES_URL="${PAPERS_PAGES_URL:-https://pavani06.github.io/papers-journal/}"

# Cron entrega PATH=/usr/bin:/bin. O projeto usa apenas stdlib, entao o python
# do sistema basta — nao ha dependencia de nvm como no reflect-daily.
PYTHON_BIN="$(command -v python3 || echo /usr/bin/python3)"

mkdir -p "${DATA_DIR}"
touch "${LOG_FILE}" 2>/dev/null || true
chmod 600 "${LOG_FILE}" 2>/dev/null || true

log() {
  local level="$1"; shift
  echo "[$(date -Iseconds)] [${level}] $*" | tee -a "${LOG_FILE}"
}

notificar() {
  local titulo="$1" prioridade="$2" tag="$3" corpo="$4"
  [ -z "${NTFY_TOPIC}" ] && return 0
  curl -s -o /dev/null \
    -H "Title: ${titulo}" -H "Priority: ${prioridade}" -H "Tags: ${tag}" \
    -d "${corpo}" "${NTFY_TOPIC}" 2>/dev/null \
    || log "WARN" "ntfy falhou"
}

# Publicar e secundario: a edicao ja esta em disco quando isto roda. Falha aqui
# avisa, mas nunca derruba o jornal do dia.
publicar() {
  local rotulo="$1"; shift
  git -C "${PROJECT_ROOT}" remote get-url origin >/dev/null 2>&1 || return 0

  # Os artefatos nascem sob DATA_DIR, mas o git opera em PROJECT_ROOT, e
  # PAPERS_DATA_DIR pode divergir (:22, src/paths.py:34). Com os dados fora do
  # repo, o staging antigo ("add edicoes docs deep") stageava nada — ou stageava
  # outra coisa — em silencio. Fail-closed e reportado.
  local data_real root_real dentro=0
  data_real="$(cd "${DATA_DIR}" 2>/dev/null && pwd -P || true)"
  root_real="$(cd "${PROJECT_ROOT}" 2>/dev/null && pwd -P || true)"
  if [ -n "${data_real}" ] && [ -n "${root_real}" ]; then
    case "${data_real}/" in "${root_real}/"*) dentro=1 ;; esac
  fi
  if [ "${dentro}" -eq 0 ]; then
    log "WARN" "dados fora do worktree; publicacao desativada"
    return 0
  fi

  # O cron stagea SO o que ele mesmo produz. deep/, docs/deep/, registro e MOC
  # tem outro produtor e ficam fora por construcao — ver src/paths.py:publicaveis.
  # Lista vazia nao e erro: cai no "Nada novo para publicar" logo abaixo.
  local -a alvos=()
  mapfile -t alvos < <("${PYTHON_BIN}" "${PROJECT_ROOT}/src/paths.py" \
    --publicaveis "$@" 2>>"${LOG_FILE}" || true)
  if [ "${#alvos[@]}" -gt 0 ]; then
    git -C "${PROJECT_ROOT}" add -- "${alvos[@]}" 2>/dev/null || true
  fi

  if git -C "${PROJECT_ROOT}" diff --cached --quiet 2>/dev/null; then
    log "INFO" "Nada novo para publicar."
    return 0
  fi
  if ! git -C "${PROJECT_ROOT}" commit -q -m "Edição de ${rotulo}" 2>>"${LOG_FILE}"; then
    log "WARN" "commit falhou; edicao permanece local"
    return 0
  fi
  if GIT_TERMINAL_PROMPT=0 git -C "${PROJECT_ROOT}" push -q origin HEAD 2>>"${LOG_FILE}"; then
    log "INFO" "Publicado: ${PAGES_URL}"
  else
    log "WARN" "push falhou; commit ficou local e sobe no proximo dia"
  fi
}

LOCK_FILE="${DATA_DIR}/.papers-daily.lock"
exec 200>"${LOCK_FILE}"
if ! flock -n 200; then
  log "WARN" "Outra instancia de papers-daily rodando. Saindo."
  exit 0
fi

STDERR_FILE=""
OUT_FILE=""
cleanup() { rm -f "${STDERR_FILE}" "${OUT_FILE}"; }
trap cleanup EXIT

STDERR_FILE=$(mktemp) || { log "ERROR" "mktemp falhou"; exit 2; }
OUT_FILE=$(mktemp) || { log "ERROR" "mktemp falhou"; exit 2; }

if [ "$#" -eq 0 ]; then
  # Passada 2 (07:00): reconciliação da janela D-1..D-3. Stdout do journal.py
  # carrega as linhas RECONCILE; com regeneração/backfill, publica e notifica
  # UMA vez com o resumo dos dias; sem mudança, silêncio.
  ALVO="reconciliação"
  log "INFO" "=== Reconciliando janela D-1..D-3 ==="

  set +e
  "${PYTHON_BIN}" "${JOURNAL_BIN}" --reconcile >"${OUT_FILE}" 2>"${STDERR_FILE}"
  RC=$?
  set -e

  cat "${STDERR_FILE}" >> "${LOG_FILE}"

  if [ "${RC}" -eq 4 ]; then
    log "INFO" "Sem publicação na janela (fim de semana prolongado). Sem edição."
    exit 0
  fi

  if [ "${RC}" -eq 0 ]; then
    MUDANCAS=$(grep -Ec '^RECONCILE [0-9-]+ (regenerado|backfill) ' "${OUT_FILE}" || true)
    if [ "${MUDANCAS}" -eq 0 ]; then
      log "INFO" "Nada mudado na janela."
      exit 0
    fi
    RESUMO=$(awk '$3=="regenerado"||$3=="backfill"{printf "%s(%s) ", $2, $3}' "${OUT_FILE}")
    mapfile -t DATAS < <(awk '$3=="regenerado"||$3=="backfill"{print $2}' "${OUT_FILE}")
    log "INFO" "DONE — reconciliação: ${RESUMO}"
    publicar "reconciliação: ${RESUMO}" "${DATAS[@]}"
    notificar "Jornal de Papers — atualizado" "default" "newspaper" \
      "Jornal atualizado: ${RESUMO}"
    exit 0
  fi

  # Falha com trabalho feito: dias regenerados/backfillados antes do erro já
  # atualizaram o snapshot em disco. Sair sem publicar os esconderia da
  # próxima passada (o diff sairia "inalterado") — publica o que deu certo
  # e SÓ ENTÃO cai no caminho de falha comum, que notifica alto e devolve
  # o código de erro citando o dia problemático.
  if grep -qE '^RECONCILE [0-9-]+ (regenerado|backfill) ' "${OUT_FILE}"; then
    RESUMO=$(awk '$3=="regenerado"||$3=="backfill"{printf "%s(%s) ", $2, $3}' "${OUT_FILE}")
    mapfile -t DATAS < <(awk '$3=="regenerado"||$3=="backfill"{print $2}' "${OUT_FILE}")
    log "INFO" "DONE — reconciliação (com falhas na janela): ${RESUMO}"
    publicar "reconciliação: ${RESUMO}" "${DATAS[@]}"
    notificar "Jornal de Papers — atualizado" "default" "newspaper" \
      "Jornal atualizado: ${RESUMO}"
  fi
else
  # Passada 1 (22:00 e manual): geração do dia explícito. O antigo guard
  # "existe -> nada a fazer" virou a regra uniforme: o journal.py compara o
  # snapshot da edição existente e só regenera em mudança material; o
  # inalterado sai em silêncio, sem publicar nem notificar.
  TARGET_DATE="$1"
  ALVO="${TARGET_DATE}"
  YEAR="${TARGET_DATE:0:4}"
  MONTH="${TARGET_DATE:5:2}"
  DEST="${DATA_DIR}/edicoes/${YEAR}/${MONTH}/${TARGET_DATE}.md"

  log "INFO" "=== Gerando jornal de ${TARGET_DATE} ==="

  set +e
  "${PYTHON_BIN}" "${JOURNAL_BIN}" --date "${TARGET_DATE}" >"${OUT_FILE}" 2>"${STDERR_FILE}"
  RC=$?
  set -e

  cat "${STDERR_FILE}" >> "${LOG_FILE}"

  if [ "${RC}" -eq 4 ]; then
    log "INFO" "Sem publicacao em ${TARGET_DATE} (fim de semana ou feriado). Sem edicao."
    exit 0
  fi

  if [ "${RC}" -eq 0 ]; then
    ACAO=$(awk '$1=="JORNAL"{print $3}' "${OUT_FILE}" | head -1)
    if [ "${ACAO}" = "inalterado" ]; then
      log "INFO" "Jornal de ${TARGET_DATE} inalterado. Nada a fazer."
      exit 0
    fi
    if [ ! -f "${DEST}" ]; then
      log "ERROR" "journal.py retornou 0 mas ${DEST} nao existe"
      RC=3
    else
      MANCHETE=$(grep -m1 '^## ' "${DEST}" | sed 's/^## //')
      N_DEST=$(sed -n 's/^destaques: //p' "${DEST}" | head -1)
      log "INFO" "DONE — ${TARGET_DATE}, ${N_DEST:-?} destaque(s)"
      publicar "${TARGET_DATE}" "${TARGET_DATE}"
      notificar "Jornal de Papers — ${TARGET_DATE}" "default" "newspaper" \
        "${MANCHETE:-Jornal disponivel} (${N_DEST:-?} destaques)"
      exit 0
    fi
  fi
fi

# Falha real: avisa alto, porque a ausencia do jornal por si so pode passar
# despercebida por dias.
case "${RC}" in
  1) REASON="erro de configuracao (key ausente, interests.md sumiu)" ;;
  2) REASON="falha de rede ou da API" ;;
  3) REASON="assercao de sanidade: feed vazio ou resposta degenerada" ;;
  *) REASON="erro inesperado (exit ${RC})" ;;
esac

# O excerto do stderr vem ANTES do veredito, nao depois. Ele ja foi anexado
# inteiro acima, e reanexa-lo depois do FALHOU fazia o log voltar no tempo
# apos o estado terminal — e so no caminho de falha, entao um log de falha
# tinha uma ordem que o de sucesso nao tem.
#
# O excerto FICA: ele existe para poupar quem le de procurar a causa no meio do
# dump inteiro, e isso e util. O defeito era a ordem, nao a existencia dele.
# Rotulado, para as linhas repetidas nao parecerem saida nova do processo.
log "ERROR" "ultimas linhas do stderr de ${ALVO}:"
tail -5 "${STDERR_FILE}" >> "${LOG_FILE}"
log "ERROR" "FALHOU em ${ALVO}: ${REASON}"

notificar "Jornal de Papers FALHOU" "high" "warning" \
  "${ALVO}: ${REASON}. Log: ${LOG_FILE}"

exit "${RC}"
