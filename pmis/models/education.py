# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,_, api
from datetime import date, datetime, time
from odoo.exceptions import  ValidationError

class PmisEducationRecord(models.Model):
    _name ="pmis.education.record"
    _description = "manage education record Here"
    partner_id = fields.Many2one("res.partner", "Partner")
    degree=fields.Many2one("pmis.degree")
    roll_no=fields.Char("Roll No")
    institute_id=fields.Many2one("res.partner","Institution/Board")
    passing_year = fields.Selection(
        selection='years_selection',
        string="Year",
        default="2021"  # as a default value it would be 2019)
    )


    result_system=fields.Many2one("pmis.result.system","Grading System")
    result_id=fields.Many2one("pmis.result.system.line","Result")
    subject_id=fields.Many2one("pmis.education.subject","Group/Subject")
    gpa=fields.Char("GPA/CGPA")
    distinction=fields.Char("Distinction")
    certificate_copy=fields.Binary("Certificate")
    def years_selection(self):
        year_list = []
        for y in range(1950, datetime.now().year + 1):
            year_list.append((str(y), str(y)))
        return year_list

class PmisEducationSubject(models.Model):
    _name ="pmis.education.subject"
    _description = "Major Subject description"
    name= fields.Char("Subject")
    degree_ids=fields.Many2many('pmis.degree','degree_subject_rel','subject_ids','degree_ids')
    description=fields.Char("details")
class PmisDegree(models.Model):
    _name ="pmis.degree"
    _description = "Degre of exam"
    name=fields.Char("Name",related='abv')
    degree=fields.Char("Degree")
    abv=fields.Char("Dgr")
    subject_ids=fields.Many2many('pmis.education.subject','degree_subject_rel','degree_ids','subject_ids')
class PmisEducationResultSystem(models.Model):
    _name ="pmis.result.system"
    _description = "result System of Exam ie; DIvision/Class/CGPA"
    name=fields.Char('Grading System')

class PmisEducation(models.Model):
    _name ="pmis.result.system.line"
    _description = "result Aystem Line ie: first Div/GPA 5"
    name = fields.Char("Grade")
    grading_system=fields.Many2one('pmis.result.system')


