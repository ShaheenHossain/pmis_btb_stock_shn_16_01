# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api,_
from datetime import date, datetime, time
from odoo.exceptions import ValidationError
from odoo.osv.expression import get_unaccent_wrapper
import re

class PmisGradeExam(models.Model):
    _name ="pmis.grade.exam"
    _description = "superior Grade Exams"
    name= fields.Char("Exam Name")
    person_id=fields.Many2one("res.partner")
    passing_year=fields.Selection(
        selection='years_selection',
        string="Year",
        default="2021"  # as a default value it would be 2019)
    )
    def years_selection(self):
        year_list = []
        for y in range(1950, datetime.now().year+1):
            year_list.append((str(y), str(y)))
        return year_list
    exam_date=fields.Date("Exam Date")
    result=fields.Char("Result")
    document = fields.Binary("Document")
    # notice_no=fields.Char("Notice No")
    # notice_date=fields.Date("Notice Date")
class PmisTraining(models.Model):
    _name ="pmis.training"
    _description = "name of Trainings"
    name= fields.Char("Course Title")

class PmisTraining_record(models.Model):
    _name ="pmis.training.line"
    _description = "Trainings of Officials"
    name= fields.Char("Course Title")
    training_id= fields.Many2one("pmis.training")
    partner_id=fields.Many2one("res.partner")
    institution_id=fields.Many2one("res.partner","Institution")
    country_id=fields.Many2one("res.country","Country")
    position=fields.Char("Position")
    category_id=fields.Many2one("pmis.training.category","Training Type")
    from_date= fields.Date("From")
    till_date= fields.Date("To")
    duration= fields.Float(string='Duration', compute="_compute_duration")
    document = fields.Binary("Document")

    @api.onchange('till_date')
    @api.constrains('till_date', 'from_date')
    def date_constrains(self):
        for rec in self:
            if rec.till_date:
                if rec.till_date < rec.from_date:
                    raise ValidationError(_('Sorry, End date Must be greater Than from date...'))

    @api.onchange('institution_id')
    def _get_country(self):
        self.ensure_one()
        self.country_id=self.institution_id.country_id

    @api.onchange('country_id')
    def _get_category(self):
        self.ensure_one()
        if self.country_id.id:
            if self.country_id != self.env.ref("base.bd"):
                self.category_id= self.env.ref("pmis.foreign_training")




    @api.onchange('from_date', 'till_date')
    def _compute_duration(self):
        for rec in self:
            if rec.till_date:
                d2 = datetime.strptime(str(rec.till_date), '%Y-%m-%d')
            else:
                d2 = datetime.strptime(str(date.today()), '%Y-%m-%d')
            if rec.from_date:
                d1 = datetime.strptime(str(rec.from_date), '%Y-%m-%d')
                d3 = d2 - d1
                rec.duration = str(d3.days)
            else:
                rec.duration = 0

class PmisTrainingCategory(models.Model):
    _name = 'pmis.training.category'
    _description = "Training type/Category"

    name=fields.Char("Training Type")
