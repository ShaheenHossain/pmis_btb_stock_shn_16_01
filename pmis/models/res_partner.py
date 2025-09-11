# -*- coding: utf-8 -*-
# Part of eagle. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
import re
import num2words
from googletrans import Translator
import num2words

class pmisCompany(models.Model):
    _inherit = "res.company"
    logo2 = fields.Binary("logo2")

class PmisRank(models.Model):
    _name = "pmis.rank"
    _description = "ranks information"
    grade = fields.Integer("grade")
    name = fields.Char("Rank")
    abv = fields.Char("Rnk")
    _sql_constraints = [
        ('name_unique', 'unique (name)',
         "Rank name must be unique, this rank name is already assigned."),
        ('abv_unique', 'unique (abv)',
         "Rank Abv must be unique, this rank abv is already assigned."),
    ]


class PmisCadre(models.Model):
    _name = "pmis.cadre"
    _description = "Bcs Cadre Information"
    name = fields.Char("Cadre")
    abv = fields.Char("cdr")




class PmisBcs(models.Model):
    _name = "pmis.bcs"
    _description = "BCS Information"
    name = fields.Char("Batch", )
    sl = fields.Integer("BCS")
    join_date = fields.Date("Cadre Date")
    _sql_constraints = [
        ('bcs_unique', 'unique (sl)',
         "BCS Sl must be unique, this BCS Serial is already assigned."),
    ]

    def appendInt(self, num):
        if num > 9:
            secondToLastDigit = str(num)[-2]
            if secondToLastDigit == '1':
                return 'th'
        lastDigit = num % 10
        if (lastDigit == 1):
            return 'st'
        elif (lastDigit == 2):
            return 'nd'
        elif (lastDigit == 3):
            return 'rd'
        else:
            return 'th'

    @api.onchange("sl")
    def get_ordinal(self):
        for rec in self:
            if rec.sl > 0:
                rec.name = str(rec.sl) + self.appendInt(rec.sl)


class PmisBCSCadre(models.Model):
    _name = "pmis.bcs.cadre"
    _description = "Various Cadre of Bcs"
    name = fields.Char("Cadre", )
    description = fields.Char("Description")
    _sql_constraints = [
        ('cadre_unique', 'unique (name)',
         "Bcs Cadre must be unique, this Name is already assigned."),
    ]



class PmisContactType(models.Model):
    _name = "pmis.contact.type"
    _description = "Type of Contact ie; Person,Education institute,Job Posting"
    name=fields.Char('PmisContactType Type')

class PmisMarital(models.Model):
    _name = "pmis.marital"
    _rec_name = 'status'
    _description = "Marital Information"
    status = fields.Char("Marital Status")
    description = fields.Char("Description")


class PmisReligion(models.Model):
    _name = "pmis.religion"
    _description = "Religion Information"
    name = fields.Char("Religion")
    abv = fields.Char("Rlgn")


class PmisWing(models.Model):
    _name = "pmis.wing"
    _description = "Section/Wing"
    name = fields.Char("Wing")
    description = fields.Char("description")

class PmisGender(models.Model):
    _name = "pmis.gender"
    _description = "Gender Information"
    name = fields.Char("Gender")
    spouse_gender=fields.Many2one("pmis.gender")
    abv = fields.Char("Gen")
    _sql_constraints = [
        ('name_unique', 'unique (name)',
         "Gender must be unique, this Gender name is already assigned."),
        ('abv_unique', 'unique (abv)',
         "Gender Abv must be unique, this Abv is already assigned."),
    ]

class PmisQuota(models.Model):
    _name = "pmis.quota"
    _description = "Define quota ex Fredom-Fighter/Tribal"
    name = fields.Char("Quota")
    description = fields.Char("Description")
    _sql_constraints = [
        ('name_unique', 'unique (name)',
         "Quota must be unique, this Quota name is already assigned."),
    ]
class PmisSports(models.Model):
    _name = "pmis.sports"
    _description = "Sports Performance"
    person_id=fields.Many2one('res.partner',"person")
    name = fields.Char("Sports")
    description = fields.Char("Description")

class PmisResearch(models.Model):
    _name = "pmis.research"
    _description = "Research Description"
    person_id=fields.Many2one('res.partner',"person")
    name = fields.Char("Research")
    description = fields.Char("Description")

# class PmisJoiningInformation(models.Model):
#     _name = "pmis.joining.info"
#     _description = "Joining info for official"
#     person_id = fields.Many2one("res.partner")
#     join_circuler_no = fields.Char("Advertisement No")
#     adv_date = fields.Date("Advertisement Date")
#     apt_no = fields.Char("Appointment No")
#     apt_date = fields.Date("Appointment Date")
#     employer = fields.Many2one("res.partner")
#     join_designation=fields.Many2one("pmis.designation")
#     join_post=fields.Many2one("pmis.rank")
#     join_wing=fields.Many2one("pmis.wing")
#     join_date = fields.Date("Joining Date")
#     join_quota=fields.Many2one("pmis.quota")
#     merit_order = fields.Integer("Merit Order")





