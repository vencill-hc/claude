# Claude Code setup — bootstrap and profile management
#
# Usage:
#   make install                       # full bootstrap on a fresh machine
#   make gstack                        # clone gstack as a sibling repo
#   make activate PROFILES="core gdu"
#   make list                          # list available profiles
#   make show                          # show currently active

REPO_DIR := $(shell pwd)
CLAUDE_DIR := $(HOME)/.claude
GSTACK_DIR := $(HOME)/Documents/git/gstack
GSTACK_REMOTE := https://github.com/garrytan/gstack.git
DEFAULT_PROFILES ?= core

.PHONY: help install dirs gstack activate list show clean

help:
	@echo "Claude Code setup"
	@echo ""
	@echo "  make install                            full bootstrap"
	@echo "  make gstack                             clone gstack repo (only needed for the 'dev' profile)"
	@echo "  make activate PROFILES=\"core gdu\"       activate one or more profiles"
	@echo "  make list                               list profiles"
	@echo "  make show                               show currently active profiles"
	@echo ""
	@echo "Defaults: PROFILES=$(DEFAULT_PROFILES)"

install: dirs gstack
	@echo "Activating default profiles: $(DEFAULT_PROFILES)"
	@node $(REPO_DIR)/activate-profile.js $(DEFAULT_PROFILES)
	@echo ""
	@echo "Done. Add to your shell rc:"
	@echo "  alias claude-profile=\"node $(REPO_DIR)/activate-profile.js\""

dirs:
	@mkdir -p $(CLAUDE_DIR)/skills $(CLAUDE_DIR)/agents $(CLAUDE_DIR)/commands

gstack:
	@if [ ! -d $(GSTACK_DIR) ]; then \
		echo "Cloning gstack to $(GSTACK_DIR)"; \
		mkdir -p $(dir $(GSTACK_DIR)); \
		git clone $(GSTACK_REMOTE) $(GSTACK_DIR); \
	else \
		echo "gstack already present at $(GSTACK_DIR)"; \
	fi

activate:
	@node $(REPO_DIR)/activate-profile.js $(PROFILES)

list:
	@node $(REPO_DIR)/activate-profile.js --list

show:
	@node $(REPO_DIR)/activate-profile.js --show

clean:
	@echo "Removing all profile-managed symlinks from $(CLAUDE_DIR)/{skills,agents,commands}"
	@for d in skills agents commands; do \
		find $(CLAUDE_DIR)/$$d -maxdepth 1 -type l -delete 2>/dev/null || true; \
	done
	@rm -f $(CLAUDE_DIR)/.active-profiles
