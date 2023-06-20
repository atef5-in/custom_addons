# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCountry(models.Model):
    _inherit = 'res.country'
    image = fields.Binary(string='image')


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    country_id = fields.Many2one('res.country', string='Country', required=True, default=38)
    region_id = fields.Many2one('res.country.group', string='Region', required=True)
    name = fields.Char(string='State Name', required=True,
                       help='Administrative divisions of a country. E.g. Fed. State, Departement, Canton')
    code = fields.Char(string='State Code', size=3,
                       help='The state code in max. three chars.', required=True)
    secteur = fields.Char(string='State Code', size=3, )
    gest = fields.Char(string='State Code')
    sect_usag = fields.Char(string='State Code')
    usag = fields.Char(string='State Code')
    c_munic = fields.Char(string='State Code')
    n_munic = fields.Char(string='State Code')
    c_a_city = fields.Char(string='State Code')
    n_a_city = fields.Char(string='State Code')
    region = fields.Char(string='State Code')
    mrc = fields.Char(string='State Code')
