# -*- coding: utf-8 -*-
{
    'name': "Website Terintegrasi untuk Daily Report & Monitoring Operasional",
    'summary': "Modul ERP untuk pencatatan dan analisis operasional",
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir_model_data.xml',
        'security/ir_model_access.xml',
        'views/pos_menu.xml',
        'views/pos_trees.xml',
        'views/pos_forms.xml',
        'views/pos_graphs.xml',
    ],
    'installable': True,
    'application': True,
}