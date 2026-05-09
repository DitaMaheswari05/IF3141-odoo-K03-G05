# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import date, timedelta
import json


class PlumeriaDashboardController(http.Controller):

    @http.route('/plumeria/dashboard', auth='user', type='http', website=False)
    def dashboard(self, periode='hari_ini', **kwargs):
        today = date.today()

        if periode == '7_hari':
            date_from = today - timedelta(days=6)
        elif periode == 'bulan_ini':
            date_from = today.replace(day=1)
        else:
            periode = 'hari_ini'
            date_from = today

        Transaksi = request.env['plumeria.transaksi.pos']
        Laporan = request.env['plumeria.laporan.operasional']
        Detail = request.env['plumeria.detail.transaksi']

        # === KPI: Total penjualan, jumlah transaksi, rata-rata ===
        domain_periode = [
            ('waktu_transaksi', '>=', str(date_from) + ' 00:00:00'),
        ]
        transaksi_all = Transaksi.search(domain_periode)
        total_penjualan = sum(transaksi_all.mapped('total_transaksi'))
        jumlah_transaksi = len(transaksi_all)
        rata_rata = total_penjualan / jumlah_transaksi if jumlah_transaksi else 0.0

        # === Tren Harian 7 Hari Terakhir (selalu 7 hari, tidak dipengaruhi filter) ===
        tren_data = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            d_str = str(d)
            d_end = str(d + timedelta(days=1))

            t_bar = Transaksi.search([
                ('divisi', '=', 'bar'),
                ('waktu_transaksi', '>=', d_str + ' 00:00:00'),
                ('waktu_transaksi', '<', d_end + ' 00:00:00'),
            ])
            t_kitchen = Transaksi.search([
                ('divisi', '=', 'kitchen'),
                ('waktu_transaksi', '>=', d_str + ' 00:00:00'),
                ('waktu_transaksi', '<', d_end + ' 00:00:00'),
            ])
            tren_data.append({
                'tanggal': d.strftime('%d/%m'),
                'bar': sum(t_bar.mapped('total_transaksi')),
                'kitchen': sum(t_kitchen.mapped('total_transaksi')),
            })

        # === Distribusi Metode Pembayaran ===
        metode_map = {'tunai': 'Tunai', 'qris': 'QRIS', 'debit': 'Debit'}
        metode_counts = {}
        for t in transaksi_all:
            label = metode_map.get(t.metode_pembayaran, t.metode_pembayaran or 'Lainnya')
            metode_counts[label] = metode_counts.get(label, 0) + 1

        # === Top 5 Produk Terlaris ===
        detail_all = Detail.search([
            ('transaksi_id', 'in', transaksi_all.ids)
        ])
        produk_totals = {}
        for d in detail_all:
            nama = d.produk_id.nama_produk if d.produk_id else 'Unknown'
            if nama not in produk_totals:
                produk_totals[nama] = {'jumlah': 0, 'revenue': 0.0}
            produk_totals[nama]['jumlah'] += d.jumlah
            produk_totals[nama]['revenue'] += d.subtotal

        top_produk = sorted(
            produk_totals.items(),
            key=lambda x: x[1]['jumlah'],
            reverse=True
        )[:5]

        # === Laporan Terkini (10 terakhir) ===
        laporan_terkini = Laporan.search([], order='tanggal desc, id desc', limit=10)

        values = {
            'periode': periode,
            'date_from': str(date_from),
            'total_penjualan': total_penjualan,
            'jumlah_transaksi': jumlah_transaksi,
            'rata_rata': rata_rata,
            # JSON untuk Chart.js
            'tren_labels': json.dumps([d['tanggal'] for d in tren_data]),
            'tren_bar': json.dumps([d['bar'] for d in tren_data]),
            'tren_kitchen': json.dumps([d['kitchen'] for d in tren_data]),
            'metode_labels': json.dumps(list(metode_counts.keys())),
            'metode_data': json.dumps(list(metode_counts.values())),
            'metode_items': list(metode_counts.items()),
            # Data tabel
            'top_produk': top_produk,
            'laporan_terkini': laporan_terkini,
        }

        return request.render('plumeria_cafe.dashboard_template', values)
