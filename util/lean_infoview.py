#!/usr/bin/env python3
"""
Lean 4 In-Memory InfoView & LSP Client Utility
Spawns a persistent `lake serve` language server process, keeps the Mathlib environment
in memory, and enables interactive sub-second goal inspection, baby-step tactic proving,
and live diagnostic streaming.
"""

import json
import os
import pathlib
import subprocess
import sys
import threading
import time
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PROJECT_DIR = (WORKSPACE_ROOT / "HopfProblem").resolve()


class LeanLspClient:
    """
    Persistent in-memory Language Server Protocol (LSP) client for Lean 4.
    Communicates with `lake serve` over standard JSON-RPC 2.0 with Content-Length framing.
    """

    def __init__(self, project_root: Optional[pathlib.Path] = None):
        self.project_root = pathlib.Path(project_root or DEFAULT_PROJECT_DIR).resolve()
        self.process: Optional[subprocess.Popen] = None
        self._msg_id = 0
        self._responses: Dict[int, Any] = {}
        self._diagnostics: Dict[str, List[Dict[str, Any]]] = {}
        self._lock = threading.Lock()
        self._running = False
        self._reader_thread: Optional[threading.Thread] = None
        self._file_versions: Dict[str, int] = {}

    def start(self):
        """Starts the persistent `lake serve` process."""
        if self.process is not None:
            return

        cmd = ["lake", "serve"]
        self.process = subprocess.Popen(
            cmd,
            cwd=str(self.project_root),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )
        self._running = True
        self._reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._reader_thread.start()

        # Perform LSP initialization handshake
        self._initialize()

    def stop(self):
        """Gracefully shuts down the LSP server process."""
        self._running = False
        if self.process:
            try:
                self.send_notification("exit")
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception:
                self.process.kill()
            self.process = None

    def _next_id(self) -> int:
        with self._lock:
            self._msg_id += 1
            return self._msg_id

    def send_request(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: float = 15.0) -> Any:
        """Sends a JSON-RPC request and synchronously waits for the response."""
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
            time.sleep(0.05)

        raise TimeoutError(f"Timed out waiting for LSP response to {method} (id={req_id})")

    def send_notification(self, method: str, params: Optional[Dict[str, Any]] = None):
        """Sends a JSON-RPC notification (one-way)."""
        msg = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }
        self._write_msg(msg)

    def _write_msg(self, msg: Dict[str, Any]):
        """Frames a JSON payload with standard Content-Length header and writes to server stdin."""
        if not self.process or not self.process.stdin:
            raise RuntimeError("Lean server process is not running.")
        body = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        try:
            self.process.stdin.write(header + body)
            self.process.stdin.flush()
        except BrokenPipeError:
            self._running = False
            raise RuntimeError("Lean server pipe broken.")

    def _read_loop(self):
        """Continuous background thread reading framed JSON-RPC messages from server stdout."""
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
                        self._handle_notification(data["method"], data.get("params", {}))
            except Exception:
                break

    def _handle_notification(self, method: str, params: Dict[str, Any]):
        """Handles server-pushed notifications such as diagnostics."""
        if method == "textDocument/publishDiagnostics":
            uri = params.get("uri", "")
            diagnostics = params.get("diagnostics", [])
            with self._lock:
                self._diagnostics[uri] = diagnostics

    def _initialize(self):
        """Initializes the LSP session."""
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

    def file_uri(self, file_path: str) -> str:
        """Resolves a relative or absolute file path to a file:// URI."""
        p = pathlib.Path(file_path)
        if not p.is_absolute():
            p = (self.project_root / p).resolve()
        return p.as_uri()

    def open_file(self, file_path: str, content: Optional[str] = None):
        """Opens a file buffer in server memory (`textDocument/didOpen`)."""
        uri = self.file_uri(file_path)
        if content is None:
            p = pathlib.Path(file_path)
            if not p.is_absolute():
                p = self.project_root / p
            content = p.read_text(encoding="utf-8")

        self._file_versions[uri] = 1
        params = {
            "textDocument": {
                "uri": uri,
                "languageId": "lean4",
                "version": 1,
                "text": content,
            }
        }
        self.send_notification("textDocument/didOpen", params)

    def change_file(self, file_path: str, new_content: str):
        """Sends incremental in-memory buffer updates (`textDocument/didChange`)."""
        uri = self.file_uri(file_path)
        version = self._file_versions.get(uri, 1) + 1
        self._file_versions[uri] = version

        params = {
            "textDocument": {
                "uri": uri,
                "version": version,
            },
            "contentChanges": [{"text": new_content}],
        }
        self.send_notification("textDocument/didChange", params)

    def get_goal(self, file_path: str, line: int, col: int, timeout: float = 8.0) -> Optional[str]:
        """
        Queries the exact Lean InfoView tactic proof state (`$/lean/plainGoal`) at (line, col).
        Note: `line` and `col` are 0-indexed in LSP.
        """
        uri = self.file_uri(file_path)
        params = {
            "textDocument": {"uri": uri},
            "position": {"line": line, "character": col},
        }
        result = self.send_request("$/lean/plainGoal", params, timeout=timeout)
        if result and "goals" in result:
            goals = result["goals"]
            if goals:
                return "\n\n".join(goals)
            return "No goals (proof complete or not in tactic state)."
        return None

    def get_term_goal(self, file_path: str, line: int, col: int, timeout: float = 8.0) -> Optional[str]:
        """Queries the Lean term goal (`$/lean/plainTermGoal`) at (line, col)."""
        uri = self.file_uri(file_path)
        params = {
            "textDocument": {"uri": uri},
            "position": {"line": line, "character": col},
        }
        result = self.send_request("$/lean/plainTermGoal", params, timeout=timeout)
        if result and "goal" in result:
            return result["goal"]
        return None

    def get_diagnostics(self, file_path: str) -> List[Dict[str, Any]]:
        """Retrieves currently reported compiler diagnostics/errors for a file."""
        uri = self.file_uri(file_path)
        with self._lock:
            return list(self._diagnostics.get(uri, []))


