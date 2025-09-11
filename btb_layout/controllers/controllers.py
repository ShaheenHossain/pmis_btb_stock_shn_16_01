# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

# class PMIS(http.Controller):
#     @http.route('/contacts', type='http',auth="user",website=True)
#     def contact(self):
#         return request.render('pmis.contacts',{})
#
#     @http.route('/thankyou', type='http', auth="public", website=True)
#     def thankyou(self):
#         return request.render('pmis.thank_you', {})
#
#     @http.route('/search_contacts', type='http', auth="public", website=True)
#     def search_contacts(self):
#         return request.render('pmis.search_contacts', {})
#
#     @http.route('/searching_contacts', type='http', auth="public", website=True)
#     def searching_contacts(self,**post):
#         search_str=post.get('name')
#         contacts=request.env['res.partner'].search([("name".lower(),"like",search_str)])
#         print(search_str)
#         return request.render('pmis.contacts',{'conta':contacts})