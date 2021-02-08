#!/bin/bash -e
# build_doc.sh - Build the documentation with different languages.
#
# Copyright (C) 2020 Basler AG
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

python generate_mkdocs_yml.py

mkdocs build -f mkdocs-en.yml --verbose --clean --strict
mkdocs build -f mkdocs-de.yml --verbose --clean --strict

cp docs/index.html site