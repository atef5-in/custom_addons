# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalMedicament(models.Model):
    _name = 'hospital.medicament'
    _description = 'hospital medicament'

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference', required=True)
    price_unit = fields.Integer(string='Price unit')
