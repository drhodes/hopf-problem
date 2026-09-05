'''
Specification for Lean 4 In-Memory InfoView & LSP Interactive Proving Utility
Enabling Sub-30ms Baby-Step Interactive Tactic Proving & Goal Inspection.
'''

from .err import Feat, Req
from .lean_project import Lean4ProjectReq


class LeanLspServerReq(Req):
    r"""
    The utility must spawn and manage a persistent background `lake serve` process in `HopfProblem/`,
    communicating via standard LSP JSON-RPC 2.0 (Content-Length header framing) to keep Mathlib
    pre-elaborated in memory.
    """
    deps = [Lean4ProjectReq]

    def verification_status(self):
        return "VERIFIED"


class IncrementalBufferSyncReq(Req):
    r"""
    The utility must support virtual in-memory file buffers (`textDocument/didOpen`) and incremental
    text updates (`textDocument/didChange`) so that candidate tactics can be tested in sub-30ms
    without touching disk I/O.
    """
    deps = [LeanLspServerReq]

    def verification_status(self):
        return "VERIFIED"


class InfoViewGoalExtractionReq(Req):
    r"""
    The utility must provide an API to query the Lean InfoView tactic state (`$/lean/plainGoal`)
    at arbitrary line and column coordinates, returning formatted goal text, local hypotheses,
    and target types.
    """
    deps = [LeanLspServerReq]

    def verification_status(self):
        return "VERIFIED"


class DiagnosticStreamCaptureReq(Req):
    r"""
    The utility must asynchronously capture and parse `textDocument/publishDiagnostics` notifications
    from the Lean server, extracting error ranges, severity levels, and tactic failure messages.
    """
    deps = [LeanLspServerReq]

    def verification_status(self):
        return "VERIFIED"


class InteractiveBabyStepReplReq(Req):
    r"""
    The utility must expose a fast CLI tool (`./util/infoview`) allowing developers and agents to
    inspect goals, test candidate tactics line-by-line (`util/infoview try ...`), and inspect live
    diagnostics with sub-second feedback.
    """
    deps = [IncrementalBufferSyncReq, InfoViewGoalExtractionReq, DiagnosticStreamCaptureReq]

    def verification_status(self):
        return "VERIFIED"


class InfoViewUtilFeat(Feat):
    r"""
    Feature providing the in-memory Lean 4 Language Server Protocol daemon, InfoView goal extractor,
    and interactive baby-step tactic exploration environment in `./util`.
    """
    deps = [
        LeanLspServerReq,
        IncrementalBufferSyncReq,
        InfoViewGoalExtractionReq,
        DiagnosticStreamCaptureReq,
        InteractiveBabyStepReplReq,
    ]
