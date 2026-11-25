#!/usr/bin/env python3
"""Narrow privileged NetworkManager helper for the localhost darts kiosk.

Reads one bounded JSON request from stdin. Accepts only scan and connect; does
not expose saved passwords or arbitrary nmcli arguments.
"""
import json
import re
import shutil
import subprocess
import sys
import os
import uuid
import tempfile
from pathlib import Path

INTERFACE = "wlp2s0"
PROFILES = Path('/etc/NetworkManager/system-connections')

MAX_REQUEST = 8192

def emit(payload):
    print(json.dumps(payload, ensure_ascii=False), flush=True)

def run_nmcli(*arguments, timeout=30):
    return subprocess.run(
        ["/usr/bin/nmcli", "--terse", *arguments],
        capture_output=True, text=True, timeout=timeout, check=False,
        env={"PATH": "/usr/sbin:/usr/bin:/sbin:/bin", "LC_ALL": "C"})

def checked(*args, timeout=30):
    result = run_nmcli(*args, timeout=timeout)
    if result.returncode:
        raise RuntimeError('WLAN-Aktion fehlgeschlagen. NetworkManager und Empfang prüfen.')
    return result.stdout.strip()

def saved():
    profiles = []
    for row in checked('--fields', 'UUID,TYPE,NAME', 'connection', 'show').splitlines():
        fields = split_nmcli(row)
        if len(fields) != 3 or fields[1] not in ('802-11-wireless', 'wifi'):
            continue
        uid, _, name = fields
        bound = checked('--get-values', 'connection.interface-name', 'connection', 'show', 'uuid', uid)
        if bound == INTERFACE:
            profiles.append({'uuid': uid, 'name': name})
    return profiles

def activate(uid):
    if not isinstance(uid, str) or not any(p['uuid'] == uid for p in saved()):
        raise ValueError('Unbekannte WLAN-Verbindung.')
    checked('connection', 'up', 'uuid', uid, 'ifname', INTERFACE, timeout=35)
    return {'ok': True}

def key_escape(value):
    return value.replace('\\', '\\\\').replace(' ', '\\s').replace('\t', '\\t')

def split_nmcli(row):
    # NetworkManager escapes colons and backslashes in terse output.
    out, current, escaped = [], "", False
    for ch in row:
        if escaped:
            current += ch
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == ":":
            out.append(current)
            current = ""
        else:
            current += ch
    out.append(current)
    return out

def scan():
    result = run_nmcli("--fields", "IN-USE,SSID,SIGNAL,SECURITY",
                       "device", "wifi", "list", "ifname", INTERFACE, "--rescan", "yes", timeout=25)
    if result.returncode:
        raise RuntimeError("WLAN-Suche nicht verfügbar. NetworkManager prüfen.")
    networks, seen, connected = [], set(), ""
    for row in result.stdout.splitlines():
        parts = split_nmcli(row)
        if len(parts) < 4:
            continue
        active, ssid, signal, security = parts[:4]
        if not ssid:
            continue
        if active == "*":
            connected = ssid
        if ssid in seen:
            continue
        seen.add(ssid)
        try:
            strength = min(100, max(0, int(signal)))
        except ValueError:
            strength = 0
        networks.append({
            "ssid": ssid, "signal": strength,
            "security": security not in ("", "--"), "active": active == "*"})
    networks.sort(key=lambda item: (not item["active"], -item["signal"]))
    device = checked('--get-values', 'GENERAL.STATE,IP4.ADDRESS', 'device', 'show', INTERFACE)
    return {"connected": connected, "device": device, "saved": saved(), "networks": networks[:40]}

def connect(ssid, password):
    if not isinstance(ssid, str) or not (1 <= len(ssid.encode("utf-8")) <= 32):
        raise ValueError("Ungültiger WLAN-Name.")
    if any(ord(ch) < 32 for ch in ssid):
        raise ValueError("Ungültiger WLAN-Name.")
    if not isinstance(password, str) or len(password) > 128 or any(ord(ch) < 32 for ch in password):
        raise ValueError("Ungültiges WLAN-Passwort.")
    if password and not (8 <= len(password) <= 63 and password.isascii()):
        raise ValueError('WPA-Passwort muss 8–63 ASCII-Zeichen enthalten.')
    uid = str(uuid.uuid4())
    text = ('[connection]\nid=Darts WLAN\nuuid=' + uid + '\ntype=wifi\ninterface-name=' + INTERFACE +
            '\nautoconnect=true\n[wifi]\nmode=infrastructure\nssid=' + ''.join(str(b) + ';' for b in ssid.encode('utf-8')) + '\n')
    if password:
        text += '[wifi-security]\nkey-mgmt=wpa-psk\npsk=' + key_escape(password) + '\n'
    text += '[ipv4]\nmethod=auto\nroute-metric=600\n[ipv6]\nmethod=auto\nroute-metric=600\n'
    # Root-only keyfile: no secrets in argv, stdout, or exception messages.
    fd, name = tempfile.mkstemp(prefix='darts-', suffix='.nmconnection', dir=PROFILES)
    path = Path(name)
    loaded = False
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
        checked('connection', 'load', str(path))
        loaded = True
        checked('connection', 'up', 'uuid', uid, 'ifname', INTERFACE, timeout=35)
        checked('connection', 'modify', 'uuid', uid, 'connection.id', 'Darts: ' + ssid)
    except Exception:
        if loaded:
            run_nmcli('connection', 'delete', 'uuid', uid)
        path.unlink(missing_ok=True)
        raise RuntimeError('WLAN-Verbindung fehlgeschlagen. Passwort und Empfang prüfen.') from None
    return {"connected": ssid}

def main():
    # Serialize across HTTP worker processes; fail fast rather than queueing secrets.
    import fcntl
    lock = os.fdopen(os.open(PROFILES / '.darts-lock', os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600), 'w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise RuntimeError('WLAN-Aktion läuft bereits.') from None
    if not shutil.which("nmcli"):
        raise RuntimeError("NetworkManager (nmcli) ist nicht installiert.")
    raw = sys.stdin.buffer.read(MAX_REQUEST + 1)
    if len(raw) > MAX_REQUEST:
        raise ValueError("Anfrage zu groß.")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Ungültige Anfrage.")
    action = payload.get("action")
    if action == "scan":
        emit(scan())
    elif action == "connect":
        emit(connect(payload.get("ssid"), payload.get("password", "")))
    elif action == 'activate':
        emit(activate(payload.get('uuid')))
    else:
        raise ValueError("Unbekannte Netzwerkaktion.")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, subprocess.TimeoutExpired, OSError, json.JSONDecodeError) as exc:
        emit({"error": 'WLAN-Aktion fehlgeschlagen. Einrichtung, Passwort und Empfang prüfen.'})
        sys.exit(1)
