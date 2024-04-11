{
    'name': 'Customer Invoice Excel Report',
    'version': '1.1',
    'category': 'Reports',
    'sequence': -1,
    'summary': 'Customer Invoice Details in Excel Report',
    'description': 'Excel report for details of customer invoice for invoice records with a specified date or with a specified range of dates',
    'author': 'Suprit-S',
    "website": "https://github.com/Suprit-S/customer_invoice_excel_report",
    'depends': ['account', 'report_xlsx'],
    'data': {
        'security/ir.model.access.csv',
        'wizard/customer_invoice_wizard.xml',
        'report/customer_invoice_excel.xml'
    },
    'application': True,
    'installable': True,
    'auto_install': False,
}