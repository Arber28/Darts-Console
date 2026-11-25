# Wi-Fi on Debian

The kiosk works offline. NetworkManager is needed only for Wi-Fi settings.
Supported: visible open and WPA/WPA2 Personal networks, DHCP, saved profiles
and automatic reconnection. Enterprise, captive-portal login, hidden networks
and WPA3-only networks require administrator setup outside the kiosk.

## Migrate only wlp2s0

Run as root at the laptop or over verified Ethernet SSH through **enp1s0**.
Do not do this through Wi-Fi SSH. Keep a second terminal open. Do not restart
networking or take enp1s0 down. Review interface definitions without publishing
their passwords. Stop if wlp2s0 has definitions outside the placeholder file,
or if the file contains any other interface.

```sh
ip -br address show enp1s0
ip route
grep -l 'wlp2s0' /etc/network/interfaces /etc/network/interfaces.d/*
# Inspect /etc/network/interfaces.d/wifi locally. It must contain only the
# known wlp2s0 placeholder stanza (DEIN-WLAN-NAME), comments and blank lines.
test -f /etc/network/interfaces.d/wifi
test ! -e /root/darts-wifi-ifupdown.backup
install -m 600 /etc/network/interfaces.d/wifi /root/darts-wifi-ifupdown.backup

# Prevent NM from taking Ethernet when the package starts.
install -d -m 755 /etc/NetworkManager/conf.d
test ! -e /etc/NetworkManager/conf.d/90-darts-interfaces.conf
cat > /etc/NetworkManager/conf.d/90-darts-interfaces.conf <<'EOF'
[main]
plugins=ifupdown,keyfile
[ifupdown]
managed=false
[keyfile]
unmanaged-devices=interface-name:enp1s0
EOF
apt-get update
apt-get install --no-install-recommends network-manager sudo

# Release only the old Wi-Fi definition before removing it from ifupdown.
ifdown --force wlp2s0
rm /etc/network/interfaces.d/wifi
systemctl enable --now NetworkManager
systemctl reload NetworkManager
nmcli device set wlp2s0 managed yes
nmcli -f DEVICE,TYPE,STATE device
ip -br address show enp1s0

# From the checked-out repository:
sh deploy/install-kiosk.sh
systemctl is-active darts-web NetworkManager ssh
```

NetworkManager must show enp1s0 as unmanaged and wlp2s0 as disconnected or
connected, not unmanaged. If not, stop and inspect other NetworkManager config
and interface definitions. Never set ifupdown managed=true globally.

Open Settings → WLAN & Netzwerk. Turn/press the encoder to choose a network
and password characters. Back cancels, Undo deletes a character, Correct
changes character set, Next connects. All printable ASCII characters are
available. Passwords are masked and cleared on exit or failed connection.
Saved connections activate without entering a password again.

## Verify on the laptop

Try a wrong password, a correct one, an open network if available, saved
activation after reboot and after temporarily losing the access point.
Check state/IP in settings. Verify all five physical controls and play an
offline match with both network cables/radio connectivity unavailable.
Verify Ethernet SSH still works throughout. Do not include credentials in
screenshots or diagnostic output.

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
node --test tests/scoring.test.js
sh tests/kiosk-smoke.sh
stat -c '%U %a %n' /opt/darts-console/deploy/wifi-helper.py
visudo -cf /etc/sudoers.d/darts-console-network
```

## Roll back the interface migration

Use the laptop terminal or Ethernet SSH. This disconnects Wi-Fi only.

```sh
nmcli device disconnect wlp2s0 || true
nmcli device set wlp2s0 managed no
install -m 600 /root/darts-wifi-ifupdown.backup /etc/network/interfaces.d/wifi
systemctl reload NetworkManager
# The restored file contains a placeholder; edit its WLAN name/password
# locally before using ifup wlp2s0. Ethernet remains under ifupdown.
```

## Privilege boundary

The HTTP server binds only 127.0.0.1, checks Host and requires a custom
header for scans; writes additionally require a local Origin and bounded
JSON body. There is no CORS permission. Only a root-owned fixed helper is
allowed through sudo; it accepts scan/connect/activate, fixes the interface
to wlp2s0 and checks saved UUIDs against profiles explicitly bound to it.
The kiosk user must not own or be able to modify /opt/darts-console or its
parents. No arbitrary command, path or interface is accepted from HTTP.

Passwords travel through stdin and a root-only mode 0600 NetworkManager
keyfile, never shell commands or process arguments. Helper errors are generic;
subprocess output is not returned. NetworkManager stores saved credentials
under /etc/NetworkManager/system-connections; protect backups as secrets.
Failed newly-created profiles are removed. Existing saved profiles remain.
This protects against web-origin attacks, not a compromised local kiosk user.
See the official nmcli and nm-settings-keyfile manuals for the profile format.
