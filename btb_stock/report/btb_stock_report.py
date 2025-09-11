# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.osv.expression import get_unaccent_wrapper
import datetime
from datetime import timedelta
import re

from odoo.addons.base.models.res_partner import Partner




class btbStockReport(models.TransientModel):
    _name="btb.stock.report"

    _description = "this model is used to prepare Report"

    product_ids=fields.Many2many("product.product")
    from_date=fields.Date("From")
    till_date=fields.Date("Till")
    report_for=fields.Selection(selection=[
        ('all',"All Products"),
        ('trans',"Transactions"),
    ],string="Print Report for",default='trans')


    def get_products(self):
        if self.product_ids:
            products=self.product_ids
        elif self.report_for=='trans':
            moves = self.env['stock.move.line'].search(
                [ ('date', '<=', self.till_date), ('date', '>=', self.from_date)],
                order='date asc')
            products=moves.mapped('product_id')
        else:
            products=self.env['product.product'].search([('id','>',0)])
        return products
    def stock_move_history(self,product_id):
        tilldate=self.till_date
        moves= self.env['stock.move.line'].search([('product_id','=',product_id.id),('date','<=',self.till_date),('date','>=',self.from_date)],order='date asc')
        return moves

    def get_opening_stock(self,product,date):
        stock=product.with_context({'to_date': date - timedelta(days=1)}).qty_available
        return stock
    def get_comment(self,move_line_id):
        if move_line_id.move_id.sale_line_id.order_id.purpose:
            return move_line_id.move_id.sale_line_id.order_id.purpose
        else:
            return move_line_id.reference