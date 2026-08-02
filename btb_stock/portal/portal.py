# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import binascii

from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.fields import Command
from odoo.http import request
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal

# class CustomerPortal(Controller):


class btbStockPortal(CustomerPortal):

    def _prepare_home_portal_values(self,counters):
        values=super(btbStockPortal,self)._prepare_home_portal_values(counters)

        user=request.env.user
        partner = user.partner_id


        requisition_count = http.request.env['sale.order'].search_count(["|",('create_uid','=',user.id),('partner_id','=',partner.id)])
        values['requisition_count']=requisition_count


        return values


    def _prepare_requisitions_domain(self, partner):
        return [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id])
        ]
    @http.route(['/my/requisitions', '/my/requisitions/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_requisitions(self, **kwargs):
        values = self._prepare_btb_stock_portal_rendering_values(requisition_page=True, **kwargs)
        request.session['my_quotations_history'] = values['requisitions'].ids[:100]
        return request.render("btb_stock.portal_my_requisitions", values)

    @http.route(['/my/requisitions/<int:order_id>'], type='http', auth="public", website=True)
    def portal_requisition_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='btb_stock.btb_print_adhijachan_patra', download=download)

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_quote_%s' % order_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': order_sudo.user_id.partner_id.lang or order_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', order_sudo.partner_id.name)
                del context
                _message_post_helper(
                    "sale.order",
                    order_sudo.id,
                    message=msg,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={order_sudo._name}' \
                      f'&id={order_sudo.id}' \
                      f'&action={order_sudo._get_portal_return_action().id}' \
                      f'&view_type=form'
        values = {
            'sale_order': order_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': order_sudo.company_id,  # Used to display correct company logo
        }

        # Payment values
        # if order_sudo._has_to_be_paid():
        #     values.update(self._get_payment_values(order_sudo))

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history_session_key = 'my_quotations_history'
        else:
            history_session_key = 'my_orders_history'

        values = self._get_page_view_values(
            order_sudo, access_token, values, history_session_key, False)

        return request.render('btb_stock.portal_template', values)

    def _get_requisition_searchbar_sortings(self):
        return {
            'date': {'label': _('Order Date'), 'order': 'date_order desc'},
            'name': {'label': _('Reference'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'state'},
        }
    def _prepare_btb_stock_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, requisition_page=False, **kwargs
    ):
        Requisitions = request.env['sale.order']

        if not sortby:
            sortby = 'date'

        partner = request.env.user.partner_id
        values = self._prepare_portal_layout_values()

        if requisition_page:
            url = "/my/requisitions"
            domain = self._prepare_requisitions_domain(partner)
        # else:
        #     url = "/my/orders"
        #     domain = self._prepare_requisitions_domain(partner)

        searchbar_sortings = self._get_requisition_searchbar_sortings()

        sort_order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        pager_values = portal_pager(
            url=url,
            total=Requisitions.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
        )
        orders = Requisitions.search(domain, order=sort_order, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'requisitions': orders.sudo(),
            'page_name': 'requisition' ,
            'pager': pager_values,
            'default_url': url,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })

        return values
