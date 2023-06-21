# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'
    employee_id = fields.Many2one('hr.employee', readonly=False)

