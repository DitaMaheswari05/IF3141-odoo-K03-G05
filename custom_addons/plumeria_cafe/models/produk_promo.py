# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Produk(models.Model):
    _name = 'plumeria.produk'
    _description = 'Master Produk / Menu Plumeria Cafe'
    _rec_name = 'nama_produk'
    _order = 'divisi, nama_produk'

    nama_produk = fields.Char(string='Nama Produk', required=True)
    divisi = fields.Selection([
        ('bar', 'Bar'),
        ('kitchen', 'Kitchen'),
    ], string='Divisi', required=True)
    harga_jual = fields.Float(string='Harga Jual (Rp)', required=True)
    hpp = fields.Float(string='HPP (Rp)')
    margin = fields.Float(
        string='Margin (%)', compute='_compute_margin', store=True
    )
    status_aktif = fields.Boolean(string='Aktif', default=True)
    promo_ids = fields.Many2many(
        'plumeria.promo',
        relation='plumeria_produk_promo_rel',
        column1='produk_id',
        column2='promo_id',
        string='Promo Terkait',
    )

    @api.depends('harga_jual', 'hpp')
    def _compute_margin(self):
        for rec in self:
            if rec.harga_jual:
                rec.margin = ((rec.harga_jual - rec.hpp) / rec.harga_jual) * 100.0
            else:
                rec.margin = 0.0


class Promo(models.Model):
    _name = 'plumeria.promo'
    _description = 'Data Kampanye Promo'
    _rec_name = 'nama_promo'
    _order = 'periode_mulai desc'

    nama_promo = fields.Char(string='Nama Promo', required=True)
    kode_promo = fields.Char(string='Kode Promo', required=True, copy=False)
    periode_mulai = fields.Date(string='Periode Mulai', required=True)
    periode_selesai = fields.Date(string='Periode Selesai', required=True)
    jenis_diskon = fields.Selection([
        ('persentase', 'Persentase (%)'),
        ('nominal', 'Nominal (Rp)'),
    ], string='Jenis Diskon', required=True)
    nilai_diskon = fields.Float(string='Nilai Diskon', required=True)
    aktif = fields.Boolean(string='Aktif', default=True)
    produk_ids = fields.Many2many(
        'plumeria.produk',
        relation='plumeria_produk_promo_rel',
        column1='promo_id',
        column2='produk_id',
        string='Produk Berlaku',
    )
    total_penggunaan = fields.Integer(
        string='Estimasi Penggunaan (30 hari)',
        compute='_compute_penggunaan',
    )

    def _compute_penggunaan(self):
        from datetime import date, timedelta
        date_30 = date.today() - timedelta(days=30)
        Detail = self.env['plumeria.detail.transaksi']
        for rec in self:
            produk_ids = rec.produk_ids.ids
            if produk_ids:
                count = Detail.search_count([
                    ('produk_id', 'in', produk_ids),
                    ('transaksi_id.waktu_transaksi', '>=', str(date_30)),
                ])
                rec.total_penggunaan = count
            else:
                rec.total_penggunaan = 0
