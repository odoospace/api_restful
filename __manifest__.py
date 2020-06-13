# -*- coding: utf-8 -*-
{
    'name': "API RESTful",

    'summary': """
        API RESTful""",

    'description': """
        Simple and secure API RESTful for Odoo
    """,

    'author': "Impulso Diagonal",
    'website': "http://www.impulso.xyz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'api',
    'version': '12.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
    #],
}
