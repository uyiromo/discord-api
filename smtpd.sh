#!/bin/bash
set -eu
set -o pipefail

VENV_DIR="/run/smtpd.venv"
if [ ! -d "$VENV_DIR" ]; then
    virtualenv -p "python3.13" "${VENV_DIR}"
fi

SRCDIR=$(dirname "$0")
${VENV_DIR}/bin/pip3 install --no-cache-dir -r "${SRCDIR}/requirements.txt"
${VENV_DIR}/bin/python3 "${SRCDIR}/smtpd.py"
