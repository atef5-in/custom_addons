# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime as dt, date
from odoo.exceptions import UserError
from odoo.tools.translate import _
import math


class TaskWork(models.Model):
    _name = 'project.task.work'
    _description = 'Project Task Work'
    _rec_name = 'id'

    work_id = fields.Char(string='work ID')
    work_id2 = fields.Char(string='work ID')

    def _default_done(self):

        for rec in self:
            if self.env.cr.dbname == 'TEST95':

                if rec.product_id.is_gantt is True:

                    sql = ("select field_250 from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql, (rec.id,))
                    datas = self.env.cr.fetchone()

                    if datas and datas[0] > 1:
                        ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
                        temp = dt.fromtimestamp(int(datas[0])).strftime('%Y-%m-%d')

                        self.env.cr.execute('update project_task_work set date_start=%s where id=%s', (temp, rec.id))
                        ##cr.execute('update project_task_work set  date_start=%s where  id = %s ' , (date_start,ids[0]))
                    sql1 = ("select field_251 from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql1, (rec.id,))
                    datas1 = self.env.cr.fetchone()

                    if datas1 and datas1[0] > 1:
                        ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
                        temp1 = dt.fromtimestamp(int(datas1[0])).strftime('%Y-%m-%d')
                        ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
                        self.env.cr.execute('update project_task_work set date_end=%s where id=%s', (temp1, rec.id))
                    sql2 = ("select field_269 from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql2, (rec.id,))
                    datas2 = self.env.cr.fetchone()

                    if datas2 and datas2[0] > 1:

                        ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
                        if datas2 != '':
                            temp2 = datas2[0]
                            ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
                            self.env.cr.execute('update project_task_work set employee_id=%s where id=%s',
                                                (temp2 or None, rec.id))

            if rec.line_ids:

                for kk in rec.line_ids.ids:
                    # do we keep browse here ?
                    rec_line = self.env['project.task.work.line']
                    if rec_line.done is True:
                        rec.done = 1
                        break
                    else:
                        rec.done = 0
            else:
                rec.done = 0

    def _default_done1(self):

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line']
                    if rec_line.done1 is True:
                        rec.done1 = 1
                        break
                    else:
                        rec.done1 = 0
            else:
                rec.done1 = 0

    def _default_done2(self):

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line']
                    if rec_line.group_id:
                        rec.done2 = 1
                        break

                    else:
                        rec.done2 = 0
            else:
                rec.done2 = 0

    def _default_done3(self):

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line']
                    if rec_line.group_id2:
                        rec.done3 = 1
                        break

                    else:
                        rec.done3 = 0
            else:
                rec.done3 = 0

    def _default_flow(self):

        for rec in self:
            self.env.cr.execute('select id from base_flow_merge_line where work_id= %s', (rec.id,))
            work_ids = self.env.cr.fetchone()
            if work_ids:
                rec.done4 = 1
            else:
                rec.done4 = 0

    def _check_color(self):

        for record in self:
            color = 0
            if record.statut in ('Soumise', 'A l''étude', 'Envoyé'):
                color = 9
            elif record.statut in (u'Approuvé Partiel', u'Approuvé'):
                color = 5
            elif record.statut in ('Refus Partiel', u'Refusé'):
                color = 2
            elif record.statut == u'Incomplet':
                color = 3
            elif record.statut in ('9032', u'Déviation', u'En résiliation'):
                color = 7
            elif record.statut in ('Encours', '', 'Sans valeur'):
                color = 6
            elif record.statut in ('Non requis', 'Annulé'):
                color = 1
            elif record.statut == u'Travaux Prép.':
                color = 8

            record.kanban_color = color

    def _get_planned(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.hours_r = hours.get(rec.id, 0.0)

    def _get_sum(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_r = hours.get(rec.id, 0.0)

    def _get_qty(self):
        result = {}
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.poteau_r = hours.get(rec.id, 0.0)

    def _get_qty_r_affect(self):

        for record in self:
            self.env.cr.execute(
                "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
                (record.task_id.id, str(record.zone), str(record.secteur)))
            q3 = self.env.cr.fetchone()
            if q3:
                record.poteau_ra = record.poteau_i - q3[0]
            else:
                record.poteau_ra = record.poteau_i

    def _get_qty_affect(self):

        for record in self:
            self.env.cr.execute(
                "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
                (record.task_id.id, str(record.zone), str(record.secteur)))
            q3 = self.env.cr.fetchone()
            if q3:
                record.poteau_da = q3[0]
            else:
                record.poteau_da = 0

    def _disponible(self):

        for book in self:
            if book.gest_id and book.gest_id.user_id:
                if book.gest_id.user_id.id == self.env.user.id or self.env.user.id == 1 or 100 in book.gest_id.user_id.groups_id.ids:
                    book.done33 = True
                else:
                    book.done33 = False
            else:
                book.done33 = False

    def _isinter(self):

        for book in self:
            book.is_intervenant = False  # to set to False.
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(kk)
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
                if tt:
                    for kk in tt:
                        self.env.cr.execute(
                            'update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
                            (tuple(kk)))
                    test = self.env['base.group.merge.automatic.wizard'].search([('id', 'in', tt), (
                        'state', '<>', 'draft')])
                    if test:
                        book.is_intervenant = True

    def _iscontrol(self):

        for book in self:
            book.is_control = False
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(kk)
                    if rec_line.group_id2:
                        if rec_line.group_id2.id not in tt:
                            tt.append(rec_line.group_id2.id)
                if tt:

                    test = self.env['base.group.merge.automatic.wizard'].search([('id', 'in', tt), (
                        'state1', '<>', 'draft')])

                    if test:
                        book.is_control = True

                    test1 = self.env['project.task.work.line'].search([('work_id2', '=', book.id or False)])
                    if test1:
                        for jj in test1:
                            rec_line = self.env['project.task.work.line'].browse(jj)
                            if rec_line.group_id2:
                                if rec_line.group_id2.id not in tt:
                                    tt.append(rec_line.group_id2.id)
                        book.is_control = True

    def _iscorr(self):

        for book in self:
            book.is_correction = False
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(kk)
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
                if tt:
                    for kk in tt:
                        self.env.cr.execute(
                            'update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
                            (tuple(kk)))
                    test = self.env['base.group.merge.automatic.wizard'].search([('id', 'in', tt), (
                        'state2', '<>', 'draft')])
                    if test:
                        book.is_correction = True
                    test1 = self.env['project.task.work.line'].search([('work_id2', '=', book.id or False)])
                    if test1:
                        for jj in test1:
                            rec_line = self.env['project.task.work.line'].browse(jj)
                            if rec_line.group_id2:
                                if rec_line.group_id2.id not in tt:
                                    tt.append(rec_line.group_id2.id)
                        book.is_correction = True

    def _get_progress(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.hours > 0:
                ratio = hours.get(rec.id, 0.0) / rec.hours
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_me = round(min(100.0 * ratio, 100), 2)

    def _get_progress_qty(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.poteau_t > 0:
                ratio = hours.get(rec.id, 0.0) / rec.poteau_t
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_qty = round(min(100.0 * ratio, 100), 2)

    def _get_progress_amount(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.total_t > 0:
                ratio = hours.get(rec.id, 0.0) / rec.total_t
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_amount = round(min(100.0 * ratio, 100), 2)

    def _get_risk(self):

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(self.ids),))
        amount = dict(self.env.cr.fetchall())
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        ratio = 'N.D'
        for rec in self:
            if rec.hours > 0 and rec.poteau_t > 0:
                if ((hours.get(rec.id, 0.0) / rec.hours) - (amount.get(rec.id, 0.0) / rec.poteau_t)) * 100 > 50:
                    ratio = 'Très Critique'
                elif ((hours.get(rec.id, 0.0) / rec.hours) - (amount.get(rec.id, 0.0) / rec.poteau_t)) * 100 > 30:
                    ratio = 'Critique'
                elif ((hours.get(rec.id, 0.0) / rec.hours) - (amount.get(rec.id, 0.0) / rec.poteau_t)) * 100 > 10:
                    ratio = 'Retard'
                elif ((hours.get(rec.id, 0.0) / rec.hours) - (amount.get(rec.id, 0.0) / rec.poteau_t)) * 100 > -10:
                    ratio = 'Normal'
                elif ((hours.get(rec.id, 0.0) / rec.hours) - (amount.get(rec.id, 0.0) / rec.poteau_t)) * 100 > -30:
                    ratio = 'En Avance'
                else:
                    ratio = 'Très en Avance'

            rec.risk = ratio

    name = fields.Char(string='Libellé Travaux', readonly=True, states={'draft': [('readonly', False)]}, )
    ftp = fields.Char(string='Lien FTP', readonly=True, states={'draft': [('readonly', False)]}, )
    job = fields.Char(string='Job', readonly=True, states={'draft': [('readonly', False)]}, )
    date = fields.Datetime('Date Doc', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    date_r = fields.Datetime(string='date', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    date_p = fields.Date(string='date', index="1")
    date_start = fields.Date(string='Date Début', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    date_end = fields.Date(string='Date Fin', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    date_start_r = fields.Date(string='Date Début Réelle', index="1", readonly=True,
                               states={'affect': [('readonly', False)]}, )
    date_end_r = fields.Date(string='Date Fin Réelle', index="1", readonly=True,
                             states={'draft': [('readonly', False)]}, )
    ex_state = fields.Char(string='ex')
    project_id = fields.Many2one('project.project', string='Projet', ondelete='set null', select=True, readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    task_id = fields.Many2one('project.task', string='Tache', ondelete='cascade', select="1", readonly=True,
                              states={'draft': [('readonly', False)]}, )
    product_id = fields.Many2one('product.product', string='T. de Service', ondelete='cascade', select="1",
                                 readonly=True, states={'draft': [('readonly', False)]}, )
    hours = fields.Float(string='Total Hrs Prévues', readonly=True, states={'draft': [('readonly', False)]}, )
    etape = fields.Char(string='Etape', readonly=True, states={'draft': [('readonly', False)]}, )
    categ_id = fields.Many2one('product.category', string='Département', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    hours_r = fields.Float(compute='_get_planned', string='Total Hrs Réalisées', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Clients', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    kit_id = fields.Many2one('product.kit', string='Nom Kit', ondelete='cascade', select="1",
                             readonly=True, states={'draft': [('readonly', False)]}, )
    total_t = fields.Float(string='Total à Facturer T', readonly=True, states={'draft': [('readonly', False)]}, )
    total_r = fields.Float(compute='_get_sum', string='Total à Facturer R', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    poteau_t = fields.Float(string='Qté demamdée', readonly=True, states={'draft': [('readonly', False)]}, )
    poteau_i = fields.Float(string='Qté T. Prévue', readonly=True, states={'draft': [('readonly', False)]}, )
    poteau_r = fields.Float(compute='_get_qty', string='Qté/Unité Réalisée', readonly=True,
                            states={'draft': [('readonly', False)]}, )
    poteau_da = fields.Float(compute='_get_qty_affect', string='Qté Déja Affect.', readonly=True,
                             states={'draft': [('readonly', False)]}, )
    poteau_ra = fields.Float(compute='_get_qty_r_affect', string='Qté N.Affecté', readonly=True,
                             states={'draft': [('readonly', False)]}, )
    poteau_reste = fields.Integer(string='N.U', readonly=True, states={'draft': [('readonly', False)]}, )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'), ],
        string='N.U', copy=False, readonly=True, states={'draft': [('readonly', False)]}, )
    sequence = fields.Integer(string='Séq', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    state_id = fields.Many2one('res.country.state', string='Municipalités')
    city = fields.Char(string='Région', readonly=True)
    state_id1 = fields.Many2one('res.country.state', string='state ID')
    state_id2 = fields.Many2one('res.country.state', string='state 2 ID ')
    precision = fields.Char(string='Precision(P)')
    permis = fields.Char(string='Permis(P)')
    date_fin = fields.Date(string='Date Fin (P)')
    prolong = fields.Char(string='Prolongation demandée(P)')
    remarque = fields.Text(string='Remarque')
    date_remis = fields.Date(string='Date Remis(P)')
    date_construt = fields.Date(string='Date Constrution(P)')
    secteur_en = fields.Char(string='Secteur Enfui(P)')
    graphe_t_b = fields.Char(string='Graphe_t_b(P)')
    dct = fields.Char(string='Dct(P)')
    active = fields.Boolean(string='Active')
    anomalie = fields.Char(string='Anomalie(P)')
    action = fields.Char(string='Action(P)')
    pourc_t = fields.Float(string='% Avancement', readonly=True, states={'draft': [('readonly', False)]}, )
    pourc_f = fields.Float(string='% Dépense', readonly=True, states={'draft': [('readonly', False)]}, )
    statut1 = fields.Many2one('project.status', string='Status', select=True)
    statut = fields.Selection([('Encours', 'Encours'),
                               ('Soumise', 'Soumise'),
                               ('A l"Etude', 'A l"étude'),
                               ('Approuve', 'Approuvé'),
                               ('Incomplet', 'Incomplet'),
                               ('En Construction', 'En Construction'),
                               ('Envoye', 'Envoyé'),
                               ('Travaux Pre.', 'Travaux Pré.'),
                               ('Refuse', 'Refusé'),
                               ('Refus Partiel', 'Refus Partiel'),
                               ('Approuve Partiel', 'Approuvé Partiel'),
                               ('Travaux Complété', 'Travaux Complété'),
                               ('Inspection', 'Inspection'),
                               ('Annule', 'Annulé'),
                               ('En Resiliation', 'En Résiliation'),
                               ('Non Requis', 'Non Requis'),
                               ('En TP-derogation approuvee', 'En TP-dérogation approuvée'),
                               ('TP completes-avec refus', 'TP complétés-avec refus'),
                               ('Deviation', 'Déviation'),
                               ('9032', 'Approbation demandeur'),
                               ('DA', 'Approbation demandeur – Dérogation Approuvé'),
                               ('DP', 'Approbation demandeur – Dérogation Partielle'),
                               ('DR', 'Approbation demandeur – Dérogation Refusé'),
                               ('AD', 'Approbation demandeur – ADR Défavorable'),
                               ('TPDP', 'En TP - Dérogation Partielle'),
                               ('TPSD', 'En TP - Sans Dérogation'),
                               ],
                              string='Status', copy=False)
    kanban_color = fields.Integer(compute='_check_color', string='Couleur')
    zone = fields.Integer(string='Zone', readonly=True, states={'draft': [('readonly', False)]}, )
    secteur = fields.Integer(string='Secteur', readonly=True, states={'draft': [('readonly', False)]}, )
    zo = fields.Char(string='Zone', readonly=True, states={'draft': [('readonly', False)]}, )
    sect = fields.Char(string='Secteur', readonly=True, states={'draft': [('readonly', False)]}, )
    user_id = fields.Many2one('res.users', string='user ID', select="1", readonly=True,
                              states={'draft': [('readonly', False)]}, )
    paylist_id = fields.Many2one('hr.payslip', string='playlist ID', select="1", readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    reviewer_id1 = fields.Many2one('hr.employee', string='Superviseur', readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    gest_id = fields.Many2one('hr.employee', string='Coordinateur', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    gest_id2 = fields.Many2one('hr.employee', string='Coordinateur 2', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    gest_id3 = fields.Many2one('hr.employee', string='Coordinateur 3', copy=True, readonly=True,
                               states={'draft': [('readonly', False)]}, )
    coordin_id1 = fields.Many2one('hr.employee', string='Coordinateur 1', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id2 = fields.Many2one('hr.employee', string='Coordinateur 2', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id3 = fields.Many2one('hr.employee', string='Coordinateur 3', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id4 = fields.Many2one('hr.employee', string='Coordinateur 4', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id5 = fields.Many2one('hr.employee', string='Coordinateur 5', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id6 = fields.Many2one('hr.employee', string='Coordinateur 6', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id7 = fields.Many2one('hr.employee', string='Coordinateur 7', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id8 = fields.Many2one('hr.employee', string='Coordinateur 8', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id9 = fields.Many2one('hr.employee', string='Coordinateur 9', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    coordin_id10 = fields.Many2one('hr.employee', string='Coordinateur 10', readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    employee_id = fields.Many2one('hr.employee', 'Employé', readonly=True, states={'draft': [('readonly', False)]}, )
    issue_id = fields.Many2one('project.issue', 'Issue ID', select="1", readonly=True,
                               states={'draft': [('readonly', False)]}, )
    dependency_task_ids = fields.Many2many('project.task.work', 'project_task_dependency_work_rel',
                                           'dependency_work_id', 'work_id', string='Dependencies')
    state = fields.Selection([('draft', 'T. Planifiés'),
                              ('affect', 'T. Affectés'),
                              ('affect_con', 'T. Affectés controle'),
                              ('affect_corr', 'T. Affectés corrction'),
                              ('tovalid', 'Ret. En cours'),
                              ('tovalidcont', 'Cont. En cours'),
                              ('validcont', 'Cont. Valides'),
                              ('tovalidcorrec', 'Corr. En cours'),
                              ('validcorrec', 'Corr. Valides'),
                              ('valid', 'T. Terminés'),
                              ('cancel', 'T. Annulés'),
                              ('pending', 'T. Suspendus'),
                              ],
                             string='Status', copy=False)
    p_done = fields.Float(string='Qté Réalisée', readonly=True, states={'draft': [('readonly', False)]}, )
    note = fields.Text(string='N.U')
    done = fields.Boolean(compute='_default_done', string='Company Currency', readonly=True,
                          states={'draft': [('readonly', False)]}, )
    done1 = fields.Boolean(compute='_default_done1', string='Company Currency', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    done2 = fields.Boolean(compute='_default_done2', string='Company Currency', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    done3 = fields.Boolean(compute='_default_done3', string='Company Currency', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    done4 = fields.Boolean(compute='_default_flow', string='Company Currency', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    color = fields.Integer(string='Nbdays', readonly=True, states={'draft': [('readonly', False)]}, )
    color1 = fields.Integer(string='Durée(Jours)', readonly=True, states={'affect': [('readonly', False)]}, )
    uom_id = fields.Many2one('product.uom', string='Unité Prévue', required=False, readonly=True,
                             states={'draft': [('readonly', False)]}, )
    uom_id_r = fields.Many2one('product.uom', string='Unité Réelle', readonly=True,
                               states={'affect': [('readonly', False)]}, )
    pourc = fields.Float('Pour C', readonly=True, states={'draft': [('readonly', False)]}, )
    rank = fields.Char('Rank', readonly=True, states={'draft': [('readonly', False)]}, )
    display = fields.Boolean(string='Réalisable')
    is_copy = fields.Boolean(string='Dupliqué')
    done33 = fields.Boolean(compute='_disponible', string='done')
    current_emp = fields.Many2one('hr.employee', string='Employé Encours', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    current_gest = fields.Many2one('hr.employee', string='Coordinateur En cours', readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    current_sup = fields.Many2one('hr.employee', string='Superviseur En cours', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    prior1 = fields.Float(string='Prior1', readonly=True, states={'draft': [('readonly', False)]}, )
    prior2 = fields.Float(string='Prior2', readonly=True, states={'draft': [('readonly', False)]}, )
    cmnt = fields.Char(string='Prior2', readonly=True, states={'draft': [('readonly', False)]}, )
    work_orig = fields.Integer(string='tache original')
    affect_emp_list = fields.Char(string='employée id')
    affect_e_l = fields.Char(string='employée id')
    affect_emp = fields.Char(string='employée')
    affect_con = fields.Char(string='controle')
    affect_cor = fields.Char(string='corrdinateur')
    affect_con_list = fields.Char(string='controle id')
    affect_cor_list = fields.Char(string='corrdinateur id')
    is_intervenant = fields.Boolean(compute='_isinter', string='intervenant')
    is_control = fields.Boolean(compute='_iscontrol', string='controle')
    is_correction = fields.Boolean(compute='_iscorr', string='correction')
    line_ids = fields.One2many('project.task.work.line', 'work_id', string='Work done')
    progress_me = fields.Float(compute='_get_progress', string='Company Currency')
    progress_qty = fields.Float(compute='_get_progress_qty', string='% Qté')
    progress_amount = fields.Float(compute='_get_progress_amount', string='% Montant')
    risk = fields.Char(compute='_get_risk', string='Risk')
    link_ids = fields.One2many('link.line', 'work_id', string='Work done')
    r_id = fields.Many2one('risk.management.category', string='r ID', readonly=True,
                           states={'draft': [('readonly', False)]}, )

    def action_affect(self):

        return {
            'name': ('Modification Travaux Permis'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'view_id': self.env.ref('eb_invoices_wizard.view_merge_tasks_form').id,
            'context': {'active_ids': self.ids,
                        'active_model': self._name,
                        'types_affect': 'intervenant'},
            'domain': []
        }

    def button_write1(self):

        self.write({'state': 'tovalid'})
        return True

    def button_cancel_write(self):

        if self.state == 'affect':
            self.write({'state': 'draft'})
        elif self.state == 'tovalid':
            self.write({'state': 'affect'})

        return {'name': "Modification Travaux",
                'res_model': "project.task.work",
                'src_model': "project.task.work",
                'view_mode': "form",
                'target': "new",
                'key2': "client_action_multi",
                'multi': "True",
                'res_id': self.ids[0],
                'type': 'ir.actions.act_window',
                }

    def button_cancel_affect(self):

        self.write({'state': 'cancel'})
        return True

    # need to modify the id of the first condition
    def button_save_(self):

        project_ids = self.ids[0]

        if self.categ_id.id == 6:
            return {
                'name': ('Modification Travaux'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': 1616,
                'target': 'new',
                'res_model': 'project.task.work',
                'res_id': self.ids[0],
                'context': {'active_id': self.ids[0]},
                'domain': [('project_id', 'in', [project_ids])]
            }
        else:
            return {
                'name': ('Modification Travaux'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': 1139,
                'target': 'new',
                'res_model': 'project.task.work',
                'res_id': self.ids[0],
                'context': {'active_id': self.ids[0]},
                'domain': [('project_id', 'in', [project_ids])]
            }

    # need to check
    def button_approve(self):

        hr_payslip = self.env['hr.payslip']
        hr_payslip_line = self.env['hr.payslip.line']
        employee_obj = self.env['hr.employee']
        task_obj = self.env['project.task.work']
        task_obj_line = self.env['project.task.work.line']

        this = task_obj.browse()

        line = this.employee_id.id
        empl = employee_obj.browse(line)
        if empl.job_id.id == 1:
            name = 'Feuille de Temps'
        else:
            name = 'Facture'

        self.env.cr.execute(
            "select cast(substr(number, 6, 8) as integer) from hr_payslip where number is not Null and name=%s and EXTRACT(YEAR FROM date_from)=%s  order by number desc limit 1",
            (name, this.date_start.year))
        q3 = self.env.cr.fetchone()
        if q3:
            res1 = q3[0] + 1
        else:
            res1 = '001'
        pay_id = hr_payslip.create({'employee_id': line,
                                    'date_from': this.date_start,
                                    'date_to': this.date_start,
                                    'contract_id': this.employee_id.contract_id.id,
                                    'name': name,
                                    'number': str(str(this.date_start.year) + '-' + str(str(res1).zfill(3))),
                                    'struct_id': 1,
                                    'currency_id': 5,
                                    })

        for tt in this.line_ids:

            if tt.state == 'tovalid' and not tt.paylist_id:
                hr_payslip_line.create({'employee_id': line,
                                        'contract_id': this.employee_id.contract_id.id,
                                        'name': ' ',
                                        'code': '-',
                                        'category_id': 1,
                                        'quantity': tt.hours_r,
                                        'slip_id': pay_id,
                                        'rate': 100,
                                        'work_id': tt.work_id.id,
                                        'quantity': tt.poteau_r,
                                        'salary_rule_id': 1,
                                        'amount': this.employee_id.contract_id.wage,
                                        })
                task_obj_line.write({'state': 'valid', 'paylist_id': pay_id})

        task_obj.write({'state': 'valid', 'paylist_id': pay_id})
        return True

    def action_open_histo(self):
        this = self[0]
        ll = []
        if this.kit_id:
            wrk = self.env['project.task.work'].search([('project_id', '=', this.project_id.id),
                                                        ('kit_id', '=', this.kit_id.id),
                                                        ('zone', '=', this.zone),
                                                        ('secteur', '=', this.secteur)])

            for work in wrk:
                hist = self.env['work.histo'].search([('work_id', '=', work.id)])
                print('hist:', hist)
                if hist:
                    for hist_line in hist.mapped('line_ids'):
                        # print('hist_line.work_histo_id.id:', hist_line.work_histo_id.id)
                        ll.append(hist_line.work_histo_id.id)

            if not ll:
                raise ValueError("Pas d'historique pour cette tâche")

            return {
                'name': 'Historique Tache',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'work.histo',
                'res_id': ll[0],
                'context': {},
                'domain': []
            }
        else:
            hist = self.env['work.histo'].search([('work_id', '=', this.id)])
            if hist:
                return {
                    'name': 'Historique Tache',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'work.histo',
                    'res_id': hist.id,
                    'context': {},
                    'domain': [('work_id', 'in', this.id)]
                }
            else:
                raise ValueError("Pas d'historique pour cette tâche")

    def action_open(self):
        project_ids = self.ids[0]
        task_obj = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        r = []
        dep = self.env['hr.academic'].search([('categ_id', '=', self.categ_id.id)])
        self.env['hr.employee'].search([]).write({'vehicle': ''})
        if dep:
            for nn in dep:
                em = self.env['hr.academic'].browse(nn, context=self.env.context).employee_id.id
                emp_obj.browse(em).write({'vehicle': '1'})
                r.append(em)
        self.write({'dep': r})
        if self.categ_id.id == 6:
            return {
                'name': 'Modification Travaux',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': self.env.ref('module_name.view_id_1').id,
                'target': 'new',
                'res_model': 'project.task.work',
                'res_id': self.id,
                'context': {'active_id': self.id},
                'domain': [('project_id', 'in', [project_ids])]
            }
        else:
            return {
                'name': ('Modification Travaux'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': self.env.ref('module_name.view_id_2').id,
                'target': 'new',
                'res_model': 'project.task.work',
                'res_id': self.id,
                'context': {'active_id': self.id},
                'domain': [('project_id', 'in', [project_ids])]
            }

    def project_open(self):
        line_obj = self.env['project.task.work']

        parent = line_obj.browse(self.ids[0])

        return {
            'name': ('Consultation Projet'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': parent.project_id.id,
            'view_id': 1758,
            'context': {},
            'domain': []
        }

    def action_open_flow(self):
        work_ids = self.env['base.flow.merge.line'].search([('work_id', '=', self.id)])
        list_ids = work_ids.mapped('wizard_id.id')

        return {
            'name': 'Liste des Actions Workflows',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'popup',
            'res_model': 'base.flow.merge.automatic.wizard',
            'res_id': self.id,
            'context': {},
            'domain': [('id', 'in', list_ids)]
        }

    def action_open_group2(self):
        tt = []

        if self.line_ids:
            for rec_line in self.line_ids:
                if rec_line.group_id2:
                    if rec_line.group_id2.ids not in tt:
                        tt.append(rec_line.group_id2.ids)

        if tt:
            for kk in tt:
                self.env['base.group.merge.automatic.wizard'].search([('id', 'in', kk)]).write(
                    {'create_uid': self.env.uid})

        return {
            'name': 'Consultation Travaux Validés',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [[self.env.ref('eb_group_wizard.retour_bons_production').id, 'tree']],

            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'context': {},
            'domain': [('id', 'in', tt)]
        }

    def action_open_group3(self):
        tt = []

        for current in self:
            test1 = self.env['project.task.work.line'].search([('work_id2', '=', current.id)])
            if test1:
                for rec_line in test1:
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)

            if current.line_ids:
                for rec_line in current.line_ids:
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)

        if tt:
            self.env['base.group.merge.automatic.wizard'].search([('id', 'in', tt)]).write({'create_uid': self.env.uid})

        return {
            'name': 'Consultation Travaux Validés',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [[self.env.ref('your_module_name.view_id').id, 'tree']],
            # Replace 'your_module_name' and 'view_id' with the actual values
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'context': {},
            'domain': [('id', 'in', tt), ('state1', '!=', 'draft')]
        }

    def action_open_group4(self):
        tt = []

        for current in self:
            test1 = self.env['project.task.work.line'].search([('work_id2', '=', current.id)])
            if test1:
                for rec_line in test1:
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
            if current.line_ids:
                for rec_line in current.line_ids:
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
        if tt:
            self.env['base.group.merge.automatic.wizard'].search([('id', 'in', tt)]).write({'create_uid': self.env.uid})

        return {
            'name': 'Consultation Travaux Validés',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [[self.env.ref('your_module_name.view_id').id, 'tree']],
            # Replace 'your_module_name' and 'view_id' with the actual values
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'context': {},
            'domain': [('id', 'in', tt), ('state2', '!=', 'draft')]
        }

    def action_open_group(self):
        tt = []

        if self.line_ids:
            for rec_line in self.line_ids:
                if rec_line.group_id:
                    if rec_line.group_id.ids not in tt:
                        tt.append(rec_line.group_id.ids)

        return {
            'name': 'Consultation Travaux Validés',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'views': [[self.env.ref('your_module_name.view_id').id, 'form']],
            # Replace 'your_module_name' and 'view_id' with the actual values
            'target': 'new',
            'res_model': 'bon.show',
            'context': {},
            'domain': [('id', 'in', tt)]
        }

    def move_next(self, ids):
        current = self.env['project.task.work'].browse(ids[0])

        return {
            'name': ('Actions Workflow'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.flow.merge.automatic.wizard',
            'context': {
                'default_project_id': current.project_id.id,
                'default_date_start_r': fields.Date.today(),
                'default_zone': current.zone,
                'default_secteur': current.secteur,
            },
            'domain': [],
        }

    def action_copy(self, default=None):
        if default is None:
            default = {}
        for tt in self:
            packaging_obj = self.env['project.task.work']

            self.env.cr.execute(
                'SELECT sequence FROM project_task_work WHERE task_id=%s ORDER BY sequence DESC LIMIT 1',
                (tt.task_id.id,))
            res = self.env.cr.fetchone()
            packaging_obj.write(id[0], {'poteau_t': tt.poteau_t / 2})
            cte = packaging_obj.create({
                'project_id': tt.project_id.id,
                'sequence': res[0] + 1,
                'task_id': tt.task_id.id,
                'product_id': tt.product_id.id,
                'categ_id': tt.categ_id.id,
                'state_id': tt.state_id.id or False,
                'city': tt.city or False,
                'name': tt.name + ' * ',
                'date_start': tt.date_start,
                'date_end': tt.date_end,
                'poteau_t': tt.poteau_t / 2,
                'poteau_i': tt.poteau_i,
                'color': tt.color,
                'hours': tt.hours,
                'total_t': tt.color * 7,
                'project_id': tt.task_id.project_id.id,
                'gest_id': tt.gest_id.id,
                'uom_id': tt.uom_id.id,
                'uom_id_r': tt.uom_id_r.id,
                'ftp': tt.ftp,
                'zone': tt.zone,
                'secteur': tt.secteur,
                'state': 'draft'
            })

        return cte

    def action_issue(self):
        current = self[0]

        if current.issue_id:
            return {
                'name': 'Gestion des Incidents et Anomalies',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.issue',
                'res_id': current.issue_id.id,
                'context': {},
                'domain': [('work_id', '=', current.id)]
            }
        else:
            return {
                'name': 'Gestion des Incidents et Anomalies',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.issue',
                'context': {
                    'default_work_id': current.id,
                    'default_date_deadline': fields.Date.context_today(self),
                    'default_employee_id': current.employee_id.id or False,
                    'default_project_id': current.project_id.id,
                    'default_task_id': current.task_id.id,
                    'default_gest_id': current.gest_id.id,
                    'default_name': current.project_id.number + '-' + str(current.task_id.sequence).zfill(
                        3) + '-' + str(current.sequence).zfill(3)
                },
                'domain': []
            }

    def action_open_invoice(self):
        current = self[0]

        tt = []
        if current.line_ids:
            for rec_line in current.line_ids:
                if rec_line.paylist_id:
                    if rec_line.paylist_id.id not in tt:
                        tt.append(rec_line.paylist_id.id)
        return {
            'name': 'Consultation Facture/F.T',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'new',
            'res_model': 'hr.payslip',
            'context': {},
            'domain': [('id', 'in', tt)]
        }

    def action_open1(self):

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            # 'res_id': self.id,
            # 'res_id': self.id,
            'context': {'active_ids': self.ids,
                        'active_model': self._name,
                        },
            'domain': [],
        }

    @api.model
    def create(self, values):
        if 'active_ids' in self.env.context and self.env.context.get('active_model') == 'project.task.work':
            # If the context contains active_ids and active_model is 'project.task.work',
            # it means the wizard is being called from the 'project.task.work' model
            return self.browse(self.env.context['active_ids'])[0]
        else:
            return super(TaskWork, self).create(values)


class TaskWorkLine(models.Model):
    _name = 'project.task.work.line'
    _description = 'Project Task Work Line'

    @api.depends_context('uid')
    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('project_custom.group_super_admin')

    is_super_admin = fields.Boolean(string='Super Admin', compute='_compute_is_super_admin', method=True)
    name = fields.Char(string='Work summary', readonly=True, states={'affect': [('readonly', False)]}, )
    ftp = fields.Char(string='ftp', )
    date = fields.Datetime(string='Date', select="1")
    date_r = fields.Datetime(string='Date', select="1", readonly=True, states={'affect': [('readonly', False)]}, )
    work_id = fields.Many2one('project.task.work', string='Task Work')
    work_id2 = fields.Many2one('project.task.work', string='Event')
    date_start = fields.Date(string='Date Prévue', select="1")
    date_end = fields.Date(string='Date Fin', select="1")
    date_start_r = fields.Date(string='Date', select="1", readonly=True, states={'affect': [('readonly', False)]}, )
    date_end_r = fields.Date(string='Date', select="1", readonly=True, states={'affect': [('readonly', False)]}, )
    employee_id = fields.Many2one('hr.employee', string='Employee')
    project_id = fields.Many2one('project.project', 'Project', ondelete='set null', select=True,
                                 track_visibility='onchange', change_default=True,
                                 readonly=True, states={'affect': [('readonly', False)]}, )
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade', select="1", readonly=True,
                              states={'affect': [('readonly', False)]}, )
    product_id = fields.Many2one('product.product', string='Task', ondelete='cascade', select="1", readonly=True,
                                 states={'affect': [('readonly', False)]}, )
    hours = fields.Float(string='Total Hrs Prévues', readonly=True, states={'affect': [('readonly', False)]}, )
    hours_r = fields.Float(string='Durée(Heurs)')
    total_t = fields.Float(string='Total à Facturer T', readonly=True, states={'affect': [('readonly', False)]}, )
    total_r = fields.Float(string='Total à Facturer R', readonly=True, states={'affect': [('readonly', False)]}, )
    poteau_t = fields.Float(string='Time Spent', readonly=True, states={'affect': [('readonly', False)]}, )
    poteau_r = fields.Float(string='Time Spent')
    poteau_reste = fields.Float(string='Time Spent', readonly=True, states={'affect': [('readonly', False)]}, )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'),
    ],
        string='Status', copy=False, readonly=True, states={'affect': [('readonly', False)]}, )
    etape = fields.Char('etap', readonly=True, states={'draft': [('readonly', False)]}, )
    sequence = fields.Integer(string='Sequence', select=True, readonly=True, states={'affect': [('readonly', False)]}, )
    zone = fields.Integer(string='Color Index', readonly=True, states={'affect': [('readonly', False)]}, )
    secteur = fields.Integer(string='Color Index', readonly=True, states={'affect': [('readonly', False)]}, )
    user_id = fields.Many2one('res.users', string='USER', select="1",
                              readonly=True, states={'affect': [('readonly', False)]}, )
    paylist_id = fields.Many2one('hr.payslip', string='Done by', select="1", readonly=True,
                                 states={'affect': [('readonly', False)]}, )
    gest_id = fields.Many2one('hr.employee', string='Superviseur', readonly=True,
                              states={'affect': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Superviseur', readonly=True,
                                 states={'affect': [('readonly', False)]}, )
    issue_ids = fields.One2many('project.issue.version', 'works_id', string='Work done', readonly=True,
                                states={'affect': [('readonly', False)]}, )
    issue_id = fields.Many2one('project.issue', 'Done by', select="1", readonly=True,
                               states={'affect': [('readonly', False)]}, )
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('tovalid', 'Dde Validation'),
        ('valid', 'Bons Validés'),
        ('paid', 'Bons Facturés'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
        ('close', 'Traité')
    ],
        string='Status', copy=False)
    categ_id = fields.Many2one('product.category', string='Département', readonly=True,
                               states={'affect': [('readonly', False)]}, )
    note = fields.Text(string='Work summary', readonly=True, states={'affect': [('readonly', False)]}, )
    done = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
    done1 = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
    done2 = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
    done3 = fields.Boolean(string='is done')
    done4 = fields.Boolean(string='is done')
    auto = fields.Boolean(string='is done')
    facture = fields.Boolean(string='Facture', readonly=True, states={'affect': [('readonly', False)]}, )
    date_inv = fields.Date(string='Date', select="1")
    num = fields.Char(string='Work summary', readonly=True, states={'affect': [('readonly', False)]}, )
    color = fields.Integer(string='Durée(Jours)', readonly=True, states={'affect': [('readonly', False)]}, )
    color1 = fields.Integer(string='Color 1', readonly=True, states={'affect': [('readonly', False)]}, )
    uom_id = fields.Many2one('product.uom', string='Unité', readonly=True,
                             states={'affect': [('readonly', False)]}, required=False, )
    uom_id_r = fields.Many2one('product.uom', string='Unit of Measure', readonly=True,
                               states={'affect': [('readonly', False)]}, )
    wage = fields.Integer(string='T.H')
    total = fields.Integer(string='Total')
    rentability = fields.Float(string='Rentabilité')
    taux_horaire = fields.Float(string='T.H')

    @api.onchange('date_end_r', 'date_start_r', 'employee_id', 'task_id')
    def onchange_date_to_(self):
        """
        Update the number_of_days.
        """
        date_to = self.date_end_r
        date_from = self.date_start_r
        # date_to has to be greater than date_from
        result = {'value': {}}
        if (date_from and date_to):
            if (date_from and date_to) and (date_from > date_to):
                raise UserError(_('Warning!\nThe start date must be anterior to the end date.'))

            result = {'value': {}}
            holiday_obj = self.env['hr.holidays']
            hours_obj = self.env['training.holiday.year']

            # Compute and update the number of days
            if (date_to and date_from) and (date_from <= date_to):
                diff_day = holiday_obj._get_number_of_days(date_from, date_to, self.employee_id)
                year = hours_obj.search([('year', '=', str(date_from.year))])
                if year:
                    hr = hours_obj.browse(year[0]).hours
                else:
                    hr = 7
                result['value']['color1'] = round(math.floor(diff_day)) + 1
                result['value']['hours_r'] = (round(math.floor(diff_day)) + 1) * hr
            else:
                result['value']['color1'] = 0
                result['value']['total_r'] = 0
        return result

    @api.onchange('hours_r', 'employee_id')
    def onchange_hours_(self):
        """
        Update the number_of_days.
        """

        academic_obj = self.env['hr.academic']

        result = {'value': {}}
        # Compute and update the number of days
        if self.hours_r:
            wage = 0
            aca = academic_obj.search([('employee_id', '=', self.employee_id)])
            if aca:
                for list in aca:
                    if list:
                        ligne = academic_obj.browse(list)
                        if ligne.curr_ids:
                            for ll in ligne.curr_ids:
                                if ll.product_id and ll.uom_id:
                                    if (ll.product_id.id == self.product_id and ll.uom_id.id == self.uom_id):
                                        wage = ll.amount
                                    elif ll.product_id and ll.uom_id2:
                                        if (ll.product_id.id == self.product_id and ll.uom_id2.id == self.uom_id):
                                            wage = ll.amount2


                                elif ll.product_id and ll.uom_id2:
                                    if (ll.product_id.id == self.product_id and ll.uom_id2.id == self.uom_id):
                                        wage = ll.amount2

                                elif ll.categ_id and ll.uom_id:
                                    if (ll.categ_id.id == self.categ_id and ll.uom_id.id == self.uom_id):
                                        wage = ll.amount
                                    elif ll.categ_id and ll.uom_id2:
                                        if (ll.categ_id.id == self.categ_id and ll.uom_id2.id == self.uom_id):
                                            wage = ll.amount2

                                elif ll.categ_id and ll.uom_id2:
                                    if (ll.categ_id.id == self.categ_id and ll.uom_id2.id == self.uom_id):
                                        wage = ll.amount2

                                else:
                                    raise UserError(
                                        _('Errour!\nTaux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
                        else:
                            raise UserError(
                                _('Errour!\nTaux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
                    else:
                        raise UserError(
                            _('Errour!\nTaux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
            else:
                raise UserError(
                    _('Errour!\nTaux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))

            if wage == 0:
                raise UserError(
                    _('Errour!\nTaux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
            if self.uom_id == 5:
                result['value']['total_r'] = self.hours_r * wage
            else:
                result['value']['total_r'] = self.poteau_r * wage
        return result


class ProjectIssueVersion(models.Model):
    _name = "project.issue.version"
    works_id = fields.Many2one('project.project', string='Work ID')


class RiskManagementCategory(models.Model):
    _inherit = 'risk.management.category'
    work_id = fields.Many2one('project.task.work', string='Wizard')


class LinkLine(models.Model):
    _inherit = 'link.line'
    work_id = fields.Many2one('project.task.work', string='Event')


class ProjectStatus(models.Model):
    _name = 'project.status'
    _description = 'Project Status'

    name = fields.Char(String='Status Permis')


class HrPayslip(models.Model):
    _name = "hr.payslip"
    name = fields.Char('Name')


class ProjectIssue(models.Model):
    _name = "project.issue"
    name = fields.Char('Name')
