# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api,_
from datetime import datetime,date,time
from odoo.osv.expression import get_unaccent_wrapper
from googletrans import Translator
from odoo.exceptions import ValidationError
import re
class PmisLeaveType(models.Model):
    _name = "pmis.job.category"
    _description = "Type of job i;e permanent/temporary"
    name = fields.Char("Job Type",translate=True)
    description = fields.Char("Desription",translate=True)
class PmisLeaveType(models.Model):
    _name = 'pmis.leave.type'
    _description = "Type of Leave"
    name = fields.Char("Leave Type",translate=True)
    description = fields.Char("Desription",translate=True)
class PmisLeaveSalaryType(models.Model):
    _name = 'pmis.leave.salary.type'
    _description = "Salary rules for Leave"
    name = fields.Char("Leave Salary Type",translate=True)
    salary_payable=fields.Float("Salary %")
    description = fields.Char("Desription",translate=True)
class PmisLeave(models.Model):
    _name = "pmis.leave"
    _description = "Leav Details "
    person_id=fields.Many2one('res.partner')
    leave_type=fields.Many2one('pmis.leave.type')
    salary_type = fields.Many2one("pmis.leave.salary.type","Leave Salary Type")
    from_date = fields.Date("From",required=True)
    till_date = fields.Date("To")
    duration=fields.Float("Duration",compute='calculate_duration')
    reason = fields.Char("Reason",translate=True)
    local_foreign = fields.Selection([('local',"Local"),('foreign',"Foreign")] )
    document = fields.Binary("Document")


    @api.onchange('till_date')
    @api.constrains('till_date', 'from_date')
    def date_constrains(self):
        for rec in self:
            if rec.till_date:
                if rec.till_date < rec.from_date:
                    raise ValidationError(_('Sorry, End Date Must be greater Than Start Date...'))
    @api.onchange('till_date','from_date')
    def calculate_duration(self):
        for rec in self:
            if  rec.till_date:
                d2 = datetime.strptime(str(rec.till_date), "%Y-%m-%d")
            else:
                d2= datetime.strptime(str(date.today()), "%Y-%m-%d")
            if  rec.from_date:
                d1 = datetime.strptime(str(rec.from_date), "%Y-%m-%d")
                rec.duration = abs((d2 - d1).days)+1
            else:
                rec.duration = 0

# class PmisLeave(models.Model):
#     _name ="pmis.leave"
#     _description = "manage Leave record Here"
#     person_id=fields.Many2one('res.partner')
#     name=fields.Char("Leave" ,translate=True)
#     name_bn=fields.Char("ছুটি")
#     salary=fields.Float("Salary")
#
#     @api.onchange('name')
#     def get_translated_name(self):
#         self.ensure_one()
#         source_language = 'en'
#         destination_language = 'bn_IN'
#         main_name = self.name
#         translator = Translator()
#         result = translator.translate(main_name, src=source_language, dest=destination_language)
#         if main_name:
#             self.name_bn = result.text
#
#
