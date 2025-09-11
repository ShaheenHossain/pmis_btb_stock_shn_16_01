# -*- coding: utf-8 -*-
from odoo import api, fields, models

class CRMBHF(models.Model):
    _name = "crm.bhf"
    _description = "CRM BHF"

    uid_number = fields.Char(string="UID Nummer")
    company_name = fields.Char(string="Firmenname")
    salutation = fields.Selection([
        ('Herr', 'Herr'),
        ('Frau', 'Frau'),
        ('Divers', 'Divers')
    ], string="Anrede")
    firstname = fields.Char(string="Vorname")
    lastname = fields.Char(string="Nachname")
    email = fields.Char(string='E-Mail')

    country_code = fields.Selection([
        ('+41', '+41 (CH)'),
        ('+49', '+49 (DE)'),
        ('+43', '+43 (AT)'),
        ('+33', '+33 (FR)'),
        ('+39', '+39 (IT)'),
        ('+423', '+423 (LI)'),
    ], string="Vorwahl", required=True,  default="+41")

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
    # industry = fields.Char(string="Branche")

    industry = fields.Selection([
        ('Kosmetik / Beauty', 'Kosmetik / Beauty'),
        ('Einzelhandel', 'Einzelhandel'),
        ('E-Commerce', 'E-Commerce'),
        ('POS', 'POS (stationärer Handel)'),
        ('Gastronomie', 'Gastronomie'),
        ('Dienstleistungen', 'Dienstleistungen'),
    ], string='Branche', required=True)


    website_url = fields.Char(string='Website', placeholder="https://www.beispielshop.ch")

    monthly_sales_estimated = fields.Char(
        string="Monatlicher Umsatz (geschätzt):",
        # currency_field='currency_id',
        placeholder= 'z.B. 30000',
        help="Estimated monthly sales volume")

    annual_revenue = fields.Char(
        string="Jahresumsatz (geschätzt):",
        # currency_field='currency_id',
        placeholder= 'z.B. 350000',
        help="Annual turnover estimated")


    average_transaction_value = fields.Char(
        string="Durchschnittlicher Transaktionswert:",
        placeholder= 'z.B. 120',
        help="The average value of confirmed sale orders"
    )


    monthly_transaction_value = fields.Char(
        string="Transaktionen pro Monat (geschätzt):",
        placeholder= 'z.B. 200',
        help="Monthly Transaction"
    )

    pos_cash_register_system = fields.Char(
        string="POS-/Kassensystem:",
        placeholder= 'z.B. SwissPOS, Lightspeed',
        help="SwissPOS, Lightspeed"
    )

    online_shop_system = fields.Char(
        string="Online - Shop - System:",
        placeholder= 'z.B. Shopify, Woocommerce',
        help="Online - Shop - System Shopify, Woocommerce"
    )

    online_shop_system = fields.Char(
        string="Online - Shop - System:",
        placeholder= 'z.B. Shopify, Woocommerce',
        help="Online - Shop - System Shopify, Woocommerce"
    )

    payment_methods = fields.Char(
        string="Zahlungsarten (Mehrfachauswahl möglich):",
        placeholder= 'z.B. Zahlungsarten ',
        help="Zahlungsarten"
    )


    credit_card = fields.Boolean(string='Kreditkarte')
    debit_card = fields.Boolean(string='Debitkarte')
    twint = fields.Boolean(string='Twint')
    apple_pay = fields.Boolean(string='Apple Pay')
    google_pay = fields.Boolean(string='Google Pay')
    samsung_pay = fields.Boolean(string='Samsung Pay')
    post_finance = fields.Boolean(string='PostFinance')
    purchase_on_account = fields.Boolean(string='Kauf auf Rechnung')
    prepayment = fields.Boolean(string='Vorauskasse')
    others = fields.Boolean(string='Sonstige')

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
