
# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, content_disposition
from datetime import datetime
import base64
import logging
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class pmisweb(http.Controller):

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
                'uid_number', 'company_name', 'salutation',
                'firstname', 'lastname', 'email', 'industry',
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
                'uid_number': kw.get('uid_number'),
                'company_name': kw.get('company_name'),
                'salutation': kw.get('salutation'),
                'firstname': kw.get('firstname'),
                'lastname': kw.get('lastname'),
                'email': kw.get('email'),
                'country_code': kw.get('country_code', '+41'),
                'phone_number': kw.get('phone_number'),
                'address': kw.get('address'),
                'street': kw.get('street'),
                'house_number': kw.get('house_number'),
                'postal_code': kw.get('postal_code'),
                'city': kw.get('city'),
                'country_id': int(kw.get('country_id')) if kw.get('country_id') else None,
                'industry': kw.get('industry'),
                'website_url': kw.get('website_url'),
                'monthly_sales_estimated': kw.get('monthly_sales_estimated'),
                'annual_revenue': kw.get('annual_revenue'),
                'average_transaction_value': kw.get('average_transaction_value'),
                'monthly_transaction_value': kw.get('monthly_transaction_value'),
                'pos_cash_register_system': kw.get('pos_cash_register_system'),
                'online_shop_system': kw.get('online_shop_system'),
                'payment_methods': kw.get('payment_methods'),
                'credit_card': 'credit_card' in kw,
                'debit_card': 'debit_card' in kw,
                'twint': 'twint' in kw,
                'apple_pay': 'apple_pay' in kw,
                'google_pay': 'google_pay' in kw,
                'samsung_pay': 'samsung_pay' in kw,
                'post_finance': 'post_finance' in kw,
                'purchase_on_account': 'purchase_on_account' in kw,
                'prepayment': 'prepayment' in kw,
                'others': 'others' in kw,
                'ticket_no': f"BHF-{now.strftime('%Y')}-",
                # 'other_problems': kw.get('other_problems'),
            }

            image_types = ['image/jpeg', 'image/png']
            pdf_types = ['application/pdf']

            if not kw.get('identity_card_front'):
                raise ValidationError(_("Identity card front is required"))
            if not kw.get('identity_card_back'):
                raise ValidationError(_("Identity card back is required"))
            if not kw.get('commercial_register_extract'):
                raise ValidationError(_("Commercial register extract is required"))

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
            bhf_val['ticket_no'] = ticket.ticket_no
            bhf_val['success'] = True

            return request.render("pmisweb.ticket_welcome", bhf_val)

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

            filename = getattr(record, f"{field}_filename") or f"{field}.{'pdf' if field == 'commercial_register_extract' else 'jpg'}"

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
