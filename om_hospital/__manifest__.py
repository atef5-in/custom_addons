# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",

    'summary': """
        Hospital Management Application""",

    'description': """
    """,

    'author': "Atef",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base','mail','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/female_doctor_view.xml',
        'views/male_doctor_view.xml',
        'views/medicament_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
