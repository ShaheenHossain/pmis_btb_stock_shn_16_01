# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api,_
from datetime import date, datetime, time
from odoo.exceptions import ValidationError
from odoo.osv.expression import get_unaccent_wrapper
import re


class PmisAddlQualification(models.Model):
    _name = "pmis.addl.qualification"
    _description = "Additional Professional Qualification"
    description = fields.Char("Description")
    name=fields.Char("Qualification")
    person_id=fields.Many2one('res.partner')

class PmisJournal(models.Model):
    _name = "pmis.journal"
    _description = "Name of Journal"
    name=fields.Char("Journal")

class PmisPublications(models.Model):
    _name ="pmis.publications"
    name=fields.Char("Name")
    _description = "Publication Information"
    journal_id=fields.Many2one("pmis.journal")
    subject=fields.Char("Subject")
    person_id=fields.Many2one("res.partner")
    publication_type = fields.Selection([
        ('book','Books'),
        ('periodicals','Periodicals'),
        ('journal','Journals'),
        ('mono','Monograph'),
        ])
    description = fields.Char("Description")
    publish_date = fields.Date("Date")
    journal_no = fields.Integer("Journal_no")

class PmisTravel(models.Model):
    _name ="pmis.travel"
    _description = "Travel Informations"
    person_id=fields.Many2one("res.partner")
    country_id = fields.Many2one("res.country")
    purpose = fields.Char("Purpose")
    from_date = fields.Date("From")
    till_date = fields.Date("To")
    duration = fields.Float(string='Duration', compute="_compute_duration")
    remarks = fields.Char(string='Remarks')
    document = fields.Binary("Document")

    @api.onchange('till_date')
    @api.constrains('till_date', 'from_date')
    def date_constrains(self):
        for rec in self:
            if rec.till_date:
                if rec.till_date < rec.from_date:
                    raise ValidationError(_('Sorry, End date Must be greater Than from date...'))

    @api.onchange('from_date', 'till_date')
    def _compute_duration(self):
        for rec in self:
            if rec.till_date:
                d2 = datetime.strptime(str(rec.till_date), '%Y-%m-%d')
            else:
                d2 = datetime.strptime(str(date.today()), "%Y-%m-%d")
            if rec.from_date:
                d1 = datetime.strptime(str(rec.from_date), '%Y-%m-%d')
                d3 = d2 - d1
                rec.duration = str(d3.days)
            else:
                rec.duration = 0

# class PmisPublication(models.Model):
#     _name ="pmis.publication"
#
#     books = fields.Char("Books")
#     periodicals = fields.Char("Periodicals")
#     monograph = fields.Char("Monograph")
#     journals = fields.Char("Journals")
#     description = fields.Char("Description")
#     publish_date = fields.Date("Date")

class PmisPromotionNature(models.Model):
    _name ="pmis.promotion.nature"
    _description = "Nature of Promotions"
    name = fields.Char("Nature")
    description = fields.Char("Description")

class PmisOutsourcingCategory(models.Model):
    _name ="pmis.outsourcing.category"
    _description = "Outsourcing Categories"
    _rec_name = "category"
    category = fields.Char("Category")
    _description=fields.Char("Description")

class PmisServiceGrade(models.Model):
    _name ="pmis.service.grade"
    _description = "Service Grades"
    _rec_name ="grade"
    grade = fields.Char("Grade")
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,default=lambda self: self.env['res.currency'].search([('name','=','BDT')]).id)
    basic_salary=fields.Monetary("basic")
    description = fields.Char("Description")

class PmisLanguageProficiency(models.Model):
    _name ="pmis.language.proficiency"
    _description = "Language Proficiency"
    person_id=fields.Many2one('res.partner')
    name = fields.Many2one("res.lang",'language')
    can_read = fields.Boolean("Read")
    can_write = fields.Boolean("Write")
    can_speak = fields.Boolean("Speak")
    can_listen = fields.Boolean("Listen & Understand")
    exam = fields.Char("Special skill/Exam")
    exam_date = fields.Date("Exam Date")
    _sql_constraints = [
        ('person_language_uniq',
         'unique (person_id,name)',
         'Language for certain person is unique.')
    ]

