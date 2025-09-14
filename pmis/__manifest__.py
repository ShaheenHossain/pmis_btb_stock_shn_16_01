{
    'name': "PMIS",

    'summary': """
        Project for PMIS""",

    'description': """
        design an inventory project for pmis
    """,

    'author': "SM Ashraf",
    'website': "https://www.khan-store.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','website','btb_layout','portal'],

    # always loaded
    'data': [
            "data/pmis.contact.type.csv",
            "data/pmis_rank.xml",
            # "data/pmis.designation.csv",
            "data/pmis.result.system.csv",
            "data/pmis.result.system.line.csv",
            "data/pmis.education.subject.csv",
            "data/pmis_organisation.xml",
            "data/pmis.bcs.csv",
            "data/pmis.bcs.cadre.csv",
            "data/data.xml",
            "data/pmis.training.category.csv",
            "data/pmis_leave.xml",
            "data/pmis.job.category.csv",
            "data/pmis.quota.csv",
            "data/pmis.service.grade.csv",
            "views/partner_views.xml",
            "views/partner_online_views.xml",
            "views/person_views.xml",
            "views/pmis_views.xml",
            "views/leave.xml",
            "views/views.xml",
            "security/pmis_security.xml",
            "security/ir.model.access.csv",
            "report/pmis_report.xml",
            "report/pmis_report_wizard.xml",
            "views/actions.xml",
            "views/menus.xml",
            "portal/pmis_portal_templates.xml",
            # "views/pmis_create_user.xml",

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        "demo/pmis.publications.csv",
        "demo/pmis.training.csv",
        "demo/pmis.training.line.csv",
    ],


    "auto_install": False,
    'application': True,
    'license': 'LGPL-3',
    "installable": True,
}
# -*- coding: utf-8 -*-

