"""
Unit tests verifying BuildMetadataReq and Makefile git revision & build date functionality.
"""

import os
import re
import subprocess
import unittest

from spec.lean_project import BuildMetadataReq, LeanProjectFeat


class TestBuildMetadata(unittest.TestCase):

    def setUp(self):
        self.workspace_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.makefile_path = os.path.join(self.workspace_root, "Makefile")

    def test_spec_build_metadata_req(self):
        """Verify BuildMetadataReq spec class contracts."""
        req = BuildMetadataReq()
        self.assertEqual(req.verification_status(), "VERIFIED")
        
        rev = req.git_revision()
        self.assertTrue(len(rev) >= 4, f"Invalid git revision: {rev}")
        
        date_str = req.build_date()
        self.assertIn("UTC", date_str)
        self.assertRegex(date_str, r"^\d{4}-\d{2}-\d{2}")

    def test_lean_project_feat_includes_metadata_req(self):
        """Verify LeanProjectFeat declares dependency on BuildMetadataReq."""
        self.assertIn(BuildMetadataReq, LeanProjectFeat.deps)

    def test_makefile_defines_git_rev_and_build_date(self):
        """Verify Makefile defines GIT_REV and BUILD_DATE variables."""
        with open(self.makefile_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("GIT_REV", content, "Makefile must define GIT_REV")
        self.assertIn("BUILD_DATE", content, "Makefile must define BUILD_DATE")

    def test_make_version_target(self):
        """Verify `make version` outputs git revision and build date."""
        proc = subprocess.run(
            ["make", "version"],
            cwd=self.workspace_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, f"make version failed: {proc.stderr}")
        self.assertIn("Git Revision:", proc.stdout)
        self.assertIn("Build Date:", proc.stdout)

    def test_make_help_displays_metadata(self):
        """Verify `make help` displays git revision and build date."""
        proc = subprocess.run(
            ["make", "help"],
            cwd=self.workspace_root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, f"make help failed: {proc.stderr}")
        self.assertIn("Revision:", proc.stdout)
        self.assertIn("Build Date:", proc.stdout)


if __name__ == "__main__":
    unittest.main()
