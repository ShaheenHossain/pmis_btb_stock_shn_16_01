# -*- coding: utf-8 -*-
{
    'name': "BTB External Document Layout",

    'summary': """
        External document Layout for Bangladesh Parjatan Corporation""",

    'description': """
        design Pad for Bangladesh Parjatan Corporation for external Reports
    """,

    'author': "SM Ashraf",
    'website': "https://www.khan-store.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
            "data/res.lang.csv",
            "data/res.country.state.csv",
            "data/parjatan.xml",
            "views/partner_views.xml",
            "report/report_layout.xml",
            "security/btb_security.xml",


        ],
    'assets': {
        'web.assets_backend': [
            ('replace', 'web/static/src/legacy/scss/list_view.scss', 'btb_layout/static/src/scss/list_view.scss'),
        ],
    },
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