def interactive_repl(project_root: str, file_path: str):
    """
    Interactive command-line REPL for baby-step tactic exploration with live InfoView feedback.
    """
    print(f"\n=======================================================")
    print(f"   Lean 4 In-Memory InfoView Interactive Assistant     ")
    print(f"=======================================================")
    print(f"Project Root: {project_root}")
    print(f"Target File:  {file_path}")
    print(f"Starting in-memory Lean LSP server (`lake serve`)...")

    client = LeanLspClient(pathlib.Path(project_root))
    try:
        client.start()
        print("✔ Lean LSP server connected and initialized.")

        client.open_file(file_path)
        time.sleep(1.0)  # Allow initial elaboration

        # Read target file lines
        p = pathlib.Path(file_path)
        if not p.is_absolute():
            p = pathlib.Path(project_root) / p
        lines = p.read_text(encoding="utf-8").splitlines()

        print(f"File loaded ({len(lines)} lines).")
        print("\nCommands:")
        print("  goal <line> <col>       - Inspect InfoView goal state at line/col (1-indexed)")
        print("  diag                    - Show current compiler diagnostics/errors")
        print("  try <line> <tactic>     - Test tactic insertion at line and view new goal")
        print("  view <line> [count]     - View surrounding lines of code")
        print("  quit / exit             - Exit assistant\n")

        while True:
            try:
                raw_input = input("lean-infoview> ").strip()
            except (EOFError, KeyboardInterrupt):
                break

            if not raw_input:
                continue

            parts = raw_input.split(maxsplit=2)
            cmd = parts[0].lower()

            if cmd in ("quit", "exit", "q"):
                break
            elif cmd == "goal":
                if len(parts) < 2:
                    print("Usage: goal <line> [col=0] (1-indexed)")
                    continue
                line_idx = int(parts[1]) - 1
                col_idx = int(parts[2]) - 1 if len(parts) > 2 else 0
                goal = client.get_goal(file_path, line_idx, col_idx)
                print("\n--- InfoView Tactic State ---")
                print(goal or "No active goal found.")
                print("-----------------------------\n")
            elif cmd == "diag":
                diags = client.get_diagnostics(file_path)
                if not diags:
                    print("✔ Zero diagnostics (clean compilation).")
                else:
                    print(f"\n--- Diagnostics ({len(diags)}) ---")
                    for d in diags:
                        sev = d.get("severity", 1)
                        sev_str = "ERROR" if sev == 1 else "WARNING" if sev == 2 else "INFO"
                        r = d.get("range", {}).get("start", {})
                        l = r.get("line", 0) + 1
                        c = r.get("character", 0) + 1
                        print(f"[{sev_str}] Line {l}:{c} -> {d.get('message')}")
                    print("------------------------\n")
            elif cmd == "view":
                if len(parts) < 2:
                    print("Usage: view <line> [count=10]")
                    continue
                center_line = int(parts[1])
                count = int(parts[2]) if len(parts) > 2 else 10
                start_l = max(1, center_line - count // 2)
                end_l = min(len(lines), start_l + count)
                print(f"\n--- Code [{start_l}..{end_l}] ---")
                for i in range(start_l, end_l + 1):
                    prefix = " > " if i == center_line else "   "
                    print(f"{prefix}{i:4d} | {lines[i-1]}")
                print("-----------------------\n")
            elif cmd == "try":
                if len(parts) < 3:
                    print("Usage: try <line> <tactic>")
                    continue
                target_line = int(parts[1])
                tactic_text = parts[2]

                # Insert tactic in memory
                new_lines = list(lines)
                indent = "  "
                if 1 <= target_line <= len(new_lines):
                    curr_line = new_lines[target_line - 1]
                    indent = curr_line[:len(curr_line) - len(curr_line.lstrip())]
                new_lines.insert(target_line, f"{indent}{tactic_text}")
                new_content = "\n".join(new_lines)

                client.change_file(file_path, new_content)
                time.sleep(0.5)

                # Check goal immediately after insertion
                goal = client.get_goal(file_path, target_line, len(indent))
                print(f"\n--- InfoView Result after `{tactic_text}` ---")
                print(goal or "Goal closed or no tactic state.")
                print("--------------------------------------------\n")
            else:
                print(f"Unknown command: `{cmd}`. Available: goal, diag, try, view, quit")

    finally:
        client.stop()
        print("Lean LSP server stopped.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python util/lean_infoview.py <file_path> <line> <col>")
        print("  python util/lean_infoview.py --interactive <file_path>")
        sys.exit(1)

    project_dir = str(DEFAULT_PROJECT_DIR)

    if sys.argv[1] == "--interactive":
        target = sys.argv[2] if len(sys.argv) > 2 else "HopfProblem/Basic.lean"
        interactive_repl(project_dir, target)
    else:
        target_file = sys.argv[1]
        line_num = int(sys.argv[2]) - 1 if len(sys.argv) > 2 else 0
        col_num = int(sys.argv[3]) - 1 if len(sys.argv) > 3 else 0

        cli = LeanLspClient(pathlib.Path(project_dir))
        try:
            cli.start()
            cli.open_file(target_file)
            time.sleep(1.0)
            goal_res = cli.get_goal(target_file, line_num, col_num)
            print(f"InfoView Goal at {target_file}:{line_num+1}:{col_num+1}:\n")
            print(goal_res or "No goal found.")
        finally:
            cli.stop()
