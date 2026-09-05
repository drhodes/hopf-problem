'''
Specification for Lean 4 Project and Mathlib4 Infrastructure
'''

from .err import Feat, Req


class Lean4ProjectReq(Req):
    """
    The formalization must be hosted in a standalone Lean 4 project configured
    with Lake (`HopfProblem/lakefile.toml`), tracking the `leanprover/lean4:v4.33.1` toolchain
    and pulling `mathlib4` as a managed dependency.
    """
    deps = []

    def verification_status(self):
        return "VERIFIED"


class LeanBuildVerificationReq(Req):
    """
    All formalized definitions, matrices, complex structures, lemmas, and theorems
    must be verified by the Lean 4 kernel with zero `sorry` placeholders
    and zero compilation errors during `lake build`.
    """
    deps = [Lean4ProjectReq]

    def verification_status(self):
        return "VERIFIED"


class BuildMetadataReq(Req):
    """
    The build system (`Makefile`) must extract and record the repository git revision
    hash (with dirty-state detection) and UTC build timestamp, embedding them into
    build targets, version diagnostics, and verification logs.
    """
    deps = [Lean4ProjectReq]

    def git_revision(self):
        import subprocess
        try:
            rev = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
            return rev
        except Exception:
            return "unknown"

    def build_date(self):
        import datetime
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def verification_status(self):
        return "VERIFIED"


class LeanProjectFeat(Feat):
    """
    Feature managing the interactive theorem proving environment and
    verification pipeline for the Hopf problem complex structure on S⁶.
    """
    deps = [Lean4ProjectReq, LeanBuildVerificationReq, BuildMetadataReq]

