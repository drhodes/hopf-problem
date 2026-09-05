"""
Unit and Contract Tests for Paper URL Deep Linking.
Verifies compliance with PaperUrlDeepLinkingReq and LeanSourcePaperDeepLinkingReq.
"""

import os
import re
import unittest

from spec.audit_document import PaperUrlDeepLinkingReq, LeanSourcePaperDeepLinkingReq


class TestPaperUrlDeepLinking(unittest.TestCase):
    def setUp(self):
        self.spec_req = PaperUrlDeepLinkingReq()
        self.lean_req = LeanSourcePaperDeepLinkingReq()
        self.workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def test_spec_attributes(self):
        """Verify that specifications declare the canonical base URL and page mapping."""
        self.assertEqual(self.spec_req.base_url(), "https://alpo.ge/s6.pdf")
        self.assertEqual(self.lean_req.base_url(), "https://alpo.ge/s6.pdf")
        mapping = self.spec_req.canon_page_mapping()
        self.assertIsInstance(mapping, dict)
        self.assertGreaterEqual(len(mapping), 20)

    def test_canonical_page_bounds(self):
        """Verify that all referenced page numbers exist within s6.pdf (1 to 108)."""
        mapping = self.spec_req.canon_page_mapping()
        for key, page in mapping.items():
            self.assertIsInstance(page, int, f"Page for {key} must be an integer")
            self.assertGreaterEqual(page, 1, f"Page for {key} must be >= 1")
            self.assertLessEqual(page, 108, f"Page for {key} must be <= 108")
            url = self.spec_req.page_url(page)
            self.assertTrue(url.startswith("https://alpo.ge/s6.pdf#page="))

    def test_audit_tex_contains_deep_links(self):
        """Verify that audit_landscape.tex has hyperlinks to https://alpo.ge/s6.pdf."""
        tex_path = os.path.join(self.workspace_root, "audit_landscape.tex")
        self.assertTrue(os.path.exists(tex_path), "audit_landscape.tex must exist")
        with open(tex_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for presence of canonical URL base with page fragment
        links = re.findall(r"https://alpo\.ge/s6\.pdf#page=(\d+)", content)
        self.assertGreater(len(links), 20, f"Expected at least 20 deep links in audit_landscape.tex, found {len(links)}")

    def test_lean_sources_contain_deep_links(self):
        """Verify that target Lean source files in HopfProblem/ contain paper deep links."""
        modules = self.lean_req.target_modules()
        for mod in modules:
            mod_path = os.path.join(self.workspace_root, mod)
            self.assertTrue(os.path.exists(mod_path), f"Lean module {mod} must exist")
            with open(mod_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(
                "https://alpo.ge/s6.pdf",
                content,
                f"Lean file {mod} must link to https://alpo.ge/s6.pdf"
            )


if __name__ == "__main__":
    unittest.main()
