# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
import time


class MergePermisLine(models.Model):
    _name = 'base.permis.merge.line'
    _order = 'min_id asc'

    wizard_id = fields.Many2one('base.permis.merge.automatic.wizard', string='Wizard')
    min_id = fields.Integer(string='MinID')
    aggr_ids = fields.Char(string='Ids')
    zone = fields.Integer(string='zone')
    secteur = fields.Integer(string='secteur')
    secteur_to = fields.Integer(string='secteur')
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    poteau_t = fields.Integer(string='Time Spent')


class EbMergePermis(models.Model):
    _name = 'base.permis.merge.automatic.wizard'

    @api.model
    def default_get(self, fields_list):
        res = super(EbMergePermis, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids')

        if self.env.context.get('active_model') == 'project.task.work' and active_ids:
            work = self.env['project.task.work'].browse(active_ids[0])
            if 'Demande' not in work.name:
                raise UserError(_('Action Impossible!\nSeules les demandes de permis sont à sélectionner!'))
            for jj in active_ids:
                work = self.env['project.task.work'].browse(jj)
                self._cr.execute('update project_task_work set  state=%s where id=%s ', ('affect', work.id))
                if not work.employee_id:
                    self._cr.execute('update project_task_work set  employee_id=%s where id=%s ', (30, work.id))
                if work.kit_id:
                    res.update({'project_id': work.project_id.id, 'zone': work.zone, 'secteur': work.secteur,
                                'employee_id': work.employee_id.id or 30})
                else:
                    res.update({'project_id': work.project_id.id, 'zone': work.zone, 'secteur': work.secteur,
                                'employee_id': work.employee_id.id or 30})
            return res

    project_id = fields.Many2one('project.project', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    date_from = fields.Date(string='Wizard', select=True, default=time.strftime('%Y-01-01'))
    date_to = fields.Date(string='Wizard', select=True, default=datetime.today())
    partner_id = fields.Many2one('res.partner', string='Wizard')
    product_id = fields.Many2one('product.product', string='Wizard')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Validé')
    ], string='Priority', default='draft', select=True)
    week_no = fields.Selection([
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52')], string='Priority', select=True, default=str(time.strftime('%W')))
    year_no = fields.Char(string='Priority', default=str(time.strftime('%Y')))
    name = fields.Char(string='Priority', default='Subdivision Zone-Secteur')
    work_ids = fields.Many2many('project.task', string='Works')
    user_id = fields.Many2one('res.users', 'Assigned to', index=True)
    employee_id = fields.Many2one('hr.employee', 'Assigned to', index=True)
    dst_task_id = fields.Many2one('project.task', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")
    zone = fields.Integer(string="zone")
    secteur = fields.Integer(string="secteur")
    line_ids = fields.One2many(
        'base.permis.merge.line', 'wizard_id', string=u"Role lines", copy=True)

    @api.model
    def action_merge(self):
        names = []
        # write the name of the destination task because it will overwritten
        if self.dst_task_id:
            names.append(self.dst_task_id.name)
        else:
            raise Warning('You must select a Destination Task')
        desc = []
        # also write the description of the destination task because it will be overwritten
        desc.append(self.dst_task_id.description)
        for id in self.work_ids:
            if id.id != self.dst_task_id.id:
                for name in id:
                    names.append(name.name)
                    desc.append(name.description)
                # append the names and desc to the empty lists

                # self.task_ids.write({'message_ids' : self.dst_task_id.message_ids})
        # transfering the messages from task_ids to dst_task_id
        for message in self.task_ids:
            for msg_id in message.message_ids:
                msg_id.write({'res_id': self.dst_task_id.id})

        # Check for planned hours and if any collect them all and place dst_task_id
        plan_hours = self.dst_task_id.planned_hours
        for hour in self.task_ids:
            for time in hour:
                plan_hours += time.planned_hours
        # Write to dst_task_id full planned hours from all tasks
        self.dst_task_id.write({'planned_hours': plan_hours})

        # actual writing to the tasks
        transformed_names = ', '.join(names)
        self.dst_task_id.write({'name': transformed_names})

        # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), names)

        transformed_desc = ', '.join(desc)
        self.dst_task_id.write({'description': transformed_desc})

        # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), desc)
        # Posting a note in the merged and archived tasks
        ###################################################################
        # get the base url from ir.config_parameter
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # loop all active tasks
        for task in self.task_ids:
            # post the link to every task
            task.message_post(
                body="This task has been merged into: " '%s/#id=%s&amp;view_type=form&amp;model=project.task' % (
                    base_url, self.dst_task_id.id))

        self.task_ids.write({'active': False})
        # explicitly write the dst_task_id TRUE for ACTIVE for security reasons

        self.dst_task_id.write({'active': True})

        # Check if user has been assigned and if not raise error

        if self.user_id.id:
            # write the Assiged TO user_id
            self.dst_task_id.write({'user_id': self.user_id.id})
        elif self.dst_task_id.user_id.id:
            self.dst_task_id.write({'user_id': self.dst_task_id.user_id.id})
        else:
            raise UserError(
                _('There is no user assigned to the merged task, and the destination task doesn''t have assigned user too!!!'))

        return True

    # def onchange_week_(self, cr, uid, ids, year_no, week_no, context=None):
    #     result = {'value': {}}
    #
    #     d = date(int(year_no), 1, 1)
    #     if (d.weekday() <= 3):
    #         d = d - dt.timedelta(d.weekday())
    #     else:
    #         d = d + dt.timedelta(7 - d.weekday())
    #     dlt = dt.timedelta(days=(int(week_no) - 1) * 7)
    #
    #     result['value']['date_from'] = d + dlt
    #     result['value']['date_to'] = d + dlt + dt.timedelta(days=6)
    #     return result

    # @api.model
    # def action_copy1(self):
    #
    #     return super(project_task, self).copy(vals)

    def action_copy(self, id):

        # your changes
        for current in self.browse(id):
            for tt in current.work_ids:
                self.env.cr.execute(
                    'select sequence from project_task_work where task_id=%s and sequence is not Null order by sequence desc limit 1',
                    (tt.id,))
                res = self.env.cr.fetchone()

                if res:
                    sequence = res[0] + 1
                sequence = 60001
                kk = self.env['project.task.work'].search([('project_id', '=', tt.project_id.id),
                                                           ('sequence', '=', sequence)])

                while kk:
                    sequence = sequence + 1
                    kk = self.env['project.task.work'].search([('project_id', '=', tt.project_id.id),
                                                               ('sequence', '=', sequence)])
                if tt.product_id:
                    self.env['project.task.work'].create({
                        'task_id': tt.id,
                        'product_id': tt.product_id.id,
                        'name': tt.name,
                        'date_start': tt.date_start,
                        'date_end': tt.date_end,
                        'poteau_t': tt.qte,
                        'color': tt.color,
                        'total_t': tt.color * 7,  ##*work.employee_id.contract_id.wage
                        'project_id': tt.project_id.id,
                        'partner_id': tt.project_id.partner_id.id,
                        'gest_id': tt.reviewer_id.id or False,
                        'employee_id': current.employee_id.id or False,
                        'current_emp': current.employee_id.id or False,
                        'uom_id': tt.uom_id.id,
                        'uom_id_r': tt.uom_id.id,
                        'ftp': tt.ftp,
                        'etape': tt.etape,
                        'zone': current.zone,
                        'secteur': current.secteur,
                        'zo': 'Zone ' + str(current.zone).zfill(1),
                        'sect': 'Secteur ' + str(current.secteur).zfill(2),
                        'categ_id': 6,
                        'state': 'affect',
                        'priority': tt.priority,
                        'sequence': sequence,
                        'active': True,
                        'display': True,
                        'gest_id3': tt.coordin_id.id,
                        'reviewer_id1': tt.reviewer_id1.id or False,
                        'coordin_id1': tt.coordin_id1.id or False,
                        'coordin_id2': tt.coordin_id2.id or False,
                        'coordin_id3': tt.coordin_id3.id or False,
                        'coordin_id4': tt.coordin_id4.id or False,
                    })
                else:
                    for hh in tt.kit_id.type_id.ids:
                        pr = self.env['product.product'].browse(hh)
                        self.env['project.task.work'].create({
                            'task_id': tt.id,
                            'product_id': pr.id,
                            'kit_id': tt.kit_id.id,
                            'name': tt.name,
                            'date_start': tt.date_start,
                            'date_end': tt.date_end,
                            'poteau_t': tt.qte,
                            'color': tt.color,
                            'total_t': tt.color * 7,  ##*work.employee_id.contract_id.wage
                            'project_id': tt.project_id.id,
                            'partner_id': tt.project_id.partner_id.id,
                            'gest_id': tt.reviewer_id.id or False,
                            'employee_id': current.employee_id.id or False,
                            'current_emp': current.employee_id.id or False,
                            'uom_id': tt.uom_id.id,
                            'uom_id_r': tt.uom_id.id,
                            'ftp': tt.ftp,
                            'etape': tt.etape,
                            'zone': current.zone,
                            'secteur': current.secteur,
                            'zo': 'Zone ' + str(current.zone).zfill(1),
                            'sect': 'Secteur ' + str(current.secteur).zfill(2),
                            'categ_id': 6,
                            'state': 'affect',
                            'priority': tt.priority,
                            'sequence': sequence,
                            'active': True,
                            'display': True,
                            'gest_id3': tt.coordin_id.id,
                            'reviewer_id1': tt.reviewer_id1.id or False,
                            'coordin_id1': tt.coordin_id1.id or False,
                            'coordin_id2': tt.coordin_id2.id or False,
                            'coordin_id3': tt.coordin_id3.id or False,
                            'coordin_id4': tt.coordin_id4.id or False,
                        })

        view = self.env['sh.message.wizard']

        view_id = view and view.id or False
        return {
            'name': 'Travaux de Permis générés avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }

    # def show_results(self):
    #
    #     """
    #     Action that shows the list of (non-draft) account moves from
    #     the selected journals and periods, so the user can review
    #     the renumbered account moves.
    #     """
    #     ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%project_id )
    #     ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article % s  !")%ids )
    #     current = self.browse(cr, uid, ids[0], context=context)
    #     if current.project_id:
    #         if not current.task_ids:
    #             raise osv.except_osv(_('Action impossible!'), _("Vous devez sélectionner les étapes concernées!"))
    #         if not current.line_ids:
    #             raise osv.except_osv(_('Action impossible!'), _("Vous devez Mentionner les Zones et Secteurs!"))
    #         l = []
    #         for tt in current.task_ids.ids:
    #             ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%tt )
    #             this_p = self.pool.get('project.task').browse(cr, uid, tt, context=context)
    #             l.append(this_p.name)
    #         cr.execute(
    #             'select id from project_task_work where project_id= %s and date_start>=%s and date_start <=%s and state in %s and etape in %s',
    #             (current.project_id.id, current.date_from, current.date_to, ('draft', 'affect'), tuple(l)))
    #         pp = cr.fetchall()
    #
    #         for kk in pp:
    #             if kk:
    #                 s2 = self.pool.get('project.task.work').browse(cr, uid, kk, context=context)
    #                 sequence_w = 0
    #                 for jj in current.line_ids:
    #
    #                     if jj.zone == 0 and jj.secteur > 0:
    #                         for hh in range(jj.secteur, jj.secteur_to + 1):
    #                             sequence_w = sequence_w + 1
    #                             if jj.employee_id:
    #                                 employee = jj.employee_id.id
    #                             else:
    #                                 employee = s2.employee_id.id or False
    #                             if jj.date_from:
    #                                 date_from = jj.date_from
    #                             else:
    #                                 date_from = s2.date_start
    #                             if jj.date_to:
    #                                 date_to = jj.date_to
    #                             else:
    #                                 date_to = s2.date_end
    #                             if jj.poteau_t:
    #                                 poteau_t = jj.poteau_t
    #                             else:
    #                                 poteau_t = s2.poteau_t
    #                             self.pool.get('base.group.merge.line').create(cr, uid, {
    #                                 'task_id': s2.task_id.id,
    #                                 'categ_id': s2.categ_id.id,
    #                                 'product_id': s2.product_id.id,
    #                                 'name': s2.name + ' - Secteur ' + str(hh),
    #                                 'date_start': date_from,
    #                                 'date_end': date_to,
    #                                 'poteau_i': s2.poteau_t,
    #                                 'poteau_t': poteau_t,
    #                                 'color': s2.color,
    #                                 'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                 'project_id': s2.project_id.id,
    #                                 'bon_id': current.id,
    #                                 'gest_id': s2.gest_id.id or False,
    #                                 'employee_id': employee,
    #                                 'uom_id': s2.uom_id.id,
    #                                 'uom_id_r': s2.uom_id.id,
    #                                 'ftp': s2.ftp,
    #                                 'state': s2.state,
    #                                 'work_id': s2.id,
    #                                 'sequence': s2.sequence + sequence_w,
    #                                 'zone': 0,
    #                                 'secteur': hh,
    #                                 'wiz_id': current.id
    #
    #                             }, context=context)
    #                     elif jj.zone > 0 and jj.secteur > 0:
    #                         for hh in range(jj.zone, jj.zone + 1):
    #                             for vv in range(jj.secteur, jj.secteur_to + 1):
    #                                 if jj.employee_id:
    #                                     employee = jj.employee_id.id
    #                                 else:
    #                                     employee = s2.employee_id.id or False
    #                                 if jj.date_from:
    #                                     date_from = jj.date_from
    #                                 else:
    #                                     date_from = s2.date_start
    #                                 if jj.date_to:
    #                                     date_to = jj.date_to
    #                                 else:
    #                                     date_to = s2.date_end
    #                                 if jj.poteau_t:
    #                                     poteau_t = jj.poteau_t
    #                                 else:
    #                                     poteau_t = s2.poteau_t
    #                                 sequence_w = sequence_w + 1
    #                                 self.pool.get('base.group.merge.line').create(cr, uid, {
    #                                     'task_id': s2.task_id.id,
    #                                     'categ_id': s2.categ_id.id,
    #                                     'product_id': s2.product_id.id,
    #                                     'name': s2.name + ' - Zone ' + str(hh) + ' - Secteur ' + str(vv),
    #                                     'date_start': date_from,
    #                                     'date_end': date_to,
    #                                     'poteau_i': s2.poteau_t,
    #                                     'poteau_t': poteau_t,
    #                                     'color': s2.color,
    #                                     'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                     'project_id': s2.project_id.id,
    #                                     'bon_id': current.id,
    #                                     'gest_id': s2.gest_id.id or False,
    #                                     'employee_id': employee,
    #                                     'uom_id': s2.uom_id.id,
    #                                     'uom_id_r': s2.uom_id.id,
    #                                     'ftp': s2.ftp,
    #                                     'state': s2.state,
    #                                     'work_id': s2.id,
    #                                     'zone': hh,
    #                                     'secteur': vv,
    #                                     'wiz_id': current.id,
    #                                     'sequence': s2.sequence + sequence_w
    #
    #                                 }, context=context)
    #                     elif jj.zone > 0 and jj.secteur == 0:
    #                         for hh in range(jj.zone, jj.zone + 1):
    #                             if jj.employee_id:
    #                                 employee = jj.employee_id.id
    #                             else:
    #                                 employee = s2.employee_id.id or False
    #                             if jj.date_from:
    #                                 date_from = jj.date_from
    #                             else:
    #                                 date_from = s2.date_start
    #                             if jj.date_to:
    #                                 date_to = jj.date_to
    #                             else:
    #                                 date_to = s2.date_end
    #                             if jj.poteau_t:
    #                                 poteau_t = jj.poteau_t
    #                             else:
    #                                 poteau_t = s2.poteau_t
    #                             sequence_w = sequence_w + 1
    #                             self.pool.get('base.group.merge.line').create(cr, uid, {
    #                                 'task_id': s2.task_id.id,
    #                                 'categ_id': s2.categ_id.id,
    #                                 'product_id': s2.product_id.id,
    #                                 'name': s2.name + ' - Zone ' + str(hh),
    #                                 'date_start': date_from,
    #                                 'date_end': date_to,
    #                                 'poteau_i': s2.poteau_t,
    #                                 'poteau_t': poteau_t,
    #                                 'color': s2.color,
    #                                 'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                 'project_id': s2.project_id.id,
    #                                 'bon_id': current.id,
    #                                 'gest_id': s2.gest_id.id or False,
    #                                 'employee_id': employee,
    #                                 'uom_id': s2.uom_id.id,
    #                                 'uom_id_r': s2.uom_id.id,
    #                                 'ftp': s2.ftp,
    #                                 'state': s2.state,
    #                                 'work_id': s2.id,
    #                                 'zone': hh,
    #                                 'secteur': 0,
    #                                 'wiz_id': current.id,
    #                                 'sequence': s2.sequence + sequence_w
    #
    #                             }, context=context)
    #
    #     return True
    #
    # def apply_(self, cr, uid, ids, context=None):
    #
    #     """
    #     Action that shows the list of (non-draft) account moves from
    #     the selected journals and periods, so the user can review
    #     the renumbered account moves.
    #     """
    #     ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%project_id )
    #     ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article % s  !")%ids )
    #     current = self.browse(cr, uid, ids[0], context=context)
    #     if current.project_id:
    #
    #         if not current.line_ids1:
    #             raise osv.except_osv(_('Action impossible!'), _("Aucune Ligne à Créer!"))
    #
    #         for s2 in current.line_ids1:
    #             if s2.employee_id:
    #                 cr.execute(
    #                     "INSERT INTO project_task_work (task_id,categ_id,product_id,name,uom_id,date_start,date_end," \
    #                     " poteau_i,poteau_t,color,hours,total_t,project_id,gest_id,employee_id,uom_id_r,etape,state,zone,secteur,sequence,zo,sect,gest_id3,current_gest,current_sup,reviwer_id1,coordin_id1,coordin_id2,coordin_id3,coordin_id4,partner_id) VALUES" \
    #                     " ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    #                     % (s2.task_id.id, s2.categ_id.id, s2.product_id.id, s2.name, s2.uom_id.id,
    #                        s2.date_start, s2.date_end, s2.poteau_i, s2.poteau_t, int(s2.color), s2.hours, s2.total_t,
    #                        s2.project_id.id, s2.gest_id.id,
    #                        s2.employee_id.id, s2.uom_id.id, s2.etape, 'affect', s2.zone, s2.secteur, s2.sequence,
    #                        'Zone ' + s2.zo, 'Secteur ' + s2.sect, s2.task_id.coordin_id.id or False,
    #                        s2.task_id.coordin_id.id or False, s2.gest_id.id or False,
    #                        s2.task_id.reviwer_id1.id or False, s2.task_id.coordin_id1.id or False,
    #                        s2.task_id.coordin_id2.id or False, s2.task_id.coordin_id3.id or False,
    #                        s2.task_id.coordin_id4.id or False, s2.project_id.partner_id.id or False))
    #             else:
    #                 cr.execute(
    #                     "INSERT INTO project_task_work (task_id,categ_id,product_id,name,uom_id,date_start,date_end," \
    #                     " poteau_i,poteau_t,color,hours,total_t,project_id,gest_id,uom_id_r,etape,state,zone,secteur,sequence,zo,sect,gest_id3,current_gest,current_sup,reviwer_id1,coordin_id1,coordin_id2,coordin_id3,coordin_id4,partner_id) VALUES" \
    #                     " ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    #                     % (s2.task_id.id, s2.categ_id.id, s2.product_id.id, s2.name, s2.uom_id.id,
    #                        s2.date_start, s2.date_end, s2.poteau_i, s2.poteau_t, int(s2.color), s2.hours, s2.total_t,
    #                        s2.project_id.id, s2.gest_id.id,
    #                        s2.uom_id.id, s2.etape, 'draft', s2.zone, s2.secteur, s2.sequence, 'Zone ' + s2.zo,
    #                        'Secteur ' + s2.sect, s2.task_id.coordin_id.id or False, s2.task_id.coordin_id.id or False,
    #                        s2.gest_id.id or False, s2.task_id.reviwer_id1.id or False,
    #                        s2.task_id.coordin_id1.id or False, s2.task_id.coordin_id2.id or False,
    #                        s2.task_id.coordin_id3.id or False, s2.task_id.coordin_id4.id or False,
    #                        s2.project_id.partner_id.id or False))
    #     ##               else:
    #     ##                self.pool.get('project.task.work').create(cr, uid, {
    #     ##                                'task_id': s2.task_id.id,
    #     ##                                'categ_id': s2.categ_id.id,
    #     ##                                'product_id': s2.product_id.id,
    #     ##                                'name': s2.name,
    #     ##                                'date_start': s2.date_start,
    #     ##                                'date_end': s2.date_end,
    #     ##                                'poteau_i': s2.poteau_i,
    #     ##                                'poteau_t': s2.poteau_t,
    #     ##                                'color': s2.color,
    #     ##                                'hours': s2.hours,
    #     ##                                'total_t':s2.total_t ,  ##*work.employee_id.contract_id.wage
    #     ##                                'project_id': s2.project_id.id,
    #     ##
    #     ##                                'gest_id': s2.gest_id.id or False,
    #     ##                                'employee_id': s2.employee_id.id or False,
    #     ##                                'uom_id': s2.uom_id.id,
    #     ##                                'uom_id_r': s2.uom_id.id,
    #     ##
    #     ##                                'etape': s2.etape,
    #     ##                                'state': 'draft',
    #     ##
    #     ##                                'zone': s2.zone,
    #     ##                                'secteur': s2.secteur,
    #     ##                                'sequence': s2.sequence,
    #     ##
    #     ##                            }, context=context)
    #
    #     self.write(cr, uid, current.id, {'state': 'open'}, context=context)
    #     view = self.pool.get('sh_message.sh_message_wizard')
    #
    #     view_id = view and view.id or False
    #     ##        context = dict(self._context or {})
    #     ##context['message'] = context['custom_value']
    #     return {
    #         'name': 'Travaux générés avec Succès',
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'sh.message.wizard',
    #         'views': [(view_id, 'form')],
    #         'view_id': view_id,
    #         'target': 'new',
    #         'context': context
    #     }
    #
    # @api.one
    # def action_copy3(self):
    #     packaging_obj = self.pool.get('project.task')
    #     packaging_copy = packaging_obj.copy_data(self._cr, self._uid, self.dst_task_id.id)
    #     packaging_obj.write({'name': 'dfsdf'})
    #     return True
    #     ### packaging_copy.write({'product_id':self.product_id})
