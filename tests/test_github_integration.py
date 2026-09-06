"""
Unit tests verifying GitHub repository integration, GitHub Pages site,
and deep links from audit_landscape.tex/pdf to the GitHub repo.
"""

import os
import re
import unittest

from spec.audit_document import AuditDocumentFeat, AuditDocumentGitHubDeepLinkingReq
from spec.github_pages import GitHubPagesFeat, GitHubPagesSiteReq, GitHubRepositoryReq
from spec.main_spec import HopfProblemResolutionFeat


class TestGitHubIntegration(unittest.TestCase):

    def setUp(self):
        self.workspace_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.audit_tex_path = os.path.join(self.workspace_root, "audit_landscape.tex")
        self.docs_dir = os.path.join(self.workspace_root, "docs")
        self.index_html_path = os.path.join(self.docs_dir, "index.html")

    def test_spec_contracts(self):
        """Verify GitHub spec classes and dependency declarations."""
        repo_req = GitHubRepositoryReq()
        self.assertEqual(repo_req.repo_url(), "https://github.com/drhodes/hopf-problem")
        self.assertEqual(repo_req.default_branch(), "main")

        pages_req = GitHubPagesSiteReq()
        self.assertEqual(pages_req.pages_url(), "https://drhodes.github.io/hopf-problem/")
        self.assertEqual(pages_req.pages_source_dir(), "docs")

        audit_gh_req = AuditDocumentGitHubDeepLinkingReq()
        self.assertEqual(audit_gh_req.github_repo_url(), "https://github.com/drhodes/hopf-problem")

        self.assertIn(AuditDocumentGitHubDeepLinkingReq, AuditDocumentFeat.deps)
        self.assertIn(GitHubPagesFeat, HopfProblemResolutionFeat.deps)
        self.assertIn(GitHubRepositoryReq, GitHubPagesFeat.deps)
        self.assertIn(GitHubPagesSiteReq, GitHubPagesFeat.deps)

    def test_docs_index_html_exists_and_contains_summary(self):
        """Verify docs/index.html exists and provides full summary and links."""
        self.assertTrue(os.path.exists(self.index_html_path), "docs/index.html must exist")
        with open(self.index_html_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check title and mathematical subject
        self.assertIn("Hopf Problem", html)
        self.assertIn("Complex Structure on S⁶", html)

        # Check links to PDFs and GitHub
        self.assertIn("audit_landscape.pdf", html)
        self.assertIn("https://github.com/drhodes/hopf-problem", html)
        self.assertTrue(
            "alpo.ge/s6.pdf" in html or "paper/main.pdf" in html or "paper.pdf" in html,
            "Must link to the paper PDF"
        )

        # Check invariants presence
        self.assertIn("Smale-Barden", html)
        self.assertIn("b₂(X) = 0", html)

    def test_audit_tex_has_github_links(self):
        """Verify audit_landscape.tex contains active links to the GitHub repo."""
        self.assertTrue(os.path.exists(self.audit_tex_path), "audit_landscape.tex must exist")
        with open(self.audit_tex_path, "r", encoding="utf-8") as f:
            tex = f.read()

        # Check repository link
        self.assertIn("github.com/drhodes/hopf-problem", tex)

        # Check source links into the repo via \githublean definition and usages
        self.assertIn(r"\newcommand{\githublean}[2]{\href{https://github.com/drhodes/hopf-problem/blob/main/HopfProblem/HopfProblem/#1}{#2}}", tex)
        macro_usages = re.findall(r"\\githublean\{(\w+\.lean)\}", tex)
        self.assertGreater(
            len(macro_usages),
            10,
            f"Expected at least 10 Lean source link macro usages into GitHub repo, found {len(macro_usages)}"
        )


if __name__ == "__main__":
    unittest.main()
