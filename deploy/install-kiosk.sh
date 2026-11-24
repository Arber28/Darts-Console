#!/bin/sh
set -eu

[ "$(id -u)" -eq 0 ] || { echo 'Run as root.' >&2; exit 1; }
cd "$(dirname "$0")/.."
for program in sway chromium dbus-run-session python3 sudo; do
    command -v "$program" >/dev/null
done

install -d /opt/darts-console/web /opt/darts-console/deploy /etc/darts-console \
    /etc/systemd/system/getty@tty1.service.d
install -m 644 web/index.html web/scoring.js /opt/darts-console/web/
install -m 755 deploy/browser deploy/kiosk-login /opt/darts-console/deploy/
install -m 644 deploy/api-server.py deploy/update-from-github.py /opt/darts-console/deploy/
install -m 755 deploy/wifi-helper.py /opt/darts-console/deploy/wifi-helper.py

if ! id darts-kiosk >/dev/null 2>&1; then
    useradd --create-home --home-dir /var/lib/darts-kiosk \
        --shell /opt/darts-console/deploy/kiosk-login darts-kiosk
fi

# Give the dedicated kiosk service read access to local V4L2 cameras.
# Supplementary group membership takes effect on the service restart below.
if getent group video >/dev/null 2>&1; then
    usermod -aG video darts-kiosk
fi

if [ ! -e /etc/darts-console/sway.conf ]; then
    install -m 644 deploy/sway.conf /etc/darts-console/sway.conf
fi
install -m 644 deploy/darts-web.service /etc/systemd/system/darts-web.service
install -m 644 deploy/darts-console-update.service /etc/systemd/system/darts-console-update.service
install -d -m 755 /etc/sudoers.d
printf '%s\n' 'darts-kiosk ALL=(root) NOPASSWD: /usr/bin/systemctl start --no-block darts-console-update.service' > /etc/sudoers.d/darts-console-update
printf '%s\n' 'darts-kiosk ALL=(root) NOPASSWD: /usr/bin/python3 /opt/darts-console/deploy/wifi-helper.py' > /etc/sudoers.d/darts-console-network
chmod 440 /etc/sudoers.d/darts-console-network
visudo -cf /etc/sudoers.d/darts-console-network >/dev/null
chmod 440 /etc/sudoers.d/darts-console-update
visudo -cf /etc/sudoers.d/darts-console-update >/dev/null
install -m 644 deploy/getty.conf /etc/systemd/system/getty@tty1.service.d/darts-console.conf
systemctl daemon-reload
systemctl enable --now darts-web.service
systemctl restart darts-web.service
echo 'Kiosk installed. From an independent terminal, run systemctl restart getty@tty1 to activate it.'
