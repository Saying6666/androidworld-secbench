#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CONFIG_PATH="${1:-configs/default.yaml}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[INFO] Project root: ${PROJECT_ROOT}"
echo "[INFO] Config path: ${CONFIG_PATH}"

cd "${PROJECT_ROOT}"
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

if [ ! -f "runner.py" ]; then
  echo "[ERROR] runner.py not found in project root."
  exit 1
fi

if [ ! -f "${CONFIG_PATH}" ]; then
  echo "[ERROR] Config file not found: ${CONFIG_PATH}"
  exit 1
fi

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  echo "[ERROR] Python interpreter not found: ${PYTHON_BIN}"
  exit 1
fi

mkdir -p outputs/runs outputs/steps outputs/reports

echo "[INFO] Running demo..."
"${PYTHON_BIN}" runner.py --config "${CONFIG_PATH}"

echo "[INFO] Demo finished."
echo "[INFO] Run logs:    outputs/runs/"
echo "[INFO] Step logs:   outputs/steps/"
echo "[INFO] Reports dir: outputs/reports/"
