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


# from openerp.osv.orm import setup_modifiers


class ProjectCustom(models.Model):
    _description = 'custom project'
    _inherit = ['project.project']
    _inherits = {
        'mail.alias': 'alias_id',
    }

    # _get_progress_hr
    def _compute_progress_hr(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s and state in ('valid','paid') GROUP BY project_id",
            (tuple(ids),))
        data = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.hours > 0:
                ratio = data.get(rec.id, 0.0) / rec.hours
            else:
                ratio = data.get(rec.id, 0.0)
            result[rec.id] = round(min(100.0 * ratio, 100), 2)
        return result

    # _get_progress_amount
    def _compute_progress_amount(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s and state in ('valid','paid') GROUP BY project_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            if rec.ct > 0:
                ratio = hours.get(rec.id, 0.0) / rec.ct
            else:
                ratio = hours.get(rec.id, 0.0)
            result[rec.id] = round(min(100.0 * ratio, 100), 2)
        return result

    # _get_planned
    def _compute_total_planned(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.project_id IN %s GROUP BY project_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            result[rec.id] = hours.get(rec.id, 0.0)
        return result

    # _get_effective
    def _compute_total_effective(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_effective), 0.0) FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())

        for rec in self:
            result[rec.id] = hours.get(rec.id, 0.0)
        return result

    # _get_remaining
    def _compute_total_remaining(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_remaining), 0.0) FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            result[rec.id] = hours.get(rec.id, 0.0)
        return result

    # _get_sum
    def _compute_total_r(self, cr, uid, ids, field_name, arg, context=None):
        result = {}
        self.env.cr.execute(
            "SELECT project_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.project_id IN %s GROUP BY project_id",
            (('valid', 'paid'), tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            result[rec.id] = hours.get(rec.id, 0.0)
        return result

    # _get_attached_docs
    def _compute_attached_docs(self, cr, uid, ids, field_name, arg, context):
        res = {}
        attachment = self.env['ir.attachment']
        task = self.env['project.task']
        for id in ids:
            project_attachments = attachment.search(cr, uid,
                                                    [('res_model', '=', 'project.project'), ('res_id', '=', id)],
                                                    context=context, count=True)
            task_ids = task.search(cr, uid, [('project_id', '=', id)], context=context)
            task_attachments = attachment.search(cr, uid,
                                                 [('res_model', '=', 'project.task'), ('res_id', 'in', task_ids)],
                                                 context=context, count=True)
            res[id] = (project_attachments or 0) + (task_attachments or 0)
        return res

    # _task_count
    # def _compute_task_count(self):
    #     res = {}
    #     for tasks in self:
    #         res[tasks.id] = len(tasks.task_ids)
    #     return res

    # _get_progress
    def compute_progress_me(self, cr, uid, ids, field_name, arg, context=None):
        result = {}

        self.env.cr.execute(
            "SELECT project_id, CASE WHEN SUM(total_planned) >0 Then COALESCE(SUM(total_effective)/SUM(total_planned), 0.0)  else COALESCE(SUM(total_effective), 0.0) end FROM project_task WHERE project_task.project_id IN %s GROUP BY project_id",
            (tuple(ids),))
        hours = dict(self.env.cr.fetchall())
        if hours:
            for rec in self:
                result[rec.id] = round(min(100.0 * hours.get(rec.id, 0.0), 99.99), 2)
        return result

    @api.depends_context('uid')
    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('om_hospital.group_super_admin')

    @api.depends_context('uid')
    def _compute_is_admin(self):
        for record in self:
            record.is_admin = self.env.user.has_group('om_hospital.group_admin')

    is_super_admin = fields.Boolean(string='Super Admin', compute='_compute_is_super_admin')
    is_admin = fields.Boolean(string='Is Admin', compute='_compute_is_admin')
    active = fields.Boolean(string='Active', readonly=True, states={'draft': [('readonly', False)]}, )
    is_kit = fields.Boolean(string='Is Kit', readonly=True, states={'draft': [('readonly', False)]}, )
    priority = fields.Selection([('0', 'Faible'), ('1', 'Normale'), ('2', 'Elevée')], 'Priority', select=True,
                                readonly=True, states={'draft': [('readonly', False)]}, )
    sequence = fields.Integer(string='Sequence', help="Gives the sequence order when displaying a list of Projects.",
                              readonly=True, states={'draft': [('readonly', False)]}, )
    bord = fields.Char(string='Bord', readonly=True, states={'draft': [('readonly', False)]}, )
    type3 = fields.Many2one('project.type.custom', string='Type projet', select=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    type2 = fields.Selection(
        [('0', 'Projets clés'), ('1', 'Projet régulier'), ('2', 'Refus de permis'), ('3', 'Incomplet'),
         ('4', 'Changement de conception'), ('5', 'Plan détaillé'), ('6', 'Projet civile'),
         ('7', 'Ingénierie locataire HQ')
            , ('8', 'Projet Permis'), ('9', 'Projet Clé')],
        'Priority', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    fact = fields.Selection([('0', 'Non Facturable'), ('1', 'Facturable')],
                            'Priority', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    ref = fields.Char(string='Reference', readonly=True, states={'draft': [('readonly', False)]}, )
    km = fields.Char(string='Km', readonly=True, states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    partner_id2 = fields.Many2one('res.partner', string='Customer')
    comment = fields.Char(string='Comment', readonly=True, states={'draft': [('readonly', False)]}, )
    npc = fields.Char(string='NPC', readonly=True, states={'draft': [('readonly', False)]}, )
    note = fields.Text(string='Note', readonly=True, states={'draft': [('readonly', False)]}, )
    number = fields.Char(string='Number', size=64, readonly=True, states={'draft': [('readonly', False)]}, )
    analytic_account_id = fields.Many2one('account.analytic.account', string='Contract/Analytic',
                                          help="Link this project to an analytic account if you need financial "
                                               "management on projects."
                                               "It enables you to connect projects with budgets, planning, cost and "
                                               "revenue analysis, time sheets on projects, etc.",
                                          ondelete="cascade")
    affect_ids = fields.One2many('agreement.fees.amortization.line', 'project_id', string='Alias', readonly=True,
                                 states={'draft': [('readonly', False)]}, copy=True)
    # progress_amount = fields.Float(string='Progress Amount', compute='_compute_progress_amount')
    members = fields.Many2many('res.users', 'project_user_rel', 'project_id', 'uid', 'Project Members',
                               help="Project's members are users who can have an access to the tasks related to this project.",
                               states={'close': [('readonly', True)], 'cancelled': [('readonly', True)]})
    tasks = fields.One2many('project.task', 'project_id', string='Task Activities', readonly=True,
                            states={'draft': [('readonly', False)]}, copy=True)
    # hours_r = fields.Float(string='Hours_r', readonly=True, compute='_compute_progress_hr',
    #                        states={'draft': [('readonly', False)]})
    # total_r = fields.Float(string='Total_r', compute='_compute_total_r', readonly=True,
    #                        states={'draft': [('readonly', False)]})
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
    # task_count = fields.Integer(string="Number of Tasks", compute='_compute_task_count')
    task_ids = fields.One2many('project.task', 'project_id', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    task_ids2 = fields.One2many('project.task', 'project_id')
    color = fields.Integer(string='Color Index', readonly=True, states={'draft': [('readonly', False)]}, )
    parent_id = fields.Integer(string='Parent ID', readonly=True, states={'draft': [('readonly', False)]}, )
    date = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]}, )
    # date_start = fields.Date(string='Start Date', readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    # date_end = fields.Date(string='End Date', readonly=True, states={'draft': [('readonly', False)]}, copy=True)
    date_s = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]}, )
    date_e = fields.Date(string='date', readonly=True, states={'draft': [('readonly', False)]}, )
    # alias_id has the same definition in project.project
    # alias_id = fields.Many2one('mail.alias', string='Alias', ondelete="restrict", required=True,
    #                            help="Internal email associated with this project. Incoming emails are automatically "
    #                                 "synchronized"
    #                                 "with Tasks (or optionally Issues if the Issue Tracker module is installed).")
    country_id = fields.Many2one('res.country', string='Country ID', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    fees_id = fields.Many2one('agreement.fees', string='Fees ID', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    r_id = fields.Many2one('risk.management.category', string='R ID', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    state_id = fields.Many2one('res.country.state', string='Alias')
    etap = fields.Char(string='Char', readonly=True, states={'draft': [('readonly', False)]}, )
    city = fields.Char(string='City', readonly=True, states={'draft': [('readonly', False)]}, )
    ftp = fields.Char(string='FTP', readonly=True, states={'draft': [('readonly', False)]}, )
    ct = fields.Float(string='CT', readonly=True, states={'draft': [('readonly', False)]}, )
    cp = fields.Float(string='CP', readonly=True, states={'draft': [('readonly', False)]}, )
    current_ph = fields.Char(string='Phase En cours', readonly=True, states={'draft': [('readonly', False)]}, )
    pourc_t = fields.Float(string='% Avancement', readonly=True, states={'draft': [('readonly', False)]}, )
    pourc_f = fields.Float(string='% Dépense', readonly=True, states={'draft': [('readonly', False)]}, )
    hours = fields.Float(string='Hours', readonly=True, states={'draft': [('readonly', False)]}, )
    total_p = fields.Float(string='Total P', readonly=True, states={'draft': [('readonly', False)]}, )
    jrs = fields.Float('JRS', readonly=True, states={'draft': [('readonly', False)]}, )
    resp_id = fields.Many2one('hr.employee', string='Resp ID', readonly=True, states={'draft': [('readonly', False)]}, )
    # total_planned = fields.Float(compute='_compute_total_planned', string='Company Currency',
    #                              readonly=True,
    #                              states={'draft': [('readonly', False)]}, )
    # total_effective = fields.Float(compute='_compute_total_effective', type='float', string='Company Currency',
    #                                readonly=True,
    #                                states={'draft': [('readonly', False)]}, )
    # total_remaining = fields.Float(compute='_compute_total_remaining', string='Company Currency',
    #                                readonly=True,
    #                                states={'draft': [('readonly', False)]}, )
    # progress_me = fields.Float(compute='compute_progress_me', string='Company Currency')
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
    zone = fields.Integer('Zone', readonly=True, states={'draft': [('readonly', False)]}, )
    # work_ids = fields.One2many('project.task.work', 'project_id', readonly=True,
    #                            states={'draft': [('readonly', False)]}, )
    # work_line_ids = fields.One2many('project.task.work.line', 'project_id', readonly=True,
    #                                 states={'draft': [('readonly', False)]}, )
    academic_ids = fields.One2many('hr.academic', 'project_id', 'Academic experiences', help="Academic experiences")
    parent_id1 = fields.Many2one('project.project', string='Parent Category', select=True, ondelete='cascade')
    child_id = fields.One2many('project.project', 'parent_id1', string='Child Categories')
    # need to check whether we can have the same ID or not
    # doc_count = fields.Integer(compute='_compute_attached_docs', string='Number of documents attached')


class AgreementFeesAmortizationLine(models.Model):
    _name = "agreement.fees.amortization.line"
    project_id = fields.Many2one('project.project', string='project ID')


class HrAcademic(models.Model):
    _name = "hr.academic"
    project_id = fields.Many2one('project.project', string='project ID')


class AgreementFees(models.Model):
    _name = "agreement.fees"


class RiskManagementCategory(models.Model):
    _name = "risk.management.category"


class ProjectTypeCustom(models.Model):
    _name = "project.type.custom"
