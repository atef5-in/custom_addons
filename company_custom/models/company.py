# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    tps = fields.Char(string='TPS')
    tvq = fields.Char(string='TVQ')
