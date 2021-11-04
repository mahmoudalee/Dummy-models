# -*- coding: utf-8 -*-

{
    'name': 'Discount Limit',
    'version': '14.0.0.0',
    'category': 'Extra Addons',
    'summary': 'This app will helps you to set discount limit.',
    'description': """
        set discount limit
    """,
    'author': 'Roaya',
    'depends': ['pyramids_pricelist', 'account', 'pyramids_product_fields', 'sale_margin','lot_management'],
    'data': [
        'views/sale_order.xml'
    ]

}
