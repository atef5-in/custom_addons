# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date


# class TaskWorkLine(models.Model):
#     _name = 'project.task.work.line'
#     _description = 'Project Task Work Line'
#
#     # @api.depends_context('uid')
#     # def _compute_is_super_admin(self):
#     #     for record in self:
#     #         record.is_super_admin = self.env.user.has_group('om_hospital.group_super_admin')
#
#     # is_super_admin = fields.Boolean(string='Super Admin', compute='_compute_is_super_admin', method=True)
#     name = fields.Char(string='Project')
#     ftp = fields.Char(string='ftp', )
#     date = fields.Datetime(string='Date', select="1")
#     date_r = fields.Datetime(string='Date', select="1", states={'affect': [('readonly', False)]}, )
#     work_id = fields.Many2one('project.task.work', string='Task Work')
#     work_id2 = fields.Many2one('project.task.work', string='Event')
#     wizard_id = fields.Many2one('base.invoice.merge.automatic.wizard', string='Event')
#     date_start = fields.Date(string='Date', select="1")
#     date_end = fields.Date(string='Date', select="1")
#     date_start_r = fields.Date(string='Date', select="1")
#     date_end_r = fields.Date(string='Date', select="1")
#     employee_id = fields.Many2one('hr.employee', string='Employee')
#     project_id = fields.Many2one('project.project', 'Project')
#     task_id = fields.Many2one('project.task', string='Task', select="1")
#     product_id = fields.Many2one('product.product', string='Task', )
#     hours = fields.Float(string='Time Spent')
#     hours_r = fields.Float(string='Time Spent')
#     total_t = fields.Float(string='Time Spent', states={'affect': [('readonly', False)]}, )
#     total_r = fields.Float(string='Time Spent', states={'affect': [('readonly', False)]}, )
#     poteau_t = fields.Float(string='Time Spent', states={'affect': [('readonly', False)]}, )
#     poteau_r = fields.Float(string='Time Spent')
#     poteau_reste = fields.Float(string='Time Spent', states={'affect': [('readonly', False)]}, )
#     total_part = fields.Selection([
#         ('partiel', 'Partiel'),
#         ('total', 'Total'),
#     ],
#         string='Status', copy=False, readonly=True, states={'affect': [('readonly', False)]}, )
#     etape = fields.Char('etap', readonly=True, states={'draft': [('readonly', False)]}, )
#     sequence = fields.Integer(string='Sequence', select=True, states={'affect': [('readonly', False)]}, )
#     zone = fields.Integer(string='Color Index', states={'affect': [('readonly', False)]}, )
#     secteur = fields.Integer(string='Color Index', states={'affect': [('readonly', False)]}, )
#     user_id = fields.Many2one('res.users', string='Done by', select="1",
#                               readonly=True, states={'affect': [('readonly', False)]}, )
#     paylist_id = fields.Many2one('hr.payslip', 'Done by', select="1", readonly=True,
#                                  states={'affect': [('readonly', False)]}, )
#     gest_id = fields.Many2one('hr.employee', string='Superviseur', states={'affect': [('readonly', False)]}, )
#     partner_id = fields.Many2one('res.partner', string='Superviseur', readonly=True,
#                                  states={'affect': [('readonly', False)]}, )
#     issue_ids = fields.One2many('project.issue.version', 'works_id', string='Work done', readonly=True,
#                                 states={'affect': [('readonly', False)]}, )
#     issue_id = fields.Many2one('project.issue', 'Done by', select="1", readonly=True,
#                                states={'affect': [('readonly', False)]}, )
#     state = fields.Selection([
#         ('draft', 'Brouillon'),
#         ('tovalid', 'Dde Validation'),
#         ('valid', 'Bons Validés'),
#         ('paid', 'Bons Facturés'),
#         ('cancel', 'T. Annulés'),
#         ('pending', 'T. Suspendus'),
#         ('close', 'Traité')
#     ],
#         string='Status', copy=False)
#     categ_id = fields.Many2one('product.category', string='Tags', readonly=True,
#                                states={'affect': [('readonly', False)]}, )
#     note = fields.Text(string='Work summary', readonly=True, states={'affect': [('readonly', False)]}, )
#     done = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
#     done1 = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
#     done2 = fields.Boolean(string='is done', readonly=True, states={'affect': [('readonly', False)]}, )
#     done3 = fields.Boolean(string='is done')
#     done4 = fields.Boolean(string='is done')
#     auto = fields.Boolean(string='is done')
#     group_id = fields.Many2one('bon.show', string='Done by', select="1", readonly=False,  # readonly=True,
#                                states={'affect': [('readonly', False)]}, )
#     group_id2 = fields.Many2one('base.group', 'Done by', select="1", readonly=True,
#                                 states={'affect': [('readonly', False)]}, )
#     facture = fields.Boolean(string='Facture', readonly=True, states={'affect': [('readonly', False)]}, )
#     date_inv = fields.Date(string='Date', select="1")
#     num = fields.Char(string='Work summary', readonly=True, states={'affect': [('readonly', False)]}, )
#     color = fields.Integer(string='Color', states={'affect': [('readonly', False)]}, )
#     color1 = fields.Integer(string='Color 1', states={'affect': [('readonly', False)]}, )
#     uom_id = fields.Many2one('product.uom', states={'affect': [('readonly', False)]}, )
#     uom_id_r = fields.Many2one('product.uom', string='Unit of Measure', readonly=True,
#                                states={'affect': [('readonly', False)]}, )
#     wage = fields.Integer(string='T.H')
#     total = fields.Integer(string='Total')
#     rentability = fields.Float(string='Rentabilité')
#     taux_horaire = fields.Float(string='T.H')
#
#
# class ProjectIssueVersion(models.Model):
#     _name = "project.issue.version"
#     works_id = fields.Many2one('project.project', string='Work ID')
#
#
# class RiskManagementCategory(models.Model):
#     _name = "risk.management.category"
#     name = fields.Char()
#
#
# class ProductCategory(models.Model):
#     _name = "product.category"
#     name = fields.Char('Name')
#
#
# # class ProductKit(models.Model):
# #     _name = "product.kit"
# #     name = fields.Char('Name')
#
#
# class ProjectStatus(models.Model):
#     _name = "project.status"
#     name = fields.Char('Name')
#
#
# class LinkType(models.Model):
#     _name = "link.type"
#     work_id = fields.Many2one('project.task.work', string='project ID')
#
#     ftp = fields.Char()
#     name = fields.Char()
#     source = fields.Char()
#
#
# class HrPayslip(models.Model):
#     _name = "hr.payslip"
#     name = fields.Char('Name')
#
#
# class BonShow(models.Model):
#     _name = "bon.show"
#     name = fields.Char('Name')
#
#     group_id = fields.Integer(string='Done by', select="1", readonly=False)
#
#
# class ProjectIssue(models.Model):
#     _name = "project.issue"
#     name = fields.Char('Name')
#
#
# class ProductUOM(models.Model):
#     _name = "product.uom"
#     name = fields.Char('Name')
#
#
# class BaseTaskMergeAutomaticWizard(models.Model):
#     _name = "base.task.merge.automatic.wizard"
#     name = fields.Char('Name')
#
#
# class BaseGroup(models.Model):
#     _name = "base.group"
#     name = fields.Char('Name')
#
#
# class BaseInvoiceMergeAutomaticWizard(models.Model):
#     _name = "base.invoice.merge.automatic.wizard"
#     name = fields.Char('Name')
#
#
class WorkHisto(models.Model):
    _name = "work.histo"
    name = fields.Char('Name')

    work_id = fields.Char(string='work ID')
    task_id = fields.Char(string='task_id', select="1")
    categ_id = fields.Char(string='categ_id', select="1")
    project_id = fields.Char(string='project_id', select="1")
    partner_id = fields.Char(string='partner_id', select="1")
    # line_ids = fields.One2many('project.task.work.', 'work_id', string='Work done')
    product_id = fields.Char(string='product_id', select="1")
    date = fields.Datetime(string='Date', select="1")
    create_a = fields.Datetime(string='Date', select="1")
    zone = fields.Integer(string='Zone (entier)', states={'draft': [('readonly', False)]}, )
    secteur = fields.Integer(string='Zone (entier)', states={'draft': [('readonly', False)]}, )


class WorkHistoLine(models.Model):
    _name = "work.histo.line"

    name = fields.Char('Name')
    type = fields.Char(string='work ID')
    create_by = fields.Char(string='task_id', select="1")
    work_histo_id = fields.Char(string='categ_id', select="1")
    date = fields.Datetime(string='Date', select="1")
    coment1 = fields.Char(string='partner_id', select="1")
    id_object = fields.Char(string='product_id', select="1")


# from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError
#
#
# class Department(models.Model):
#     _name = "hr.academic"
#     _description = "Academic"
#     _order = "name"
#
#     name = fields.Char(string='Name field in hr acadmic')
#     employee_id = fields.Many2one('hr.employee', string='Employee')
#     categ_id = fields.Many2one('product.category', string='Wizard')
#
# # class BonShow(models.Model):
# #     _name = "bon.show"
# #     _description = "Bon Show"
