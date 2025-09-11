# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CRMBHF(models.Model):
    _name = "crm.bhf"
    _description = "CRM BHF"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']

    # website_user_id = fields.Many2one('res.users', string='Website User',
    #                                   default=lambda self: self.env.user if self.env.user.has_group(
    #                                       'base.group_public') else False)

    website_user_id = fields.Many2one('res.users', string='Portal User')
    partner_id = fields.Many2one('res.partner', string='Customer')

    def _compute_access_url(self):
        for record in self:
            record.access_url = '/my/bhf/%s' % (record.id)


    uid_number = fields.Char(string="PDS ID")
    pds_id_number = fields.Char(string="PDS ID")
    govt_id_number = fields.Char(string="GOVT ID")
    name = fields.Char(string="Name English")
    name_bn = fields.Char(string="Name Bangla")
    father_name = fields.Char(string="Father Name")
    father_name_bn = fields.Char(string="Father Name Bangla")
    mother_name = fields.Char("Mother's Name")
    mother_name_bn = fields.Char("মাতার নাম")


    dob = fields.Date("Date of Birth")


    email = fields.Char(string='E-Mail')

    phone_number = fields.Char(string="Telefon")
    address = fields.Text(string='Address')

    street = fields.Char(string="Straße")
    house_number = fields.Char(string="Nr.")
    postal_code = fields.Char(string="PLZ")
    city = fields.Char(string="Ort")
    country_id = fields.Many2one(
        'res.country',
        string='Land',
        default=lambda self: self.env.ref('base.ch'))

    country = fields.Selection([
        ('CH', 'Schweiz'),
        ('DE', 'Deutschland'),
        ('AT', 'Österreich')
    ], string="Land")

    pos_system = fields.Char(string="POS-System")
    shop_system = fields.Char(string="Shop-System")


    identity_card_front = fields.Binary(string="Personalausweis – Vorderseite", attachment=True)
    identity_card_front_filename = fields.Char("Front File Name")

    identity_card_back = fields.Binary(string="Personalausweis – Rückseite", attachment=True)
    identity_card_back_filename = fields.Char("Back File Name")

    commercial_register_extract = fields.Binary(string="Handelsregisterauszug (PDF)", attachment=True,)
    commercial_register_extract_filename = fields.Char("Register File Name")

    ticket_id = fields.Many2one('crm.bhf', string='Ticket ID')

    tenant = fields.Text(string='Tenant')
    # email = fields.Text(string='Email Address')
    building = fields.Text(string='Building')
    flat = fields.Text(string='Flat')

    problem_type = fields.Text(string='Problem Type')
    problem_category = fields.Text(string='Problem Category')

    property = fields.Text(string='Property')
    problem = fields.Text(string='Problem')
    work_type = fields.Text(string='Type of Work')
    problem_detail = fields.Text(string='Problem Detail')
    priority = fields.Text(string='Priority')
    # address = fields.Text(string='Address')
    ticket_no = fields.Text(string='Application No.')


    def _compute_access_url(self):
        for record in self:
            record.access_url = '/my/bhf/%s' % (record.id)