class PmisDesignation(models.Model):
    _name = "pmis.designation"
    _description = "Designation Description"
    grade = fields.Integer("grade")
    name = fields.Char("Designation",translate=True)
    abv = fields.Char("Desgn",translate=True)
    _sql_constraints = [
        ('name_unique', 'unique (name)',
         "Designation name must be unique, this Designation name is already assigned."),
        ('abv_unique', 'unique (abv)',
         "Designation Abv must be unique, this Designation abv is already assigned."),
    ]

# class PmisPoliceVerification(models.Model):
#     _name = "pmis.pvr"
#     _description = "Police Verification Report "
#     _rec_name = 'description'
#     description = fields.Char("Desription",translate=True)
#     person_id=fields.Many2one("res.partner")
#     pvr_no = fields.Char("Police Verification")
#     pvr_date = fields.Date("Date")
#     pvr_image = fields.Binary("PVR Copy",help="Upload PVR copy")
class PmisPayFixationRecords(models.Model):
    _name = "pmis.pay.fix"
    _description = "Pay Fixation Records Here "
    description = fields.Char("Desription",translate=True)
    person_id=fields.Many2one("res.partner")
    pay_fix_date=fields.Date("Date")
    pay_scale=fields.Char("Pay Scale")
    basic=fields.Float("Basic")
    total=fields.Float("Total")
    sal_cut=fields.Float("Salary Cut")

class PmisBank(models.Model):
    _inherits = {'res.partner':'partner_id'}
    _name = 'pmis.bank'
    _description = "bank accounts info"
    description =fields.Char( "Description")

class PmisBankAccounts(models.Model):
    _name = 'pmis.bank.accounts'
    _description = "bank accounts info"
    description =fields.Char( "Description")
    _rec_name = 'ac_no'
    person_id=fields.Many2one('res.partner')
    ac_no=fields.Char("Account No")
    bank_id=fields.Many2one("pmis.bank")
    branch=fields.Char("Branch")
    routing_no=fields.Char("Routing")
class PMisChildren(models.Model):
    _name = 'pmis.children'
    _description = "Children Information Here"
    description =fields.Char( "Description")
    name =fields.Char("name")
    dob=fields.Date("Date of Birth")
    sex=fields.Many2one('pmis.gender')
    child_of_ids=fields.Many2many(comodel_name='res.partner', relation='person_child_rel', column1='child_id', column2='person_id',
                     string='Children')

class resUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields):
        res = super(resUsers, self).default_get(fields)

        if 'default_partner_id' in self._context:
            res['partner_id'] = self._context.get('default_partner_id')

        return res

