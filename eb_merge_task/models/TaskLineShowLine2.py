# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaskLineShowLine2(models.Model):
    _name = 'task_line.show.line2'

    wizard_id = fields.Many2one('base.task.merge.automatic.wizard', string='Role Lines', inverse_name='line_ids2')
    sequence = fields.Integer(string='Séq', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    project_id = fields.Many2one('project.project', string='Wizard')
    categ_id = fields.Char(string='Département')
    product_id = fields.Many2one('product.product', string='Wizard')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date Fin')
    color = fields.Date(string="Durée (Jours)")
    gest_id = fields.Many2one('hr.employee', string='Superviseur', readonly=True, )
    work_id = fields.Boolean(string="Durée (Jours)")
    state = fields.Date(string="Durée (Jours)")