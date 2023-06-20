# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCountry(models.Model):
    _inherit = 'res.country'
    image = fields.Binary(string='image')


class ResCountryState(models.Model):
    _inherit = 'res.country.state'
    code = fields.Char(required=False)
    country_id = fields.Many2one('res.country', required=False)