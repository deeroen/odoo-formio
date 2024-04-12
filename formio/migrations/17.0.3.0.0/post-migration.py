# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import ast
import json
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    options_default = env.ref('formio.formio_builder_js_options_default')
    options_default_dict = json.loads(options_default.value)

    # 1. formio.builder.js.options
    # Merge options, but keep existing options.
    for js_options in env['formio.builder.js.options'].search([]):
        try:
            options_dict = json.loads(js_options.value)
        except Exception:
            options_dict = ast.literal_eval(js_options.value)
        # Keep options_dict['editForm'] and add options_default_dict['editForm']
        write_options_dict = {
            **options_dict['editForm'],
            **options_default_dict['editForm']
        }
        value = json.dumps({'editForm': write_options_dict}, indent=4)
        js_options.write({'value': value})

    # 2. formio.builder
    # Merge options, but keep existing options.
    domain = [('formio_js_options', '!=', False)]
    for builder in env['formio.builder'].search(domain):
        try:
            options_dict = json.loads(builder.formio_js_options)
        except Exception:
            options_dict = ast.literal_eval(builder.formio_js_options)
        # Keep options_dict['editForm'] and add options_default_dict['editForm']
        write_options_dict = {
            **options_dict['editForm'],
            **options_default_dict['editForm']
        }
        formio_js_options = json.dumps({'editForm': write_options_dict}, indent=4)
        builder.write({'formio_js_options': formio_js_options})

    # 3. formio.builder
    # Add options.
    domain = [('formio_js_options', '=', False)]
    builders = env['formio.builder'].search(domain)
    builders.write({'formio_js_options': options_default.value})
