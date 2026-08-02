import io
from datetime import timedelta

from odoo import http
from odoo.http import request


# class btbStock(http.Controller):


class BtbStockReportController(http.Controller):

    @http.route('/btb_stock/stock_report/xlsx/<int:wizard_id>', type='http', auth='user')
    def export_stock_report_xlsx(self, wizard_id, **kwargs):
        import xlsxwriter

        wizard = request.env['btb.stock.report'].browse(wizard_id)
        wizard.check_access_rights('read')
        wizard.check_access_rule('read')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        header_fmt = workbook.add_format({
            'bold': True, 'bg_color': '#0B3D59', 'font_color': 'white', 'border': 1,
        })
        title_fmt = workbook.add_format({'bold': True, 'font_size': 14, 'font_color': '#0B3D59'})
        num_fmt = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        cell_fmt = workbook.add_format({'border': 1})

        sheet = workbook.add_worksheet('Stock Ledger')
        sheet.write(0, 0, 'Stock Movement Report', title_fmt)
        sheet.write(1, 0, 'Period: %s to %s' % (wizard.from_date, wizard.till_date))

        row = 3
        columns = ['Date', 'Received', 'Previous', 'Distributed', 'Remaining', 'Comment', 'Number', 'Req. By']
        widths = [14, 12, 12, 12, 12, 30, 16, 24]
        for col, width in enumerate(widths):
            sheet.set_column(col, col, width)

        products = wizard.get_products()
        for product in products:
            row += 1
            sheet.merge_range(row, 0, row, len(columns) - 1, product.name, header_fmt)
            row += 1
            for col, label in enumerate(columns):
                sheet.write(row, col, label, header_fmt)
            row += 1

            moves = wizard.stock_move_history(product)
            remind = 0
            opening_stock = 0
            if moves:
                opening_stock = wizard.get_opening_stock(moves[0].product_id, moves[0].date - timedelta(days=1))
                for i, move in enumerate(moves):
                    previous = opening_stock if i == 0 else remind
                    is_stock_out = move.move_id.location_id.name == 'Stock'
                    received = 0 if is_stock_out else move.qty_done
                    distributed = move.qty_done if is_stock_out else 0
                    remind = (previous - move.qty_done) if is_stock_out else (previous + move.qty_done)
                    requester = move.env['sale.order'].search([('name', '=', move.origin)], limit=1).partner_id.name or ''
                    sheet.write(row, 0, str(move.date.strftime('%d/%m/%Y')), cell_fmt)
                    sheet.write_number(row, 1, received, num_fmt)
                    sheet.write_number(row, 2, previous, num_fmt)
                    sheet.write_number(row, 3, distributed, num_fmt)
                    sheet.write_number(row, 4, remind, num_fmt)
                    sheet.write(row, 5, wizard.get_comment(move) or '', cell_fmt)
                    sheet.write(row, 6, move.origin or '', cell_fmt)
                    sheet.write(row, 7, requester, cell_fmt)
                    row += 1
            else:
                opening_stock = wizard.get_opening_stock(product, wizard.till_date)
                sheet.write(row, 0, str(wizard.till_date), cell_fmt)
                sheet.write_number(row, 2, opening_stock, num_fmt)
                sheet.write_number(row, 4, opening_stock, num_fmt)
                sheet.write(row, 5, 'No transaction in this period', cell_fmt)
                row += 1
            row += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="Stock_Ledger_Report.xlsx"'),
            ],
        )


class BtbStockMobileApiController(http.Controller):
    """Lightweight, read-only status endpoint intended for the companion mobile app.
    Additive only — does not expose write access, and only returns requisitions
    the logged-in user is already allowed to see (record rules still apply)."""

    @http.route('/api/btb/requisitions', type='json', auth='user')
    def get_my_requisitions(self, limit=50, **kwargs):
        orders = request.env['sale.order'].search(
            [('user_id', '=', request.env.user.id)], order='date_order desc', limit=limit
        )
        return {
            'requisitions': [{
                'id': o.id,
                'name': o.name,
                'state': o.state,
                'purpose': o.purpose,
                'amount_total': o.amount_total,
                'date_order': o.date_order and o.date_order.strftime('%Y-%m-%d %H:%M:%S') or False,
                'second_approval_required': o.second_approval_required,
                'second_approved': bool(o.second_approved_by),
            } for o in orders]
        }
