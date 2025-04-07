#!/bin/bash
set -eu
set -o pipefail

if [ ! -d ".venv" ]; then
    virtualenv -p "python3.13" .venv
    .venv/bin/pip3 install --no-cache-dir -r ./requirements.txt
fi

OPTDIR=/opt/discord-api
sudo rm -rf ${OPTDIR}
sudo cp -r ../discord-api ${OPTDIR}
sudo cp smtpd-discord.service /etc/systemd/system/smtpd-discord.service
sudo systemctl daemon-reload
sudo systemctl stop smtpd-discord
sudo systemctl start smtpd-discord
