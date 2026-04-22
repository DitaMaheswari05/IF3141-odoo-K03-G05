# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Pengguna(models.Model):
    _name = 'pos.pengguna'
    _description = 'Entitas Pengguna (Stakeholder)'
    _rec_name = 'nama_stakeholder'

    id_pengguna = fields.Char(string="ID Pengguna", required=True, copy=False)
    nama_stakeholder = fields.Char(string="Nama Stakeholder", required=True)
    peran = fields.Selection([
        ('ho', 'Head of Operations'),
        ('finance', 'Finance'),
        ('marketing', 'Marketing'),
        ('head_bar', 'Head Bar'),
        ('head_kitchen', 'Head Kitchen'),
        ('developer', 'Developer'),
        ('ext', 'External')
    ], string="Peran", required=True)


class Produk(models.Model):
    _name = 'pos.produk'
    _description = 'Entitas Produk'
    _rec_name = 'nama_produk'

    id_produk = fields.Char(string="ID Produk", required=True, copy=False)
    nama_produk = fields.Char(string="Nama Produk", required=True)
    kategori = fields.Char(string="Kategori")
    harga_dasar = fields.Integer(string="Harga Dasar", required=True)

    # Relasi D-08 (Promo Produk) - Dipetakan di
    promo_ids = fields.Many2many(
        comodel_name='pos.promo', 
        relation='promo_produk', 
        column1='id_produk', 
        column2='id_promo', 
        string="Promo Dipetakan"
    )

class Promo(models.Model):
    _name = 'pos.promo'
    _description = 'Entitas Promo'
    _rec_name = 'nama_promo'

    id_promo = fields.Char(string="ID Promo", required=True, copy=False)
    nama_promo = fields.Char(string="Nama Promo", required=True)
    periode_mulai = fields.Date(string="Periode Mulai")
    periode_selesai = fields.Date(string="Periode Selesai")

    # Relasi D-08 (Promo Produk) - Dipetakan di
    produk_ids = fields.Many2many(
        comodel_name='pos.produk', 
        relation='promo_produk', 
        column1='id_promo', 
        column2='id_produk', 
        string="Produk Terkait"
    )

class TransaksiPOS(models.Model):
    _name = 'pos.transaksi'
    _description = 'Entitas Transaksi POS'
    _rec_name = 'id_transaksi'

    id_transaksi = fields.Char(string="ID Transaksi", required=True, copy=False)
    waktu_transaksi = fields.Datetime(string="Waktu Transaksi", default=fields.Datetime.now, required=True)
    total_transaksi = fields.Integer(string="Total Transaksi", compute='_compute_total', store=True)

    # Relasi "Terdiri dari" ke Detail Transaksi
    detail_ids = fields.One2many('pos.detail_transaksi', 'id_transaksi', string="Detail Transaksi")

    @api.depends('detail_ids.harga_satuan', 'detail_ids.jumlah_penjualan')
    def _compute_total(self):
        for record in self:
            record.total_transaksi = sum((detail.harga_satuan * detail.jumlah_penjualan) for detail in record.detail_ids)

class RekapKeuangan(models.Model):
    _name = 'pos.rekap'
    _description = 'Entitas Rekap Keuangan'
    _rec_name = 'id_rekap'

    id_rekap = fields.Char(string="ID Rekap", required=True, copy=False)
    tanggal = fields.Date(string="Tanggal Rekap", required=True)
    total_pemasukan = fields.Integer(string="Total Pemasukan")
    
    # FK Pembuat/Pencatat
    id_pengguna = fields.Many2one('pos.pengguna', string="Pencatat Rekap (Finance)")

    # Relasi Inverse "Membuat" (Dari Laporan Operasional)
    laporan_ids = fields.One2many('pos.laporan', 'id_rekap', string="Daftar Laporan Operasional")

class LaporanOperasional(models.Model):
    _name = 'pos.laporan'
    _description = 'Entitas Laporan Operasional'
    _rec_name = 'id_laporan'

    id_laporan = fields.Char(string="ID Laporan", required=True, copy=False)
    tanggal = fields.Date(string="Tanggal Laporan", required=True)
    isi_laporan = fields.Text(string="Isi Laporan")
    kendala = fields.Text(string="Kendala Operasional")
    
    # FK Pembuat Laporan
    id_pengguna = fields.Many2one('pos.pengguna', string="Pembuat Laporan")

    # Relasi "Membuat" ke Rekap Keuangan
    id_rekap = fields.Many2one('pos.rekap', string="Direkap Pada (Rekap Keuangan)")

    # Relasi Inverse "Tercatat di" (Dari Detail Transaksi)
    detail_transaksi_ids = fields.One2many('pos.detail_transaksi', 'laporan_id', string="Detail Transaksi Terkait")

class DetailTransaksi(models.Model):
    _name = 'pos.detail_transaksi'
    _description = 'Entitas Detail Transaksi'
    _rec_name = 'id_detail'

    id_detail = fields.Char(string="ID Detail", required=True, copy=False)
    
    # FK Relasi "Terdiri dari"
    id_transaksi = fields.Many2one('pos.transaksi', string="Transaksi POS", required=True, ondelete='cascade')
    
    # FK Relasi "Mencakup"
    id_produk = fields.Many2one('pos.produk', string="Produk", required=True)
    
    # FK Relasi "Tercatat di"
    laporan_id = fields.Many2one('pos.laporan', string="Tercatat di Laporan")

    jumlah_penjualan = fields.Integer(string="Jumlah Penjualan", default=1, required=True)
    harga_satuan = fields.Integer(string="Harga Satuan", required=True)

    @api.onchange('id_produk')
    def _onchange_produk(self):
        # Otomatis mengisi harga satuan berdasarkan harga dasar produk yang dipilih
        if self.id_produk:
            self.harga_satuan = self.id_produk.harga_dasar