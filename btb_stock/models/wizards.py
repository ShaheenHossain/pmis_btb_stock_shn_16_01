# -*- coding: utf-8 -*-
from odoo import fields, models, api


class BtbCancelReasonWizard(models.TransientModel):
    _name = "btb.stock.cancel.reason.wizard"
    _description = "Capture a reason before cancelling a requisition"

    order_id = fields.Many2one("sale.order", "Requisition", required=True)
    reason = fields.Text("Cancellation Reason", required=True)

    def action_confirm_cancel(self):
        self.ensure_one()
        self.order_id.write({'cancel_reason': self.reason})
        self.order_id.action_cancel()
        return {'type': 'ir.actions.act_window_close'}
