# -*- coding: utf-8 -*-

from odoo import models, fields, api


# ----------------------------------------------------------
# UOM
# ----------------------------------------------------------

class ProductUomCateg(models.Model):
    _name = 'product.uom.categ'
    _description = 'Product uom categ'

    name = fields.Char(string='Name', required=True, translate=True, )


class ProductUom(models.Model):
    _name = 'product.uom'
    _description = 'Product Unit of Measure'

    # _order = "name"

    def _compute_factor_inv(self):
        return self.factor and (1.0 / self.factor) or 0.0

    def _factor_inv(self):
        for uom in self:
            uom.factor_inv = self._compute_factor_inv()

    def _factor_inv_write(self):
        return self.write({'factor': self._compute_factor_inv()})

    # def name_create(self, cr, uid, name, context=None):
    #     """ The UoM category and factor are required, so we'll have to add temporary values
    #         for imported UoMs """
    #     if not context:
    #         context = {}
    #     uom_categ = self.pool.get('product.uom.categ')
    #     values = {self._rec_name: name, 'factor': 1}
    # look for the category based on the english name, i.e. no context on purpose!
    # TODO: should find a way to have it translated but not created until actually used
    # if not context.get('default_category_id'):
    #     categ_misc = 'Unsorted/Imported Units'
    #     categ_id = uom_categ.search(cr, uid, [('name', '=', categ_misc)])
    #     if categ_id:
    #         values['category_id'] = categ_id[0]
    #     else:
    #         values['category_id'] = uom_categ.name_create(
    #             cr, uid, categ_misc, context=context)[0]
    # uom_id = self.create(cr, uid, values, context=context)
    # return self.name_get(cr, uid, [uom_id], context=context)[0]
    #
    # def create(self, cr, uid, data, context=None):
    #     if 'factor_inv' in data:
    #         if data['factor_inv'] != 1:
    #             data['factor'] = self._compute_factor_inv(data['factor_inv'])
    #         del(data['factor_inv'])
    #     return super(product_uom, self).create(cr, uid, data, context)

    name = fields.Char(string='Unit of Measure', required=True, translate=True)
    category_id = fields.Many2one('product.uom.categ', string='Unit of Measure Category', required=True,
                                  ondelete='cascade',
                                  help="Conversion between Units of Measure can only occur if they belong to the same "
                                       "category. The conversion will be made based on the ratios.")
    factor = fields.Float(string='Ratio', required=True, digits=0,  # force NUMERIC with unlimited precision
                          help='How much bigger or smaller this unit is compared to the reference Unit of Measure for '
                               'this category:\n' \
                               '1 * (reference unit) = ratio * (this unit)', default=1.0, )
    factor_inv = fields.Float(compute='_factor_inv', digits=0,  # force NUMERIC with unlimited precision
                              inverse='_factor_inv_write',
                              string='Bigger Ratio',
                              help='How many times this Unit of Measure is bigger than the reference Unit of '
                                   'Measure in this category:\n' \
                                   '1 * (this unit) = ratio * (reference unit)', required=True),
    rounding = fields.Float(string='Rounding Precision', digits=0, required=True, default=0.01,
                            help="The computed quantity will be a multiple of this value. " \
                                 "Use 1.0 for a Unit of Measure that cannot be further split, such as a piece.")
    active = fields.Boolean(string='Active', default=1,
                            help="By unchecking the active field you can disable a unit of measure without deleting it.")
    uom_type = fields.Selection([('bigger', 'Bigger than the reference Unit of Measure'),
                                 ('reference', 'Reference Unit of Measure for this category'),
                                 ('smaller', 'Smaller than the reference Unit of Measure')], 'Type',
                                required=1, default='reference')

    _sql_constraints = [
        ('factor_gt_zero', 'CHECK (factor!=0)', 'The conversion ratio for a unit of measure cannot be 0!')
    ]


