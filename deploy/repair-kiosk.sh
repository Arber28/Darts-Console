#!/bin/sh
set -eu
[ "$(id -u)" -eq 0 ] || exit 1
cd "$(dirname "$0")/.."
sh deploy/install-kiosk.sh
systemctl stop getty@tty1
# End orphaned kiosk processes, including launchers from earlier logins.
loginctl terminate-user darts-kiosk || true
systemctl start getty@tty1
