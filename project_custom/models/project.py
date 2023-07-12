# -*- coding: utf-8 -*-

from odoo import models, fields, api
# import pymysql as py
from datetime import datetime, date
import lxml.etree
import time
import datetime as dt
from odoo import SUPERUSER_ID
from odoo import tools
# from openerp.addons.resource.faces import task as Task
from odoo.tools.float_utils import float_is_zero
from odoo.tools.translate import _
import math
from datetime import timedelta
from odoo.exceptions import UserError


# from openerp.osv.orm import setup_modifiers


class ProjectCustom(models.Model):
    _description = 'custom project'
    _inherit = ['project.project']
    _inherits = {
        'mail.alias': 'alias_id',
    }
    _rec_name = 'id'
    _order = "npc"

    # def _auto_init(self, cr, context=None):
    #     """ Installation hook: aliases, project.project """
    #     # create aliases for all projects and avoid constraint errors
    #     alias_context = dict(context, alias_model_name='project.task')
    #     return self.pool.get('mail.alias').migrate_to_alias(cr, self._name, self._table,
    #                                                         super(project, self)._auto_init,
    #                                                         'project.task', self._columns['alias_id'], 'id',
    #                                                         alias_prefix='project+',
    #                                                         alias_defaults={'project_id': 'id'}, context=alias_context)
    #
    # def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
    #     if user == 1:
    #         return super(project, self).search(cr, user, args, offset=offset, limit=limit, order=order, context=context,
    #                                            count=count)
    #     if context and context.get('user_preference'):
    #         cr.execute("""SELECT project.id FROM project_project project
    #                        LEFT JOIN account_analytic_account account ON account.id = project.analytic_account_id
    #                        LEFT JOIN project_user_rel rel ON rel.project_id = project.id
    #                        WHERE (account.user_id = %s or rel.uid = %s)""" % (user, user))
    #         return [(r[0]) for r in cr.fetchall()]
    #     return super(project, self).search(cr, user, args, offset=offset, limit=limit, order=order,
    #                                        context=context, count=count)
    #
    # def onchange_partner_id(self, cr, uid, ids, part=False, context=None):
    #     partner_obj = self.pool.get('res.partner')
    #     val = {}
    #     if not part:
    #         return {'value': val}
    #     if 'pricelist_id' in self.fields_get(cr, uid, context=context):
    #         pricelist = partner_obj.read(cr, uid, part, ['property_product_pricelist'], context=context)
    #         pricelist_id = pricelist.get('property_product_pricelist', False) and \
    #                        pricelist.get('property_product_pricelist')[0] or False
    #         val['pricelist_id'] = pricelist_id
    #     return {'value': val}
    #
    # def _get_projects_from_tasks(self, cr, uid, task_ids, context=None):
    #     tasks = self.pool.get('project.task').browse(cr, uid, task_ids, context=context)
    #     project_ids = [task.project_id.id for task in tasks if task.project_id]
    #     return self.pool.get('project.project')._get_project_and_parents(cr, uid, project_ids, context)
    #
    # def _get_project_and_parents(self, cr, uid, ids, context=None):
    #     """ return the project ids and all their parent projects """
    #     res = set(ids)
    #     while ids:
    #         cr.execute("""
    #             SELECT DISTINCT parent.id
    #             FROM project_project project, project_project parent, account_analytic_account account
    #             WHERE project.analytic_account_id = account.id
    #             AND parent.analytic_account_id = account.parent_id
    #             AND project.id IN %s
    #             """, (tuple(ids),))
    #         ids = [t[0] for t in cr.fetchall()]
    #         res.update(ids)
    #     return list(res)
    #
    # def _get_project_and_children(self, cr, uid, ids, context=None):
    #     """ retrieve all children projects of project ids;
    #         return a dictionary mapping each project to its parent project (or None)
    #     """
    #     res = dict.fromkeys(ids, None)
    #     while ids:
    #         cr.execute("""
    #             SELECT project.id, parent.id
    #             FROM project_project project, project_project parent, account_analytic_account account
    #             WHERE project.analytic_account_id = account.id
    #             AND parent.analytic_account_id = account.parent_id
    #             AND parent.id IN %s
    #             """, (tuple(ids),))
    #         dic = dict(cr.fetchall())
    #         res.update(dic)
    #         ids = dic.keys()
    #     return res

    def _get_progress_hr(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s and state in ('valid','paid') GROUP BY project_id",
            (tuple(self.ids),))
        data = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.hours > 0:
                ratio = data.get(rec.id, 0.0) / rec.hours
            else:
                ratio = data.get(rec.id, 0.0)
            rec.hours_r = round(min(100.0 * ratio, 100), 2)

    def _get_progress_amount(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s and state in ('valid','paid') GROUP BY project_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.ct > 0:
                ratio = hours.get(rec.id, 0.0) / rec.ct
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_amount = round(min(100.0 * ratio, 100), 2)

    def _get_planned(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s GROUP BY project_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_planned = hours.get(rec.id, 0.0)

    def _get_effective(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_effective), 0.0) FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            rec.total_effective = hours.get(rec.id, 0.0)

    def _get_remaining(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_remaining), 0.0) FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_remaining = hours.get(rec.id, 0.0)

    def _get_sum(self):

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.project_id IN %s GROUP BY project_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_r = hours.get(rec.id, 0.0)

    def _get_attached_docs(self):

        attachment = self.env['ir.attachment']
        task = self.env['project.task']
        project_attachments = attachment.search_count([
            ('res_model', '=', 'project.project'),
            ('res_id', '=', self.id)
        ])

        task_ids = task.search([('project_id', '=', self.id)]).ids
        task_attachments = attachment.search_count([
            ('res_model', '=', 'project.task'),
            ('res_id', 'in', task_ids)
        ])

        self.doc_count = project_attachments + task_attachments

    def _task_count(self):

        for tasks in self:
            tasks.task_count = len(tasks.task_ids)

    def _get_progress(self):

        self.env.cr.execute(
            "SELECT project_id, CASE WHEN SUM(total_planned) >0 Then COALESCE(SUM(total_effective)/SUM(total_planned), 0.0)  else COALESCE(SUM(total_effective), 0.0) end FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        if hours:
            for rec in self:
                rec.progress_me = round(min(100.0 * hours.get(rec.id, 0.0), 99.99), 2)

    @api.depends_context('uid')
    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('project_custom.group_super_admin')

    @api.depends_context('uid')
    def _compute_is_admin(self):
        for record in self:
            record.is_admin = self.env.user.has_group('project_custom.group_admin')

    is_super_admin = fields.Boolean(string='Super Admin', compute='_compute_is_super_admin')
    is_admin = fields.Boolean(string='Is Admin', compute='_compute_is_admin')
    active = fields.Boolean(string='Active', readonly=True, states={'draft': [('readonly', False)]}, default=True, )
    is_kit = fields.Boolean(string='Is Kit', readonly=True, states={'draft': [('readonly', False)]}, default=True, )
    priority = fields.Selection([('0', 'Faible'), ('1', 'Normale'), ('2', 'Elevée')], string='Priorité Projet',
                                select=True, readonly=True, states={'draft': [('readonly', False)]}, default='0', )
    sequence = fields.Integer(string='Sequence', help="Gives the sequence order when displaying a list of Projects.",
                              readonly=True, states={'draft': [('readonly', False)]}, default=10000, )
    bord = fields.Char(string='N° PO', readonly=True, states={'draft': [('readonly', False)]}, )
    type3 = fields.Many2one('project.type.custom', string='Type Projet', select=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    type2 = fields.Selection(
        [('0', 'Projets clés'), ('1', 'Projet régulier'), ('2', 'Refus de permis'), ('3', 'Incomplet'),
         ('4', 'Changement de conception'), ('5', 'Plan détaillé'), ('6', 'Projet civile'),
         ('7', 'Ingénierie locataire HQ')
            , ('8', 'Projet Permis'), ('9', 'Projet Clé')],
        string='Priority', select=True, readonly=True, states={'draft': [('readonly', False)]}, default='', )
    fact = fields.Selection([('0', 'Non Facturable'), ('1', 'Facturable')],
                            string='Facturable', select=True, readonly=True, states={'draft': [('readonly', False)]},
                            default='0', )
    ref = fields.Char(string='Nbre Poteaux', readonly=True, states={'draft': [('readonly', False)]}, )
    km = fields.Char(string='Nbre KM', readonly=True, states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Client', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    partner_id2 = fields.Many2one('res.partner', string='Customer')
    comment = fields.Char(string='Comment', readonly=True, states={'draft': [('readonly', False)]}, )
    npc = fields.Char(string='N° Project Client', readonly=True, states={'draft': [('readonly', False)]}, )
    note = fields.Text(string='Note', readonly=True, states={'draft': [('readonly', False)]}, )
    number = fields.Char(string='N°', size=64, readonly=True, states={'draft': [('readonly', False)]}, )
    analytic_account_id = fields.Many2one('account.analytic.account', string='Contract/Analytic',
                                          help="Link this project to an analytic account if you need financial "
                                               "management on projects."
                                               "It enables you to connect projects with budgets, planning, cost and "
                                               "revenue analysis, time sheets on projects, etc.",
                                          ondelete="cascade")
    affect_ids = fields.One2many('agreement.fees.amortization.line', 'project_id', string='Alias', readonly=True,
                                 states={'draft': [('readonly', False)]}, copy=True)
    progress_amount = fields.Float(string='% Dépense', compute='_get_progress_amount')
    members = fields.Many2many('res.users', 'project_user_rel', 'project_id', 'uid', 'Project Members',
                               help="Project's members are users who can have an access to the tasks related to this project.",
                               states={'close': [('readonly', True)], 'cancelled': [('readonly', True)]})
    tasks = fields.One2many('project.task', 'project_id', string='Task Activities', readonly=True,
                            states={'draft': [('readonly', False)]}, copy=True)
    hours_r = fields.Float(string='percentpie', readonly=True, compute='_get_progress_hr',
                           states={'draft': [('readonly', False)]})
    total_r = fields.Float(string='Total_r', compute='_get_sum', readonly=True,
                           states={'draft': [('readonly', False)]})
    # planned_hours = fields.function(_progress_rate, multi="progress", string='Planned Time',
    #                                  help="Sum of planned hours of all tasks related to this project and its child projects.",
    #                                  store={
    #                                      'project.project': (
    #                                          _get_project_and_parents, ['tasks', 'parent_id', 'child_ids'], 10),
    #                                      'project.task': (_get_projects_from_tasks,
    #                                                       ['planned_hours', 'remaining_hours', 'work_ids',
    #                                                        'stage_id'], 20),
    #                                  })
    # effective_hours = fields.function(_progress_rate, multi="progress", string='Time Spent',
    #                                    help="Sum of spent hours of all tasks related to this project and its child projects.",
    #                                    store={
    #                                        'project.project': (
    #                                            _get_project_and_parents, ['tasks', 'parent_id', 'child_ids'], 10),
    #                                        'project.task': (_get_projects_from_tasks,
    #                                                         ['planned_hours', 'remaining_hours', 'work_ids',
    #                                                          'stage_id'], 20),
    #                                    })
    # total_hours = fields.function(_progress_rate, multi="progress", string='Total Time',
    #                                help="Sum of total hours of all tasks related to this project and its child projects.",
    #                                store={
    #                                    'project.project': (
    #                                        _get_project_and_parents, ['tasks', 'parent_id', 'child_ids'], 10),
    #                                    'project.task': (_get_projects_from_tasks,
    #                                                     ['planned_hours', 'remaining_hours', 'work_ids',
    #                                                      'stage_id'], 20),
    #                                })
    # progress_rate = fields.function(_progress_rate, multi="progress", string='Progress', type='float',
    #                                  group_operator="avg",
    #                                  help="Percent of tasks closed according to the total of tasks todo.",
    #                                  store={
    #                                      'project.project': (
    #                                          _get_project_and_parents, ['tasks', 'parent_id', 'child_ids'], 10),
    #                                      'project.task': (_get_projects_from_tasks,
    #                                                       ['planned_hours', 'remaining_hours', 'work_ids',
    #                                                        'stage_id'], 20),
    #                                  })
    resource_calendar_id = fields.Many2one('resource.calendar', string='Working Time',
                                           help="Timetable working hours to adjust the gantt diagram report",
                                           states={'close': [('readonly', True)]})
    type_ids = fields.Many2many('project.task', 'project_task_type_rel', 'project_id', 'type_id', 'Tasks Stages',
                                readonly=True, states={'draft': [('readonly', False)]}, )
    task_count = fields.Integer(string="Number of Tasks", compute='_task_count')
    task_ids = fields.One2many('project.task', 'project_id', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    task_ids2 = fields.One2many('project.task', 'project_id')
    color = fields.Integer(string='Color Index', readonly=True, states={'draft': [('readonly', False)]}, )
    parent_id = fields.Integer(string='Parent ID', readonly=True, states={'draft': [('readonly', False)]}, )
    date = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]},
                       default=lambda *a: time.strftime('%Y-%m-%d'), )
    date_start = fields.Date(string='Date de Début', readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    date_end = fields.Date(string='Date de Livraison', readonly=True, states={'draft': [('readonly', False)]},
                           copy=True)
    date_s = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]}, )
    date_e = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]}, )
    country_id = fields.Many2one('res.country', string='Pays', readonly=True,
                                 states={'draft': [('readonly', False)]}, default=38, )
    fees_id = fields.Many2one('agreement.fees', string='Contrat lié', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    state_id = fields.Many2one('res.country.state', string='Municipalités')
    etap = fields.Char(string='Char', readonly=True, states={'draft': [('readonly', False)]}, )
    city = fields.Char(string='Région', readonly=True, states={'draft': [('readonly', False)]}, )
    ftp = fields.Char(string='Lien FTP', readonly=True, states={'draft': [('readonly', False)]}, )
    ct = fields.Float(string='CT', readonly=True, states={'draft': [('readonly', False)]}, )
    cp = fields.Float(string='CP', readonly=True, states={'draft': [('readonly', False)]}, )
    current_ph = fields.Char(string='Phase En cours', readonly=True, states={'draft': [('readonly', False)]}, )
    pourc_t = fields.Float(string='% Avancement', readonly=True, states={'draft': [('readonly', False)]}, )
    pourc_f = fields.Float(string='% Dépense', readonly=True, states={'draft': [('readonly', False)]}, )
    hours = fields.Float(string='Hours', readonly=True, states={'draft': [('readonly', False)]}, )
    total_p = fields.Float(string='Total P', readonly=True, states={'draft': [('readonly', False)]}, )
    jrs = fields.Float('JRS', readonly=True, states={'draft': [('readonly', False)]}, )
    resp_id = fields.Many2one('hr.employee', string='Chef du Project', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    total_planned = fields.Float(compute='_get_planned', string='Company Currency',
                                 readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    total_effective = fields.Float(compute='_get_effective', type='float', string='Company Currency',
                                   readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    total_remaining = fields.Float(compute='_get_remaining', string='Company Currency',
                                   readonly=True,
                                   states={'draft': [('readonly', False)]}, )
    progress_me = fields.Float(compute='_get_progress', string='Company Currency')
    # alias_model is to be removed
    # _alias_models = _get_alias_models
    # alias_model = fields.Selection(string="Alias Model", selection=_get_alias_models,
    #                                required=True,
    #                                help="The kind of document created when an email is received on this project's "
    #                                     "email alias")
    # privacy_visibility = fields.Selection(_visibility_selection, 'Privacy / Visibility', required=True,
    #                                        help="Holds visibility of the tasks or issues that belong to the current project:\n"
    #                                             "- Public: everybody sees everything; if portal is activated, portal users\n"
    #                                             "   see all tasks or issues; if anonymous portal is activated, visitors\n"
    #                                             "   see all tasks or issues\n"
    #                                             "- Portal (only available if Portal is installed): employees see everything;\n"
    #                                             "   if portal is activated, portal users see the tasks or issues followed by\n"
    #                                             "   them or by someone of their company\n"
    #                                             "- Employees Only: employees see all tasks or issues\n"
    #                                             "- Followers Only: employees see only the followed tasks or issues; if portal\n"
    #                                             "   is activated, portal users see the followed tasks or issues.")
    state = fields.Selection([('template', 'Template'),
                              ('draft', 'Brouillon'),
                              ('open', 'Confirmé'),
                              ('cancelled', 'Annulée'),
                              ('pending', 'Suspendu'),
                              ('close', 'Terminé')],
                             string='Status', required=True, copy=False, default='draft')
    zone = fields.Integer('Zone', readonly=True, states={'draft': [('readonly', False)]}, default=1, )
    work_ids = fields.One2many('project.task.work', 'project_id', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    work_line_ids = fields.One2many('project.task.work.line', 'project_id', readonly=True,
                                    states={'draft': [('readonly', False)]}, )
    academic_ids = fields.One2many('hr.academic', 'project_id', string='Academic experiences', help="Academic experiences")
    parent_id1 = fields.Many2one('project.project', string='Project Parent', select=True, ondelete='cascade',
                                 default=False, )
    child_id = fields.One2many('project.project', 'parent_id1', string='Child Categories')
    doc_count = fields.Integer(compute='_get_attached_docs', string='Number of documents attached')
    name = fields.Char(required=False, string='Nom', )
    issue_ids = fields.One2many('project.issue', 'project_id')

    _sql_constraints = [
        ('project_date_greater', 'check(date_end >= date_start)',
         'Error! Project start date must be before project end date.')
    ]

    def action_open_project(self):

        if self.is_kit is True:
            return {
                'name': ('Consulter Projet'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('project_custom.view_custom_project_form').id,
                'target': 'current',
                'res_model': 'project.project',
                'res_id': self.ids[0],
                'flags': {'initial_mode': 'edit'},
                'context': {},
                'domain': []
            }
        else:
            return {
                'name': ('Consulter Projet'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': self.env.ref('project_custom.view_kit_false').id,
                'target': 'current',
                'res_model': 'project.project',
                'res_id': self.ids[0],
                'context': {},
                'domain': [],
                'flags': {'initial_mode': 'edit'},
            }

    def set_compute2(self):
        task_obj = self.env['project.task']
        for project in self:
            compteur = 0
            etape = ''
            task_ids_ord = task_obj.search([('project_id', '=', project.id)], order='sequence,id').ids
            for task_id in task_ids_ord:
                task = task_obj.browse(task_id)
                if task.dc:
                    if 'Etap' in task.dc:
                        compteur = (compteur - (compteur % 10000)) + 10000
                        etape = task.dc
                    else:
                        if compteur < 10000:
                            compteur = 10000 + compteur + 10
                        else:
                            compteur = compteur + 100
                    task.write(
                        {'sequence': compteur, 'etape': etape, 'state_id': project.state_id.id, 'city': project.city})
                else:
                    if 'Etap' in task.name:
                        compteur = (compteur - (compteur % 10000)) + 10000
                        etape = task.name
                    else:
                        if compteur < 10000:
                            compteur = 10000 + compteur + 10
                        else:
                            compteur = compteur + 100
                    task.write({'sequence': compteur, 'etape': etape, 'dc': task.name, 'state_id': project.state_id.id,
                                'city': project.city})
        return True

    def set_open2(self):

        return self.write({'state': 'draft'})

    def set_done(self):
        self.env.cr.execute('update project_task_work set  ex_state=state where project_id =%s', (self.ids[0],))
        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('close', self.ids[0]))
        self.env.cr.execute('update project_task_work set  state=%s where project_id =%s', ('valid', self.ids[0]))
        return self.write({'state': 'close'})

    def set_open(self):

        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('draft', self.ids[0]))
        self.env.cr.execute('update project_task_work set  state=%s where project_id =%s', ('draft', self.ids[0]))
        self.write({'state': 'draft'})
        if self.is_kit is True:
            return {
                'name': ('Gestion Projet'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'project.project',
                'res_id': self.ids[0],
                'view_id': self.env.ref('project_custom.view_custom_project_form').id,
                'context': {},
                'domain': []
            }
        else:
            return {
                'name': ('Gestion Projet'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
                'res_model': 'project.project',
                'res_id': self.ids[0],
                'view_id': self.env.ref('project_custom.view_kit_false').id,
                'context': {},
                'domain': []
            }

    def set_pending(self):
        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('pending', self.ids[0]))
        self.env.cr.execute('update project_task_work set  state=%s where project_id =%s', ('pending', self.ids[0]))
        return self.write({'state': 'pending'})

    def set_cancel(self):

        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('cancelled', self.ids[0]))
        return self.write({'state': 'cancelled'})

    def set_reopen(self):

        self.env.cr.execute('update project_project set  state=%s where id =%s', ('open', self.ids[0]))
        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('open', self.ids[0]))
        self.env.cr.execute('update project_task_work set  state=%s where project_id =%s', ('tovalid', self.ids[0]))
        return True

    def set_validate(self):

        self.set_compute2()
        self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('open', self.ids[0]))
        self.env.cr.execute('update project_task set  partner_id=%s where project_id =%s',
                            (self.partner_id.id, self.ids[0]))
        task_obj_line = self.env['project.task.work']
        self.write({'state': 'open'})

        for project in self:
            self.env.cr.execute(
                "select cast(substr(number, 5, 7) as integer) from project_project where number is not Null and EXTRACT(YEAR FROM date)=%s and parent_id1 is Null and state<>'draft' AND position('-' in number) = 0 order by cast(number as integer) desc limit 1",
                (str(project.date.year),))
            q3 = self.env.cr.fetchone()
            if q3:
                res1 = q3[0] + 1
            else:
                res1 = '001'
            ct = 0

            if not project.number:
                self.write({'number': str(str(project.date.year) + str(str(res1).zfill(3))),
                            'name': str(str(project.date.year) + ' - ' + str(str(res1).zfill(3)))})

            for task in project.task_ids:

                if project.date_s:

                    if not task.date_start:
                        self.env['project.task'].write({'date_start': project.date_s})

                if project.date_e:
                    if not task.date_end:
                        self.env['project.task'].write({'date_end': project.date_e})

                if not task.date_start or not task.date_end:
                    raise UserError(_('Erreur ! Vous devez avoir une date de début et une date de fin pour chaque '
                                      'tâche ! - %s !') % (task.name))

                tt = task_obj_line.search([('project_id', '=', project.id), ('task_id', '=', task.id)], order='id')
                if not tt:
                    if not task.priority:
                        self.env['project.task'].write({'priority': project.priority,
                                                        'state_id': project.state_id.id or False,
                                                        'city': project.city})
                    if task.kit_id:
                        for hh in task.kit_id.type_ids.ids:
                            pr = self.env['product.product'].browse(hh)
                            if pr.is_load is True:
                                self.env['project.task.work'].create({
                                    'task_id': task.id,
                                    'categ_id': task.categ_id.id,
                                    'product_id': pr.id,
                                    'name': task.kit_id.name,
                                    'date_start': task.date_start,
                                    'date_end': task.date_end,
                                    'poteau_t': task.qte,
                                    'poteau_i': task.qte,
                                    'color': task.color,
                                    'etape': task.etape,
                                    'zone': 0,
                                    'secteur': 0,
                                    'total_t': task.color * 7,
                                    'hours': task.color * 7,
                                    'project_id': task.project_id.id,
                                    'partner_id': task.project_id.partner_id.id,
                                    # 'planned_hours': task.color * 7,
                                    'state_id': project.state_id.id or False,
                                    'city': project.city,
                                    'gest_id': task.reviewer_id.id or False,
                                    'reviewer_id1': task.reviewer_id1.id or False,
                                    'coordin_id1': task.coordin_id1.id or False,
                                    'coordin_id2': task.coordin_id2.id or False,
                                    'coordin_id3': task.coordin_id3.id or False,
                                    'coordin_id4': task.coordin_id4.id or False,
                                    'uom_id': pr.uom_id.id,
                                    'uom_id_r': pr.uom_id.id,
                                    'ftp': task.ftp,
                                    'kit_id': task.kit_id.id,
                                    'state': 'draft',
                                    'sequence': task.sequence,
                                    'display': True,
                                    'active': True,
                                    'gest_id3': task.coordin_id.id or False,
                                    'current_gest': task.coordin_id.id or False,
                                    'current_sup': task.reviewer_id.id or False,

                                })

                    elif int(task.rank) > 0 and int(task.rank) < 2:
                        if not 'Etape' in task.product_id.name and task.product_id.is_load:
                            ct = ct + (task.color * 7)
                            self.env['project.task.work'].create({
                                'task_id': task.id,
                                'categ_id': task.categ_id.id,
                                'product_id': task.product_id.id,
                                'name': task.name,
                                'date_start': task.date_start,
                                'date_end': task.date_end,
                                'poteau_t': task.qte,
                                'poteau_i': task.qte,
                                'color': task.color,
                                'etape': task.etape,
                                'zone': 0,
                                'secteur': 0,
                                'total_t': task.color * 7,
                                'hours': task.color * 7,
                                'project_id': task.project_id.id,
                                'partner_id': task.project_id.partner_id.id,
                                # 'planned_hours': task.color * 7,
                                'state_id': project.state_id.id or False,
                                'city': project.city,
                                'gest_id': task.reviewer_id.id or False,
                                'reviewer_id1': task.reviewer_id1.id or False,
                                'coordin_id1': task.coordin_id1.id or False,
                                'coordin_id2': task.coordin_id2.id or False,
                                'coordin_id3': task.coordin_id3.id or False,
                                'coordin_id4': task.coordin_id4.id or False,
                                'uom_id': task.uom_id.id,
                                'uom_id_r': task.uom_id.id,
                                'ftp': task.ftp,
                                'state': 'draft',
                                'sequence': task.sequence,
                                'display': True,
                                'active': True,
                                'gest_id3': task.coordin_id.id or False,
                                'current_gest': task.coordin_id.id or False,
                                'current_sup': task.reviewer_id.id or False,

                            })
                    else:
                        if not 'Etape' in task.product_id.name and task.product_id.is_load:
                            ct = ct + (task.color * 7)
                            self.env['project.task.work'].create({
                                'task_id': task.id,
                                'categ_id': task.categ_id.id,
                                'product_id': task.product_id.id,
                                'name': task.name,
                                'date_start': task.date_start,
                                'date_end': task.date_end,
                                'poteau_t': task.qte,
                                'poteau_i': task.qte,
                                'color': task.color,
                                'zone': 0,
                                'secteur': 0,
                                'etape': task.etape,
                                'total_t': task.color * 7,
                                'hours': task.color * 7,
                                'project_id': task.project_id.id,
                                'partner_id': task.project_id.partner_id.id,
                                # 'planned_hours': task.color * 7,
                                'state_id': project.state_id.id or False,
                                'city': project.city,
                                'gest_id': task.reviewer_id.id or False,
                                'reviewer_id1': task.reviewer_id1.id or False,
                                'coordin_id1': task.coordin_id1.id or False,
                                'coordin_id2': task.coordin_id2.id or False,
                                'coordin_id3': task.coordin_id3.id or False,
                                'coordin_id4': task.coordin_id4.id or False,
                                'uom_id': task.uom_id.id,
                                'uom_id_r': task.uom_id.id,
                                'ftp': task.ftp,
                                'state': 'draft',
                                'sequence': task.sequence,
                                'display': False,
                                'active': True,
                                'gest_id3': task.coordin_id.id or False,
                                'current_gest': task.coordin_id.id or False,
                                'current_sup': task.reviewer_id.id or False,
                            })

            self.write({'ct': ct})
        return True

    def set_apply_partner(self):

        if self.partner_id2:
            self.env.cr.execute('update project_task_work_line set  partner_id=%s where project_id =%s',
                                (self.partner_id2.id, self.ids[0]))
            self.env.cr.execute('update project_task_work set  partner_id=%s where project_id =%s',
                                (self.partner_id2.id, self.ids[0]))
            self.env.cr.execute('update project_task set  partner_id=%s where project_id =%s',
                                (self.partner_id2.id, self.ids[0]))

            return self.write({'partner_id': self.partner_id2.id})

    def set_force_open(self):

        if self.state == 'close':
            self.env.cr.execute('update project_task_work set  state=ex_state where project_id =%s', (self.ids[0],))
            self.env.cr.execute('update project_task set  state=%s where project_id =%s', ('open', self.ids[0]))

    @api.onchange('date')
    def onchange_date(self):
        result = {'value': {}}
        if self.date:
            self.env.cr.execute(
                "select cast(substr(number, 5, 7) as integer) from project_project where number is not Null and EXTRACT(YEAR FROM date)=%s and parent_id1 is Null  AND position('-' in number) = 0 order by cast(number as integer) desc limit 1",
                (self.date.year,))
            q3 = self.env.cr.fetchone()

            if q3:
                res1 = q3[0] + 1
            else:
                res1 = '001'
            result['value']['number'] = str(str(self.date.year) + str(str(res1).zfill(3)))
            result['value']['name'] = str(str(self.date.year) + ' - ' + str(str(res1).zfill(3)))
        return result

    @api.onchange('state_id')
    def onchange_munic(self):
        if self.state_id:
            state_obj = self.env['res.country.state']
            state = state_obj.browse(self.state_id.id)
            return {'value': {'city': state.region}}
        return {}


class AgreementFeesAmortizationLine(models.Model):
    _name = "agreement.fees.amortization.line"
    project_id = fields.Many2one('project.project', string='project ID')


class AgreementFees(models.Model):
    _name = "agreement.fees"


class ProjectTypeCustom(models.Model):
    _name = "project.type.custom"
    name = fields.Char(string='Type du Projet')


class ProjectIssue(models.Model):
    _name = "project.issue"
    project_id = fields.Many2one('project.project')
    name = fields.Char()
    task_id = fields.Char()
    work_id = fields.Char()
    state = fields.Char()
