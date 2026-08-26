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

log "ERROR" "FALHOU em ${TARGET_DATE}: ${REASON}"
tail -5 "${STDERR_FILE}" >> "${LOG_FILE}"

notificar "Jornal de Papers FALHOU" "high" "warning" \
  "${TARGET_DATE}: ${REASON}. Log: ${LOG_FILE}"

exit "${RC}"
