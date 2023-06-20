# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _

ADDRESS_FIELDS = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _has_image(self):
        for record in self:
            record.has_image = bool(record.image)

    image = fields.Binary(string='Image',
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
    ean13 = fields.Char(string='EAN13', size=13)
    use_parent_address = fields.Boolean(string='Use Company Address',
                                        help="Select this if you want to set company's address information  for this "
                                             "contact")
    fax = fields.Char(string='Fax')
    street2 = fields.Char(string='Street2')
    customer = fields.Boolean(string='Customer', help="Check this box if this contact is a customer.")
    supplier = fields.Boolean(string='Supplier',
                              help="Check this box if this contact is a supplier. If it's not checked, purchase "
                                   "people will not see it when encoding a purchase order.")
    comment = fields.Text('Notes')
    has_image = fields.Boolean(compute='_has_image', string='image ?')
    notify_email = fields.Selection([
        ('none', 'Jamais'),
        ('no', 'Tous les messages'),
    ],
        string='Email ?', required=True, )
    lat = fields.Float(string=u'Latitude', digits=(9, 6))
    lng = fields.Float(string=u'Longitude', digits=(9, 6))
    map = fields.Text()
    partner_latitude = fields.Float(string='Geo Latitude')
    partner_longitude = fields.Float(string='Geo Longitude')
    date_localization = fields.Date(string='Geo Localization Date')
    opt_out = fields.Boolean(string='Opt-Out')

    @api.onchange('use_parent_address', 'parent_id')
    def onchange_address(self):
        def value_or_id(val):
            """ return val or val.id if val is a browse record """
            return val if isinstance(val, (bool, int, float, str)) else val.id

        result = {}
        if self.parent_id:
            if self.ids:
                partner = self.browse(self.ids[0])
                if partner.parent_id and partner.parent_id.id != self.parent_id:
                    result['warning'] = {'title': _('Warning'),
                                         'message': _('Changing the company of a contact should only be done if it '
                                                      'was never correctly set. If an existing contact starts working for a new '
                                                      'company then a new contact should be created under that new '
                                                      'company. You can use the "Discard" button to abandon this change.')}
            if self.use_parent_address:
                parent = self.browse(self.parent_id)
                address_fields = self._address_fields()
                result['value'] = dict((key, value_or_id(parent[key])) for key in address_fields)
        else:
            result['value'] = {'use_parent_address': False}
        return result

    def _address_fields(self):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        return list(ADDRESS_FIELDS)

    def open_parent(self):
        """ Utility method used to add an "Open Parent" button in partner views """
        partner = self.browse(self.ids[0])
        return {'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'form',
                'res_id': partner.parent_id.id,
                'target': 'new',
                'flags': {'form': {'action_buttons': True}}}


class ResPartnerBankType(models.Model):
    _description = 'Bank Account Type'
    _name = 'res.partner.bank.type'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    code = fields.Char(string='Code', size=64, required=True)
    field_ids = fields.One2many('res.partner.bank.type.field', 'bank_type_id', string='Type Fields')
    format_layout = fields.Text(string='Format Layout', translate=True,
                                default=lambda *args: "%(bank_name)s: %(acc_number)s")


class ResPartnerBankTypeFields(models.Model):
    _description = 'Bank type fields'
    _name = 'res.partner.bank.type.field'
    _order = 'name'
    name = fields.Char(string='Field Name', required=True, translate=True)
    bank_type_id = fields.Many2one('res.partner.bank.type', string='Bank Type', required=True, ondelete='cascade')
    required = fields.Boolean('Required')
    readonly = fields.Boolean('Readonly')
    size = fields.Integer('Max. Size')


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    def _bank_type_get(self):
        bank_type_obj = self.env['res.partner.bank.type']
        result = []
        type_ids = bank_type_obj.search([])
        bank_types = bank_type_obj.browse(type_ids)
        for bank_type in bank_types:
            result.append((bank_type.code, bank_type.name))
        return result

    owner_name = fields.Char(string='Account Owner Name')
    state = fields.Selection(selection='_bank_type_get', string='Bank Account Type', required=True,
                             change_default=True)


class ResBank(models.Model):
    _inherit = 'res.bank'

    name = fields.Char(required=False)