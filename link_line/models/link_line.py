# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LinkLine(models.Model):
    _name = 'link.line'

    name = fields.Char(string='Work summary', readonly=False)
    ftp = fields.Char(string='ftp')
    model = fields.Char(string='model')
    affect_id = fields.Many2one('base.invoices.merge.automatic.wizard', string='Event')
    source = fields.Char(string='Source')
    id_record = fields.Integer(string='Id record')

    def action_open(self):

        if self.source == 'affectation':
            return {
                'name': 'Affectation Ressource',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'popup',
                'res_model': 'base.invoices.merge.automatic.wizard',
                'res_id': self.id_record,
                'context': {},
                'domain': []
            }
        elif self.source == 'work_flow':
            return {
                'name': 'Action Workflow',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'popup',
                'res_model': 'base.flow.merge.automatic.wizard',
                'res_id': self.id_record,
                'context': {},
                'domain': []
            }
