# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date


class TaskWork(models.Model):
    _name = 'project.task.work'
    _description = 'Project Task Work'

    def _compute_default_done(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        ##

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
                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.done is True:
                        result[rec.id] = 1
                        break
                    else:
                        result[rec.id] = 0
            ##                        exit
            ##                    else:
            ##                        result[rec.id] =0
            else:
                result[rec.id] = 0

        return result

    def _compute_default_done1(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.done1 is True:
                        result[rec.id] = 1
                        break
                    else:
                        result[rec.id] = 0
            ##                        exit
            ##                    else:
            ##                        result[rec.id] =0
            else:
                result[rec.id] = 0

        return result

    def _compute_default_done2(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.group_id:
                        result[rec.id] = 1
                        break

                    else:
                        result[rec.id] = 0

            ##                        exit
            ##                    else:
            ##                        result[rec.id] =0
            else:
                result[rec.id] = 0

        return result

    def _compute_default_done3(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        for rec in self:
            if rec.line_ids:

                for kk in rec.line_ids.ids:

                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.group_id2:
                        result[rec.id] = 1
                        break

                    else:
                        result[rec.id] = 0

            ##                        exit
            ##                    else:
            ##                        result[rec.id] =0
            else:
                result[rec.id] = 0

        return result

    def _compute_default_flow(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        current = ids[0]
        list = []
        for rec in self:
            self.env.cr.execute('select id from base_flow_merge_line where work_id= %s', (rec.id,))
            work_ids = self.env.cr.fetchone()
            if work_ids:
                result[rec.id] = 1
            else:
                result[rec.id] = 0

        return result

    # _check_color
    def _compute_kanban_color(self, cr, uid, ids, field_name, arg, context):

        res = {}
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

            res[record.id] = color
        return res

    # _get_planned
    # def _compute_hours_r(self, cr, uid, ids, field_name, arg, context=None):
    #     result = {}
    #     self.env.cr.execute(
    #         "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
    #         (tuple(ids),))
    #     hours = dict(self.env.cr.fetchall())
    # ,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
    # for rec in self:
    #     result[rec.id] = hours.get(rec.id, 0.0)
    # return result

    # _get_sum
    def _compute_total_r(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        ##cr.execute("SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.work_id IN %s GROUP BY work_id",(('valid','paid'),tuple(ids),))
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
            (tuple(ids),))

        hours = dict(self.env.cr.fetchall())
        ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
        for rec in self:
            result[rec.id] = hours.get(rec.id, 0.0)
        return result

    def _get_qty(self):
        result = {}
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.poteau_r = hours.get(rec.id, 0.0)


    # _get_qty_r_affect
    def _compute_poteau_ra(self, cr, uid, ids, field_name, arg, context=None):

        x = {}
        for record in self:
            self.env.cr.execute(
                "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
                (record.task_id.id, str(record.zone), str(record.secteur)))
            q3 = self.env.cr.fetchone()
            ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%record.zone)
            if q3:
                x[record.id] = record.poteau_i - q3[0]
            else:
                x[record.id] = record.poteau_i
        return x

    # _get_qty_affect
    # def _compute_poteau_da(self, cr, uid, ids, field_name, arg, context=None):
    #
    #     x = {}
    #     for record in self:
    #         self.env.cr.execute(
    #             "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
    #             (record.task_id.id, str(record.zone), str(record.secteur)))
    #         q3 = self.env.cr.fetchone()
    ### raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%record.zone)
    # if q3:
    #     x[record.id] = q3[0]
    # else:
    #     x[record.id] = 0
    # return x

    def _disponible(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        for book in self:
            if book.gest_id and book.gest_id.user_id:
                if book.gest_id.user_id.id == uid or uid == 1 or 100 in book.gest_id.user_id.groups_id.ids:  ##or book..user_id.id==uid:
                    result[book.id] = True
                else:
                    result[book.id] = False
            else:
                result[book.id] = False
        return result

    # _isinter
    def _compute_is_inter(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        current = self
        for book in current:
            result[book.id] = False
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
                if tt:
                    for kk in tt:
                        self.env.cr.execute(
                            'update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
                            (uid, tuple(kk)))
                    test = self.env['base.group.merge.automatic.wizard'].search(cr, uid, [('id', 'in', tt), (
                        'state', '<>', 'draft')])
                    if test:
                        result[book.id] = True
        return result

    # iscontrol
    def _compute_is_control(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        current = self
        for book in current:
            result[book.id] = False
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.group_id2:
                        if rec_line.group_id2.id not in tt:
                            tt.append(rec_line.group_id2.id)
                if tt:

                    test = self.env['base.group.merge.automatic.wizard'].search(cr, uid, [('id', 'in', tt), (
                        'state1', '<>', 'draft')])

                    if test:
                        result[book.id] = True

                    test1 = self.env['project.task.work.line'].search(cr, uid,
                                                                      [('work_id2', '=', book.id or False)])
                    ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%test1)
                    if test1:
                        for jj in test1:
                            rec_line = self.env['project.task.work.line'].browse(cr, uid, jj, context=context)
                            if rec_line.group_id2:
                                if rec_line.group_id2.id not in tt:
                                    tt.append(rec_line.group_id2.id)
                        result[book.id] = True

        return result

    # _iscorr
    def _compute_is_corr(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        current = self
        for book in current:
            result[book.id] = False
            if book.line_ids:
                tt = []
                for kk in book.line_ids.ids:
                    rec_line = self.env['project.task.work.line'].browse(cr, uid, kk, context=context)
                    if rec_line.group_id2:
                        if rec_line.group_id2.ids not in tt:
                            tt.append(rec_line.group_id2.ids)
                if tt:
                    for kk in tt:
                        self.env.cr.execute(
                            'update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
                            (uid, tuple(kk)))
                    test = self.env['base.group.merge.automatic.wizard'].search(cr, uid, [('id', 'in', tt), (
                        'state2', '<>', 'draft')])
                    if test:
                        result[book.id] = True
                    test1 = self.env['project.task.work.line'].search(cr, uid,
                                                                      [('work_id2', '=', book.id or False)])
                    if test1:
                        for jj in test1:
                            rec_line = self.env['project.task.work.line'].browse(cr, uid, jj, context=context)
                            if rec_line.group_id2:
                                if rec_line.group_id2.id not in tt:
                                    tt.append(rec_line.group_id2.id)
                        result[book.id] = True
        return result

    def _compute_get_progress(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())

        ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
        for rec in self:
            ##result[rec.id] = hours.get(rec.id, 0.0)
            ## raise osv.exc
            if rec.hours > 0:
                ratio = hours.get(rec.id, 0.0) / rec.hours
            else:
                ratio = hours.get(rec.id, 0.0)
            result[rec.id] = round(min(100.0 * ratio, 100), 2)
        return result

    # def _compute_progress_qty(self, cr, uid, ids, field_name, arg, context=None):
    #     result = {}
    #
    #     self.env.cr.execute(
    #         "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
    #         (tuple(ids),))
    #     hours = dict(self.env.cr.fetchall())
    #
    # ,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
    # for rec in self:
    # result[rec.id] = hours.get(rec.id, 0.0)
    # raise osv.exc
    # if rec.poteau_t > 0:
    #     ratio = hours.get(rec.id, 0.0) / rec.poteau_t
    # else:
    #     ratio = hours.get(rec.id, 0.0)
    # result[rec.id] = round(min(100.0 * ratio, 100), 2)
    # return result

    def _compute_progress_amount(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%hours)
        ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
        for rec in self:
            ##result[rec.id] = hours.get(rec.id, 0.0)
            ## raise osv.exc
            if rec.total_t > 0:
                ratio = hours.get(rec.id, 0.0) / rec.total_t
            else:
                ratio = hours.get(rec.id, 0.0)
            result[rec.id] = round(min(100.0 * ratio, 100), 2)
        return result

    def _compute_get_risk(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(ids),))
        amount = dict(self.env.cr.fetchall())
        ##res = super(project_task_work, self).default_get(cr, uid, fields, context=context)
        self.env.cr.execute(
            "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s and state in ('valid','paid') GROUP BY work_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        ratio = 'N.D'
        for rec in self:
            ##result[rec.id] = hours.get(rec.id, 0.0)
            ## raise osv.exc
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

            result[rec.id] = ratio
        return result

    name = fields.Char(string='Nom Service', )
    ftp = fields.Char(string='Ftp', )
    job = fields.Char(string='Job', )
    date = fields.Datetime('Date Doc', index="1", )
    date_r = fields.Datetime(string='date', index="1", )
    date_p = fields.Date(string='date', index="1")
    date_start = fields.Date(string='Date Début', index="1", )
    date_end = fields.Date(string='Date Fin', index="1", )
    date_start_r = fields.Date(string='Date Début Réelle', index="1", readonly=True,
                               states={'affect': [('readonly', False)]}, )
    date_end_r = fields.Date(string='Date Fin Réelle', index="1", )
    ex_state = fields.Char(string='ex')
    r_id = fields.Many2one('risk.management.category', string='r ID', )
    project_id = fields.Many2one('project.project', string='Project', ondelete='set null', select=True, )
    task_id = fields.Many2one('project.task', string='Activités', ondelete='cascade', select="1", )
    product_id = fields.Many2one('product.product', string='T. de Service', ondelete='cascade', select="1", )
    hours = fields.Float(string='Hours', )
    ## hours_r = fields.Float(string='Hours r', )
    etape = fields.Char(string='Etape', )
    categ_id = fields.Many2one('product.category', string='Département', )
    # hours_r = fields.Float(compute='_compute_hours_r', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Clients', )
    kit_id = fields.Many2one('product.kit', string='Kit ID', ondelete='cascade', select="1", )
    total_t = fields.Float(string='Total à Facturer T', )
    # total_r = fields.Float(compute='_compute_total_r', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    poteau_t = fields.Float(string='Qté demamdée', )
    poteau_i = fields.Float(string='N.U', )
    poteau_r = fields.Float(compute='_get_qty', string='Company Currency', readonly=True,
                            states={'draft': [('readonly', False)]}, )
    # poteau_da = fields.Float(compute='_compute_poteau_da', string='Company Currency', readonly=True,
    #                          states={'draft': [('readonly', False)]}, )
    # poteau_ra = fields.Float(compute='_compute_poteau_ra', string='Company Currency', readonly=True,
    #                          states={'draft': [('readonly', False)]}, )
    poteau_reste = fields.Integer(string='N.U', )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'), ],
        string='N.U', copy=False, )
    sequence = fields.Integer(string='Sequence', select=True, )
    state_id = fields.Many2one('res.country.state', string='Cité/Ville')
    city = fields.Char(string='City', readonly=True)
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
    pourc_t = fields.Float(string='% Avancement', )
    pourc_f = fields.Float(string='% Dépense', )
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
    # kanban_color = fields.Integer(compute='_compute_kanban_color', string='Couleur')
    link_ids = fields.One2many('link.type', 'work_id', string='Work done')
    zone = fields.Integer(string='Zone (entier)', )
    secteur = fields.Integer(string='Secteur (entier)', )
    zo = fields.Char(string='Zone', )
    sect = fields.Char(string='Secteur', )
    user_id = fields.Many2one('res.users', string='user ID', select="1", )
    paylist_id = fields.Many2one('hr.payslip', string='playlist ID', select="1", )
    reviewer_id1 = fields.Many2one('hr.employee', string='Superviseur', )
    gest_id = fields.Many2one('hr.employee', string='Coordinateur', )
    gest_id2 = fields.Many2one('hr.employee', string='Coordinateur 2', )
    gest_id3 = fields.Many2one('hr.employee', string='Coordinateur 3', copy=True)
    coordin_id1 = fields.Many2one('hr.employee', string='Coordinateur 1', )
    coordin_id2 = fields.Many2one('hr.employee', string='Coordinateur 2', )
    coordin_id3 = fields.Many2one('hr.employee', string='Coordinateur 3', )
    coordin_id4 = fields.Many2one('hr.employee', string='Coordinateur 4', )
    coordin_id5 = fields.Many2one('hr.employee', string='Coordinateur 5', )
    coordin_id6 = fields.Many2one('hr.employee', string='Coordinateur 6', )
    coordin_id7 = fields.Many2one('hr.employee', string='Coordinateur 7', )
    coordin_id8 = fields.Many2one('hr.employee', string='Coordinateur 8', )
    coordin_id9 = fields.Many2one('hr.employee', string='Coordinateur 9', )
    coordin_id10 = fields.Many2one('hr.employee', string='Coordinateur 10', )
    ## 'emp_ids': fields.one2many('depart_category_rel', 'categ_id', 'Task',readonly=True, states={'draft':[('readonly',False)]})
    ## 'emp_ids': fields.many2many('hr.employee', 'depart_category_rel', 'depart_id', 'emp_id', 'Tags',domain="[('depart_id', '=', categ_id)]",)
    employee_id = fields.Many2one('hr.employee', 'Employés', )
    issue_id = fields.Many2one('project.issue', 'Issue ID', select="1", )
    group_id = fields.Many2one('bon.show', 'group ID', select="1", )
    group_id2 = fields.Many2one('base.group.merge.automatic.wizard', string='group 2 ID', select="1", )
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
    p_done = fields.Float(string='Qté Réalisée', )
    note = fields.Text(string='N.U')
    # done = fields.Boolean(compute='_compute_default_done', string='Company Currency', readonly=True,
    #                       states={'draft': [('readonly', False)]}, )
    # done1 = fields.Boolean(compute='_compute_default_done1', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    # done2 = fields.Boolean(compute='_compute_default_done2', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    # done3 = fields.Boolean(compute='_compute_default_done3', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    # done4 = fields.Boolean(compute='_compute_default_flow', string='Company Currency', readonly=True,
    #                        states={'draft': [('readonly', False)]}, )
    color = fields.Integer(string='Nbdays', )
    color1 = fields.Integer('Nbdays', )
    uom_id = fields.Many2one('product.uom', string='Unité Prévue', required=True, )
    uom_id_r = fields.Many2one('product.uom', string='Unité Réelle', )
    w_id = fields.Many2one('base.task.merge.automatic.wizard', 'Company', )
    pourc = fields.Float('Pour C', )
    rank = fields.Char('Rank', )
    display = fields.Boolean(string='Réalisable')
    is_copy = fields.Boolean(string='Dupliqué')
    # done33 = fields.Boolean(compute='_disponible', string='done')
    current_emp = fields.Many2one('hr.employee', string='Employé Encours', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    current_gest = fields.Many2one('hr.employee', string='Coordinateur En cours', readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    current_sup = fields.Many2one('hr.employee', string='Superviseur En cours', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    prior1 = fields.Float(string='Prior1', )
    prior2 = fields.Float(string='Prior2', )
    cmnt = fields.Char(string='Prior2', )
    work_orig = fields.Integer(string='tache original')
    affect_emp_list = fields.Char(string='employée id')
    affect_e_l = fields.Char(string='employée id')
    affect_emp = fields.Char(string='employée')
    affect_con = fields.Char(string='controle')
    affect_cor = fields.Char(string='corrdinateur')
    affect_con_list = fields.Char(string='controle id')
    affect_cor_list = fields.Char(string='corrdinateur id')
    # is_intervenant = fields.Boolean(compute='_compute_is_inter', string='intervenant')
    # is_control = fields.Boolean(compute='_compute_is_control', string='controle')
    # is_correction = fields.Boolean(compute='_compute_is_corr', string='correction')
    ## 'event_id'   : fields.many2one('event.event','Event')
    line_ids = fields.One2many('project.task.work.line', 'work_id', string='Work done')
    # progress_me = fields.Float(compute='_compute_get_progress', string='Company Currency')
    # progress_qty = fields.Float(compute='_compute_progress_qty', string='Company Currency')
    # progress_amount = fields.Float(compute='_compute_progress_amount', string='Company Currency')
    # risk = fields.Char(compute='_compute_get_risk', string='Risk')


class TaskWorkLine(models.Model):
    _name = 'project.task.work.line'
    _description = 'Project Task Work Line'

    @api.depends_context('uid')
    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('om_hospital.group_super_admin')

    is_super_admin = fields.Boolean(string='Super Admin', compute='_compute_is_super_admin', method=True)
    name = fields.Char(string='Work summary', )
    ftp = fields.Char(string='ftp', )
    date = fields.Datetime(string='Date', select="1")
    date_r = fields.Datetime(string='Date', select="1", )
    ### 'event_id'   : fields.many2one('RES','Event'),
    work_id = fields.Many2one('project.task.work', string='Task Work')
    work_id2 = fields.Many2one('project.task.work', string='Event')
    wizard_id = fields.Many2one('base.invoice.merge.automatic.wizard', string='Event')
    date_start = fields.Date(string='Date', select="1")
    date_end = fields.Date(string='Date', select="1")
    date_start_r = fields.Date(string='Date', select="1", )
    date_end_r = fields.Date(string='Date', select="1", )
    employee_id = fields.Many2one('hr.employee', string='Employee')
    project_id = fields.Many2one('project.project', 'Project', ondelete='set null', select=True,
                                 track_visibility='onchange', change_default=True, )
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade', select="1", )
    product_id = fields.Many2one('product.product', string='Task', ondelete='cascade', select="1", )
    hours = fields.Float(string='Time Spent', )
    hours_r = fields.Float(string='Time Spent')
    total_t = fields.Float(string='Time Spent', )
    total_r = fields.Float(string='Time Spent', )
    poteau_t = fields.Float(string='Time Spent', )
    poteau_r = fields.Float(string='Time Spent')
    poteau_reste = fields.Float(string='Time Spent', )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'),
    ],
        string='Status', copy=False, )
    etape = fields.Char('etap', )
    sequence = fields.Integer(string='Sequence', select=True, )
    zone = fields.Integer(string='Color Index', )
    secteur = fields.Integer(string='Color Index', )
    user_id = fields.Many2one('res.users', string='Done by', select="1", )
    paylist_id = fields.Many2one('hr.payslip', 'Done by', select="1", )
    gest_id = fields.Many2one('hr.employee', string='Superviseur', )
    partner_id = fields.Many2one('res.partner', string='Superviseur', )
    issue_ids = fields.One2many('project.issue.version', 'works_id', string='Work done', )
    issue_id = fields.Many2one('project.issue', 'Done by', select="1", )
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
    categ_id = fields.Many2one('product.category', string='Tags', )
    note = fields.Text(string='Work summary', )
    done = fields.Boolean(string='is done', )
    done1 = fields.Boolean(string='is done', )
    done2 = fields.Boolean(string='is done', )
    done3 = fields.Boolean(string='is done')
    done4 = fields.Boolean(string='is done')
    auto = fields.Boolean(string='is done')
    group_id = fields.Many2one('bon.show', string='Done by', select="1", )
    ## 'group_id2': fields.many2one('base.group.merge.automatic.wizard', 'Done by',  select="1",readonly=True, states={'affect':[('readonly',False)]},),
    group_id2 = fields.Many2one('base.group', 'Done by', select="1", )
    facture = fields.Boolean(string='Facture', )
    date_inv = fields.Date(string='Date', select="1")
    num = fields.Char(string='Work summary', )
    color = fields.Integer(string='Color', )
    color1 = fields.Integer(string='Color 1', )
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', )
    uom_id_r = fields.Many2one('product.uom', string='Unit of Measure', )
    wage = fields.Integer(string='T.H')
    total = fields.Integer(string='Total')
    rentability = fields.Float(string='Rentabilité')
    taux_horaire = fields.Float(string='T.H')


class ProjectIssueVersion(models.Model):
    _name = "project.issue.version"
    works_id = fields.Many2one('project.project', string='Work ID')


class BaseGroupMergeAutomaticWizard(models.Model):
    _name = "base.group.merge.automatic.wizard"
    name = fields.Char('Name')


class RiskManagementCategory(models.Model):
    _name = "risk.management.category"
    name = fields.Char()


class ProductCategory(models.Model):
    _name = "product.category"
    name = fields.Char('Name')


class ProductKit(models.Model):
    _name = "product.kit"
    name = fields.Char('Name')


class ProjectStatus(models.Model):
    _name = "project.status"
    name = fields.Char('Name')


class LinkType(models.Model):
    _name = "link.type"
    work_id = fields.Many2one('project.task.work', string='project ID')

    ftp = fields.Char()
    name = fields.Char()
    source = fields.Char()


class HrPayslip(models.Model):
    _name = "hr.payslip"
    name = fields.Char('Name')


class BonShow(models.Model):
    _name = "bon.show"
    name = fields.Char('Name')


class ProjectIssue(models.Model):
    _name = "project.issue"
    name = fields.Char('Name')


class ProductUOM(models.Model):
    _name = "product.uom"
    name = fields.Char('Name')


class BaseTaskMergeAutomaticWizard(models.Model):
    _name = "base.task.merge.automatic.wizard"
    name = fields.Char('Name')


class BaseGroup(models.Model):
    _name = "base.group"
    name = fields.Char('Name')


class BaseInvoiceMergeAutomaticWizard(models.Model):
    _name = "base.invoice.merge.automatic.wizard"
    name = fields.Char('Name')
