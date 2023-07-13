# -*- coding: utf-8 -*-
{
    'name': "Merge Work",

    'summary': """
        The merge_work_wizard module merges multiple tasks into one,
                """,

    'description': """
        Merging multiple tasks into one is now possible with this module.
        Go to Project --> Tasks (list view) and select multiple tasks, in the action button
        there will be Merge Tasks option. The wizard will open and place your settings there.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project_custom'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/m_work.xml',
        'views/button.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'sequence': -640,
}
