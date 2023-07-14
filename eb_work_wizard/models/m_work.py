# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date


class MergeWorksLine(models.TransientModel):
    _name = 'base.work.merge.line'
    _order = 'min_id asc'

    wizard_id = fields.Many2one('base.work.merge.automatic.wizard', string='Wizard')
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
    note = fields.Text(string='Work summary')
    done = fields.Boolean(string='is done')
    color1 = fields.Integer(string='Nbdays')
    uom_id_r = fields.Many2one('product.uom', string='Wizard')


class EbMergeWorks(models.TransientModel):
    _name = 'base.work.merge.automatic.wizard'
    _description = 'Merge works'

    @api.model
    def default_get(self, fields_list):
        res = super(EbMergeWorks, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')

        if self.env.context.get('active_model') == 'project.task.work' and active_ids:

            for task in active_ids:
                work = self.env['project.task.work'].browse(task)
                if work.kit_id:
                    vv = []
                    kit_list = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('zone', '=', work.zone)
                            , ('secteur', '=', work.secteur), ('kit_id', '=', work.kit_id.id), ('rank', '=', work.rank),
                         ('product_id.name', 'not ilike', '%correction%'), ('product_id.name', 'not ilike', '%cont%')
                            , ('product_id.name', 'not ilike', '%gestion client%')])
                    for hh in kit_list.ids:
                        work = self.env['project.task.work'].browse(hh)
                        vv.append(work.id)
                    res['work_ids'] = vv
                else:
                    res['work_ids'] = active_ids
                context = self._context
                current_uid = context.get('uid')
                res_user = self.env['res.users'].browse(current_uid)
                categ_ids = self.env['hr.academic'].search([('employee_id', '=', res_user.employee_id.id)])
                jj = []
                if categ_ids:
                    for ll in categ_ids.ids:
                        dep = self.env['hr.academic'].browse(ll)
                        jj.append(dep.categ_id.id)
                # if work.categ_id.id not in jj:
                #     raise UserError(
                #         _("Action impossible!\nVous n'êtes pas autorisé à exécuter cette action sur un département externe"))
        return res

    work_ids = fields.Many2many('project.task.work', string='works')  # 'merge_tasks_rel', 'merge_id', 'task_id',)
    user_id = fields.Many2one('res.users', 'Assigned to', index=True)
    dst_work_id = fields.Many2one('project.task.work', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")
    zone = fields.Integer(string="zone")
    secteur = fields.Integer(string="secteur")
    is_devide = fields.Boolean(string="secteur", default=True)
    name = fields.Char(string="zone")
    state = fields.Selection([
        ('draft', 'T. Planifiés'),
        ('affect', 'T. Affectés'),
        ('tovalid', 'T. Réalisés'),
        ('valid', 'Factures en Attentes'),
        ('paid', 'Factures Approuvées'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
        ('close', 'Traité')
    ], string="Assigned"),

    # @api.model
    # def action_merge(self):
    #     names = []
    #     # write the name of the destination task because it will overwritten
    #     if self.dst_work_id:
    #         names.append(self.dst_work_id.name)
    #     else:
    #         ##raise UserError(_("You must select a Destination Task"))
    #         raise Warning('You must select a Destination work')
    #
    #     desc = []
    #     # also write the description of the destination work because it will be overwritten
    #     desc.append(self.dst_work_id.description)
    #     for id in self.work_ids:
    #         if id.id != self.dst_work_id.id:
    #             for name in id:
    #                 names.append(name.name)
    #                 desc.append(name.description)
    #             # append the names and desc to the empty lists
    #
    #             # self.work_ids.write({'message_ids' : self.dst_work_id.message_ids})
    #     # transfering the messages from work_ids to dst_work_id
    #     for message in self.work_ids:
    #         for msg_id in message.message_ids:
    #             msg_id.write({'res_id': self.dst_work_id.id})
    #
    #     # Transfer the timesheets from work_ids to dst_work_id
    #     ##        for timesheet in self.work_ids:
    #     ##            for ts_id in timesheet.timesheet_ids:
    #     ##                ts_id.write({'work_id': self.dst_work_id.id})
    #     # the work id for timesheet is updated with the dst_work_id.id
    #
    #     # # #loop the work_ids and transfer the tag_ids to the dst_work_id
    #     ##        for work in self.work_ids:
    #     ##            for tag in work.tag_ids:
    #     ##                tag.write({'tag_ids': (6, 0, [self.dst_work_id.id])})
    #
    #     # Check for planned hours and if any collect them all and place dst_work_id
    #     plan_hours = self.dst_work_id.planned_hours
    #     for hour in self.work_ids:
    #         for time in hour:
    #             plan_hours += time.planned_hours
    #     # Write to dst_work_id full planned hours from all works
    #     self.dst_work_id.write({'planned_hours': plan_hours})
    #
    #     # actual writing to the works
    #     transformed_names = ', '.join([unicode(i) for i in names])
    #     self.dst_work_id.write({'name': transformed_names})
    #
    #     # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), names)
    #
    #     transformed_desc = ', '.join([unicode(i) for i in desc])
    #     self.dst_work_id.write({'description': transformed_desc})
    #
    #     # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), desc)
    #     # Posting a note in the merged and archived works
    #     ###################################################################
    #     # get the base url from ir.config_parameter
    #     base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #     # loop all active works
    #     for work in self.work_ids:
    #         # post the link to every work
    #         work.message_post(
    #             body="This work has been merged into: " '%s/#id=%s&amp;view_type=form&amp;model=project.work' % (
    #             base_url, self.dst_work_id.id))
    #
    #     self.work_ids.write({'active': False})
    #     # explicitly write the dst_work_id TRUE for ACTIVE for security reasons
    #
    #     self.dst_work_id.write({'active': True})
    #
    #     # Check if user has been assigned and if not raise error
    #
    #     if self.user_id.id:
    #         # write the Assiged TO user_id
    #         self.dst_work_id.write({'user_id': self.user_id.id})
    #     elif self.dst_work_id.user_id.id:
    #         self.dst_work_id.write({'user_id': self.dst_work_id.user_id.id})
    #     else:
    #         # raise UserError(_("There is no user assigned to the merged work, and the destination work doesn't have assigned user too!!!"))
    #         raise Warning(
    #             'There is no user assigned to the merged work, and the destination work doesn''t have assigned user too!!!')
    #
    #     # For project_id check if any is given from user, if not use the project_id from dst_work_id project
    #     # write the project id to the dst_work_id
    #     ##        if self.dst_project:
    #     ##            self.dst_work_id.write({'project_id': self.dst_project.id})
    #     ##        else:
    #     ##            self.dst_work_id.write({'project_id': self.dst_work_id.project_id.id})
    #
    #     return True
    #
    # ##    def copy(self, default=None):
    # ##          default = dict(default or {})
    # ##          default.update({'weight': float(43)})
    # ##          return super(ProductTemplate, self).copy(default)
    # @api.multi
    # def action_copy1(self, default=None):
    #
    #     return super(project_work, self).copy(vals)
    #
    # ##    self.env['project.task'].copy(self.dst_task_id.id)
    # def button_close(self, cr, uid, ids, context=None):
    #     return {'type': 'ir.actions.act_window_close'}
    #
    def action_copy(self):

        for current in self.browse(self.id):
            for tt in current.work_ids:
                work = self.env['project.task.work'].browse(tt.id)
                if work.state == 'pending':
                    raise UserError(_('Action impossible!\nImpossible de dupliquer une ligne suspendue!'))
                packaging_obj = self.env['project.task.work']
                self.env.cr.execute(
                    'select sequence from project_task_work where task_id=%s and sequence is not Null order by sequence desc limit 1',
                    (tt.task_id.id,))
                res = self.env.cr.fetchone()
                sequence = res[0] + 1
                kk = self.env['project.task.work'].search([('project_id', '=', tt.project_id.id),
                                                           ('sequence', '=', sequence)])

                while kk:
                    sequence = sequence + 1
                    kk = self.env['project.task.work'].search([('project_id', '=', tt.project_id.id),
                                                               ('sequence', '=', sequence)])
                if current.is_devide:
                    qty = tt.poteau_i / 2
                    reste = tt.poteau_i - (tt.poteau_i / 2)
                else:
                    qty = tt.poteau_i
                    reste = tt.poteau_i
                if current.name:
                    new_name = tt.name + ' - ' + current.name
                else:
                    new_name = tt.name
                packaging_obj.browse(tt.id).write({'poteau_t': qty})

                cte = packaging_obj.create({
                    'project_id': tt.project_id.id,
                    'sequence': sequence,
                    'task_id': tt.task_id.id,
                    'product_id': tt.product_id.id,
                    'name': new_name,
                    'date_start': tt.date_start,
                    'date_end': tt.date_end,
                    'poteau_t': reste,
                    'color': tt.color,
                    'total_t': tt.color * 7,  ##*work.employee_id.contract_id.wage
                    'poteau_i': tt.poteau_i,
                    'categ_id': tt.categ_id.id,
                    'state_id': tt.state_id.id or False,
                    'city': tt.city or False,
                    'gest_id': tt.gest_id.id,
                    'uom_id': tt.uom_id.id,
                    'uom_id_r': tt.uom_id_r.id,
                    'hours': tt.hours,
                    'etape': tt.etape,
                    'ftp': tt.ftp,
                    'zone': tt.zone,
                    'secteur': tt.secteur,
                    'zo': 'Zone ' + str(tt.zone).zfill(1),
                    'sect': 'Secteur ' + str(tt.secteur).zfill(2),
                    'state': 'draft',
                    'active': True,
                    'display': tt.display,
                    'is_copy': True,
                    'current_gest': tt.gest_id.id or False,
                    'current_sup': tt.gest_id3.id or False,
                    'gest_id3': tt.gest_id3.id or False,
                    'reviewer_id1': tt.reviewer_id1.id or False,
                    'coordin_id1': tt.coordin_id1.id or False,
                    'coordin_id2': tt.coordin_id2.id or False,
                    'coordin_id3': tt.coordin_id3.id or False,
                    'coordin_id4': tt.coordin_id4.id or False,
                    'coordin_id5': tt.coordin_id5.id or False,
                    'coordin_id6': tt.coordin_id6.id or False,
                    'coordin_id7': tt.coordin_id7.id or False,
                    'coordin_id8': tt.coordin_id8.id or False,
                    'coordin_id9': tt.coordin_id9.id or False,
                    'coordin_id10': tt.coordin_id10.id or False,
                    'partner_id': tt.partner_id.id or False,
                    'kit_id': tt.kit_id.id or False,
                    'rank': str(datetime.now().strftime("%d/%m/%Y %H:%M"))
                })
                res_user = self.env['res.users'].browse(self.env.user.id)
                wk_histo = self.env['work.histo'].search([('work_id', '=', tt.id)])
                wk_histo_id = self.env['work.histo'].browse(wk_histo).id
                self.env['work.histo.line'].create({
                    'type': 'duplication',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': wk_histo_id,
                    'date': datetime.now(),
                    'coment1': current.name or False,
                    'id_object': current.id,
                })
                # for histo in wk_histo:
                #     self.env['work.histo.line'].create({
                #         'type': 'duplication',
                #         'create_by': res_user.employee_id.name,
                #         'work_histo_id': histo.id,
                #         'date': datetime.now(),
                #         'coment1': current.name or False,
                #         'id_object': current.id,
                #     })
                self.env['work.histo'].create({
                    'task_id': tt.task_id.id,
                    'work_id': cte.id,
                    'categ_id': tt.categ_id.id,
                    'product_id': tt.product_id.id,
                    'name': tt.name,
                    'date': tt.date_start,
                    'create_a': datetime.now(),
                    'create_by': res_user.employee_id.name,
                    'zone': tt.zone,
                    'secteur': tt.secteur,
                    'project_id': tt.project_id.id,
                    'partner_id': tt.project_id.partner_id.id,
                })
        return True

