# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date


class TaskWork(models.Model):
    _name = 'project.task.work'
    _description = 'Project Task Work'
    _rec_name = 'id'

    # ftp = fields.Char(string='Ftp', readonly=True, states={'draft': [('readonly', False)]}, )
    # job = fields.Char(string='Job', readonly=True, states={'draft': [('readonly', False)]}, )
    # date = fields.Datetime('Date Doc', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    # date_r = fields.Datetime(string='date', index="1", readonly=True, states={'draft': [('readonly', False)]}, )
    # date_p = fields.Date(string='date', index="1")
    date_start = fields.Date(string='Date Début project', index="1")
    date_end = fields.Date(string='Date Fin project', index="1")
    date_start_r = fields.Date(string='Date Début Réelle Task', index="1",
                               states={'affect': [('readonly', False)]}, )
    date_end_r = fields.Date(string='Date Fin Réelle Task', index="1",
                             states={'draft': [('readonly', False)]}, )
    # ex_state = fields.Char(string='ex')
    # r_id = fields.Many2one('risk.management.category', string='r ID', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Activités', select="1")
    product_id = fields.Many2one('product.product', string='T. de Service')
    hours = fields.Float(string='Hours')
    ## hours_r = fields.Float(string='Hours r', )
    etape = fields.Char(string='Etape', readonly=True, states={'draft': [('readonly', False)]}, )
    categ_id = fields.Many2one('product.category', string='Département', states={'draft': [('readonly', False)]}, )
    # hours_r = fields.Float(compute='_get_planned', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Clients', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    kit_id = fields.Many2one('product.kit', string='Kit ID', select="1",
                             readonly=True, states={'draft': [('readonly', False)]}, )
    # total_t = fields.Float(string='Total à Facturer T', readonly=True, states={'draft': [('readonly', False)]}, )
    # total_r = fields.Float(compute='_get_sum', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    poteau_t = fields.Float(string='Qté demamdée', states={'draft': [('readonly', False)]}, )
    # poteau_i = fields.Float(string='N.U', readonly=True, states={'draft': [('readonly', False)]}, )
    poteau_r = fields.Float(compute='_get_qty', string='Company Currency', readonly=True,
                            states={'draft': [('readonly', False)]}, )
    # poteau_da = fields.Float(compute='_get_qty_affect', string='Company Currency', readonly=True,
    #                          states={'draft': [('readonly', False)]}, )
    # poteau_ra = fields.Float(compute='_get_qty_r_affect', string='Company Currency', readonly=True,
    #                          states={'draft': [('readonly', False)]}, )
    # poteau_reste = fields.Integer(string='N.U', readonly=True, states={'draft': [('readonly', False)]}, )
    # total_part = fields.Selection([
    #     ('partiel', 'Partiel'),
    #     ('total', 'Total'), ],
    #     string='N.U', copy=False, readonly=True, states={'draft': [('readonly', False)]}, )
    sequence = fields.Integer(string='Sequence', select=True, states={'draft': [('readonly', False)]}, )
    # state_id = fields.Many2one('res.country.state', string='Cité/Ville')
    city = fields.Char(string='City', readonly=True)
    # state_id1 = fields.Many2one('res.country.state', string='state ID')
    # state_id2 = fields.Many2one('res.country.state', string='state 2 ID ')
    precision = fields.Char(string='Precision(P)')
    permis = fields.Char(string='Permis(P)')
    date_fin = fields.Date(string='Date Fin (P)')
    prolong = fields.Char(string='Prolongation demandée(P)')
    remarque = fields.Text(string='Remarque')
    date_remis = fields.Date(string='Date Remis(P)')
    date_construt = fields.Date(string='Date Constrution(P)')
    secteur_en = fields.Char(string='Secteur Enfui(P)')
    graphe_t_b = fields.Char(string='Graphe_t_b(P)')
    # dct = fields.Char(string='Dct(P)')
    active = fields.Boolean(string='Active', default=True)
    # active = fields.Boolean(default=True)
    # anomalie = fields.Char(string='Anomalie(P)')
    # action = fields.Char(string='Action(P)')
    # pourc_t = fields.Float(string='% Avancement', readonly=True, states={'draft': [('readonly', False)]}, )
    # pourc_f = fields.Float(string='% Dépense', readonly=True, states={'draft': [('readonly', False)]}, )
    # statut1 = fields.Many2one('project.status', string='Status', select=True)
    # statut = fields.Selection([('Encours', 'Encours'),
    #                            ('Soumise', 'Soumise'),
    #                            ('A l"Etude', 'A l"étude'),
    #                            ('Approuve', 'Approuvé'),
    #                            ('Incomplet', 'Incomplet'),
    #                            ('En Construction', 'En Construction'),
    #                            ('Envoye', 'Envoyé'),
    #                            ('Travaux Pre.', 'Travaux Pré.'),
    #                            ('Refuse', 'Refusé'),
    #                            ('Refus Partiel', 'Refus Partiel'),
    #                            ('Approuve Partiel', 'Approuvé Partiel'),
    #                            ('Travaux Complété', 'Travaux Complété'),
    #                            ('Inspection', 'Inspection'),
    #                            ('Annule', 'Annulé'),
    #                            ('En Resiliation', 'En Résiliation'),
    #                            ('Non Requis', 'Non Requis'),
    #                            ('En TP-derogation approuvee', 'En TP-dérogation approuvée'),
    #                            ('TP completes-avec refus', 'TP complétés-avec refus'),
    #                            ('Deviation', 'Déviation'),
    #                            ('9032', 'Approbation demandeur'),
    #                            ('DA', 'Approbation demandeur – Dérogation Approuvé'),
    #                            ('DP', 'Approbation demandeur – Dérogation Partielle'),
    #                            ('DR', 'Approbation demandeur – Dérogation Refusé'),
    #                            ('AD', 'Approbation demandeur – ADR Défavorable'),
    #                            ('TPDP', 'En TP - Dérogation Partielle'),
    #                            ('TPSD', 'En TP - Sans Dérogation'),
    #                            ],
    #                           string='Status', copy=False)
    # kanban_color = fields.Integer(compute='_compute_kanban_color', string='Couleur')
    # link_ids = fields.One2many('link.type', 'work_id', string='Work done')
    zone = fields.Integer(string='Zone (entier)', states={'draft': [('readonly', False)]}, )
    secteur = fields.Integer(string='Secteur (entier)', states={'draft': [('readonly', False)]}, )
    zo = fields.Char(string='Zone', readonly=True, states={'draft': [('readonly', False)]}, )
    sect = fields.Char(string='Secteur', readonly=True, states={'draft': [('readonly', False)]}, )
    work_id = fields.Char(string='work ID')
    work_id2 = fields.Char(string='work ID')
    # user_id = fields.Many2one('res.users', string='user ID', select="1", readonly=True,
    #                           states={'draft': [('readonly', False)]}, )
    # paylist_id = fields.Many2one('hr.payslip', string='playlist ID', select="1", readonly=True,
    #                              states={'draft': [('readonly', False)]}, )
    # reviewer_id1 = fields.Many2one('hr.employee', string='Superviseur', readonly=True,
    #                                states={'draft': [('readonly', False)]}, )
    gest_id = fields.Many2one('hr.employee', string='Coordinateur')
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
    employee_id = fields.Many2one('hr.employee', 'Employés')
    # issue_id = fields.Many2one('project.issue', 'Issue ID', select="1", readonly=True,
    #                            states={'draft': [('readonly', False)]}, )
    group_id = fields.Many2one('bon.show', 'group ID', select="1", readonly=False,
                               states={'draft': [('readonly', False)]}, )
    group_id2 = fields.Many2one('base.group.merge.automatic.wizard', string='group 2 ID', select="1", readonly=True,
                                states={'draft': [('readonly', False)]}, )
    # dependency_task_ids = fields.Many2many('project.task.work', 'project_task_dependency_work_rel',
    #                                        'dependency_work_id', 'work_id', string='Dependencies')
    state = fields.Selection([
        ('affect', 'T. Affectés'),
        ('draft', 'T. Planifiés'),
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
    color = fields.Integer(string='Nbdays')
    # color1 = fields.Integer('Nbdays', readonly=True, states={'affect': [('readonly', False)]}, )
    uom_id = fields.Many2one('product.uom', string='Unité Prévue', required=True)
    uom_id_r = fields.Many2one('product.uom', string='Unité Réelle', readonly=True,
                               states={'affect': [('readonly', False)]}, )
    w_id = fields.Many2one('base.task.merge.automatic.wizard', string='Company', readonly=True,
                           states={'draft': [('readonly', False)]}, )
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

    # progress_me = fields.Float(compute='_get_progress', string='Company Currency')
    # progress_qty = fields.Float(compute='_get_progress_qty', string='Company Currency')
    # progress_amount = fields.Float(compute='_get_progress_amount', string='Company Currency')
    # risk = fields.Char(compute='_get_risk', string='Risk')
    def _default_done(self):

        for rec in self:
            if self.env.cr.dbname == 'TEST95':

                if rec.product_id.is_gantt is True:

                    sql = ("select field_250 from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql, (rec.id,))
                    datas = self.env.cr.fetchone()

                    if datas and datas[0] > 1:
                        ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
                        temp = datetime.fromtimestamp(int(datas[0])).strftime('%Y-%m-%d')

                        self.env.cr.execute('update project_task_work set date_start=%s where id=%s', (temp, rec.id))
                        ##cr.execute('update project_task_work set  date_start=%s where  id = %s ' , (date_start,ids[0]))
                    sql1 = ("select field_251 from app_entity_26 WHERE id = %s")
                    self.env.cr.execute(sql1, (rec.id,))
                    datas1 = self.env.cr.fetchone()

                    if datas1 and datas1[0] > 1:
                        ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
                        temp1 = datetime.fromtimestamp(int(datas1[0])).strftime('%Y-%m-%d')
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
                if book.gest_id.user_id.id == self.uid or self.uid == 1 or 100 in book.gest_id.user_id.groups_id.ids:  ##or book..user_id.id==uid:
                    book.done33 = True
                else:
                    book.done33 = False
            else:
                book.done33 = False

    def _isinter(self):

        for book in self:
            book.is_intervenant = False
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

    name = fields.Char(string='Nom Service')

    def action_open1(self):

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
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
