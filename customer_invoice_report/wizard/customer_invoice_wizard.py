from odoo import models, fields, api

class CustomerInvoiceWizard(models.TransientModel):
    _name = 'customer.invoice.wizard'

    invoice_date = fields.Date('Invoiced Date')
    invoice_to_date = fields.Date('Invoiced To Date')
    specific_date = fields.Boolean('Specific Date')
    year_and_month = fields.Boolean('Year & Month')
    month = fields.Selection(
        [
            ('01', 'January'),
            ('02', 'February'),
            ('03', 'March'),
            ('04', 'April'),
            ('05', 'May'),
            ('06', 'June'),
            ('07', 'July'),
            ('08', 'August'),
            ('09', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December'),
        ],
        string="Month"
    )

    @api.model
    def year_selection(self):
        year = 2000
        year_list = []
        while year != 3000:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(
        year_selection,
        string="Year"
    )

    @api.onchange('specific_date', 'year_and_month')
    def date_checks_change(self):
        self.invoice_date = False
        self.invoice_to_date = False
        self.year = False
        self.month = False

    # Rendering report action - xlsx
    def print_excel_report(self):
        return self.env.ref('customer_invoice_report.customer_invoice_report').report_action(self)