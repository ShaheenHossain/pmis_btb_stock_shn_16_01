# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_, api
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
import re
import num2words
from googletrans import Translator
import num2words

class pmisCompany(models.Model):
    _inherit = "res.company"
    logo2 = fields.Binary("logo2")

class ResPartner(models.Model):
    _inherit = "res.partner"

    pds_id = fields.Char("PDS ID")
    _sql_constraints = [
        ('pds_id_unique', 'unique (pds_id)',
         "PDS ID must be unique, this PDS ID is already assigned."),
    ]
    def get_customized_action(self):
        pmis=self.env['ir.module.module'].search([('name', '=', 'pmis')])
        if pmis and pmis.state=='installed':
            return {
                'type': 'ir.actions.act_window',
                'name': _('Employee'),
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                # 'form_view_id': 'ref="base.view_partner_form"',
                'views': [
                    [self.env.ref('pmis.pmis_res_partner_list').id, 'tree'],
                    [self.env.ref('base.view_partner_form').id, 'form'],
                ],
                # 'view_id': view_id_tree.id,
                # 'view_ids': 'eval="[(5, 0, 0),(0, 0, {\'view_mode\': \'tree\', \'view_id\': ref(\'pmis.pmis_res_partner_list\')}),(0, 0, {\'view_mode\': \'form\', \'view_id\': ref(\'base.view_partner_form\')})]"',
                # 'views': [('pmis.pmis_res_partner_list', 'tree'), ('base.view_partner_form', 'form')],
                'target': 'current',
                'domain': [('pds_id', '>',1)]
                # 'res_id': your.model.id,
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'name': _('Employee'),
                'res_model': 'res.partner',
                'view_type': 'form',
                'view_mode': 'tree,form',
                # 'view_id': view_id_tree.id,
                # 'views': [(view_id_tree.id, 'tree'), (view_id_form.id, 'form')],
                'target': 'current',
                'domain': [('is_company', '=', False)]
                # 'res_id': your.model.id,
            }
