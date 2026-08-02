# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request

from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment import utils as payment_utils
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager


# class CustomerPortal(portal.CustomerPortal):
#
#     def _prepare_home_portal_values(self, counters):
#         values = super()._prepare_home_portal_values(counters)
#         partner = request.env.user.partner_id
#
#         SaleOrder = request.env['sale.order']
#         if 'quotation_count' in counters:
#             values['quotation_count'] = SaleOrder.search_count(self._prepare_quotations_domain(partner)) \
#                 if SaleOrder.check_access_rights('read', raise_exception=False) else 0
#         if 'order_count' in counters:
#             values['order_count'] = SaleOrder.search_count(self._prepare_orders_domain(partner)) \
#                 if SaleOrder.check_access_rights('read', raise_exception=False) else 0
#
#         return values
