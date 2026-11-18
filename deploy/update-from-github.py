#!/usr/bin/env python3
"""Update only the two web assets, never local profiles, browser data or OS."""
import base64
import json
import os
import shutil
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

TARGET = Path("/opt/darts-console/web")
STATUS = Path("/var/lib/darts-kiosk/update-status.json")
BASE = "https://raw.githubusercontent.com/Arber28/Darts-Console/main/web/"
API = "https://api.github.com/repos/Arber28/Darts-Console/contents/web/"
TOKEN_FILE = Path("/etc/darts-console/github-token")
FILES = ("index.html", "scoring.js")
MAX_BYTES = 2 * 1024 * 1024

def publish(state, message):
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps({"state": state, "message": message, "updated_at": int(time.time())})
    fd, tmp = tempfile.mkstemp(prefix=".update-", dir=STATUS.parent)
    with os.fdopen(fd, "w") as out:
        out.write(payload)
    os.chmod(tmp, 0o644)
    os.replace(tmp, STATUS)

def download(name):
    headers = {"User-Agent": "DartsConsole-Updater/1"}
    if TOKEN_FILE.is_file():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
        if not token:
            raise RuntimeError("GitHub token file is empty")
        headers.update({"Authorization": "Bearer " + token,
                        "Accept": "application/vnd.github+json",
                        "X-GitHub-Api-Version": "2022-11-28"})
        request = urllib.request.Request(API + name + "?ref=main", headers=headers)
    else:
        request = urllib.request.Request(BASE + name, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status != 200:
                raise RuntimeError("GitHub returned HTTP " + str(response.status))
            raw = response.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as error:
        if error.code in (401, 403, 404):
            raise RuntimeError("GitHub access denied. Configure a read-only token in /etc/darts-console/github-token.") from None
        raise
    if len(raw) > MAX_BYTES:
        raise RuntimeError("GitHub response is too large")
    if TOKEN_FILE.is_file():
        try:
            payload = json.loads(raw)
            data = base64.b64decode(payload["content"], validate=False)
        except (ValueError, KeyError, TypeError) as error:
            raise RuntimeError("Invalid response from GitHub API") from error
    else:
        data = raw
    if len(data) > MAX_BYTES:
        raise RuntimeError("GitHub file is too large")
    if name == "index.html" and not (data.startswith(b"<!doctype html>") and b"</html>" in data):
        raise RuntimeError("Invalid HTML received")
    if name == "scoring.js" and not (b"const Scoring" in data and b"replay(" in data):
        raise RuntimeError("Invalid scoring script received")
    return data

def main():
    publish("downloading", "Downloading the latest main version")
    with tempfile.TemporaryDirectory(prefix="darts-console-update-") as folder:
        staging = Path(folder)
        contents = {name: download(name) for name in FILES}
        if all((TARGET / name).is_file() and
               (TARGET / name).read_bytes() == contents[name] for name in FILES):
            publish("up-to-date", "Already running the latest GitHub version")
            return
        for name, data in contents.items():
            (staging / name).write_bytes(data)
        publish("installing", "Installing verified files")
        backups = {name: (TARGET / name).read_bytes() if (TARGET / name).exists() else None
                   for name in FILES}
        installed = []
        try:
            for name in FILES:
                tmp = TARGET / ("." + name + ".new")
                shutil.copyfile(staging / name, tmp)
                os.chmod(tmp, 0o644)
                os.replace(tmp, TARGET / name)
                installed.append(name)
        except Exception:
            for name in installed:
                if backups[name] is None:
                    (TARGET / name).unlink(missing_ok=True)
                else:
                    tmp = TARGET / ("." + name + ".rollback")
                    tmp.write_bytes(backups[name])
                    os.chmod(tmp, 0o644)
                    os.replace(tmp, TARGET / name)
            raise
    publish("updated", "Update installed. Reloading the console")

if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, urllib.error.URLError, ValueError) as error:
        publish("error", "Update failed: " + str(error)[:220])
        raise
