# Minimal makefile for Sphinx documentation generation and deployment.

# Author: Nicolas Limpert, Marcus Meeßen (minor changes)
# Copyright: Copyright (C) 2019 MASCOR Institute
# Version: 1.1

# Variables can be set from command line.
SILENT         = @
SPHINX_OPTIONS =
SPHINX_BUILD   = sphinx-build
SOURCE_DIR     = .
BUILD_DIR      = build/author
REMOTE_ADDRESS = 
REMOTE_USER    = 
DEPLOY_ROOT    = 
DEPLOY_DIR     =

# Put it first so that "make" without argument is like "make help".
help:
	$(SILENT) $(SPHINX_BUILD) -M help           \
	                          "$(SOURCE_DIR)"   \
	                          "$(BUILD_DIR)"    \
	                          $(SPHINX_OPTIONS) \
	                          $(O)
	$(SILENT) echo " \033[1;34m server \033[1;37m\033[0m"   \
	               "    to execute a local web server"      \
	               "\n \033[1;34m deploy \033[1;37m\033[0m" \
	               "    to deploy to a production server"

.PHONY: help

server:
	$(SILENT) echo " ---------------------------------------------------------" \
	               "\n -- Starting local web server in terminal..."             \
	               "\n -- Visit http://localhost:8000/ with a web browser."     \
	               "\n -- Press Control-C to stop the local web server."
	$(SILENT) cd $(BUILD_DIR)/html/          \
	          && trap 'echo " -> DONE!"' INT \
	          && python3 -m http.server

.PHONY: server

deploy:
	$(SILENT) echo " ---------------------------------------------------------" \
	               "\n -- Deploying to production server..."
	$(SILENT) rsync -avz $(BUILD_DIR)/html/                                     \
	                $(REMOTE_USER)@$(REMOTE_ADDRESS):$(DEPLOY_ROOT)$(DEPLOY_DIR)\
             && echo " -> DONE!"

.PHONY: deploy

# Catch-all target that routes all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINX_OPTIONS).
%: Makefile
	$(SILENT) $(SPHINX_BUILD) -M $@             \
	                          "$(SOURCE_DIR)"   \
	                          "$(BUILD_DIR)"    \
	                          $(SPHINX_OPTIONS) \
	                          $(O)

.PHONY: Makefile
