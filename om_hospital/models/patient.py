# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hospital Patient'

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    active = fields.Boolean(string='Active', default=True)
    doc_ids = fields.Many2many('hospital.doctor', string='Control Doctors')
    user_id = fields.Many2one('res.users', string='User')
