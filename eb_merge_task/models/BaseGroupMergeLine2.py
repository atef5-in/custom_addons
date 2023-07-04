# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BaseGroupMergeLine2(models.Model):
    _name = 'base.group.merge.line2'
    _description = 'Base Group Merge Line'
    _order = 'min_id asc'

    wiz_id = fields.Many2one('base.task.merge.automatic.wizard', string='Wizard')
    r_id = fields.Many2one('risk.management.category', string='Wizard')
    min_id = fields.Integer(string='Wizard')
    aggr_ids = fields.Char(string='Ids')
    ftp = fields.Char(string='FTP')
    zo = fields.Char(string='Zone')
    name = fields.Char(string='Name')
    line_id = fields.Many2one('project.task.work.line', string='Wizard')
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    categ_id = fields.Many2one('product.category', string='Tags')
    product_id = fields.Many2one('product.product', string='Tags')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    date_start_r = fields.Date(string='Date')
    date_end_r = fields.Date(string='Date')
    date_start = fields.Date(string='Date')
    date_end = fields.Date(string='Date')
    color = fields.Float(string='Time Spent')
    uom_id = fields.Many2one('product.uom', string='Wizard')
    etape = fields.Char(string='Time Spent')
    hours = fields.Float(string='Time Spent')
    poteau_i = fields.Float(string='Time Spent')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    gest_id = fields.Many2one('hr.employee', string='Wizard')
    hours_r = fields.Float(string='Time Spent')
    total_t = fields.Float(string='Time Spent')
    total_r = fields.Float(string='Time Spent')
    poteau_t = fields.Float(string='Time Spent')
    poteau_r = fields.Float(string='Time Spent')
    wage = fields.Float(string='Time Spent')
    amount_line = fields.Float(string='Time Spent')
    poteau_reste = fields.Float(string='Time Spent')
    sequence = fields.Integer(string='Sequence')
    is_service = fields.Boolean(string='serv')
    zone = fields.Integer(string='Color Index')
    secteur = fields.Integer(string='Color Index')
    state = fields.Selection([
        ('draft', 'T. Planifiés'),
        ('affect', 'T. Affectés'),
        ('tovalid', 'Ret. Encours'),
        ('tovalidcont', 'Cont. Encours'),
        ('validcont', 'Cont. Valides'),
        ('tovalidcorrec', 'Corr. Encours'),
        ('validcorrec', 'Corr. Valides'),
        ('valid', 'T. Terminés'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
    ], string='Status', copy=False)
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Cloturé'),
    ], string='Status', copy=False)

    note = fields.Text(string='Work summary')
    done = fields.Boolean(string='Is Done')
    color1 = fields.Integer(string='Nbdays')
    link_id = fields.Many2one('project.task', string='Wizard')
    uom_id_r = fields.Many2one('product.uom', string='Wizard')
    is_display = fields.Boolean('Ids')