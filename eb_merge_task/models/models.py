# -*- coding: utf-8 -*-
from datetime import date, timedelta
from multiprocessing import connection

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools.safe_eval import time, datetime


class MergeTasksLine(models.Model):
    _name = 'base.task.merge.line'
    _description = 'base_task_merge_line'

    min_id = fields.Integer(string='MinID', order='min_id asc')
    aggr_ids = fields.Char('Ids')
    zone = fields.Integer(string="Zone")
    zo = fields.Char(string="Zone")
    secteur = fields.Integer(string="Secteur")
    secteur_to = fields.Integer(string="Secteur")
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    poteau_t = fields.Float('Time Spent')
    is_display = fields.Boolean(string='Ids')
    plans = fields.Char(string='Ids')
    from_int = fields.Integer(string='MinID')
    to_int = fields.Integer(string='MinID')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    wizard_id = fields.Many2one('base.task.merge.automatic.wizard', string='Wizard')


class EbMergeTasks(models.Model):
    _name = 'base.task.merge.automatic.wizard'
    _description = 'Merge Tasks'
    _rec_name = 'name'

    def show_results(self):
        self.ensure_one()

        current = self
        self.env['base.group.merge.line2'].sudo().search([('wiz_id', '=', current.id)]).unlink()

        res_cpt = []
        if current.project_id:
            if current.type == '1':
                if not current.task_ids:
                    raise UserError(_("Action impossible! Vous devez sélectionner les étapes/kits concernées!"))
                if not current.line_ids:
                    raise UserError(_("Action impossible! Vous devez Mentionner les Zones et Secteurs!"))

                task_ids = current.task_ids.ids
                kit_ids = [task.kit_id.id for task in current.task_ids if task.kit_id]
                non_kit_task_names = [task.name for task in current.task_ids if not task.kit_id]

                if kit_ids:
                    tasks = self.env['project.task.work'].sudo().search([
                        ('project_id', '=', current.project_id.id),
                        ('state', 'in', ('draft', 'affect')),
                        ('kit_id', 'in', kit_ids),
                        ('active', '=', True),
                        ('is_copy', '=', False)
                    ])
                else:
                    tasks = self.env['project.task.work'].sudo().search([
                        ('project_id', '=', current.project_id.id),
                        ('state', 'in', ('draft', 'affect')),
                        ('etape', 'in', non_kit_task_names)
                    ])

                res_cpt = tasks.ids

            elif current.type == '2':
                if not current.task_ids:
                    raise UserError(_("Action impossible! Vous devez sélectionner les étapes/kits concernées!"))
                if not current.line_ids:
                    raise UserError(_("Action impossible! Vous devez Mentionner les Zones et Secteurs!"))

                task_ids = current.task_ids.ids
                kit_ids = [task.kit_id.id for task in current.task_ids if task.kit_id]
                non_kit_task_names = [task.name for task in current.task_ids if not task.kit_id]

                if kit_ids:
                    tasks = self.env['project.task.work'].sudo().search([
                        ('project_id', '=', current.project_id.id),
                        ('kit_id', 'in', kit_ids),
                        ('active', '=', True),
                        ('zone', '=', current.zone),
                        ('secteur', '=', current.secteur)
                    ])
                else:
                    tasks = self.env['project.task.work'].sudo().search([
                        ('project_id', '=', current.project_id.id),
                        ('active', '=', True),
                        ('zone', '=', current.zone),
                        ('secteur', '=', current.secteur),
                        ('etape', 'in', non_kit_task_names)
                    ])

                res_cpt = tasks.ids

        for task_work_id in res_cpt:
            task_work = self.env['project.task.work'].sudo().browse(task_work_id)
            sequence_w = 0
            if task_work.task_id:
                sequence_w = task_work.task_id.sequence

            for line in current.line_ids:
                if line.secteur > line.secteur_to:
                    raise UserError(
                        _("Action impossible! Le secteur de départ doit être plus petit que le secteur de fin!"))

                if line.zone == 0 and line.secteur > 0:
                    for secteur in range(line.secteur, line.secteur_to + 1):
                        employee_id = line.employee_id and line.employee_id.id or False
                        new_group_line = self.env['base.group.merge.line2'].sudo().create({
                            'wiz_id': current.id,
                            'project_id': current.project_id.id,
                            'kit_id': task_work.kit_id.id,
                            'task_id': task_work.task_id.id,
                            'employee_id': employee_id,
                            'zone': line.zone,
                            'secteur': secteur,
                            'is_copy': False,
                            'sequence_w': sequence_w,
                        })
                elif line.zone > 0 and line.secteur > 0:
                    employee_id = line.employee_id and line.employee_id.id or False
                    new_group_line = self.env['base.group.merge.line2'].sudo().create({
                        'wiz_id': current.id,
                        'project_id': current.project_id.id,
                        'kit_id': task_work.kit_id.id,
                        'task_id': task_work.task_id.id,
                        'employee_id': employee_id,
                        'zone': line.zone,
                        'secteur': line.secteur,
                        'is_copy': False,
                        'sequence_w': sequence_w,
                    })

        return True

    def button_import2(self):
        current = self
        work_ = self.env['project.task.work']
        task_ = self.env['project.task']
        task_line_show_line2 = self.env['task_line.show.line2']

        task_line_show_line2.search([('wizard_id', '=', current.id)]).unlink()

        list1 = []
        for task in current.task_ids:
            tt = work_.search([('project_id', '=', task.project_id.id), ('etape', 'ilike', task.product_id.name),
                               ('is_copy', '=', False)], order='sequence asc')
            for ss in tt:
                ki = work_.browse(ss)
                if ki.task_id.id not in list1:
                    list1.append(ki.id)

        for ji in list1:
            kk = work_.browse(ji)
            task_line_show_line2.create({
                'product_id': kk.product_id.id,
                'gest_id': kk.gest_id.id,
                'state': 'draft',
                'color': kk.color,
                'task_id': kk.task_id.id,
                'categ_id': kk.categ_id.id,
                'etape': kk.etape,
                'date_start_r': kk.date_start_r,
                'date_end_r': kk.date_end_r,
                'date_start': kk.date_start,
                'date_end': kk.date_end,
                'poteau_t': kk.poteau_t,
                'sequence': kk.sequence,
                'work_id': kk.id,
                'project_id': kk.project_id.id,
                'uom_id': kk.uom_id.id,
                'uom_id_r': kk.uom_id.id,
                'wizard_id': current.id,
            })

        return True

    def apply_(self):
        current = self[0]

        if current.project_id:
            if not current.line_ids1:
                raise UserError(_("Action impossible! Aucune Ligne à Créer!"))

            for s2 in current.line_ids1:
                if current.exist:
                    found = self.env['project.task.work'].search([
                        ('project_id', '=', current.project_id.id),
                        ('zone', '=', s2.zone),
                        ('secteur', '=', s2.secteur)
                    ])

                seq = s2.sequence + 1
                kk = self.env['project.task.work'].search([
                    ('project_id', '=', current.project_id.id),
                    ('sequence', '=', seq)
                ])
                res_user = self.env['res.users'].browse(self._uid)

                while kk:
                    seq += 1
                    kk = self.env['project.task.work'].search([
                        ('project_id', '=', current.project_id.id),
                        ('sequence', '=', seq)
                    ])

                if s2.task_id.kit_id:
                    self.env.cr.execute("""
                        INSERT INTO project_task_work (kit_id, task_id, categ_id, product_id, name, uom_id, date_start, date_end,
                        poteau_i, poteau_t, color, hours, total_t, project_id, gest_id, uom_id_r, etape, state, zone, secteur, sequence, active,
                        w_id, display, zo, sect, gest_id3, current_gest, current_sup, reviewer_id1, coordin_id1, coordin_id2, coordin_id3,
                        coordin_id4, coordin_id5, coordin_id6, coordin_id7, coordin_id8, coordin_id9, coordin_id10, partner_id, work_orig)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        s2.task_id.kit_id.id, s2.task_id.id, s2.categ_id.id, s2.product_id.id,
                        s2.name.replace("'", "''"),
                        s2.uom_id.id, s2.date_start, s2.date_end, s2.poteau_i, s2.poteau_t, int(s2.color), s2.hours,
                        s2.total_t,
                        s2.project_id.id, s2.gest_id.id, s2.uom_id.id, s2.etape, 'draft', s2.zone, s2.secteur, seq,
                        True,
                        current.id, s2.is_display, 'Zone ' + s2.zo, 'Secteur ' + str(s2.secteur).zfill(2),
                        int(s2.task_id.coordin_id.id), int(s2.task_id.coordin_id.id), int(s2.gest_id.id),
                        int(s2.task_id.reviewer_id1.id), int(s2.task_id.coordin_id1.id), int(s2.task_id.coordin_id2.id),
                        int(s2.task_id.coordin_id3.id), int(s2.task_id.coordin_id4.id), int(s2.task_id.coordin_id5.id),
                        int(s2.task_id.coordin_id6.id), int(s2.task_id.coordin_id7.id), int(s2.task_id.coordin_id8.id),
                        int(s2.task_id.coordin_id9.id), int(s2.task_id.coordin_id10.id),
                        int(s2.project_id.partner_id.id),
                        int(s2.id)
                    ))
                else:
                    for s3 in current.work_ids:
                        self.env.cr.execute("""
                            INSERT INTO project_task_work (task_id, categ_id, product_id, name, uom_id, date_start, date_end,
                            poteau_i, poteau_t, color, hours, total_t, project_id, gest_id, uom_id_r, etape, state, zone, secteur, sequence,
                            active, w_id, display, zo, sect, gest_id3, current_gest, current_sup, reviewer_id1, coordin_id1, coordin_id2,
                            coordin_id3, coordin_id4, coordin_id5, coordin_id6, coordin_id7, coordin_id8, coordin_id9, coordin_id10,
                            partner_id, work_orig)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            s2.task_id.id, s2.categ_id.id, s2.product_id.id, s2.name.replace("'", "''"), s2.uom_id.id,
                            s2.date_start, s2.date_end, s2.poteau_i, s2.poteau_t, int(s2.color), s2.hours, s2.total_t,
                            s2.project_id.id, s2.gest_id.id, s2.uom_id.id, s2.etape, 'draft', s2.zone, s2.secteur, seq,
                            True,
                            current.id, s2.is_display, 'Zone ' + s2.zo, 'Secteur ' + str(s2.secteur).zfill(2),
                            int(s2.task_id.coordin_id.id), int(s2.task_id.coordin_id.id), int(s2.gest_id.id),
                            int(s2.task_id.reviewer_id1.id), int(s2.task_id.coordin_id1.id),
                            int(s2.task_id.coordin_id2.id),
                            int(s2.task_id.coordin_id3.id), int(s2.task_id.coordin_id4.id),
                            int(s2.task_id.coordin_id5.id),
                            int(s2.task_id.coordin_id6.id), int(s2.task_id.coordin_id7.id),
                            int(s2.task_id.coordin_id8.id),
                            int(s2.task_id.coordin_id9.id), int(s2.task_id.coordin_id10.id),
                            int(s2.project_id.partner_id.id),
                            int(s2.id)
                        ))

                        self.env.cr.execute("""
                            SELECT id FROM project_task_work WHERE project_id=%s AND task_id=%s AND zone=%s AND secteur=%s
                        """, (s2.project_id.id, s2.task_id.id, s2.zone, s2.secteur))
                        sql_result = self.env.cr.fetchone()
                        sql_work = self.env['work.histo'].search([('work_id', '=', s3.id)])
                        if sql_work:
                            histo = self.env['work.histo'].create({
                                'task_id': s2.task_id.id,
                                'work_id': sql_result,
                                'categ_id': s2.categ_id.id,
                                'product_id': s2.product_id.id,
                                'name': s2.name,
                                'work_sup_id': sql_work[0],
                                'date': s2.date_start,
                                'create_a': datetime.now(),
                                'create_by': res_user.employee_id.name,
                                'zone': s2.zone,
                                'secteur': s2.secteur,
                                'project_id': s2.project_id.id,
                                'partner_id': s2.project_id.partner_id.id,
                            })
                        else:
                            histo = self.env['work.histo'].create({
                                'task_id': s2.task_id.id,
                                'work_id': sql_result,
                                'categ_id': s2.categ_id.id,
                                'product_id': s2.product_id.id,
                                'name': s2.name,
                                'date': s2.date_start,
                                'create_a': datetime.now(),
                                'create_by': res_user.employee_id.name,
                                'zone': s2.zone,
                                'secteur': s2.secteur,
                                'project_id': s2.project_id.id,
                                'partner_id': s2.project_id.partner_id.id,
                            })

                if len(current.work_ids) > 0:
                    for s3 in current.work_ids:
                        if current.type == '1':
                            s3.write({'active': False, 'w_id': current.id})
                        else:
                            if current.choix == '2':
                                s3.write({'active': False, 'w_id': current.id})
                            else:
                                s3.write({'w_id': current.id})
                else:
                    l = []
                    v = []
                    res_cpt = []
                    for tt in current.task_ids.ids:
                        this_p = self.env['project.task'].browse(tt)
                        if this_p.kit_id:
                            v.append(this_p.kit_id.id)

                    if len(v) > 0:
                        tasks = self.env['project.task'].search([
                            ('project_id', '=', current.project_id.id),
                            ('state', 'in', ['draft', 'affect']),
                            ('kit_id', 'in', v),
                            ('active', '=', True),
                            ('is_copy', '=', False)
                        ])
                        ll1 = tasks.ids

                        for nn in ll1:
                            wrk = self.env['project.task.work'].browse(nn)
                            res_cpt.append(wrk.id)

                        for kk in res_cpt:
                            if current.type == '1':
                                self.env['project.task.work'].browse(kk).write({'active': False, 'w_id': current.id})
                            else:
                                if current.choix == '2':
                                    self.env['project.task.work'].browse(kk).write(
                                        {'active': False, 'w_id': current.id})
                                else:
                                    self.env['project.task.work'].browse(kk).write({'w_id': current.id})

                    current.write({'state': 'open'})
                    view = self.env.ref('sh_message.sh_message_sh_message_wizard')
                    if self.env.cr.dbname == 'DEMO222':
                        found = self.env['project.task.work'].search([('w_id', '=', current.id)])
                        if found:
                            for jj in found:
                                s2 = jj

                                sq40 = (
                                           "INSERT INTO app_entity_26 (id,date_added,date_updated,created_by,parent_item_id,field_243,"
                                           "field_253,field_255,field_256,field_260,field_261,field_259,field_258,field_264,field_271,"
                                           "field_272,field_268,field_244,field_250,field_251,field_269,field_263,field_287,field_273,"
                                           "field_274) VALUES (%s,'%s','%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s',%s,'%s',"
                                           "%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s')") % (
                                           s2.id,
                                           int(datetime.strptime(s2.date_start or s2.create_date[:10],
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           int(datetime.strptime(s2.date_start or s2.create_date[:10],
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           1,
                                           s2.project_id.id,
                                           s2.name.encode('ascii', 'ignore').replace("'", "\\'"),
                                           s2.project_id.id,
                                           s2.sequence or '',
                                           str(s2.project_id.partner_id.id) or '',
                                           s2.product_id.name.encode('ascii', 'ignore').replace("'", "\\'") or '',
                                           s2.categ_id.name.encode('ascii', 'ignore').replace("'", "\\'") or '',
                                           str(s2.task_id.coordin_id.id) or '',
                                           str(s2.gest_id.id) or '',
                                           s2.poteau_t or 0,
                                           int(datetime.strptime(s2.date_start_r or '2000-01-01',
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           int(datetime.strptime(s2.date_end_r or '2000-01-01',
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           str(s2.task_id.id) or '',
                                           '72',
                                           int(datetime.strptime(s2.date_start or s2.create_date[:10],
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           int(datetime.strptime(s2.date_end or '2000-01-01',
                                                                 '%Y-%m-%d').timestamp()) or '',
                                           str(s2.employee_id.id if s2.employee_id else '') or '',
                                           str(s2.uom_id.id) or '',
                                           '',
                                           str(s2.zone) or '',
                                           str(s2.secteur) or '')

                                sq41 = (
                                           "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                           s2.id, 244, '72')
                                sq42 = (
                                           "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                           s2.id, 253, s2.project_id.id)
                                sq43 = (
                                           "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                           s2.id, 256, s2.project_id.partner_id.id)
                                sq44 = (
                                           "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                           s2.id, 268, s2.task_id.id)
                                if s2.gest_id:
                                    sq45 = (
                                               "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                               s2.id, 258, s2.gest_id.id)
                                    self.env.cr.execute(sq45)
                                if s2.task_id.coordin_id3:
                                    sq46 = (
                                               "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                               s2.id, 259, s2.task_id.coordin_id3.id)
                                    self.env.cr.execute(sq46)
                                if s2.employee_id:
                                    sq47 = (
                                               "INSERT INTO app_entity_26_values (items_id,fields_id,value) VALUES ('%s','%s','%s')") % (
                                               s2.id, 269, s2.employee_id.id)
                                    self.env.cr.execute(sq47)
                                self.env.cr.execute(sq40)
                                self.env.cr.execute(sq41)
                                self.env.cr.execute(sq42)
                                self.env.cr.execute(sq43)
                                self.env.cr.execute(sq44)
                                self.env.cr.commit()

                    view_id = view and view.id or False
                    return {
                        'name': 'Taches générées avec Succès',
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'sh.message.wizard',
                        'views': [(view_id, 'form')],
                        'view_id': view_id,
                        'target': 'new',
                        'context': self.env.context
                    }

    def cancel_(self):

        cursor = connection.cursor()

        current = self
        found = self.env['project.task.work'].search([('w_id', '=', current.id), ('employee_id', '!=', False)])
        if found:
            for tt in found:
                raise UserError(
                    _('Attention ! Une Affectation est faite avec cette configuration: Projet %s, Zone: %s, Secteur: %s, Intervenant: %s') % (
                        current.project_id.npc, tt.zone, tt.secteur, tt.employee_id.name))

        if self.env.cr.dbname == 'DEMO':
            found1 = self.env['project.task.work'].search([('w_id', '=', current.id), ('active', '=', True)])
            if found1:
                for jj in found1:
                    sql1 = ("delete from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql1, (jj,))
                    connection.commit()

            found2 = self.env['project.task.work'].search([('w_id', '=', current.id), ('active', '=', False)])

        connection.close()

        self.env.cr.execute("delete from project_task_work where w_id=%s and active is True", (current.id,))
        self.env.cr.execute("update project_task_work set active=True where w_id=%s", (current.id,))
        self.env.cr.execute("update project_task_work set w_id=NULL where w_id=%s", (current.id,))

        current.write({'state': 'draft'})

        view = self.env.ref('sh_message.sh_message_sh_message_wizard', raise_if_not_found=False)
        view_id = view.id if view else False

        return {
            'name': 'Annulation faite avec Succès',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'context': self.env.context
        }

    name = fields.Char()
    disponible = fields.Boolean(compute='_compute_disponible', string='Disponible')
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    exist = fields.Boolean(string='Ids', default=True)
    year_no = fields.Char(string='Priority', default=lambda self: str(time.strftime('%Y')))
    is_kit = fields.Boolean(string="Email")
    zone = fields.Integer(string='Zone')
    secteur = fields.Integer(string='Secteur')

    project_id = fields.Many2one('project.project', string='Wizard')
    partner_id = fields.Many2one('res.partner', string='wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    product_id = fields.Many2one('product.product', string='Wizard')
    task_ids = fields.Many2many('project.task', string='Tasks')
    work_ids = fields.Many2many('project.task.work', string='Tasks')
    user_id = fields.Many2one('res.users', string='Assigned to')
    dst_task_id = fields.Many2one('project.task', string='Destination Task')
    dst_project = fields.Many2one('project.project', string='Project')
    line_ids = fields.One2many('base.task.merge.line', 'wizard_id', string='Role Lines', copy=True)
    line_ids1 = fields.One2many('base.group.merge.line2', 'wiz_id', string='Role Lines', copy=True)
    line_ids2 = fields.One2many('task_line.show.line2', 'wizard_id', string='Role Lines', copy=True)

    choix = fields.Selection([
        ('1', 'Garder Les Taches Sources Actives'),
        ('2', 'Archiver les Taches Sources')

    ],

        string='Priority', select=True)

    type = fields.Selection([
        ('1', 'Nouvelle Subdivision'),
        ('2', 'Modification Subdivision Existante'),
        ('3', 'Ajouter Subdivision A Partir d"une Existante')
    ], string='Type', select=True)

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Validé')
    ], string='Priority', default='draft', select=True)

    week_no = fields.Selection([
        ('00', '00'),
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
        ('52', '52')
    ], string='Priority', select=True, default=lambda self: str(time.strftime('%W')))

    keep = fields.Selection([
        ('active', 'Actives'),
        ('inactive', 'Archivées'),
        ('both', 'Actives et Archivées')
    ], string='Keep', default='active')

    def default_get(self, fields_list):
        res = super(EbMergeTasks, self).default_get(fields_list)
        # J'ai mis à jour la signature de la méthode pour utiliser fields_list.
        # De plus, j'ai remplacé res['task_ids'] = active_ids par res.update({'task_ids': active_ids})
        # pour garantir le comportement correct en cas d'autres valeurs existantes dans le dictionnaire.
        active_ids = self.env.context.get('active_ids')
        # vérifie si le modèle actif (le modèle à partir duquel cette méthode est appelée) est égal à 'project.task' et s'il existe des active_ids dans le contexte.
        if self.env.context.get('active_model') == 'project.task' and active_ids:
            # Si les conditions sont satisfaites, elle met à jour le dictionnaire res en ajoutant la clé 'task_ids' avec la valeur des active_ids.
            # La méthode update est utilisée pour garantir que les autres valeurs du dictionnaire ne sont pas écrasées.
            res.update({'task_ids': active_ids})
        return res

        # Cette méthode utilise le décorateur @api.depends pour indiquer que le calcul du champ disponible doit dépendre de la valeur du champ project_id.user_id
        # Lorsque cette méthode est exécutée, elle itère sur chaque enregistrement (book) pour effectuer les opérations suivantes :
        # vérifie si l'ID de l'utilisateur associé au champ 'user_id' de l'enregistrement 'book.project_id' est égal à l'ID de l'utilisateur actuellement connecté (self.env.user.id).
        # Si les deux ID correspondent, cela signifie que l'utilisateur actuel est associé au projet correspondant à 'book.project_id'. Dans ce cas, le champ 'disponible' de 'book' est défini sur 'True'.
        # Si les deux ID ne correspondent pas, cela signifie que l'utilisateur actuel n'est pas associé au projet correspondant à 'book.project_id'. Dans ce cas, le champ 'disponible' de book est défini sur 'False'

    @api.depends('project_id.user_id')
    def _compute_disponible(self):
        for book in self:
            if book.project_id.user_id.id == self.env.user.id:
                book.disponible = True
            else:
                book.disponible = False

    def _compute_default_flow(self):
        result = {}
        for rec in self:
            work_ids = self.env['base.flow.merge.line'].search_count([('work_id', '=', rec.id)])
            if work_ids:
                result[rec.id] = 1
            else:
                result[rec.id] = 0

        return result

    def action_merge(self):
        names = []

        if self.dst_task_id:
            names.append(self.dst_task_id.name)
        else:
            raise UserError(_('You must select a Destination Task'))

        desc = []

        desc.append(self.dst_task_id.description)
        for record in self.task_ids:
            if record.id != self.dst_task_id.id:
                names.append(record.name)
                desc.append(record.description)

        for message in self.task_ids:
            for msg_id in message.message_ids:
                msg_id.res_id = self.dst_task_id.id

        plan_hours = self.dst_task_id.planned_hours
        for hour in self.task_ids:
            for time in hour.timesheet_ids:
                plan_hours += time.planned_hours

        self.dst_task_id.planned_hours = plan_hours

        transformed_names = ', '.join(names)
        self.dst_task_id.name = transformed_names

        transformed_desc = ', '.join(desc)
        self.dst_task_id.description = transformed_desc

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for task in self.task_ids:
            task.message_post(
                body=f"This task has been merged into: {base_url}/web#id={self.dst_task_id.id}&model=project.task")

        self.task_ids.active = False
        self.dst_task_id.active = True

        if self.user_id:
            self.dst_task_id.user_id = self.user_id
        elif self.dst_task_id.user_id:
            self.dst_task_id.user_id = self.dst_task_id.user_id
        else:
            raise UserError(
                _('There is no user assigned to the merged task, and the destination task does not have an assigned user!'))

        return True

    @api.onchange('year_no', 'week_no')
    def onchange_week_(self):

        # The result variable is no longer used since the method directly assigns values to the fields.
        if self.year_no and self.week_no:  # The method now uses the self parameter to access the field values.
            d = date(self.year_no, 1, 1)
            # The date object is created using date(self.year_no, 1, 1) instead of date(int(year_no), 1, 1).
            if d.weekday() <= 3:
                d = d - timedelta(d.weekday())
                # The timedelta class is imported separately with from datetime import timedelta.
            else:
                d = d + timedelta(7 - d.weekday())
            dlt = timedelta(days=(int(self.week_no) - 1) * 7)

            self.date_from = d + dlt
            self.date_to = d + dlt + timedelta(days=6)

    @api.onchange('project_id')
    def onchange_project_id(self):

        if self.project_id:
            self.task_ids = False
            self.work_ids = False

        return {'value': {}}

    @api.onchange('exist')
    def onchange_exist(self):
        if not self.exist:
            raise UserError(
                _("Attention!\nSi vous décocher cette option, le système ne vérifiera pas l'existence du Project-Zone-Secteur!"))

    @api.onchange('project_id', 'task_ids')
    def onchange_project_id(self):

        ltask1 = []
        ltask2 = []
        zz = []

        if self.project_id:
            tt = self.env['project.task'].search([('project_id', '=', self.project_id.id)], order='sequence asc')

            for task in tt:
                if self.project_id.is_kit and task.kit_id.id not in ltask1:
                    ltask1.append(task.kit_id.id)
                    ltask2.append(task.id)
                elif 'Etape' in task.product_id.name and task.product_id.name not in ltask1:
                    ltask1.append(task.product_id.name)
                    ltask2.append(task.id)

            zz = self.env['project.task'].search([('id', 'in', ltask2)], order='sequence asc').ids

        return {'domain': {'task_ids': [('id', 'in', zz)]}}

    @api.onchange('project_id', 'task_ids', 'zone', 'secteur', 'keep', 'type')
    def onchange_categ_id(self):

        list_ = []
        list1 = []
        list2 = []
        tt = []

        task_work = self.env['project.task.work']

        if self.type == '1':
            is_kit = False

            if self.task_ids:
                for kk in self.task_ids.ids:
                    task = self.env['project.task'].browse(kk)

                    if task.kit_id:
                        is_kit = True
                        for jj in task.work_ids.ids:
                            work = task_work.browse(jj)

                            if work.kit_id.id not in list1:
                                list1.append(work.kit_id.id)
                                list2.append(work.id)
                    else:
                        list_.append(task.product_id.name)

                if is_kit:
                    tt = self.env['project.task.work'].search([('id', 'in', list2)], order='sequence asc').ids
                else:
                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('zone', '=', 0),
                        ('secteur', '=', 0),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids
            else:
                if self.project_id:
                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('is_copy', '=', False),
                        ('kit_id', '=', False),
                        ('zone', '=', 0),
                        ('secteur', '=', 0),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids

                    if not tt:
                        for task in tt:
                            work = task_work.browse(task.id)

                            if work.kit_id:
                                if work.kit_id.id not in list1:
                                    list1.append(work.id)

                        tt = self.env['project.task.work'].search([('id', 'in', list1)], order='sequence asc').ids

        else:
            if self.keep == 'active':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('active', '=', True),
                        ('secteur', '=', self.secteur)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('active', '=', True),
                            ('secteur', '=', self.secteur)
                        ], order='sequence asc').ids

            elif self.keep == 'inactive':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('active', '=', False),
                        ('secteur', '=', self.secteur)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('active', '=', False),
                            ('secteur', '=', self.secteur)
                        ], order='sequence asc').ids

            elif self.keep == 'both':
                if self.task_ids:
                    for kk in self.task_ids.ids:
                        task = self.env['project.task'].browse(kk)
                        list_.append(task.product_id.name)

                    tt = self.env['project.task.work'].search([
                        ('project_id', '=', self.project_id.id),
                        ('etape', 'in', list_),
                        ('is_copy', '=', False),
                        ('secteur', '=', self.secteur),
                        '|', ('active', '=', True), ('active', '=', False)
                    ], order='sequence asc').ids
                else:
                    if self.project_id:
                        tt = self.env['project.task.work'].search([
                            ('project_id', '=', self.project_id.id),
                            ('is_copy', '=', False),
                            ('secteur', '=', self.secteur),
                            '|', ('active', '=', True), ('active', '=', False)
                        ], order='sequence asc').ids

        return {'domain': {'work_ids': [('id', 'in', tt)]}}

    def action_copy1(self):
        return super().copy()

    def action_copy(self, default=None):
        if default is None:
            default = {}

        for current in self:
            for tt in current.task_ids:
                packaging_obj = self.env['project.task']

                if current.zone == 0 and current.secteur == 0:
                    vals = {
                        'task_id': tt.id,
                        'product_id': tt.product_id.id,
                        'name': tt.name,
                        'date_start': tt.date_start,
                        'date_end': tt.date_end,
                        'poteau_t': tt.qte,
                        'color': tt.color,
                        'total_t': tt.color * 7,
                        'project_id': tt.project_id.id,
                        'gest_id': tt.reviewer_id.id or False,
                        'uom_id': tt.uom_id.id,
                        'uom_id_r': tt.uom_id.id,
                        'ftp': tt.ftp,
                        'zone': tt.zone,
                        'secteur': tt.secteur,
                        'state': 'draft',
                        'priority': tt.priority,
                    }
                    cte = packaging_obj.create(vals)

                elif current.zone > 0 and current.secteur == 0:
                    for cc in range(1, current.zone + 1):
                        vals = {
                            'task_id': tt.id,
                            'product_id': tt.product_id.id,
                            'name': tt.name + ' Zone ' + str(cc),
                            'date_start': tt.date_start,
                            'date_end': tt.date_end,
                            'poteau_t': tt.qte,
                            'color': tt.color,
                            'total_t': tt.color * 7,
                            'project_id': tt.project_id.id,
                            'gest_id': tt.reviewer_id.id or False,
                            'uom_id': tt.uom_id.id,
                            'uom_id_r': tt.uom_id.id,
                            'ftp': tt.ftp,
                            'zone': cc,
                            'secteur': 0,
                            'state': 'draft',
                            'priority': tt.priority,
                        }
                        cte = packaging_obj.create(vals)

                elif current.zone > 0 and current.secteur > 0:
                    for cc in range(1, current.zone + 1):
                        for cc1 in range(1, current.secteur + 1):
                            vals = {
                                'task_id': tt.id,
                                'product_id': tt.product_id.id,
                                'name': tt.name + ' Zone ' + str(cc) + ' Secteur ' + str(cc1),
                                'date_start': tt.date_start,
                                'date_end': tt.date_end,
                                'poteau_t': tt.qte,
                                'color': tt.color,
                                'total_t': tt.color * 7,
                                'project_id': tt.project_id.id,
                                'gest_id': tt.reviewer_id.id or False,
                                'uom_id': tt.uom_id.id,
                                'uom_id_r': tt.uom_id.id,
                                'ftp': tt.ftp,
                                'zone': cc,
                                'secteur': cc1,
                                'priority': tt.priority,
                                'state': 'draft',
                            }
                            cte = packaging_obj.create(vals)

        return cte

    def action_copy3(self):
        packaging_obj = self.env['project.task']
        packaging_copy = packaging_obj.copy(self.dst_task_id.id)
        packaging_copy.write({'name': 'dfsdf'})
        return True


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    w_id = fields.Many2one('base.task.merge.automatic.wizard', string='Company', readonly=True,
                           states={'draft': [('readonly', False)]}, )
