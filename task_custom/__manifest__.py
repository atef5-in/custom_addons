# -*- coding: utf-8 -*-
{
    'name': "Task Custom",

    'summary': """
        Project Task""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'task_work', 'product_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/task.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application' : True,
    'sequence': -980,
}
