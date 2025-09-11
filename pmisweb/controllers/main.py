# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, content_disposition
from datetime import datetime
import base64
import logging
from odoo.exceptions import ValidationError, AccessError, MissingError
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import pager as portal_pager

_logger = logging.getLogger(__name__)


class PmiswebPortal(portal.CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'bhf_count' in counters:
            domain = []
            if not request.env.user._is_public():
                domain = [
                    '|',
                    ('website_user_id', '=', request.env.user.id),
                    ('email', '=', request.env.user.email)
                ]
            values['bhf_count'] = request.env['crm.bhf'].search_count(domain)
        return values


    @http.route(['/my/bhf', '/my/bhf/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_bhf(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        CrmBHF = request.env['crm.bhf']

        domain = []
        if not request.env.user._is_public():
            domain = [
                '|',
                ('website_user_id', '=', request.env.user.id),
                ('email', '=', request.env.user.email)
            ]

        # Count for pager
        bhf_count = CrmBHF.search_count(domain)

        # Make pager
        pager = portal_pager(
            url="/my/bhf",
            url_args={'date_begin': date_begin, 'date_end': date_end},
            total=bhf_count,
            page=page,
            step=self._items_per_page
        )

        # Content
        bhfs = CrmBHF.search(domain, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_bhf_history'] = bhfs.ids[:100]

        values.update({
            'bhfs': bhfs,
            'page_name': 'bhf',
            'pager': pager,
            'default_url': '/my/bhf',
        })
        return request.render("pmisweb.portal_my_bhf", values)

    @http.route('/my/bhf/<int:bhf_id>', type='http', auth="user", website=True)
    def portal_my_bhf_form(self, bhf_id, access_token=None, **kw):
        try:
            bhf_sudo = self._document_check_access('crm.bhf', bhf_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = {
            'bhf': bhf_sudo,
            'page_name': 'bhf',
        }
        return request.render("pmisweb.portal_my_bhf_form", values)


class PmiswebController(http.Controller):

    @http.route('/web/bhf', type='http', website=True, auth='public')
    def hospital_signup(self, **kw):
        """Render the initial form"""
        countries = request.env['res.country'].sudo().search([])
        return request.render("pmisweb.bhf", {
            'countries': countries,
            'default_country': request.env.ref('base.ch').id
        })

    @http.route('/create/bhf/', type='http', website=True, auth='public', csrf=True)
    def create_partner(self, **kw):
        """Handle form submission with file uploads"""
        now = datetime.now()

        def validate_required_fields(data):
            """Validate required form fields"""
            required_fields = [
                'pds_id_number', 'govt_id_number', 'name', 'name_bn', 'email',
            ]
            missing = [field for field in required_fields if not data.get(field)]
            if missing:
                raise ValidationError(_("Missing required fields: %s") % ", ".join(missing))

        def process_upload(file_field, allowed_types=None, max_size=10 * 1024 * 1024):
            """Process file upload with validation"""
            try:
                if file_field and hasattr(file_field, 'read'):
                    file_content = file_field.read()

                    if not file_content:
                        raise ValidationError(_("Uploaded file is empty"))

                    if len(file_content) > max_size:
                        raise ValidationError(_("File size exceeds maximum allowed (10MB)"))

                    if allowed_types and file_field.content_type not in allowed_types:
                        raise ValidationError(_("Invalid file type. Allowed: %s") % ", ".join(allowed_types))

                    return {
                        'content': base64.b64encode(file_content),
                        'filename': file_field.filename,
                        'content_type': file_field.content_type
                    }
                return None
            except Exception as e:
                _logger.error("Error processing file upload: %s", str(e))
                raise ValidationError(_("Error processing file upload: %s") % str(e))

        try:
            _logger.info("Form data received: %s", {k: v for k, v in kw.items() if not hasattr(v, 'read')})
            _logger.info("Files received: %s", {k: v.filename for k, v in kw.items() if hasattr(v, 'read')})

            validate_required_fields(kw)

            bhf_val = {
                'pds_id_number': kw.get('pds_id_number'),
                'govt_id_number': kw.get('govt_id_number'),
                'name': kw.get('name'),
                'name_bn': kw.get('name_bn'),
                'father_name': kw.get('father_name'),
                'father_name_bn': kw.get('father_name_bn'),
                'mother_name': kw.get('mother_name'),
                'mother_name_bn': kw.get('mother_name_bn'),
                'email': kw.get('email'),
                'phone_number': kw.get('phone_number'),
                'address': kw.get('address'),
                'street': kw.get('street'),
                'house_number': kw.get('house_number'),
                'postal_code': kw.get('postal_code'),
                'city': kw.get('city'),
                'country_id': int(kw.get('country_id')) if kw.get('country_id') else None,
                'ticket_no': f"BHF-{now.strftime('%Y')}-",
            }

            # Link to portal user if logged in
            if not request.env.user._is_public():
                bhf_val.update({
                    'website_user_id': request.env.user.id,
                    'partner_id': request.env.user.partner_id.id
                })

            # Process file uploads
            image_types = ['image/jpeg', 'image/png']
            pdf_types = ['application/pdf']

            identity_front = process_upload(kw.get('identity_card_front'), allowed_types=image_types)
            if identity_front:
                bhf_val.update({
                    'identity_card_front': identity_front['content'],
                    'identity_card_front_filename': identity_front['filename']
                })

            identity_back = process_upload(kw.get('identity_card_back'), allowed_types=image_types)
            if identity_back:
                bhf_val.update({
                    'identity_card_back': identity_back['content'],
                    'identity_card_back_filename': identity_back['filename']
                })

            register_extract = process_upload(kw.get('commercial_register_extract'), allowed_types=pdf_types)
            if register_extract:
                bhf_val.update({
                    'commercial_register_extract': register_extract['content'],
                    'commercial_register_extract_filename': register_extract['filename']
                })

            ticket = request.env['crm.bhf'].sudo().create(bhf_val)
            ticket.write({'ticket_no': f"BHF-{now.strftime('%Y')}-{ticket.id}"})

            return request.render("pmisweb.ticket_welcome", {
                'ticket_no': ticket.ticket_no,
                'success': True,
                **bhf_val
            })

        except ValidationError as ve:
            _logger.warning("Validation error: %s", str(ve))
            countries = request.env['res.country'].sudo().search([])
            return request.render("pmisweb.bhf", {
                'error': str(ve),
                'countries': countries,
                'default_country': request.env.ref('base.ch').id,
                'form_data': {k: v for k, v in kw.items() if not hasattr(v, 'read')}
            })
        except Exception as e:
            _logger.exception("Error creating CRM BHF record")
            countries = request.env['res.country'].sudo().search([])
            return request.render("pmisweb.bhf", {
                'error': _("An unexpected error occurred. Please try again later."),
                'countries': countries,
                'default_country': request.env.ref('base.ch').id,
                'form_data': {k: v for k, v in kw.items() if not hasattr(v, 'read')}
            })

    @http.route('/download/bhf/<int:rec_id>/<string:field>', type='http', auth="public")
    def download_attachment(self, rec_id, field, **kw):
        try:
            record = request.env['crm.bhf'].sudo().browse(rec_id)
            if not record.exists():
                return request.not_found()

            if field not in ['identity_card_front', 'identity_card_back', 'commercial_register_extract']:
                return request.not_found()

            file_content = base64.b64decode(getattr(record, field) or '')
            if not file_content:
                return request.not_found()

            filename = getattr(record,
                               f"{field}_filename") or f"{field}.{'pdf' if field == 'commercial_register_extract' else 'jpg'}"

            return request.make_response(
                file_content,
                headers=[
                    ('Content-Type', 'application/octet-stream'),
                    ('Content-Disposition', content_disposition(filename))
                ]
            )
        except Exception as e:
            _logger.error("Error downloading attachment: %s", str(e))
            return request.not_found()