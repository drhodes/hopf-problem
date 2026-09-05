"""
Specification for GitHub Repository, GitHub Pages, and Remote Dissemination
"""

from .err import Feat, Req
from .lean_project import Lean4ProjectReq


class GitHubRepositoryReq(Req):
    """
    The formalization codebase must be published to a public GitHub repository
    under the user namespace (drhodes/hopf-problem), tracking git branches,
    tags, and commits with remote origin configured.
    """
    deps = [Lean4ProjectReq]

    def repo_url(self):
        return "https://github.com/drhodes/hopf-problem"

    def default_branch(self):
        return "main"


class GitHubPagesSiteReq(Req):
    """
    A public-facing GitHub Pages documentation site must be deployed at
    https://drhodes.github.io/hopf-problem/ from the `docs/` tree, serving
    an elegant, academic summary of the formalization, mirror of the README,
    and direct download/viewing links for the landscape audit PDF and research paper.
    """
    deps = [GitHubRepositoryReq]

    def pages_url(self):
        return "https://drhodes.github.io/hopf-problem/"

    def pages_source_dir(self):
        return "docs"


class GitHubPagesFeat(Feat):
    """
    Feature governing remote repository hosting, web dissemination via GitHub Pages,
    and reciprocal hyperlinking between documentation, paper, and code.
    """
    deps = [GitHubRepositoryReq, GitHubPagesSiteReq]
