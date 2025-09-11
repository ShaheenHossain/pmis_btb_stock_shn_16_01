# -*- coding: utf-8 -*-
{
    'name': "Stock, Bangladesh Tourism Board",

    'summary': """
        Stock Customisation For Bangladesh Tourism Board""",

    'description': """
        design an inventory project for Bangladesh TOurism Board
    """,

    'author': "SM Ashraf",
    'website': "https://www.khan-store.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'inventory',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_stock','website','btb_layout','portal'],

    # always loaded
    'data': [
            "security/btb_security.xml",
            "security/ir.model.access.csv",
            "views/views.xml",
            "report/btb_adhijachan_patra.xml",
            "report/btb_stock_report.xml",
            "views/menus.xml",
            "data/parjatan.xml",
            "data/product.template.csv",
            # "data/product.product.csv", here is import eror
            "report/report_layout.xml",
            "portal/portal_templates.xml",



    ],
    # only loaded in demonstration mode
    'demo': [
        # "demo/pmis.travel.csv",
        # "demo/pmis.publications.csv",
        'demo/demo.xml',
    ],


    "auto_install": False,
    'application': True,
    'license': 'LGPL-3',
    "installable": True,
}