class ProductUl(models.Model):
    _name = "product.ul"
    _description = "Logistic Unit"

    name = fields.Char(string='Name', select=True, required=True, translate=True)
    type = fields.Selection([('unit', 'Unit'), ('pack', 'Pack'), ('box', 'Box'), ('pallet', 'Pallet')],
                            string='Type', required=True)
    height = fields.Float(string='Height', help='The height of the package')
    width = fields.Float(string='Width', help='The width of the package')
    length = fields.Float(string='Length', help='The length of the package')
    weight = fields.Float(string='Empty Package Weight')


# ----------------------------------------------------------
# Categories
# ----------------------------------------------------------


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _description = "Product Category"
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    # @api.multi
    # def name_get(self):
    #     def get_names(cat):
    #         """ Return the list [cat.name, cat.parent_id.name, ...] """
    #         res = []
    #         while cat:
    #             res.append(cat.name)
    #             cat = cat.parent_id
    #         return res
    #
    #     return [(cat.id, " / ".join(reversed(get_names(cat)))) for cat in self]

    # def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     if not context:
    #         context = {}
    #     if name:
    # Be sure name_search is symetric to name_get
    # categories = name.split(' / ')
    # parents = list(categories)
    # child = parents.pop()
    # domain = [('name', operator, child)]
    # if parents:
    #     names_ids = self.name_search(cr, uid, ' / '.join(parents), args=args, operator='ilike', context=context, limit=limit)
    #     category_ids = [name_id[0] for name_id in names_ids]
    #     if operator in expression.NEGATIVE_TERM_OPERATORS:
    #         category_ids = self.search(cr, uid, [('id', 'not in', category_ids)])
    #         domain = expression.OR([[('parent_id', 'in', category_ids)], domain])
    #     else:
    #         domain = expression.AND([[('parent_id', 'in', category_ids)], domain])
    #     for i in range(1, len(categories)):
    #         domain = [[('name', operator, ' / '.join(categories[-1 - i:]))], domain]
    #         if operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = expression.AND(domain)
    #         else:
    #             domain = expression.OR(domain)
    # ids = self.search(cr, uid, expression.AND([domain, args]), limit=limit, context=context)
    # else:
    #     ids = self.search(cr, uid, args, limit=limit, context=context)
    # return self.name_get(cr, uid, ids, context)
    #
    # def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.name_get(cr, uid, ids, context=context)
    #     return dict(res)

    name = fields.Char(string='Name', required=True, translate=True, select=True)
    # complete_name = fields.Char(compute='_name_get_fnc', string='Name')
    parent_id = fields.Many2one('product.category', string='Parent Category', select=True, ondelete='cascade')
    coordin_id = fields.Many2one('hr.employee', string='Parent Category', )
    emp_ids = fields.Many2many('hr.employee', 'depart_category_rel', 'depart_id', 'emp_id', string='Tags')
    child_id = fields.One2many('product.category', 'parent_id', string='Child Categories')
    sequence = fields.Integer(string='Sequence', select=True, help="Gives the sequence order when displaying a list of "
                                                                   "product categories.")
    type = fields.Selection([('view', 'View'), ('normal', 'Normal')], string='Category Type', default='normal',
                            help="A category of the view type is a virtual category that can be used as the parent of "
                                 "another category to create a hierarchical structure.")
    parent_left = fields.Integer(string='Left Parent', select=1)
    parent_right = fields.Integer(string='Right Parent', select=1)

    # _constraints = [
    #     (osv.osv._check_recursion, 'Error ! You cannot create recursive categories.', ['parent_id'])
    # ]


