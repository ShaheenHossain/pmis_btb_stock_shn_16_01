# -*- coding: utf-8 -*-
"""Post-migration script for btb_stock 16.0.1.1.5.

Uninstalls apps that are not needed on this instance and were causing
issues (e.g. the "Missing field string information for the field
'enable_ocn'" error in Settings, coming from mail_mobile) or are simply
unused clutter.

Note: this only runs when the module is *upgraded* through this version
(e.g. `-u btb_stock`), not on a fresh install. If these apps should also
be removed on a brand new install, a post_init_hook should be added too.
"""
from odoo import api, SUPERUSER_ID

MODULES_TO_UNINSTALL = [
    'mail_mobile',
    'web_map',
    'currency_rate_live',
    'account_invoice_extract',
]


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    modules = env['ir.module.module'].search([
        ('name', 'in', MODULES_TO_UNINSTALL),
        ('state', '=', 'installed'),
    ])
    # if modules:
    #     modules.button_immediate_uninstall()
    return True