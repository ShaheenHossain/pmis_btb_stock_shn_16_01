# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
import datetime
from odoo.osv.expression import get_unaccent_wrapper
import re
READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel'}
}

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    document=fields.Binary('Document/Challan')
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    document=fields.Binary('Document/Challan')
    validity_date = fields.Date(
        string="Sheduled Date",
        compute='_compute_validity_date',
        store=True, readonly=False, copy=False, precompute=True,
        states=READONLY_FIELD_STATES)
    approved_by=fields.Many2one("res.users","Approved By")
    approved_on=fields.Datetime("Approval Date")
    confirmed_by=fields.Many2one("res.users","Confirmed By")
    confirmed_on=fields.Datetime("Confirmation Date")
    state = fields.Selection(
        selection=[
            ('draft', "Requisition"),
            ('sent', "Submitted"),
            ('approved', "Requisition Approved"),
            ('sale', "Confirmed"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    purpose=fields.Char("Purpose")

    def action_cancel(self):
        return self._action_cancel()



    def action_approve(self):

        for order in self:
            order.state="approved"
            order.approved_by=self.env.user.id
            order.approved_on=datetime.datetime.now()

    def action_confirm(self):


        self.confirmed_by=self.env.user.id
        self.confirmed_on=datetime.datetime.now()

        return super(SaleOrder,self).action_confirm()

    def action_submit(self):

        for order in self:
            order.state="sent"

    def _compute_access_url(self):
        # super()._compute_access_url()
        for order in self:
            order.access_url = f'/my/requisitions/{order.id}'

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    current_stock=fields.Float("Current Stock",compute="get_stock_status",store="True")
    free_stock=fields.Float("Free Qty" ,compute="get_stock_status",store="True")

    @api.depends("product_id")
    def get_stock_status(self):
        for rec in self:
            rec.current_stock=rec.qty_available_today
            rec.free_stock=rec.free_qty_today
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    detailed_type = fields.Selection(selection_add=[
        ('product', 'Storable Product')
    ], tracking=True, ondelete={'product': 'set consu'},default='product')