#!/bin/sh
set -eu

[ "$(id -u)" -eq 0 ] || { echo 'Run as root.' >&2; exit 1; }
cd "$(dirname "$0")/.."
for program in sway chromium dbus-run-session python3; do
    command -v "$program" >/dev/null
done

install -d /opt/darts-console/web /opt/darts-console/deploy /etc/darts-console \
    /etc/systemd/system/getty@tty1.service.d
install -m 644 web/index.html web/scoring.js /opt/darts-console/web/
install -m 755 deploy/browser deploy/kiosk-login /opt/darts-console/deploy/

if ! id darts-kiosk >/dev/null 2>&1; then
    useradd --create-home --home-dir /var/lib/darts-kiosk \
        --shell /opt/darts-console/deploy/kiosk-login darts-kiosk
fi

if [ ! -e /etc/darts-console/sway.conf ]; then
    install -m 644 deploy/sway.conf /etc/darts-console/sway.conf
fi
install -m 644 deploy/darts-web.service /etc/systemd/system/darts-web.service
install -m 644 deploy/getty.conf /etc/systemd/system/getty@tty1.service.d/darts-console.conf
systemctl daemon-reload
systemctl enable --now darts-web.service
echo 'Kiosk installed. From an independent terminal, run systemctl restart getty@tty1 to activate it.'
