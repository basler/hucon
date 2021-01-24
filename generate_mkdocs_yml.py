#!/usr/bin/env python3
""" generate_mkdocs_yml.py - Generate the mkdocs config files for the different
                             languages based on the config template and doc config json file.

    Copyright (C) 2020 Basler AG
    All rights reserved.

    This software may be modified and distributed under the terms
    of the BSD license.  See the LICENSE file for details.
"""

from jinja2 import Template
import json

with open('docs_config.json') as json_file:
    config = json.load(json_file)

    for language in config['language']:

        with open('mkdocs-template.yml') as tmp_file:
            config['language'][language]['language'] = language
            tmp = Template(tmp_file.read())
            msg = tmp.render(config['language'][language])

            with open('mkdocs-%s.yml' % language, 'w') as lang_file:
                lang_file.write(msg)
