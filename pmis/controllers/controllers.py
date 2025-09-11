# -*- coding: utf-8 -*-
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request

class pmisController(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'contact_count' in counters:
            values['contact_count'] = 0
        return values

    @http.route('/my/pmis', type='http', auth='user', website=True)
    def my_pmis_form(self,**kw):
        partner = request.env.user.partner_id
        return request.render('pmis.portal_form',{"person":partner})

    @http.route('/pmiss', type='http', auth='user', website=True)
    def my_pmis(self, **kw):
        partner = request.env.user.partner_id
        return request.render('pmis.portal_my_pmis', {"persons": partner})