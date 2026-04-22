# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Produk(models.Model):
    _name = 'pos.produk'
    _description = 'Entitas Produk'

    name = fields.Char(string="Nama Produk", required=True)
    harga = fields.Float(string="Harga Satuan", required=True)
    promo_ids = fields.Many2many('pos.promo', 'pos_promo_produk_rel', 'produk_id', 'promo_id', string="Promo Dipetakan")

class Promo(models.Model):
    _name = 'pos.promo'
    _description = 'Entitas Promo'

    name = fields.Char(string="Nama Promo", required=True)
    persentase_diskon = fields.Float(string="Diskon (%)")
    produk_ids = fields.Many2many('pos.produk', 'pos_promo_produk_rel', 'promo_id', 'produk_id', string="Produk Terkait")

class TransaksiPOS(models.Model):
    _name = 'pos.transaksi'
    _description = 'Entitas Transaksi POS'

    name = fields.Char(string="ID Transaksi", required=True, copy=False, readonly=True, default='Baru')
    tanggal = fields.Datetime(string="Tanggal Transaksi", default=fields.Datetime.now, required=True)
    # Menggunakan tabel res.users bawaan Odoo untuk entitas Pengguna
    pengguna_id = fields.Many2one('res.users', string="Kasir / Pengguna", default=lambda self: self.env.user)
    detail_ids = fields.One2many('pos.detail_transaksi', 'transaksi_id', string="Detail Transaksi")
    total_transaksi = fields.Float(string="Total Transaksi", compute='_compute_total', store=True)

    @api.depends('detail_ids.subtotal')
    def _compute_total(self):
        for record in self:
            record.total_transaksi = sum(detail.subtotal for detail in record.detail_ids)

class DetailTransaksi(models.Model):
    _name = 'pos.detail_transaksi'
    _description = 'Entitas Detail Transaksi'

    transaksi_id = fields.Many2one('pos.transaksi', string="Transaksi", ondelete='cascade')
    produk_id = fields.Many2one('pos.produk', string="Produk", required=True)
    harga_satuan = fields.Float(string="Harga Satuan", related='produk_id.harga', readonly=True)
    jumlah_penjualan = fields.Integer(string="Jumlah Penjualan", default=1, required=True)
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('harga_satuan', 'jumlah_penjualan')
    def _compute_subtotal(self):
        for record in self:
            record.subtotal = record.harga_satuan * record.jumlah_penjualan

class LaporanOperasional(models.Model):
    _name = 'pos.laporan'
    _description = 'Entitas Laporan Operasional'

    tanggal_laporan = fields.Date(string="Tanggal Laporan", required=True)
    pembuat_id = fields.Many2one('res.users', string="Dibuat Oleh", default=lambda self: self.env.user)
    total_pendapatan = fields.Float(string="Total Pendapatan Terkalkulasi")

class RekapKeuangan(models.Model):
    _name = 'pos.rekap'
    _description = 'Entitas Rekap Keuangan'

    periode = fields.Char(string="Periode Rekap", required=True)
    pembuat_id = fields.Many2one('res.users', string="Dibuat Oleh", default=lambda self: self.env.user)
    total_keuangan = fields.Float(string="Total Keuangan")