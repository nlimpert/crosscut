# Minimal makefile for Sphinx documentation generation and deployment.
#
# Author: Nicolas Limpert, Marcus Meeßen (minor changes)
# Copyright: Copyright (C) 2019 MASCOR Institute
# Version: 1.0
SILENT         = @

# You can set these variables from the command line.
SPHINX_OPTIONS =
SPHINX_BUILD   = sphinx-build
SOURCE_DIR     = .
BUILD_DIR      = build
DEPLOY_DIR     =

# Put it first so that "make" without argument is like "make help".
help:
	$(SILENT) $(SPHINX_BUILD) -M help \
	                         "$(SOURCE_DIR)" \
	                         "$(BUILD_DIR)" \
	                         $(SPHINX_OPTIONS) \
	                         $(O)
	$(SILENT) echo " \033[1;34m server \033[1;37m   " \
	               "\033[0m to execute a local web server"
	$(SILENT) echo " \033[1;34m deploy \033[1;37m   " \
	               "\033[0m to deploy to production server"

.PHONY: help

server:
	$(SILENT) echo " ---------------------------------------------------------- "
	$(SILENT) echo " -- Starting local web server in terminal..."
	$(SILENT) echo " -- Visit localhost:8000/ with your web browser."
	$(SILENT) echo " -- Press Control-C to stop the local web server."
	$(SILENT) cd build/html \
	          && trap 'echo " -> DONE!"' 2 \
	          && python3 -m http.server

.PHONY: server

deploy:
	$(SILENT) echo " ---------------------------------------------------------- "
	$(SILENT) echo " -- Deploying to production server..."
	$(SILENT) rsync -avz build/html/ \
	                robolab@maskor.fh-aachen.de:/var/www/vhosts/rosin.maskor.fh-aachen.de/$(DEPLOY_DIR)
	$(SILENT) echo " -> DONE!"

.PHONY: deploy

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINX_OPTIONS).
%: Makefile
	$(SILENT) $(SPHINX_BUILD) -M $@ \
	                         "$(SOURCE_DIR)" \
	                         "$(BUILD_DIR)" \
	                         $(SPHINX_OPTIONS) \
	                         $(O)

.PHONY: Makefile
