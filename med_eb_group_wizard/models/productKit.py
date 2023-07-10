# -*- coding: utf-8 -*-

from lxml import etree
# from openerp import models, fields, api, _
from odoo import models, fields, api, _
# from odoo.osv import osv
from odoo.exceptions import ValidationError
from datetime import datetime
import datetime as dt
import math


class productKit(models.Model):
    _name = "product.kit"
    _description = "product kit"

    kit_id = fields.Char(string="KIT ID")
