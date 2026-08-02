# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
import datetime
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError
import re
READONLY_FIELD_STATES = {
    state: [('readonly', True)]
    for state in {'sale', 'done', 'cancel'}
}

class partner(models.Model):
    _inherit = 'res.partner'
    state=fields.Selection(selection=[
            ('draft', "Draft"),
            ('sent', "Submitted"),
            ('approved', "Approved"),
            ('sale', "Confirmed")],
    string = "Status",
    readonly = True, copy = False, index = True,
    tracking = 3,
    default = 'draft')

class ResCompany(models.Model):
    _inherit = 'res.company'
    btb_second_approval_threshold = fields.Monetary(
        "2nd Approval Threshold", currency_field='currency_id', default=0.0,
        help="Requisitions with a total at or above this amount require an additional "
             "Finance Approver sign-off before they can be confirmed. Set to 0 to disable.")


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

    cancel_reason = fields.Text("Cancellation Reason", readonly=True, copy=False)

    second_approval_required = fields.Boolean(
        "Requires 2nd Approval", compute="_compute_second_approval_required", store=True)
    second_approved_by = fields.Many2one("res.users", "2nd Approved By", readonly=True, copy=False)
    second_approved_on = fields.Datetime("2nd Approval Date", readonly=True, copy=False)

    @api.depends('amount_total', 'company_id.btb_second_approval_threshold')
    def _compute_second_approval_required(self):
        for order in self:
            threshold = order.company_id.btb_second_approval_threshold or 0.0
            order.second_approval_required = bool(threshold) and order.amount_total >= threshold

    def action_cancel(self):
        return self._action_cancel()



    def action_approve(self):

        for order in self:
            order.state="approved"
            order.approved_by=self.env.user.id
            order.approved_on=datetime.datetime.now()

    def action_second_approve(self):
        for order in self:
            if order.state != 'approved':
                raise UserError(_("Only requisitions already approved by a Store Manager can receive a 2nd level approval."))
            order.second_approved_by = self.env.user.id
            order.second_approved_on = datetime.datetime.now()

    def action_confirm(self):
        for order in self:
            if order.second_approval_required and not order.second_approved_by:
                raise UserError(_(
                    "This requisition totals %s, which is at or above the 2nd approval "
                    "threshold. A Finance Approver must approve it before it can be confirmed."
                ) % order.amount_total)

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
    line_no = fields.Integer("Sl.", compute="_compute_line_no")

    @api.depends("product_id")
    def get_stock_status(self):
        for rec in self:
            rec.current_stock=rec.qty_available_today
            rec.free_stock=rec.free_qty_today

    @api.depends('order_id.order_line', 'sequence')
    def _compute_line_no(self):
        for order in self.mapped('order_id'):
            counted_lines = order.order_line.filtered(lambda l: not l.display_type)
            for idx, line in enumerate(counted_lines, start=1):
                line.line_no = idx
            for line in (order.order_line - counted_lines):
                line.line_no = 0
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    detailed_type = fields.Selection(selection_add=[
        ('product', 'Storable Product')
    ], tracking=True, ondelete={'product': 'set consu'},default='product')

    btb_minimum_stock_qty = fields.Float(
        "Minimum Stock Qty", default=0.0,
        help="When the free quantity on hand drops below this level, Store Managers "
             "are notified. Set to 0 to disable alerts for this product.")

    def _cron_btb_check_low_stock(self):
        """Scheduled action: notify Store Managers about products below their
        minimum stock threshold. Purely additive — does not alter any existing
        field, model, or workflow."""
        low_stock_products = self.search([('btb_minimum_stock_qty', '>', 0)])
        low_stock_products = low_stock_products.filtered(
            lambda p: p.free_qty_today < p.btb_minimum_stock_qty
        )
        if not low_stock_products:
            return
        managers = self.env.ref('btb_stock.group_account_btb_stock_manager').users
        if not managers:
            return
        lines = "\n".join(
            "- %s: %.2f in stock (minimum %.2f)" % (p.name, p.free_qty_today, p.btb_minimum_stock_qty)
            for p in low_stock_products
        )
        note = _("Low stock alert:\n%s") % lines
        for user in managers:
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'note': note,
                'user_id': user.id,
                'res_id': low_stock_products[0].id,
                'res_model_id': self.env['ir.model']._get('product.template').id,
                'summary': _('Low stock: %d product(s) below minimum') % len(low_stock_products),
            })
