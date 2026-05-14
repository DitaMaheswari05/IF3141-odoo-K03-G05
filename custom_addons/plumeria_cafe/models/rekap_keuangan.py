# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class RekapKeuangan(models.Model):
    _name = 'plumeria.rekap.keuangan'
    _description = 'Rekap Keuangan Harian'
    _rec_name = 'name'
    _order = 'tanggal desc, divisi'

    name = fields.Char(string='Nama Rekap', compute='_compute_name', store=True)
    tanggal = fields.Date(string='Tanggal', required=True, default=fields.Date.today)
    divisi = fields.Selection([
        ('bar', 'Bar'),
        ('kitchen', 'Kitchen'),
    ], string='Divisi', required=True)

    total_kas = fields.Float(
        string='Total Kas Aktual (Rp)', required=True,
        help='Total pemasukan kas yang dihitung oleh Finance'
    )
    total_pos = fields.Float(
        string='Total Transaksi POS (Rp)', readonly=True,
        help='Total dari sistem POS untuk divisi dan tanggal ini'
    )
    delta = fields.Float(
        string='Selisih (Rp)', compute='_compute_status', store=True
    )
    status_rekonsiliasi = fields.Selection([
        ('pending', 'Belum Direkonsiliasi'),
        ('cocok', 'Cocok'),
        ('selisih', 'Selisih Ditemukan'),
    ], string='Status', default='pending', compute='_compute_status', store=True)

    catatan = fields.Text(string='Catatan Rekonsiliasi')
    laporan_ids = fields.One2many(
        'plumeria.laporan.operasional', 'rekap_id', string='Laporan Terkait'
    )

    @api.depends('tanggal', 'divisi')
    def _compute_name(self):
        divisi_label = {'bar': 'Bar', 'kitchen': 'Kitchen'}
        for rec in self:
            div = divisi_label.get(rec.divisi, '')
            tgl = str(rec.tanggal) if rec.tanggal else ''
            rec.name = f'Rekap {div} - {tgl}'

    @api.depends('total_kas', 'total_pos')
    def _compute_status(self):
        for rec in self:
            rec.delta = rec.total_kas - rec.total_pos
            if rec.total_pos == 0 and rec.total_kas == 0:
                rec.status_rekonsiliasi = 'pending'
            elif abs(rec.delta) < 1.0:
                rec.status_rekonsiliasi = 'cocok'
            else:
                rec.status_rekonsiliasi = 'selisih'

    def action_hitung_total_pos(self):
        for rec in self:
            if not rec.tanggal or not rec.divisi:
                continue
            date_start = rec.tanggal
            date_end = rec.tanggal + timedelta(days=1)
            transaksi = self.env['plumeria.transaksi.pos'].search([
                ('divisi', '=', rec.divisi),
                ('waktu_transaksi', '>=', str(date_start) + ' 00:00:00'),
                ('waktu_transaksi', '<', str(date_end) + ' 00:00:00'),
            ])
            rec.total_pos = sum(transaksi.mapped('total_transaksi'))
            rec.action_tarik_laporan()

    def write(self, vals):
        result = super().write(vals)
        for rec in self:
            if rec.status_rekonsiliasi == 'cocok':
                laporan_approved = rec.laporan_ids.filtered(
                    lambda l: l.state == 'approved'
                )
                if laporan_approved:
                    laporan_approved.write({'state': 'archived'})
        return result
    
    @api.onchange('tanggal', 'divisi')
    def _onchange_tarik_laporan(self):
        if self.tanggal and self.divisi:
            laporan_terkait = self.env['plumeria.laporan.operasional'].search([
                ('tanggal', '=', self.tanggal),
                ('divisi', '=', self.divisi),
            ])
            self.laporan_ids = [(6, 0, laporan_terkait.ids)]

    def action_tarik_laporan(self):
        for rec in self:
            if not rec.tanggal or not rec.divisi:
                continue
            laporan_terkait = self.env['plumeria.laporan.operasional'].search([
                ('tanggal', '=', rec.tanggal),
                ('divisi', '=', rec.divisi),
                ('state', '=', 'approved')
            ])
            if laporan_terkait:
                rec.laporan_ids = [(6, 0, laporan_terkait.ids)]
            else:
                pass
