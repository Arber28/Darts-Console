# On-device software updates

The console runs a static UI and a loopback-only update API on `127.0.0.1:8765`.
In **Settings > Software update**, choose **Update from GitHub** and confirm.
The updater downloads only `web/index.html` and `web/scoring.js` from
`Arber28/Darts-Console`'s `main` branch. No OS packages are installed;
no shell scripts from GitHub are executed. Matches, localStorage, browser
profile, Pico firmware and camera calibration are not modified.

## One-time installation

Use SSH or an independent terminal with internet access. Obtain the latest
source using your normal authenticated GitHub access, then run:

```sh
sudo apt-get install sudo
sudo sh deploy/install-kiosk.sh
systemctl is-active darts-web.service
```

The installer creates `darts-console-update.service` and grants the
unprivileged kiosk account permission to start *only* that service. The
update endpoint is not exposed to the LAN. The web page requires confirmation
before requesting an update.

## Private GitHub repository

Because this repository may be private, configure a **fine-grained read-only
personal access token** on the laptop. Restrict the token to this repository
with **Contents: Read-only**. Never commit the token or paste it into chat.

Store the token as root in `/etc/darts-console/github-token`:

```sh
sudo install -m 600 -o root -g root /dev/null /etc/darts-console/github-token
sudoedit /etc/darts-console/github-token
```

Paste the token into the editor, save, then exit. The update service
automatically uses GitHub's authenticated Contents API. If no token is
configured, it attempts a public raw download; private repositories will
return an access error. Only the root update service can read this token.

## Offline behavior

If no internet is available, the current console continues working.
The update shows an error and leaves existing UI files untouched.
The update downloads both files before replacing either one and rolls back
if file installation fails.

## Troubleshooting

```sh
curl http://127.0.0.1:8765/api/update/status
sudo systemctl status darts-console-update.service
sudo journalctl -u darts-console-update.service -n 40 --no-pager
```

The updates button requires the new installer once. Copying only the
HTML file is not sufficient; it must be backed by the local update API
and systemd service.
