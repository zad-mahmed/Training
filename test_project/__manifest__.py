# -*- coding: utf-8 -*-
{
    'name': 'Purchase requset',
    'author': 'Mahmoud Ahmed',
    'category': 'Purchases',
    'version': '17.0.0.1',
    'depends': ['base', 'purchase',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/purchase_request_views.xml',
        'views/rejection_wizard_views.xml'

    ],
    'installable': True
}
