from odoo import models

class CustomerInvoiceExcel(models.AbstractModel):
    _name = 'report.customer_invoice_report.report_customer_invoice_xls'
    _inherit = 'report.report_xlsx.abstract'

    # Generating xlsx report using 'report_xlsx' module
    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet('Invoice Supporting')
        format1 = workbook.add_format({'bold': True, 'bg_color': 'decoration-success'})
        date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd/mm/yyyy'})

        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 8, 20)

        row = 0
        col = 0
        sheet.write(row, col, 'S.NO', format1)
        sheet.write(row, col + 1, 'INV NUMBER', format1)
        sheet.write(row, col + 2, 'INV DATE', format1)
        sheet.write(row, col + 3, 'SO NUMBER', format1)
        sheet.write(row, col + 4, 'CURRENCY', format1)
        sheet.write(row, col + 5, 'UNTAXED AMOUNT', format1)
        sheet.write(row, col + 6, 'TAX AMOUNT', format1)
        sheet.write(row, col + 7, 'TOTAL', format1)
        sheet.write(row, col + 8, 'PAYMENT STATUS', format1)

        domain_list = [('move_type', '=', 'out_invoice')]

        if lines.specific_date:
            domain_list.append(('invoice_date', '=', lines.invoice_date))
        elif lines.year_and_month:
            year_month_recs = []
            for rec in self.env['account.move'].search(domain_list):
                if rec.invoice_date:
                    if rec.invoice_date.year == int(lines.year):
                        year_month_recs.append(rec.id)
            domain_list.append(('id', 'in', year_month_recs))

            if lines.month:
                year_month_recs = []
                for recs in self.env['account.move'].search(domain_list):
                    if recs.invoice_date:
                        if recs.invoice_date.month == int(lines.month):
                            year_month_recs.append(recs.id)
                domain_list[1] = ('id', 'in', year_month_recs)
        else:
            domain_list += [('invoice_date', '>=', lines.invoice_date), ('invoice_date', '<=', lines.invoice_to_date)]

        invoice_list = self.env['account.move'].search(domain_list)

        sl_no = 1
        row = 1
        for recs in invoice_list:
            sheet.write(row, col, sl_no)
            sheet.write(row, col + 1, recs.name)
            sheet.write(row, col + 2, recs.invoice_date, date_style)
            # To get "SO number" invoice to be created from sale order
            if recs.invoice_origin:
                sheet.write(row, col + 3, recs.invoice_origin)
            sheet.write(row, col + 4, recs.currency_id.name)
            sheet.write(row, col + 5, recs.amount_untaxed)
            sheet.write(row, col + 6, recs.amount_tax)
            sheet.write(row, col + 7, recs.amount_total)
            sheet.write(row, col + 8, dict(recs._fields['payment_state'].selection).get(recs.payment_state))
            sl_no += 1
            row += 1