class ProducePriceHistory(models.Model):
    """
    Keep track of the ``product.template`` standard prices as they are changed.
    """

    _name = 'product.price.history'
    _rec_name = 'datetime'
    _order = 'datetime desc'

    company_id = fields.Many2one('res.company', required=True)
    product_template_id = fields.Many2one('product.template', string='Product Template', required=True,
                                          ondelete='cascade')
    datetime = fields.Datetime(string='Historization Time', default=fields.Datetime.now)
    cost = fields.Float('Historized Cost')

    # def _get_default_company(self, cr, uid, context=None):
    #     if 'force_company' in context:
    #         return context['force_company']
    #     else:
    #         company = self.pool['res.users'].browse(cr, uid, uid,
    #             context=context).company_id
    #         return company.id if company else False

    # _defaults = {
    #     'company_id': _get_default_company,
    # }


# ----------------------------------------------------------
# Product Attributes
# ----------------------------------------------------------


class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _description = 'Product Attribute'
    _order = 'name'
    name = fields.Char(string='Name', translate=True, required=True)
    value_ids = fields.One2many('product.attribute.value', 'attribute_id', string='Values', copy=True)


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _order = 'sequence'

    # def _get_price_extra(self, cr, uid, ids, name, args, context=None):
    #     result = dict.fromkeys(ids, 0)
    #     if not context.get('active_id'):
    #         return result
    #
    #     for obj in self.browse(cr, uid, ids, context=context):
    #         for price_id in obj.price_ids:
    #             if price_id.product_tmpl_id.id == context.get('active_id'):
    #                 result[obj.id] = price_id.price_extra
    #                 break
    #     return result
    #
    # def _set_price_extra(self, cr, uid, id, name, value, args, context=None):
    #     if context is None:
    #         context = {}
    #     if 'active_id' not in context:
    #         return None
    #     p_obj = self.pool['product.attribute.price']
    #     p_ids = p_obj.search(cr, uid, [('value_id', '=', id), ('product_tmpl_id', '=', context['active_id'])],
    #                          context=context)
    #     if p_ids:
    #         p_obj.write(cr, uid, p_ids, {'price_extra': value}, context=context)
    #     else:
    #         p_obj.create(cr, uid, {
    #             'product_tmpl_id': context['active_id'],
    #             'value_id': id,
    #             'price_extra': value,
    #         }, context=context)
    #
    # def name_get(self, cr, uid, ids, context=None):
    #     if context and not context.get('show_attribute', True):
    #         return super(product_attribute_value, self).name_get(cr, uid, ids, context=context)
    #     res = []
    #     for value in self.browse(cr, uid, ids, context=context):
    #         res.append([value.id, "%s: %s" % (value.attribute_id.name, value.name)])
    #     return res

    sequence = fields.Integer(string='Sequence', help="Determine the display order")
    name = fields.Char(string='Value', translate=True, required=True)
    attribute_id = fields.Many2one('product.attribute', string='Attribute', required=True, ondelete='cascade')
    product_ids = fields.Many2many('product.product', id1='att_id', id2='prod_id', string='Variants',
                                   readonly=True)
    price_extra = fields.Float(compute='_get_price_extra', string='Attribute Price Extra',
                               inverse='_set_price_extra', default=0.0,
                               help="Price Extra: Extra price for the variant with this attribute value on sale "
                                    "price. eg. 200 price extra, 1000 + 200 = 1200.")
    # digits_compute = dp.get_precision('Product Price'),
    price_ids = fields.One2many('product.attribute.price', 'value_id', string='Attribute Prices', readonly=True)

    _sql_constraints = [
        ('value_company_uniq', 'unique (name,attribute_id)', 'This attribute value already exists !')
    ]

    # def unlink(self, cr, uid, ids, context=None):
    #     ctx = dict(context or {}, active_test=False)
    #     product_ids = self.pool['product.product'].search(cr, uid, [('attribute_value_ids', 'in', ids)], context=ctx)
    #     if product_ids:
    #         raise osv.except_osv(_('Integrity Error!'),
    #                              _('The operation cannot be completed:\nYou trying to delete an attribute value with a reference on a product variant.'))
    #     return super(product_attribute_value, self).unlink(cr, uid, ids, context=context)


