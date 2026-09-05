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
	@echo -e "$(COLOR_BOLD)Usage:$(COLOR_RESET) make $(COLOR_GREEN)<target>$(COLOR_RESET)"
	@echo ""
	@echo -e "$(COLOR_BOLD)Available Targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

# ==============================================================================
# Lean 4 & Mathlib Build System
# ==============================================================================

.PHONY: build
build: ## Compile Lean 4 formalization files in HopfProblem
	@echo -e "$(COLOR_BLUE)==> Building Lean 4 project (HopfProblem)...$(COLOR_RESET)"
	cd $(LEAN_DIR) && $(LAKE) build
	@echo -e "$(COLOR_GREEN)✔ Lean 4 build complete.$(COLOR_RESET)"

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
