# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MergeActivesLine(models.TransientModel):
    _name = 'base.active.merge.line'
    _order = 'min_id asc'

    wizard_id = fields.Many2one('base.active.merge.automatic.wizard', string='Wizard')
    min_id = fields.Integer(string='MinID')
    aggr_ids = fields.Char(string='Ids', required=True)
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    categ_id = fields.Many2one('product.category', string='Tags')
    product_id = fields.Many2one('product.product', string='Tags')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    date_start_r = fields.Date(string='Date')
    date_end_r = fields.Date(string='Date')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    gest_id = fields.Many2one('hr.employee', string='Wizard')
    hours_r = fields.Float(string='Time Spent')
    total_t = fields.Float(string='Time Spent')
    total_r = fields.Float(string='Time Spent')
    poteau_t = fields.Float(string='Time Spent')
    poteau_r = fields.Float(string='Time Spent')
    poteau_i = fields.Float(string='Time Spent')
    wage = fields.Float(string='Time Spent')
    amount_line = fields.Float(string='Time Spent')
    poteau_reste = fields.Integer(string='Time Spent')
    sequence = fields.Integer(string='Sequence')
    zone = fields.Integer(string='Color Index')
    secteur = fields.Integer(string='Color Index')
    state = fields.Selection([
        ('draft', 'T. Planifiés'),
        ('affect', 'T. Affectés'),
        ('tovalid', 'T. Réalisés'),
        ('valid', 'Factures en Attentes'),
        ('paid', 'Factures Approuvées'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
        ('close', 'Traité')
    ], string='Status', copy=False)
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Cloturé'),
    ], string='Status', copy=False)
    note = fields.Text(string='active summary')
    done = fields.Boolean(string='is done')
    color1 = fields.Integer(string='Nbdays')
    uom_id_r = fields.Many2one('product.uom', string='Wizard')


class EbMergeActives(models.TransientModel):
    _name = 'base.active.merge.automatic.wizard'
    _description = 'Merge actives'

    @api.model
    def default_get(self, fields_list):
        res = super(EbMergeActives, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')

        if self.env.context.get('active_model') == 'project.task.work' and active_ids:
            vv = []
            for hh in active_ids:
                work = self.env['project.task.work'].browse(hh)

                proj = []
                zo = []
                sect = []
                if work.kit_id:
                    if work.kit_id.id not in vv:
                        vv.append(work.kit_id.id)
                        proj.append(work.project_id.id)
                        zo.append(work.zone)
                        sect.append(work.secteur)
                work.update({'active': True
                             })  ##,'categ_id':work.categ_id.id
                res.update({'dst_project': work.project_id.id})
        if len(vv) > 0:

            self.env.cr.execute(
                'select DISTINCT ON (kit_id,zone,secteur) id  from project_task_work where project_id=%s  and zone = %s and secteur = %s and kit_id in %s order by kit_id,zone,secteur',
                (proj[0], zo[0], sect[0], tuple(vv),))
            ltask2 = list(self.env.cr.fetchall())

            res['work_ids'] = [item for t in ltask2 for item in t]
        else:
            res['work_ids'] = active_ids

        return res

    work_ids = fields.Many2many('project.task.work', string='actives',
                                domain=[('active', 'in', (True, False))])  # 'merge_tasks_rel', 'merge_id', 'task_id',)
    user_id = fields.Many2one('res.users', string='Assigned to', index=True)
    dst_work_id = fields.Many2one('project.task.work', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")
    zone = fields.Integer(string="zone")
    secteur = fields.Integer(string="secteur")
    is_devide = fields.Boolean(string="secteur", default=True)
    is_active = fields.Boolean(string="secteur", default=True)
    is_display = fields.Boolean(string="secteur", default=True)
    name = fields.Char(string="zone")
    state = fields.Selection([('draft', 'T. Planifiés'),
                              ('affect', 'T. Affectés'),
                              ('affect_con', 'T. Affectés controle'),
                              ('affect_corr', 'T. Affectés correction'),
                              ('tovalid', 'Ret .Encours'),
                              ('tovalidcont', 'Cont .Encours'),
                              ('validcont', 'Cont .Valides'),
                              ('tovalidcorrec', 'Corr .Encours'),
                              ('validcorrec', 'Corr .Valides'),
                              ('valid', 'T.Terminés'),
                              ('cancel', 'T. Annulés'),
                              ('pending', 'T. Suspendus'),
                              ],
                             string="Assigned")

    # @api.multi
    # def action_copy1(self, default=None):
    #
    #     return super(project_work, self).copy(vals)
    #
    # ##    self.env['project.task'].copy(self.dst_task_id.id)
    # def button_close(self, cr, uid, ids, context=None):
    #     return {'type': 'ir.actions.act_window_close'}
    #
    def action_change(self):

        for current in self.browse(self.id):
            for tt in current.work_ids.ids:
                self.env['project.task.work'].browse(tt).write(
                    {'active': current.is_active, 'display': current.is_display})
        return True

    def action_change_state(self):

        for current in self.browse(self.id):

            if current.dst_project.is_kit is True:
                for tt in current.work_ids.ids:
                    work = self.env['project.task.work'].browse(tt)
                    self.env.cr.execute(
                        'update project_task_work set  state=%s where  kit_id=%s and project_id=%s and zone=%s and secteur=%s',
                        (current.state, work.kit_id.id, work.project_id.id, work.zone, work.secteur))
            else:
                for tt in current.work_ids.ids:
                    self.env['project.task.work'].write(tt, {'state': current.state})

        return True