class PmisAwards(models.Model):
    _name ="pmis.award"
    _description = "Awards description"
    person_id=fields.Many2one('res.partner')
    name = fields.Char("Title")
    institute_id=fields.Many2one("res.partner","Institution")
    ground = fields.Char("Ground")
    award_date = fields.Date("Date")
    govt_aproved = fields.Boolean("Govt Aproval")

class PmisCaseFile(models.Model):
    _name = "pmis.case.file"
    _description = "Filed Case records here"
    person_id=fields.Many2one('res.partner')
    case_type = fields.Char("Case Type")
    start_date = fields.Date("Start Date")
    settle_date = fields.Date("Settlement Date")
    settle_description=fields.Char("Description")
    status = fields.Char("Current Status")
    remarks = fields.Char("Addl Info")
    document = fields.Binary("Document")

class PmisDisciplineryActions(models.Model):
    _name = "pmis.discipline.action"
    _description = "Disciplinery action and punishment detailed records here"
    person_id=fields.Many2one('res.partner')
    name = fields.Char("Punishment")
    offence_type = fields.Char("Nature of Offence")
    punishment_date = fields.Date("Date of Punishment")
    status = fields.Char("Current Status")
    remarks = fields.Char("Remarks")
    document = fields.Binary("Document")



class PmisPostingRecord(models.Model):
    _name = "pmis.posting.record"
    _description = "manage Posting record Here"
    partner_id=fields.Many2one('res.partner',"Person")
    # GO No add
    organisation = fields.Many2one("res.partner", "Organisation")
    section=fields.Char("Section/Department")
    location = fields.Char( "Location")
    remarks = fields.Char( "Remarks")
    country_id = fields.Many2one("res.country",related="organisation.country_id")
    # go_no = fields.Char("Govt Order No")
    # go_date = fields.Date("Govt Order Date")
    joining_date = fields.Date("From")
    pay_scale = fields.Char( "Pay Scale")
    till_date = fields.Date("To")
    designation = fields.Many2one("pmis.designation", "Designation")
    rank = fields.Many2one("pmis.rank", "Rank")
    duration = fields.Float(string='Duration', compute="_compute_duration",store=True)
    # active_grade=fields.Many2one('pmis.service.grade')
    # actual_grade=fields.Many2one('pmis.service.grade')
    document=fields.Binary('Document')

    @api.onchange('till_date')
    @api.constrains('till_date', 'joining_date')
    def date_constrains(self):
        for rec in self:
            if rec.till_date:
                if rec.till_date < rec.joining_date:
                    raise ValidationError(_('Sorry, End Date Must be greater Than Joining Date...'))

    @api.onchange('joining_date', 'till_date')
    def _compute_duration(self):
        for rec in self:
            if rec.till_date:
                d2 = datetime.strptime(str(rec.till_date), '%Y-%m-%d')
            else:
                d2=datetime.strptime(str(date.today()), '%Y-%m-%d')
            if rec.joining_date :
                d1 = datetime.strptime(str(rec.joining_date), '%Y-%m-%d')
                d1 = datetime.strptime(str(rec.joining_date), '%Y-%m-%d')
                d3 = d2 - d1
                rec.duration = str(d3.days)
            else:
                rec.duration=0


class PmisPromotionParticulars(models.Model):
    _name = "pmis.promotion.particulars"
    _description = "manage Promotion record Here"
    partner_id=fields.Many2one('res.partner',"Person")
    rank_id = fields.Many2one("pmis.rank")
    # go_no = fields.Char("Govt Order No")
    # go_date = fields.Date("Govt Order Date")
    promotion_date = fields.Date("Promtion Date")
    # promotion_nature = fields.Many2one("pmis.promotion.nature", "Nature of Promotion")
    pay_scale = fields.Char("Pay Scale")
    grade_id=fields.Many2one('pmis.service.grade',"Grade")
    document=fields.Binary("Document")


class JoiningCircular(models.Model):
    _name = "pmis.joining.circular"
    _description = "Joining Circular"
    name=fields.Char("Circular No")
    circular_date=fields.Date("Circular Date")
    attachment=fields.Binary('Document')

class PMISContract(models.Model):
    _name = "pmis.contract"
    _description = "Outsourcing Contract"
    name=fields.Char("Contract No")
    contract_date=fields.Date("COntract Date")
    attachment=fields.Binary('Contract Document')
    _sql_constraints = [("contract_unique","unique(name)","This Contract Number is allredy Used")]