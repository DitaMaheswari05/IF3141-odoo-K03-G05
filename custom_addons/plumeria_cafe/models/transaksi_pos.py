# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TransaksiPOS(models.Model):
    _name = 'plumeria.transaksi.pos'
    _description = 'Data Transaksi POS'
    _rec_name = 'id_transaksi'
    _order = 'waktu_transaksi desc'

    id_transaksi = fields.Char(string='ID Transaksi', required=True, copy=False)
    waktu_transaksi = fields.Datetime(
        string='Waktu Transaksi', required=True, default=fields.Datetime.now
    )
    divisi = fields.Selection([
        ('bar', 'Bar'),
        ('kitchen', 'Kitchen'),
    ], string='Divisi', required=True)
    metode_pembayaran = fields.Selection([
        ('tunai', 'Tunai'),
        ('qris', 'QRIS'),
        ('debit', 'Debit'),
    ], string='Metode Pembayaran', required=True)
    total_transaksi = fields.Float(
        string='Total (Rp)', compute='_compute_total', store=True
    )
    detail_ids = fields.One2many(
        'plumeria.detail.transaksi', 'transaksi_id', string='Detail Pesanan'
    )

    @api.depends('detail_ids.subtotal')
    def _compute_total(self):
        for rec in self:
            rec.total_transaksi = sum(rec.detail_ids.mapped('subtotal'))


class DetailTransaksi(models.Model):
    _name = 'plumeria.detail.transaksi'
    _description = 'Detail Item Transaksi'
    _rec_name = 'produk_id'

    transaksi_id = fields.Many2one(
        'plumeria.transaksi.pos', string='Transaksi', required=True, ondelete='cascade'
    )
    produk_id = fields.Many2one('plumeria.produk', string='Produk', required=True)
    jumlah = fields.Integer(string='Jumlah', default=1, required=True)
    harga_satuan = fields.Float(string='Harga Satuan (Rp)', required=True)
    subtotal = fields.Float(string='Subtotal (Rp)', compute='_compute_subtotal', store=True)

    @api.depends('jumlah', 'harga_satuan')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.jumlah * rec.harga_satuan

    @api.onchange('produk_id')
    def _onchange_produk(self):
        if self.produk_id:
            self.harga_satuan = self.produk_id.harga_jual
