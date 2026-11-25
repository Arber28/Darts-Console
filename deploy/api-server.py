#!/usr/bin/env python3
"""Loopback-only static server with a small, explicit update API."""
import json
import os
import subprocess
import glob
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path("/opt/darts-console/web")
STATUS = Path("/var/lib/darts-kiosk/update-status.json")
WIFI_HELPER = "/opt/darts-console/deploy/wifi-helper.py"
ADDRESS = "127.0.0.1"
PORT = 8765


def camera_devices():
    """Prefer stable physical USB ports; use only V4L2 video capture node 0."""
    found = []
    seen = set()
    candidates = sorted(glob.glob("/dev/v4l/by-path/*video-index0"))
    candidates += sorted(glob.glob("/dev/v4l/by-id/*video-index0"))
    candidates += sorted(glob.glob("/dev/video[0-9]*"),
                         key=lambda p: int(p.rsplit("video", 1)[-1]))
    for path in candidates:
        resolved = os.path.realpath(path)
        if resolved in seen or not os.path.exists(resolved):
            continue
        name = os.path.basename(resolved)
        if name.startswith("video"):
            index = Path("/sys/class/video4linux") / name / "index"
            try:
                if index.read_text(encoding="utf-8").strip() != "0":
                    continue
            except OSError:
                # A missing sysfs index does not prove this is a capture node.
                continue
        seen.add(resolved)
        found.append(path)
    return found


class Handler(SimpleHTTPRequestHandler):
    timeout = 50

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        super().end_headers()

    def json_reply(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def local_request(self):
        host = self.headers.get("Host", "")
        return host in (f"{ADDRESS}:{PORT}", ADDRESS, f"localhost:{PORT}", "localhost")

    def network_helper(self, payload):
        try:
            completed = subprocess.run(
                ["/usr/bin/sudo", "-n", "/usr/bin/python3", "-I", WIFI_HELPER],
                input=json.dumps(payload, ensure_ascii=False), capture_output=True,
                text=True, timeout=45, check=False)
        except (OSError, subprocess.TimeoutExpired):
            return self.json_reply(503, {"error": "WLAN-Dienst reagiert nicht"})
        try:
            result = json.loads(completed.stdout)
        except ValueError:
            return self.json_reply(503, {"error": "WLAN-Dienst nicht installiert oder nicht berechtigt"})
        return self.json_reply(200 if completed.returncode == 0 else 503, result)

    def valid_local_origin(self):
        return self.headers.get("Origin") in (
            f"http://{ADDRESS}:{PORT}", f"http://localhost:{PORT}")


    def camera_stream(self, number):
        devices = camera_devices()
        if number < 1 or number > 3 or len(devices) < number:
            return self.json_reply(404, {"error": "Camera not connected"})
        if not Path("/usr/bin/ffmpeg").is_file():
            return self.json_reply(503, {"error": "Install ffmpeg for local camera preview"})
        command = [
            "/usr/bin/ffmpeg", "-hide_banner", "-loglevel", "error",
            "-nostdin", "-f", "video4linux2", "-input_format", "mjpeg",
            "-framerate", "30", "-video_size", "1920x1080",
            "-i", devices[number - 1], "-c:v", "copy", "-f", "mpjpeg",
            "-boundary_tag", "frame", "pipe:1",
        ]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL)
        except OSError:
            return self.json_reply(503, {"error": "Camera capture could not start"})
        try:
            self.send_response(200)
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            while True:
                chunk = process.stdout.read(16384)
                if not chunk:
                    break
                self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            if process.stdout:
                process.stdout.close()

    def do_GET(self):
        if not self.local_request():
            return self.json_reply(403, {"error": "Local requests only"})
        path = urlsplit(self.path).path
        if path.startswith("/api/cameras/") and path.endswith("/stream"):
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "cameras"] and parts[3] == "stream" and parts[2] in ("1", "2", "3"):
                return self.camera_stream(int(parts[2]))
            return self.json_reply(404, {"error": "Unknown camera"})
        if path == "/api/network/scan":
            if self.headers.get("X-Darts-Network") != "requested":
                return self.json_reply(403, {"error": "Use the local kiosk"})
            return self.network_helper({"action": "scan"})
        if urlsplit(self.path).path == "/api/update/status":
            try:
                status = json.loads(STATUS.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                status = {"state": "not-configured", "message": "No update has been run"}
            return self.json_reply(200, status)
        return super().do_GET()

    def do_POST(self):
        if not self.local_request():
            return self.json_reply(403, {"error": "Local requests only"})
        if urlsplit(self.path).path in ("/api/network/connect", "/api/network/activate"):
            if not self.valid_local_origin() or self.headers.get("X-Darts-Network") != "requested":
                return self.json_reply(403, {"error": "Use the local kiosk"})
            if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
                return self.json_reply(415, {"error": "JSON required"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                return self.json_reply(400, {"error": "Invalid request size"})
            if length < 1 or length > 8192:
                return self.json_reply(413, {"error": "Request too large"})
            try:
                payload = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeError):
                return self.json_reply(400, {"error": "Invalid JSON"})
            if not isinstance(payload, dict):
                return self.json_reply(400, {"error": "Invalid request"})
            return self.network_helper({
                "action": "activate" if urlsplit(self.path).path.endswith("/activate") else "connect",
                "uuid": payload.get("uuid"), "ssid": payload.get("ssid"),
                "password": payload.get("password", "")})
        if urlsplit(self.path).path != "/api/update/start":
            return self.json_reply(404, {"error": "Not found"})
        # Custom header forces a browser preflight for cross-origin requests.
        if not self.valid_local_origin():
            return self.json_reply(403, {"error": "Use the local console to start updates"})
        if self.headers.get("X-Darts-Update") != "requested":
            return self.json_reply(403, {"error": "Missing update confirmation"})
        if self.headers.get("Content-Length", "0") not in ("0", ""):
            return self.json_reply(400, {"error": "No request body expected"})
        try:
            status = json.loads(STATUS.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            status = {}
        if status.get("state") in ("starting", "downloading", "installing"):
            return self.json_reply(409, {"error": "An update is already running"})
        try:
            cmd = ["/usr/bin/sudo", "-n", "/usr/bin/systemctl", "start", "--no-block",
                   "darts-console-update.service"]
            completed = subprocess.run(cmd, capture_output=True, text=True, timeout=8, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return self.json_reply(503, {"error": str(exc)})
        if completed.returncode:
            return self.json_reply(503, {"error": (completed.stderr or "Cannot start updater").strip()[:300]})
        return self.json_reply(202, {"state": "starting", "message": "Checking GitHub"})

    def do_OPTIONS(self):
        return self.json_reply(403, {"error": "Cross-origin updates are disabled"})

if __name__ == "__main__":
    os.chdir(ROOT)
    ThreadingHTTPServer((ADDRESS, PORT), Handler).serve_forever()
