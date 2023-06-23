# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'
    employee_id = fields.Many2one('hr.employee', readonly=False)


class UsersRole(models.Model):
    _name = 'res.users.role'
    group_id = fields.Many2one('res.groups', string=u"Associated group")
    line_ids = fields.One2many('res.users.role.line', 'role_id', string=u"Users")
    employee_ids = fields.Many2many('hr.employee', 'employee_role_rel', 'role_id', 'employee_id', string=u"User")
    currency_id = fields.Many2one('res.currency', default=5, string=u"Associated group")
    amount = fields.Float(string=u"Associated group")
    name = fields.Char(string=u"Name")
    partner_id = fields.Many2one('res.partner', string=u"Associated group")
    project_id = fields.Many2one('project.project', string=u"Associated group")
    agreement_id = fields.Many2one('agreement.fees', string=u"Associated group")
    state = fields.Selection([('draft', 'Brouillon'), ('done', 'Validé'), ], string='Type', default='draft')

    def set_validate(self):
        return self.write({'state': 'done'})

    def set_draft(self):
        return self.write({'state': 'draft'})


class ResUsersRoleLine(models.Model):
    _name = 'res.users.role.line'
    _description = 'Users associated to a role'

    role_id = fields.Many2one('res.users.role', string=u"Role", ondelete='cascade')
    date_from = fields.Date(string=u"From")
    date_to = fields.Date(string=u"To")
    is_enabled = fields.Boolean(string=u"Enabled", )



