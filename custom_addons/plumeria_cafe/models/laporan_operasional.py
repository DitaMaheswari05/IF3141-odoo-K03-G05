# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LaporanOperasional(models.Model):
    _name = 'plumeria.laporan.operasional'
    _description = 'Laporan Operasional Harian'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'nomor_referensi'
    _order = 'tanggal desc, id desc'

    nomor_referensi = fields.Char(
        string='Nomor Referensi', readonly=True, copy=False, default='New'
    )
    tanggal = fields.Date(
        string='Tanggal Laporan', required=True, default=fields.Date.today, tracking=True
    )
    divisi = fields.Selection([
        ('bar', 'Bar'),
        ('kitchen', 'Kitchen'),
    ], string='Divisi', required=True, tracking=True)

    total_pendapatan = fields.Float(string='Total Pendapatan (Rp)', tracking=True)
    jumlah_transaksi = fields.Integer(string='Jumlah Transaksi', tracking=True)
    metode_pembayaran = fields.Selection([
        ('tunai', 'Tunai'),
        ('qris', 'QRIS'),
        ('debit', 'Debit'),
        ('campuran', 'Campuran'),
    ], string='Metode Pembayaran Dominan', tracking=True)
    hpp = fields.Float(string='HPP (Rp)', tracking=True)
    beban_operasional = fields.Float(string='Beban Operasional (Rp)', tracking=True)
    catatan_kendala = fields.Text(string='Catatan Kendala Operasional')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Diajukan'),
        ('approved', 'Disetujui'),
        ('revised_draft', 'Perlu Revisi'),
        ('archived', 'Diarsipkan'),
    ], string='Status', default='draft', required=True, tracking=True)

    alasan_revisi = fields.Text(string='Alasan Revisi', readonly=True)
    rekap_id = fields.Many2one(
        'plumeria.rekap.keuangan', string='Rekap Keuangan', ondelete='set null'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('nomor_referensi', 'New') == 'New':
                vals['nomor_referensi'] = (
                    self.env['ir.sequence'].next_by_code('plumeria.laporan.operasional')
                    or 'New'
                )
        return super().create(vals_list)

    def action_submit(self):
        for rec in self:
            rec.write({'state': 'submitted'})

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved'})

    def action_request_revision(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Alasan Revisi',
            'res_model': 'plumeria.wizard.revisi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_laporan_id': self.id},
        }

    def action_archive_laporan(self):
        for rec in self:
            rec.write({'state': 'archived'})

    def action_reset_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})


class WizardRevisi(models.TransientModel):
    _name = 'plumeria.wizard.revisi'
    _description = 'Wizard Input Alasan Revisi'

    laporan_id = fields.Many2one('plumeria.laporan.operasional', required=True)
    alasan = fields.Text(string='Alasan Revisi', required=True)

    def action_konfirmasi(self):
        self.laporan_id.write({
            'state': 'revised_draft',
            'alasan_revisi': self.alasan,
        })
        self.laporan_id.message_post(
            body=f'<b>Revisi diminta:</b> {self.alasan}',
            message_type='comment',
            subtype_xmlid='mail.mt_note',
        )
