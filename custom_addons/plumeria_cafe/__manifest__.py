# -*- coding: utf-8 -*-
{
    'name': 'Plumeria Cafe & Creative Space',
    'summary': 'Sistem Informasi Operasional Plumeria Cafe - IF3141 K03-G05',
    'version': '17.0.1.0',
    'category': 'Custom',
    'author': 'Kelompok 05 Kelas K03',
    'depends': ['base', 'mail'],
    'data': [
        'data/demo_users.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/laporan_views.xml',
        'views/transaksi_views.xml',
        'views/produk_promo_views.xml',
        'views/rekap_views.xml',
        'views/dashboard_views.xml',
        'views/menus.xml',
        'data/demo_produk.xml',
        'data/demo_promo.xml',
        'data/demo_transaksi.xml',
        'data/demo_laporan.xml',
        'data/demo_rekap.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'plumeria_cafe/static/src/js/dashboard_action.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
