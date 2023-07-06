# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LinkLine(models.Model):
    _name = 'link.line'

    name = fields.Char(string='Work summary', readonly=False)
    ftp = fields.Char(string='ftp')
    model = fields.Char(string='model')
    work_id = fields.Many2one('project.task.work', string='Event')
    flow_id = fields.Many2one('base.flow.merge.automatic.wizard', string='Event')
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


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    link_ids = fields.One2many('link.line', 'work_id', string='Work done')


class BaseFlowMergeAutomaticWizard(models.Model):
    _inherit = 'base.flow.merge.automatic.wizard'

    link_ids = fields.One2many('link.line', 'flow_id', string="Work done", readonly=True,
                               states={'draft': [('readonly', False)]}, )
