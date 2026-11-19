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

MAX_REQUEST = 8192

def emit(payload):
    print(json.dumps(payload, ensure_ascii=False), flush=True)

def run_nmcli(*arguments, timeout=30):
    return subprocess.run(
        ["/usr/bin/nmcli", "--terse", *arguments],
        capture_output=True, text=True, timeout=timeout, check=False)

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
                       "device", "wifi", "list", "--rescan", "yes", timeout=25)
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
    return {"connected": connected, "networks": networks[:40]}

def connect(ssid, password):
    if not isinstance(ssid, str) or not (1 <= len(ssid.encode("utf-8")) <= 32):
        raise ValueError("Ungültiger WLAN-Name.")
    if any(ord(ch) < 32 for ch in ssid):
        raise ValueError("Ungültiger WLAN-Name.")
    if not isinstance(password, str) or len(password) > 128 or any(ord(ch) < 32 for ch in password):
        raise ValueError("Ungültiges WLAN-Passwort.")
    arguments = ["device", "wifi", "connect", ssid]
    if password:
        arguments += ["password", password]
    # nmcli receives credentials as process arguments. This is a local,
    # short-lived operation; credentials are never logged or returned.
    completed = run_nmcli(*arguments, timeout=35)
    if completed.returncode:
        raise RuntimeError("WLAN-Verbindung fehlgeschlagen. Passwort und Empfang prüfen.")
    return {"connected": ssid}

def main():
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
    else:
        raise ValueError("Unbekannte Netzwerkaktion.")

if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, subprocess.TimeoutExpired, OSError, json.JSONDecodeError) as exc:
        emit({"error": str(exc)[:180]})
        sys.exit(1)
