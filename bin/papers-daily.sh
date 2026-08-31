#!/usr/bin/env bash
# papers-daily.sh — Gera o jornal diario de papers do Hugging Face.
# Disparado por cron (07:00 BRT). Tambem invocavel manualmente:
#   bash ~/papers-journal/bin/papers-daily.sh [YYYY-MM-DD]
#
# Processa o dia anterior, ja fechado. A ausencia do jornal e o proprio alarme:
# quando o script falha, nenhum arquivo aparece e o ntfy avisa.
#
# Exit codes vindos de journal.py:
#   0 jornal escrito | 1 config | 2 rede/API | 3 assercao de sanidade
#   4 sem publicacao no dia (fim de semana) — nao e falha, nao notifica
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
  local data="$1"
  git -C "${PROJECT_ROOT}" remote get-url origin >/dev/null 2>&1 || return 0
  git -C "${PROJECT_ROOT}" add edicoes docs deep 2>/dev/null || true
  if git -C "${PROJECT_ROOT}" diff --cached --quiet 2>/dev/null; then
    log "INFO" "Nada novo para publicar."
    return 0
  fi
  if ! git -C "${PROJECT_ROOT}" commit -q -m "Edição de ${data}" 2>>"${LOG_FILE}"; then
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

TARGET_DATE="${1:-$(date -d 'yesterday' +%Y-%m-%d)}"
YEAR="${TARGET_DATE:0:4}"
MONTH="${TARGET_DATE:5:2}"
DEST="${DATA_DIR}/edicoes/${YEAR}/${MONTH}/${TARGET_DATE}.md"

if [ -f "${DEST}" ]; then
  log "INFO" "Jornal de ${TARGET_DATE} ja existe. Nada a fazer."
  exit 0
fi

log "INFO" "=== Gerando jornal de ${TARGET_DATE} ==="

STDERR_FILE=$(mktemp) || { log "ERROR" "mktemp falhou"; exit 2; }
trap 'rm -f "$STDERR_FILE"' EXIT

set +e
"${PYTHON_BIN}" "${JOURNAL_BIN}" --date "${TARGET_DATE}" 2>"${STDERR_FILE}"
RC=$?
set -e

cat "${STDERR_FILE}" >> "${LOG_FILE}"

if [ "${RC}" -eq 4 ]; then
  log "INFO" "Sem publicacao em ${TARGET_DATE} (fim de semana ou feriado). Sem edicao."
  exit 0
fi

if [ "${RC}" -eq 0 ]; then
  if [ ! -f "${DEST}" ]; then
    log "ERROR" "journal.py retornou 0 mas ${DEST} nao existe"
    RC=3
  else
    MANCHETE=$(grep -m1 '^## ' "${DEST}" | sed 's/^## //')
    N_DEST=$(sed -n 's/^destaques: //p' "${DEST}" | head -1)
    log "INFO" "DONE — ${TARGET_DATE}, ${N_DEST:-?} destaque(s)"
    publicar "${TARGET_DATE}"
    notificar "Jornal de Papers — ${TARGET_DATE}" "default" "newspaper" \
      "${MANCHETE:-Jornal disponivel} (${N_DEST:-?} destaques)"
    exit 0
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
# inteiro em :99, e reanexa-lo depois do FALHOU fazia o log voltar no tempo
# apos o estado terminal — e so no caminho de falha, entao um log de falha
# tinha uma ordem que o de sucesso nao tem.
#
# O excerto FICA: ele existe para poupar quem le de procurar a causa no meio do
# dump inteiro, e isso e util. O defeito era a ordem, nao a existencia dele.
# Rotulado, para as linhas repetidas nao parecerem saida nova do processo.
log "ERROR" "ultimas linhas do stderr de ${TARGET_DATE}:"
tail -5 "${STDERR_FILE}" >> "${LOG_FILE}"
log "ERROR" "FALHOU em ${TARGET_DATE}: ${REASON}"

notificar "Jornal de Papers FALHOU" "high" "warning" \
  "${TARGET_DATE}: ${REASON}. Log: ${LOG_FILE}"

exit "${RC}"
