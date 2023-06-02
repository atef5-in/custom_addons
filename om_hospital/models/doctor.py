# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalPatient(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hospital doctor'

    name = fields.Char(string='Name',tracking=True)
    ref = fields.Char(string='Reference', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male','Male'),('female','Female')], string='Gender')
    active = fields.Boolean(string='Active', default=True)