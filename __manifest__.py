# -*- coding: utf-8 -*-
{
    'name': 'Real Estate',
    'description': 'A module for managing properties for a Real Estate company',
    'category': 'Tutorials/RealEstate',
    'application': True,
    'license': 'LGPL-3',
    'author': 'Michael Duke',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_menus.xml'
    ]
}