class ResPartner(models.Model):
    _inherit = 'res.partner'

    sl = fields.Integer(string="SL")   # ✅ Fixed label
    state = fields.Selection(
        [
            ('draft', "Draft"),
            ('submitted', "Submitted"),
            ('approved', 'Approved')
        ],
        required=True,
        default='draft'
    )

    # this fields moved to btb layout
    # pds_id=fields.Char("PDS ID")
    name_bn = fields.Char("Name (BN)")
    father_name = fields.Char("Father's Name")
    father_name_bn = fields.Char("পিতার নাম")
    mother_name = fields.Char("Mother's Name")
    mother_name_bn = fields.Char("মাতার নাম")
    dob = fields.Date("Date of Birth")
    religion = fields.Many2one("pmis.religion")
    gender = fields.Many2one("pmis.gender")
    # @api.onchange('gender')
    # def gender_onchange(self):
    #     if self.gender:
    #         self.spouse_gender=self.gender.spouse_gender

    spouse_gender=fields.Many2one("pmis.gender",related='gender.spouse_gender')
    nationality_id = fields.Many2one("res.country", "Nationality" ,default=lambda self : self.env.ref("base.bd"))
    nid_no = fields.Char("NID No")
    nid_copy = fields.Binary("NID Copy")
    driving_lcn_no = fields.Char("Driving Licence No.")
    driving_lcn_exp_dt = fields.Date("& Expiration Date")
    driving_copy = fields.Binary("Driving Licence Copy")

    marital_status = fields.Selection([('single', 'Single'),('married', 'Married'),  ('divorced', 'Divorced')], string='Marital Status',
                                      track_visibility='onchange')
    passport_no = fields.Char("Passport No.")
    pssprt_exp_date = fields.Date("Expiration Date")
    passport_copy = fields.Binary("Passport Copy")
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                    ('ab-', 'AB-'), ('ab+', 'AB+')], string='Blood Group', track_visibility='onchange')
    occupation=fields.Char("Occupation")

    spouse = fields.Many2one("res.partner")
    children_ids = fields.Many2many(comodel_name='pmis.children',relation= 'person_child_rel',column1= 'person_id',column2= 'child_id', string='Children')

    # todo current posing data can be auto generated from posting records
    # cur_rank = fields.Many2one("pmis.rank", "Rank", compute="get_current_data")
    # cur_designation = fields.Many2one("pmis.designation", "Designation", compute="get_current_data")
    # cur_organisation = fields.Many2one("res.partner", "Organisation", compute="get_current_data")
    # cur_go_date = fields.Date("Govt Order ate", compute="get_current_data")
    # cur_joining_date = fields.Date("joining date", compute="get_current_data")
    # cur_location = fields.Char("Location", compute="get_current_data")

    posting_records = fields.One2many("pmis.posting.record", "partner_id")
    cur_posting_records = fields.Many2one("pmis.posting.record", "Current Posting",compute="get_current_data")

    education_records = fields.One2many("pmis.education.record", "partner_id")
    promotion_records = fields.One2many("pmis.promotion.particulars", 'partner_id')
    pay_fix_ids = fields.One2many("pmis.pay.fix", 'person_id', "Pay Fixation Records")
    dob_in_words = fields.Char(compute='_compute_dob_in_words')
    leave_records=fields.One2many("pmis.leave","person_id")
    training_records = fields.One2many("pmis.training.line", "partner_id")
    language_proficiency = fields.One2many("pmis.language.proficiency", "person_id")
    senior_grade_exam=fields.One2many("pmis.grade.exam","person_id","Senior Grade Exam")
    award_ids=fields.One2many("pmis.award",'person_id')
    travel_ids = fields.One2many("pmis.travel", "person_id")
    publication_ids=fields.One2many('pmis.publications','person_id',"Publications")
    govt_id = fields.Char("GOVT ID")

    contact_type=fields.Many2one("pmis.contact.type")
    # contact_type=fields.Selection(
    #     [
    #         ('person','Person'),
    #         ('office','Office'),
    #     ]
    # )
    sports_ids=fields.One2many("pmis.sports","person_id","sports")
    research_ids=fields.One2many("pmis.research","person_id","Research")
    disability=fields.Char('Disability')
    ethnic_minority=fields.Boolean("Ethnic Minority?")
    prov_no=fields.Char("PF No")
    pv_report=fields.Binary("Police Verification Report")
    medical_report=fields.Binary("Medical Report")
    prl_date = fields.Date("PRL/LPR Date")
    cadre_date = fields.Date(related="bcs_id.join_date")
    bcs_id = fields.Many2one("pmis.bcs", "Batch")
    bcs_cadre = fields.Many2one("pmis.bcs.cadre", "Cadre")
    go_date = fields.Date("Govt Order Date")
    bank_account_ids=fields.One2many("pmis.bank.accounts","person_id")
    
    # joining_info=fields.Many2one("pmis.joining.info")
    joining_circular_no = fields.Many2one("pmis.joining.circular","Circular No")
    circular_date = fields.Date("Circular Date",related="joining_circular_no.circular_date")
    contract_no = fields.Many2one("pmis.contract","Contract No")
    contract_date = fields.Date("Contract Date",related="contract_no.contract_date")

    # Joining Informations
    join_designation = fields.Many2one("pmis.designation","Joining Designation")
    joining_grade = fields.Many2one("pmis.service.grade")
    outsourcing_category=fields.Many2one('pmis.outsourcing.category',"Category")
    join_post = fields.Many2one("pmis.rank")
    join_wing = fields.Many2one("pmis.wing")
    join_date = fields.Date("Joining Date")
    joining_letter = fields.Binary("Joining Letter")
    merit_order = fields.Integer("Merit Order")
    job_quota=fields.Boolean("Quota")
    join_quota = fields.Many2one("pmis.quota","Joining Quota")
    quota_doc = fields.Binary("Quota Document")

    # appointment Informations
    job_category=fields.Many2one("pmis.job.category")
    apt_no = fields.Char("Appointment No")
    apt_date = fields.Date("Appointment Date")
    apt_copy = fields.Binary("Appointment Letter")
    employer = fields.Many2one("res.partner")

    # Confirmation
    conf_no = fields.Char("Confirmation Order No")
    conf_date = fields.Date("Confirmation date")
    conf_copy = fields.Binary("Confirmation Letter")
    # present Address
    post_office=fields.Char("Post Office")
    # Permanent Address
    per_house=fields.Char("House")
    per_street=fields.Char("Street")
    per_post=fields.Char("Post Office")
    per_thana=fields.Char("Thana")
    per_district=fields.Many2one("res.country.state","District")
    country_id=fields.Many2one("res.country","Country",default=lambda self : self.env.ref("base.bd"))
    per_country=fields.Many2one("res.country","Country",default=lambda self : self.env.ref("base.bd"))
    per_phone=fields.Char("Phone")
    addl_qualification=fields.One2many('pmis.addl.qualification','person_id',"Additional Professional Qualification")

    #field that is not used, to be reviewed


    home_district = fields.Many2one("res.country.state", "Home District")

    # joining_date = fields.Date("Joining Date")

    discipline =fields.One2many('pmis.discipline.action','person_id', "Disciplinnery Action")
    case_file_ids =fields.One2many('pmis.case.file','person_id', "Case Filed")

    tin_no=fields.Char("TIN No")
    tin_copy=fields.Binary("TIN Certificate")

    freedom_fighter = fields.Selection([('yes', "Yes"), ('no', 'No')])



    # permanent address

    organization = fields.Char("Organization")
    location = fields.Char("Location")
    current_designation = fields.Char("Current Designation")



    @api.onchange('dob')
    def _compute_dob_in_words(self):
        for partner in self:
            if partner.dob:
                dob = partner.dob

                month = dob.strftime('%B')  # date_of_birth.month
                day = num2words.num2words(dob.day, to='ordinal')
                year = num2words.num2words(dob.year)
                partner.dob_in_words = "{} {} in year {}".format(day, month, year).upper()

            else:
                partner.dob_in_words = False

    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['submitted', 'approved'])
        return orders.write({
            'state': 'draft',
            'signature': False,
            'signed_by': False,
            'signed_on': False,
        })
    def action_approved(self):
        orders = self.filtered(lambda s: s.state in ['submitted', 'approved'])
        return orders.write({
            'state': 'submitted',
            'signature': False,
            'signed_by': False,
            'signed_on': False,
        })


    def local_training_mandatory(self):
        self.ensure_one()
        trainings=self.env['pmis.training.line'].search([('partner_id','=',self.id),('category_id','=',1)])
        return trainings
    def local_trainings(self):
        self.ensure_one()
        trainings=self.env['pmis.training.line'].search([('partner_id','=',self.id),('category_id','=',2)])
        return trainings
    def foreign_trainings(self):
        self.ensure_one()
        trainings=self.env['pmis.training.line'].search([('partner_id','=',self.id),('category_id','=',3)])
        return trainings
    def posting_abroad(self):
        postings=self.env['pmis.posting.record'].search([('partner_id','=',self.id),('country_id','!=',self.country_id.id)])
        return postings

    def local_posting(self):
        postings=self.env['pmis.posting.record'].search([('partner_id','=',self.id),('country_id','=',self.country_id.id)])
        return postings

    @api.onchange("posting_records")
    def get_current_data(self):
        for rec in self:
            last_posting = self.env["pmis.posting.record"].search([('partner_id', '=', rec.id)], order='id desc',limit=1)
            if last_posting:
                rec.cur_posting_records=last_posting.id
                return
                # rec.cur_rank = last_posting.rank
                # rec.cur_designation = last_posting.designation
                # rec.cur_organisation = last_posting.organisation
                # rec.cur_go_date = last_posting.go_date
                # rec.cur_joining_date = last_posting.joining_date
                # rec.cur_location = last_posting.location

    @api.onchange('name')
    def get_translated_name(self):
        self.ensure_one()
        self.get_translated_value('name','name_bn')

    @api.onchange('father_name')
    def get_translated_father_name(self):
        self.ensure_one()
        self.get_translated_value('father_name','father_name_bn')

    @api.onchange('mother_name')
    def get_translated_mother_name(self):
        self.ensure_one()
        self.get_translated_value('mother_name','mother_name_bn')

    def get_translated_value(self,inputField,translatedField):
        self.ensure_one()
        source_language = 'en'
        destination_language = 'bn_IN'
        value2Translate =  getattr(self,inputField)
        translator = Translator()

        if getattr(self,inputField):
            result = translator.translate(value2Translate.upper(), src=source_language, dest=destination_language)
            if not getattr(self,translatedField):
                setattr(self,translatedField,result.text)
            else:
                return {

                    'warning': {

                        'title': 'Warning!',

                        'message': 'Please Check Bengali spelling!'}

                }
            # self.name_bn = result.text
    def action_create_user(self):
        self.ensure_one()
        existingUser=self.env['res.users'].search([('partner_id','=',self.id)])
        if existingUser.id:
            raise ValidationError("This contact already has an user:.")
            # (_('The modes in view_mode must not be duplicated: %s', existingUser.name))
        return {
            'name': 'Create User',
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'view_mode': 'form',
            'view_id': self.env.ref('base.view_users_form').id,
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
                'default_name': self.name,
                'default_phone': self.phone,
                'default_mobile': self.mobile,
                'default_login': self.email,
            }
        }