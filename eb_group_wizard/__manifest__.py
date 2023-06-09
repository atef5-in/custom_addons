{
    'name': "Declaration Des Bons",
    'summary': "A module for managing declarations of bons.",
    'description': "A module for managing declarations of bons.",
    'author': "Mohamed Ba",
    'sequence': -680,
    'website': "",
    'category': 'Project, Tasks',
    'version': '15.0.1.0.0',
    'depends': ['base',
                #             'project',
                #             'product',
                #             'task_custom',
                'task_work',
                # 'employee_custom',
                # 'product_custom'
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        # 'views/project_task_work.xml',
        'views/declaration_de_bon_controle.xml',
        'views/declaration_de_bon.xml',
        'views/declaration_de_bon_correction.xml',
        'views/retour_bon_production.xml',
    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'auto_instale': False,
    'application': True,
    'license': 'LGPL-3',
}
