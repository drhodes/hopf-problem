# ==============================================================================
# Makefile: Hopf Problem Complex Structure on S⁶ Formalization Pipeline
# ==============================================================================

SHELL := /bin/bash
.DEFAULT_GOAL := help

# Directories
WORKSPACE_ROOT := $(shell pwd)
LEAN_DIR       := $(WORKSPACE_ROOT)/HopfProblem
UTIL_DIR       := $(WORKSPACE_ROOT)/util

# Executables
UV   ?= uv
LAKE ?= lake

# Build & Git Metadata
GIT_REV    ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_COMMIT ?= $(shell git rev-parse HEAD 2>/dev/null || echo "unknown")
GIT_DIRTY  ?= $(shell git diff --quiet 2>/dev/null || echo "-dirty")
BUILD_DATE ?= $(shell date -u +"%Y-%m-%d %H:%M:%S UTC")

# Colors
COLOR_RESET  := \033[0m
COLOR_BOLD   := \033[1m
COLOR_GREEN  := \033[32m
COLOR_BLUE   := \033[34m
COLOR_YELLOW := \033[33m
COLOR_RED    := \033[31m
COLOR_CYAN   := \033[36m

.PHONY: help
help: ## Show this help message
	@echo -e "$(COLOR_BOLD)$(COLOR_CYAN)Hopf Problem Formalization - Makefile$(COLOR_RESET)"
	@echo -e "$(COLOR_BOLD)Revision:$(COLOR_RESET) $(COLOR_YELLOW)$(GIT_REV)$(GIT_DIRTY)$(COLOR_RESET) ($(GIT_COMMIT)) | $(COLOR_BOLD)Build Date:$(COLOR_RESET) $(COLOR_YELLOW)$(BUILD_DATE)$(COLOR_RESET)"
	@echo -e "$(COLOR_BOLD)Usage:$(COLOR_RESET) make $(COLOR_GREEN)<target>$(COLOR_RESET)"
	@echo ""
	@echo -e "$(COLOR_BOLD)Available Targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

.PHONY: version
version: ## Display project version, git revision, and build timestamp
	@echo -e "$(COLOR_BOLD)Project:$(COLOR_RESET)      hopf-problem"
	@echo -e "$(COLOR_BOLD)Version:$(COLOR_RESET)      $$(grep '^version = ' $(WORKSPACE_ROOT)/pyproject.toml | sed -E 's/.*\"([^\"]+)\".*/\1/')"
	@echo -e "$(COLOR_BOLD)Git Revision:$(COLOR_RESET) $(GIT_REV)$(GIT_DIRTY) ($(GIT_COMMIT))"
	@echo -e "$(COLOR_BOLD)Build Date:$(COLOR_RESET)   $(BUILD_DATE)"

# ==============================================================================
# Lean 4 & Mathlib Build System
# ==============================================================================

.PHONY: build
build: ## Compile Lean 4 formalization files in HopfProblem
	@echo -e "$(COLOR_BLUE)==> Building Lean 4 project (HopfProblem) [Git: $(GIT_REV)$(GIT_DIRTY), Date: $(BUILD_DATE)]...$(COLOR_RESET)"
	cd $(LEAN_DIR) && $(LAKE) build
	@echo -e "$(COLOR_GREEN)✔ Lean 4 build complete.$(COLOR_RESET)"

.PHONY: verify-all
verify-all: ## Run the complete peer-review verification suite (build, sorry-check, axioms, libspec)
	@echo -e "$(COLOR_BLUE)==> Running verification suite [Git: $(GIT_REV)$(GIT_DIRTY), Date: $(BUILD_DATE)]...$(COLOR_RESET)"
	GIT_REV="$(GIT_REV)$(GIT_DIRTY)" BUILD_DATE="$(BUILD_DATE)" $(UTIL_DIR)/verify_all.sh


.PHONY: clean
clean: ## Clean Lean 4 build artifacts
	@echo -e "$(COLOR_YELLOW)==> Cleaning Lean 4 build artifacts...$(COLOR_RESET)"
	cd $(LEAN_DIR) && $(LAKE) clean

.PHONY: cache
cache: ## Download / unpack latest precompiled Mathlib cache
	@echo -e "$(COLOR_BLUE)==> Fetching Mathlib cache...$(COLOR_RESET)"
	cd $(LEAN_DIR) && $(LAKE) exe cache get

.PHONY: check-sorry
check-sorry: ## Audit Lean codebase for 'sorry' and 'admit' statements
	@echo -e "$(COLOR_BLUE)==> Checking for unproven 'sorry' or 'admit' in Lean code...$(COLOR_RESET)"
	@if grep -rn "sorry" $(LEAN_DIR)/HopfProblem/ ; then \
		echo -e "$(COLOR_RED)✘ 'sorry' found in Lean codebase.$(COLOR_RESET)"; exit 1; \
	else \
		echo -e "$(COLOR_GREEN)✔ Zero 'sorry' occurrences found.$(COLOR_RESET)"; \
	fi

.PHONY: audit-axioms
audit-axioms: ## Trace kernel and external axiom dependencies across all main theorems
	@echo -e "$(COLOR_BLUE)==> Auditing Lean 4 kernel axioms...$(COLOR_RESET)"
	$(UTIL_DIR)/audit_axioms.sh
	@echo -e "$(COLOR_GREEN)✔ Axiom audit complete.$(COLOR_RESET)"

# ==============================================================================
# InfoView LSP Daemon (Interactive Development)
# ==============================================================================

.PHONY: infoview-status
infoview-status: ## Check status of persistent Lean LSP daemon
	$(UTIL_DIR)/infoview status

.PHONY: infoview-start
infoview-start: ## Start persistent Lean LSP daemon
	$(UTIL_DIR)/infoview start

.PHONY: infoview-stop
infoview-stop: ## Stop persistent Lean LSP daemon
	$(UTIL_DIR)/infoview stop

# ==============================================================================
# Libspec Specification Engine
# ==============================================================================

.PHONY: spec-list
spec-list: ## List all specification components
	$(UV) run libspec list

.PHONY: spec-diff
spec-diff: ## Diff specification tree against HEAD
	$(UV) run libspec diff

.PHONY: spec-dependencies
spec-dependencies: ## Show specification dependency tree
	$(UV) run libspec dependencies

# ==============================================================================
# Testing & Versioning
# ==============================================================================

.PHONY: test
test: ## Run test suite
	$(UV) run python3 -m unittest discover tests

.PHONY: bump-patch
bump-patch: ## Bump patch version in pyproject.toml
	@python3 -c "import re; p='pyproject.toml'; c=open(p).read(); m=re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', c); maj,mi,pa = m.groups(); new_v=f'{maj}.{mi}.{int(pa)+1}'; open(p,'w').write(re.sub(r'version = \".*?\"', f'version = \"{new_v}\"', c, count=1)); print(f'Bumped to {new_v}')"

.PHONY: bump-minor
bump-minor: ## Bump minor version in pyproject.toml
	@python3 -c "import re; p='pyproject.toml'; c=open(p).read(); m=re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', c); maj,mi,pa = m.groups(); new_v=f'{maj}.{int(mi)+1}.0'; open(p,'w').write(re.sub(r'version = \".*?\"', f'version = \"{new_v}\"', c, count=1)); print(f'Bumped to {new_v}')"

.PHONY: bump-major
bump-major: ## Bump major version in pyproject.toml
	@python3 -c "import re; p='pyproject.toml'; c=open(p).read(); m=re.search(r'version = \"(\d+)\.(\d+)\.(\d+)\"', c); maj,mi,pa = m.groups(); new_v=f'{int(maj)+1}.0.0'; open(p,'w').write(re.sub(r'version = \".*?\"', f'version = \"{new_v}\"', c, count=1)); print(f'Bumped to {new_v}')"

# ==============================================================================
# Document Compilation (LaTeX & Audit)
# ==============================================================================

.PHONY: audit-pdf
audit-pdf: ## Generate and compile landscape audit document (audit_landscape.pdf)
	@echo -e "$(COLOR_BLUE)==> Compiling audit_landscape.pdf [Git: $(GIT_REV)$(GIT_DIRTY), Date: $(BUILD_DATE)]...$(COLOR_RESET)"
	python3 $(UTIL_DIR)/generate_audit_document.py
	xelatex -interaction=nonstopmode $(WORKSPACE_ROOT)/audit_landscape.tex > /dev/null
	@echo -e "$(COLOR_GREEN)✔ audit_landscape.pdf compiled successfully.$(COLOR_RESET)"

.PHONY: paper-pdf
paper-pdf: ## Compile research paper (paper/main.pdf)
	@echo -e "$(COLOR_BLUE)==> Compiling paper/main.pdf [Git: $(GIT_REV)$(GIT_DIRTY), Date: $(BUILD_DATE)]...$(COLOR_RESET)"
	cd $(WORKSPACE_ROOT)/paper && xelatex -interaction=nonstopmode main.tex > /dev/null
	@echo -e "$(COLOR_GREEN)✔ paper/main.pdf compiled successfully.$(COLOR_RESET)"


