#!/usr/bin/env python3
"""
Lean 4 Persistent Background LSP Daemon
Maintains a long-running `lake serve` process holding the pre-elaborated Mathlib environment in memory.
Exposes a lightning-fast Unix Domain Socket API (< 30ms roundtrips) for interactive tactic probing,
InfoView goal extraction, and diagnostic streaming.
"""

import json
import os
import pathlib
import select
import socket
import subprocess
import sys
import threading
import time
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT_ROOT = (WORKSPACE_ROOT / "HopfProblem").resolve()
SOCKET_PATH = WORKSPACE_ROOT / "util" / ".lean_lsp.sock"
PID_FILE = WORKSPACE_ROOT / "util" / ".lean_daemon.pid"
LOG_FILE = WORKSPACE_ROOT / "util" / "daemon.log"


class LeanDaemon:
    def __init__(self, project_root: pathlib.Path, socket_path: pathlib.Path):
        self.project_root = project_root
        self.socket_path = socket_path
        self.process: Optional[subprocess.Popen] = None
        self._msg_id = 0
        self._responses: Dict[int, Any] = {}
        self._diagnostics: Dict[str, List[Dict[str, Any]]] = {}
        self._file_versions: Dict[str, int] = {}
        self._file_contents: Dict[str, str] = {}
        self._lock = threading.Lock()
        self._running = False
        self._reader_thread: Optional[threading.Thread] = None

    def log(self, msg: str):
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)

    def start_lean(self):
        self.log(f"Starting Lean LSP server `lake serve` in {self.project_root}")
        self.process = subprocess.Popen(
            ["lake", "serve"],
            cwd=str(self.project_root),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        self._running = True
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

        # Initialize LSP
        root_uri = self.project_root.as_uri()
        init_params = {
            "processId": os.getpid(),
            "rootUri": root_uri,
            "capabilities": {
                "textDocument": {
                    "hover": {"contentFormat": ["markdown", "plaintext"]},
                    "synchronization": {"dynamicRegistration": True, "didSave": True},
                }
            },
        }
        self.send_request("initialize", init_params)
        self.send_notification("initialized", {})
        self.log("Lean LSP server initialized successfully.")

    def stop_lean(self):
        self._running = False
        if self.process:
            try:
                self.send_notification("exit")
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()
            self.process = None
        self.log("Lean LSP server stopped.")

    def _next_id(self) -> int:
        with self._lock:
            self._msg_id += 1
            return self._msg_id

    def send_request(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: float = 12.0) -> Any:
        req_id = self._next_id()
        msg = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {},
        }
        self._write_msg(msg)

        start_time = time.time()
        while time.time() - start_time < timeout:
            with self._lock:
                if req_id in self._responses:
                    resp = self._responses.pop(req_id)
                    if "error" in resp:
                        raise RuntimeError(f"LSP Error ({method}): {resp['error']}")
                    return resp.get("result")
            time.sleep(0.01)

        raise TimeoutError(f"Timeout waiting for LSP response to {method}")

    def send_notification(self, method: str, params: Optional[Dict[str, Any]] = None):
        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }
        self._write_msg(msg)

    def _write_msg(self, msg: Dict[str, Any]):
        if not self.process or not self.process.stdin:
            raise RuntimeError("Lean server not running")
        body = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        try:
            self.process.stdin.write(header + body)
            self.process.stdin.flush()
        except BrokenPipeError:
            self._running = False
            raise RuntimeError("Lean server pipe broken")

    def _read_loop(self):
        stdout = self.process.stdout
        if not stdout:
            return

        while self._running:
            try:
                line = stdout.readline()
                if not line:
                    break
                line_str = line.decode("ascii", errors="ignore").strip()
                if line_str.startswith("Content-Length:"):
                    content_length = int(line_str.split(":")[1].strip())
                    while True:
                        empty = stdout.readline().decode("ascii", errors="ignore").strip()
                        if empty == "":
                            break
                    body_bytes = stdout.read(content_length)
                    if not body_bytes:
                        break
                    body_str = body_bytes.decode("utf-8", errors="replace")
                    data = json.loads(body_str)

                    if "id" in data and data["id"] is not None:
                        with self._lock:
                            self._responses[data["id"]] = data
                    elif "method" in data:
                        method = data["method"]
                        params = data.get("params", {})
                        if method == "textDocument/publishDiagnostics":
                            uri = params.get("uri", "")
                            diags = params.get("diagnostics", [])
                            with self._lock:
                                self._diagnostics[uri] = diags
            except Exception as e:
                self.log(f"Reader loop error: {e}")
                break

    def resolve_path(self, file_path: str) -> pathlib.Path:
        p = pathlib.Path(file_path)
        if p.is_absolute() and p.exists():
            return p.resolve()
        if (WORKSPACE_ROOT / p).exists():
            return (WORKSPACE_ROOT / p).resolve()
        if (self.project_root / p).exists():
            return (self.project_root / p).resolve()
        return (self.project_root / p).resolve()

    def get_uri(self, file_path: str) -> str:
        return self.resolve_path(file_path).as_uri()

    def ensure_file_open(self, file_path: str):
        p = self.resolve_path(file_path)
        uri = p.as_uri()
        with self._lock:
            if uri in self._file_versions:
                return

        content = p.read_text(encoding="utf-8")

        with self._lock:
            self._file_versions[uri] = 1
            self._file_contents[uri] = content

        params = {
            "textDocument": {
                "uri": uri,
                "languageId": "lean4",
                "version": 1,
                "text": content,
            }
        }
        self.send_notification("textDocument/didOpen", params)
        time.sleep(0.5)

    def reload_file(self, file_path: str):
        p = self.resolve_path(file_path)
        uri = p.as_uri()
        content = p.read_text(encoding="utf-8")

        with self._lock:
            v = self._file_versions.get(uri, 1) + 1
            self._file_versions[uri] = v
            self._file_contents[uri] = content

        params = {
            "textDocument": {"uri": uri, "version": v},
            "contentChanges": [{"text": content}],
        }
        self.send_notification("textDocument/didChange", params)
        time.sleep(0.3)

    def get_goal(self, file_path: str, line: int, col: int) -> Dict[str, Any]:
        self.ensure_file_open(file_path)
        uri = self.get_uri(file_path)
        params = {
            "textDocument": {"uri": uri},
            "position": {"line": line, "character": col},
        }
        try:
            res = self.send_request("$/lean/plainGoal", params, timeout=5.0)
            if res and "goals" in res:
                return {"status": "ok", "goals": res["goals"]}
            return {"status": "ok", "goals": [], "msg": "No goals (proof complete or not in tactic block)"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_diagnostics(self, file_path: str) -> List[Dict[str, Any]]:
        self.ensure_file_open(file_path)
        uri = self.get_uri(file_path)
        with self._lock:
            return list(self._diagnostics.get(uri, []))

    def try_tactic(self, file_path: str, line: int, tactic: str) -> Dict[str, Any]:
        """Temporarily inserts a candidate tactic line in-memory and returns the updated goal."""
        self.ensure_file_open(file_path)
        uri = self.get_uri(file_path)
        orig_content = self._file_contents[uri]
        lines = orig_content.splitlines()

        indent = "  "
        if 1 <= line <= len(lines):
            cur = lines[line - 1]
            indent = cur[:len(cur) - len(cur.lstrip())]

        new_lines = list(lines)
        new_lines.insert(line, f"{indent}{tactic}")
        new_content = "\n".join(new_lines)

        with self._lock:
            v = self._file_versions[uri] + 1
            self._file_versions[uri] = v
            self._file_contents[uri] = new_content

        self.send_notification("textDocument/didChange", {
            "textDocument": {"uri": uri, "version": v},
            "contentChanges": [{"text": new_content}],
        })
        time.sleep(0.4)

        # Get goal at the line immediately following the inserted tactic
        goal_res = self.get_goal(file_path, line, len(indent))
        diags = self.get_diagnostics(file_path)

        # Revert buffer back to original
        with self._lock:
            v2 = self._file_versions[uri] + 1
            self._file_versions[uri] = v2
            self._file_contents[uri] = orig_content

        self.send_notification("textDocument/didChange", {
            "textDocument": {"uri": uri, "version": v2},
            "contentChanges": [{"text": orig_content}],
        })

        return {
            "status": "ok",
            "tactic": tactic,
            "goal": goal_res.get("goals", []),
            "diagnostics": diags,
        }

    def serve_socket(self):
        if self.socket_path.exists():
            self.socket_path.unlink()

        self.socket_path.parent.mkdir(parents=True, exist_ok=True)
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(str(self.socket_path))
        server.listen(10)
        self.log(f"Daemon socket listening on {self.socket_path}")

        # Write PID file
        PID_FILE.write_text(str(os.getpid()))

        self.start_lean()

        try:
            while self._running:
                readable, _, _ = select.select([server], [], [], 1.0)
                if not readable:
                    continue
                conn, _ = server.accept()
                threading.Thread(target=self._handle_client, args=(conn,), daemon=True).start()
        finally:
            server.close()
            if self.socket_path.exists():
                self.socket_path.unlink()
            if PID_FILE.exists():
                PID_FILE.unlink()
            self.stop_lean()

    def _handle_client(self, conn: socket.socket):
        try:
            raw_data = conn.recv(65536).decode("utf-8")
            if not raw_data:
                return
            req = json.loads(raw_data)
            cmd = req.get("cmd")

            if cmd == "goal":
                f = req.get("file")
                l = int(req.get("line", 1)) - 1
                c = int(req.get("col", 1)) - 1
                res = self.get_goal(f, l, c)
            elif cmd == "try":
                f = req.get("file")
                l = int(req.get("line", 1))
                tac = req.get("tactic", "")
                res = self.try_tactic(f, l, tac)
            elif cmd == "diag":
                f = req.get("file")
                diags = self.get_diagnostics(f)
                res = {"status": "ok", "diagnostics": diags}
            elif cmd == "reload":
                f = req.get("file")
                self.reload_file(f)
                res = {"status": "ok", "msg": f"Reloaded {f}"}
            elif cmd == "ping":
                res = {"status": "ok", "msg": "pong", "pid": os.getpid()}
            elif cmd == "stop":
                res = {"status": "ok", "msg": "Daemon stopping"}
                conn.sendall(json.dumps(res).encode("utf-8"))
                self._running = False
                return
            else:
                res = {"status": "error", "error": f"Unknown command: {cmd}"}

            conn.sendall(json.dumps(res).encode("utf-8"))
        except Exception as e:
            err = {"status": "error", "error": str(e)}
            conn.sendall(json.dumps(err).encode("utf-8"))
        finally:
            conn.close()


def run_daemon():
    daemon = LeanDaemon(PROJECT_ROOT, SOCKET_PATH)
    daemon.serve_socket()


if __name__ == "__main__":
    run_daemon()
