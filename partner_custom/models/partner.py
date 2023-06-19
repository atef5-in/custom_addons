# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    image = fields.Binary(string='Image',
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
    ean13 = fields.Char(string='EAN13', size=13)
    use_parent_address = fields.Boolean(string='Use Company Address',
                                        help="Select this if you want to set company's address information  for this "
                                             "contact")
    fax = fields.Char(string='Fax')