class ProductAttributePrice(models.Model):
    _name = 'product.attribute.price'

    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, ondelete='cascade')
    value_id = fields.Many2one('product.attribute.value', string='Product Attribute Value', required=True,
                               ondelete='cascade')
    price_extra = fields.Float(string='Price Extra', )
    # digits_compute=dp.get_precision('Product Price')


class ProductAttributeLine(models.Model):
    _name = 'product.attribute.line'
    _rec_name = 'attribute_id'
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', required=True, ondelete='cascade')
    attribute_id = fields.Many2one('product.attribute', string='Attribute', required=True, ondelete='restrict')
    value_ids = fields.Many2many('product.attribute.value', id1='line_id', id2='val_id',
                                 string='Product Attribute Value')

    # def _check_valid_attribute(self, cr, uid, ids, context=None):
    #     obj_pal = self.browse(cr, uid, ids[0], context=context)
    #     return obj_pal.value_ids <= obj_pal.attribute_id.value_ids

    # _constraints = [
    #     (_check_valid_attribute, 'Error ! You cannot use this attribute with the following value.', ['attribute_id'])
    # ]


# ----------------------------------------------------------
# Products
# ----------------------------------------------------------

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _order = "name"

    name = fields.Char(string='Name', required=True, translate=True, select=True)
    product_manager = fields.Many2one('res.users', string='Product Manager')
    description = fields.Text(string='Description', translate=True,
                              help="A precise description of the Product, used only for internal information purposes.")
    description_purchase = fields.Text(string='Purchase Description', translate=True,
                                       help="A description of the Product that you want to communicate to your "
                                            "suppliers."
                                            "This description will be copied to every Purchase Order, Receipt and "
                                            "Supplier Invoice/Refund.")
    description_sale = fields.Text('Sale Description', translate=True,
                                   help="A description of the Product that you want to communicate to your customers. "
                                        "This description will be copied to every Sale Order, Delivery Order and "
                                        "Customer Invoice/Refund")
    type = fields.Selection([('consu', 'Consumable'), ('service', 'Service')], string='Product Type',
                            required=True, default='consu',
                            help="Consumable are product where you don't manage stock, a service is a non-material "
                                 "product provided by a company or an individual.")
    rental = fields.Boolean(string='Can be Rent')
    categ_id = fields.Many2one('product.category', string='Internal Category', required=True, change_default=True,
                               domain="[('type','=','normal')]", help="Select category for the current product")
    # price = fields.Float(compute='_product_template_price', string='Price', )
    # digits_compute=dp.get_precision('Product Price')
    list_price = fields.Float(string='Sale Price', default=1,
                              help="Base price to compute the customer price. Sometimes called the catalog price.")
    # digits_compute = dp.get_precision('Product Price')
    # standard_price = fields.property(type='float', digits_compute=dp.get_precision('Product Price'),
    #                                   help="Cost price of the product template used for standard stock valuation in accounting and used as a base price on purchase orders. "
    #                                        "Expressed in the default unit of measure of the product.",
    #                                   groups="base.group_user", string="Cost Price", default=0.0, )
    volume = fields.Float(string='Volume', help="The volume in m3.")
    weight = fields.Float(string='Gross Weight', help="The gross weight in Kg.")
    # digits_compute = dp.get_precision('Stock Weight'),
    weight_net = fields.Float(string='Net Weight', help="The net weight in Kg.")
    # digits_compute = dp.get_precision('Stock Weight')
    warranty = fields.Float(string='Warranty')
    sale_ok = fields.Boolean(string='Can be Sold', help="Specify if the product can be selected in a sales order line.",
                             default=1, )
    state = fields.Selection([('', ''),
                              ('draft', 'In Development'),
                              ('sellable', 'Normal'),
                              ('end', 'End of Lifecycle'),
                              ('obsolete', 'Obsolete')], string='Status')
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=False,
                             help="Default Unit of Measure used for all stock operation.")
    uom_po_id = fields.Many2one('product.uom', string='Purchase Unit of Measure', required=True,
                                help="Default Unit of Measure used for purchase orders. It must be in the same "
                                     "category than the default unit of measure.")
    uos_id = fields.Many2one('product.uom', string='Unit of Sale',
                             help='Specify a unit of measure here if invoicing is made in another unit of measure '
                                  'than inventory. Keep empty to use the default unit of measure.')
    uos_coeff = fields.Float(string='Unit of Measure -> UOS Coeff',
                             help='Coefficient to convert default Unit of Measure to Unit of Sale\n'
                                  ' uos = uom * coeff')
    # digits_compute = dp.get_precision('Product UoS'),
    mes_type = fields.Selection((('fixed', 'Fixed'), ('variable', 'Variable')), string='Measure Type', default='fixed', )
    company_id = fields.Many2one('res.company', string='Company', select=1)
    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(string='Image',
                          help="This field holds the image used as image for the product, limited to 1024x1024px.")
    # packaging_ids = fields.One2many('product.packaging', 'product_tmpl_id', string='Logistical Units',
    #                                 help="Gives the different ways to package the same product. This has no impact on "
    #                                      "the picking order and is mainly used if you use the EDI module.")
    # seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id', string='Supplier')
    active = fields.Boolean(string='Active', default=1,
                            help="If unchecked, it will allow you to hide the product without removing it.")
    color = fields.Integer(string='Color Index')
    # is_product_variant = fields.Boolean(compute='_is_product_variant', string='Is product variant')
    parent_id = fields.Many2one('product.product', string='Parent Category', select=True, ondelete='cascade')
    child_id = fields.One2many('product.product', 'parent_id', string='Child Categories')
    arent_left = fields.Integer(string='Left Parent', select=1)
    parent_right = fields.Integer(string='Right Parent', select=1)
    attribute_line_ids = fields.One2many('product.attribute.line', 'product_tmpl_id', string='Product Attributes')
    product_variant_ids = fields.One2many('product.product', 'product_tmpl_id', string='Products', required=True)
    # product_variant_count = fields.Integer(compute='_get_product_variant_count', string='# of Product Variants')

    # related to display product product information if is_product_variant
    # ean13 = fields.related('product_variant_ids', 'ean13', type='char', string='EAN13 Barcode')
    # default_code = fields.related('product_variant_ids', 'default_code', type='char', string='Internal Reference')
    # lst_price = fields.related('list_price', type="float", string='Public Price',
    #                             digits_compute=dp.get_precision('Product Price'))
    # seller_delay = fields.related('seller_ids', 'delay', type='integer', string='Supplier Lead Time',
    #                                help="This is the average delay in days between the purchase order confirmation and the receipts for this product and for the default supplier. It is used by the scheduler to order requests based on reordering delays.")
    # seller_qty': fields.related('seller_ids', 'qty', type='float', string='Supplier Quantity',
    #                              help="This is minimum quantity to purchase from Main Supplier.")
    # seller_id': fields.related('seller_ids', 'name', type='many2one', relation='res.partner', string='Main Supplier',
    #                             help="Main Supplier who has highest priority in Supplier List.")

    # image_medium': fields.function(_get_image, fnct_inv=_set_image,
    #                                 string="Medium-sized image", type="binary", multi="_get_image",
    #                                 store={
    #                                     'product.template': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #                                 },
    #                                 help="Medium-sized image of the product. It is automatically " \
    #                                      "resized as a 128x128px image, with aspect ratio preserved, " \
    #                                      "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
    # image_small': fields.function(_get_image, fnct_inv=_set_image,
    #                                string="Small-sized image", type="binary", multi="_get_image",
    #                                store={
    #                                    'product.template': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #                                },
    #                                help="Small-sized image of the product. It is automatically " \
    #                                     "resized as a 64x64px image, with aspect ratio preserved. " \
    #                                     "Use this field anywhere a small image is required."),


