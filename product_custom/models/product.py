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

    name = fields.Char(required=False)


class ProductKit(models.Model):
    _name = "product.kit"
    _description = 'Product kit'

    name = fields.Char(string='Nom Kit', required=True)
    type_ids = fields.Many2many('product.product', string='product', readonly=False)
    description = fields.Text(string='Description')
    categ_id = fields.Many2one('product.category', string='product')

    # def button_compute(self, cr, uid, ids, context=None, set_total=False):
    #     ##self.calculer(self, uid, ids,context)
    #     this = self.browse(cr, uid, ids[0], context=context)
    #     proj_t_w_obj = self.pool.get('project.task.work')
    #     proj_obj = self.pool.get('project.project')
    #     for inv in self.browse(cr, uid, ids, context=context):
    #         for dd in inv.type_id.ids:
    #             pr = self.pool.get('product.product').browse(cr, uid, dd, context=context)
    #             p1 = proj_obj.search(cr, uid, [('state', '=', 'open'), ('is_kit', '=', True)], limit=0, order='id',
    #                                  context=context)
    #             for ss in p1:
    #                 tt = proj_t_w_obj.search(cr, uid,
    #                                          [('project_id', '=', ss), ('kit_id', '=', inv.id), ('product_id', '=', dd)],
    #                                          limit=0, order='id', context=context)
    #
    #                 if not tt:
    #                     tt1 = proj_t_w_obj.search(cr, uid, [('project_id', '=', ss), ('kit_id', '=', inv.id)], limit=0,
    #                                               order='id', context=context)
    #                     if tt1:
    #                         l1 = proj_t_w_obj.browse(cr, uid, tt1[0], context=context)
    #                         sql = self.pool.get('project.task.work').create(cr, uid, {
    #                             'task_id': l1.task_id.id,
    #                             'categ_id': l1.categ_id.id,
    #                             'product_id': dd,
    #                             'name': this.name,
    #                             'date_start': l1.date_start,
    #                             'date_end': l1.date_end,
    #                             'poteau_t': l1.poteau_t,
    #                             'poteau_i': l1.poteau_r,
    #                             'color': l1.color,
    #                             'etape': l1.etape,
    #                             'zone': l1.zone,
    #                             'secteur': l1.secteur,
    #                             'total_t': l1.total_t,  ##*work.employee_id.contract_id.wage
    #                             'hours': l1.hours,
    #                             'project_id': l1.project_id.id,
    #                             'partner_id': l1.project_id.partner_id.id,
    #
    #                             'state_id': l1.project_id.state_id.id or False,
    #                             'city': l1.project_id.city,
    #                             'gest_id': l1.gest_id.id or False,
    #                             'reviewer_id1': l1.reviewer_id1.id or False,
    #                             'coordin_id1': l1.coordin_id1.id or False,
    #                             'coordin_id2': l1.coordin_id2.id or False,
    #                             'coordin_id3': l1.coordin_id3.id or False,
    #                             'coordin_id4': l1.coordin_id4.id or False,
    #                             'uom_id': l1.uom_id.id,
    #                             'uom_id_r': l1.uom_id_r.id,
    #                             'ftp': l1.ftp,
    #                             'state': 'draft',
    #                             'sequence': l1.sequence,
    #                             'display': True,
    #                             'active': True,
    #                             'gest_id3': l1.gest_id3.id or False,
    #                             'current_gest': l1.current_gest.id or False,
    #                             'current_sup': l1.current_sup.id or False
    #
    #                         }, context=context)
    #
    #     return True


class ProductProduct(models.Model):
    _inherit = 'product.product'
    # _parent_name = "parent_id"
    # _parent_store = True
    # _parent_order = 'name'
    _order = 'priority desc, default_code, name, id'

    # def _product_price(self, cr, uid, ids, name, arg, context=None):
    #     plobj = self.pool.get('product.pricelist')
    #     res = {}
    #     if context is None:
    #         context = {}
    #     quantity = context.get('quantity') or 1.0
    #     pricelist = context.get('pricelist', False)
    #     partner = context.get('partner', False)
    #     if pricelist:
    #         # Support context pricelists specified as display_name or ID for compatibility
    #         if isinstance(pricelist, basestring):
    #             pricelist_ids = plobj.name_search(
    #                 cr, uid, pricelist, operator='=', context=context, limit=1)
    #             pricelist = pricelist_ids[0][0] if pricelist_ids else pricelist
    #
    #         if isinstance(pricelist, (int, long)):
    #             products = self.browse(cr, uid, ids, context=context)
    #             qtys = map(lambda x: (x, quantity, partner), products)
    #             pl = plobj.browse(cr, uid, pricelist, context=context)
    #             price = plobj._price_get_multi(cr, uid, pl, qtys, context=context)
    #             for id in ids:
    #                 res[id] = price.get(id, 0.0)
    #     for id in ids:
    #         res.setdefault(id, 0.0)
    #     return res
    #
    # def view_header_get(self, cr, uid, view_id, view_type, context=None):
    #     if context is None:
    #         context = {}
    #     res = super(product_product, self).view_header_get(cr, uid, view_id, view_type, context)
    #     if (context.get('categ_id', False)):
    #         return _('Products: ') + self.pool.get('product.category').browse(cr, uid, context['categ_id'],
    #                                                                           context=context).name
    #     return res
    #
    # def _product_lst_price(self, cr, uid, ids, name, arg, context=None):
    #     product_uom_obj = self.pool.get('product.uom')
    #     res = dict.fromkeys(ids, 0.0)
    #
    #     for product in self.browse(cr, uid, ids, context=context):
    #         if 'uom' in context:
    #             uom = product.uos_id or product.uom_id
    #             res[product.id] = product_uom_obj._compute_price(cr, uid,
    #                                                              uom.id, product.list_price, context['uom'])
    #         else:
    #             res[product.id] = product.list_price
    #         res[product.id] = res[product.id] + product.price_extra
    #
    #     return res
    #
    # def _set_product_lst_price(self, cr, uid, id, name, value, args, context=None):
    #     product_uom_obj = self.pool.get('product.uom')
    #
    #     product = self.browse(cr, uid, id, context=context)
    #     if 'uom' in context:
    #         uom = product.uos_id or product.uom_id
    #         value = product_uom_obj._compute_price(cr, uid,
    #                                                context['uom'], value, uom.id)
    #     value = value - product.price_extra
    #
    #     return product.write({'list_price': value})
    #
    # def _get_partner_code_name(self, cr, uid, ids, product, partner_id, context=None):
    #     for supinfo in product.seller_ids:
    #         if supinfo.name.id == partner_id:
    #             return {'code': supinfo.product_code or product.default_code,
    #                     'name': supinfo.product_name or product.name}
    #     res = {'code': product.default_code, 'name': product.name}
    #     return res
    #
    # def _product_code(self, cr, uid, ids, name, arg, context=None):
    #     res = {}
    #     if context is None:
    #         context = {}
    #     for p in self.browse(cr, uid, ids, context=context):
    #         res[p.id] = self._get_partner_code_name(cr, uid, [], p, context.get('partner_id', None), context=context)[
    #             'code']
    #     return res
    #
    # def _product_partner_ref(self, cr, uid, ids, name, arg, context=None):
    #     res = {}
    #     if context is None:
    #         context = {}
    #     for p in self.browse(cr, uid, ids, context=context):
    #         data = self._get_partner_code_name(cr, uid, [], p, context.get('partner_id', None), context=context)
    #         if not data['code']:
    #             data['code'] = p.code
    #         if not data['name']:
    #             data['name'] = p.name
    #         res[p.id] = (data['code'] and ('[' + data['code'] + '] ') or '') + (data['name'] or '')
    #     return res
    #
    # def _is_product_variant_impl(self, cr, uid, ids, name, arg, context=None):
    #     return dict.fromkeys(ids, True)
    #
    # def _get_name_template_ids(self, cr, uid, ids, context=None):
    #     template_ids = self.pool.get('product.product').search(cr, uid, [('product_tmpl_id', 'in', ids)])
    #     return list(set(template_ids))
    #
    # def _get_image_variant(self, cr, uid, ids, name, args, context=None):
    #     result = dict.fromkeys(ids, False)
    #     for obj in self.browse(cr, uid, ids, context=context):
    #         if context.get('bin_size'):
    #             result[obj.id] = obj.image_variant
    #         else:
    #             result[obj.id] = \
    #             tools.image_get_resized_images(obj.image_variant, return_big=True, avoid_resize_medium=True)[name]
    #         if not result[obj.id]:
    #             result[obj.id] = getattr(obj.product_tmpl_id, name)
    #     return result
    #
    # def _set_image_variant(self, cr, uid, id, name, value, args, context=None):
    #     image = tools.image_resize_image_big(value)
    #
    #     product = self.browse(cr, uid, id, context=context)
    #     if product.product_tmpl_id.image:
    #         product.image_variant = image
    #     else:
    #         product.product_tmpl_id.image = image
    #
    # def _get_price_extra(self, cr, uid, ids, name, args, context=None):
    #     result = dict.fromkeys(ids, False)
    #     for product in self.browse(cr, uid, ids, context=context):
    #         price_extra = 0.0
    #         for variant_id in product.attribute_value_ids:
    #             for price_id in variant_id.price_ids:
    #                 if price_id.product_tmpl_id.id == product.product_tmpl_id.id:
    #                     price_extra += price_id.price_extra
    #         result[product.id] = price_extra
    #     return result

    name = fields.Char(string='Internal Reference', select=True)
    is_devide = fields.Boolean(string='Active')
    is_invoice = fields.Boolean('Active')
    is_ft = fields.Boolean('Active')
    is_purchase = fields.Boolean('Active')
    is_gantt = fields.Boolean('Active')
    is_load = fields.Boolean('Active')
    ean13 = fields.Char(string='EAN13 Barcode', size=13,
                        help="International Article Number used for product identification.")
    # name_template = fields.related('product_tmpl_id', 'name', string="Template Name", type='char', store={
    #     'product.template': (_get_name_template_ids, ['name'], 10),
    #     'product.product': (lambda self, cr, uid, ids, c=None: ids, [], 10),
    # }, select=True, default=3, )
    attribute_value_ids = fields.Many2many('product.attribute.value', id1='prod_id', id2='att_id',
                                           string='Attributes', readonly=True, ondelete='restrict')
    parent_id = fields.Many2one('product.product', string='Parent Category', select=True, ondelete='cascade')
    child_id = fields.One2many('product.product', 'parent_id', string='Child Categories')
    prod_id = fields.Many2many('product.product', 'product_product_rel', 'product_id', 'prod_id', string='part')
    uom_id = fields.Many2one('product.uom', string='Unit of Measure',
                             help="Default Unit of Measure used for all stock operation.")
    ##'uom_po_id': fields.many2one('product.uom', 'Purchase Unit of Measure', required=True, help="Default Unit of Measure used for purchase orders. It must be in the same category than the default unit of measure."),
    uos_id = fields.Many2one('product.uom', 'Unit of Sale')
    pu = fields.Float(string='Internal Reference', select=True)
    ##'type': fields.selection([('view','View'), ('normal','Normal')], 'Category Type', help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
    parent_left = fields.Integer(string='Left Parent', select=1)
    parent_right = fields.Integer(string='Right Parent', select=1)
    # image: all image fields are base64 encoded and PIL-supported
    image_variant = fields.Binary(string='Variant Image',
                                  help="This field holds the image used as image for the product variant, limited to 1024x1024px.")
    image = fields.Binary(compute='_get_image_variant', inverse='_set_image_variant',
                          string="Big-sized image",
                          help="Image of the product variant (Big-sized image of product template if false). It is automatically " \
                               "resized as a 1024x1024px image, with aspect ratio preserved.")
    image_small = fields.Binary(compute='_get_image_variant', inverse='_set_image_variant',
                                string="Small-sized image",
                                help="Image of the product variant (Small-sized image of product template if false).")
    image_medium = fields.Binary(compute='_get_image_variant', inverse='_set_image_variant',
                                 string="Medium-sized image",
                                 help="Image of the product vaiant (Medium-sized image of product template if false).")
    categ_id = fields.Many2one('product.category', string='Internal Category', change_default=True,
                               domain="[('type','=','normal')]", help="Select category for the current product")

    # def unlink(self, cr, uid, ids, context=None):
    #     unlink_ids = []
    #     unlink_product_tmpl_ids = []
    #     for product in self.browse(cr, uid, ids, context=context):
    #         # Check if product still exists, in case it has been unlinked by unlinking its template
    #         if not product.exists():
    #             continue
    #         tmpl_id = product.product_tmpl_id.id
    #         # Check if the product is last product of this template
    #         other_product_ids = self.search(cr, uid, [('product_tmpl_id', '=', tmpl_id), ('id', '!=', product.id)],
    #                                         context=context)
    #         if not other_product_ids:
    #             unlink_product_tmpl_ids.append(tmpl_id)
    #         unlink_ids.append(product.id)
    #     res = super(product_product, self).unlink(cr, uid, unlink_ids, context=context)
    #     # delete templates after calling super, as deleting template could lead to deleting
    #     # products due to ondelete='cascade'
    #     self.pool.get('product.template').unlink(cr, uid, unlink_product_tmpl_ids, context=context)
    #     return res
    #
    # def onchange_type(self, cr, uid, ids, type):
    #     return {}
    #
    def action_open(self):

        return {
            'name': ('Modification Travaux Permis'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'product.product',
            'views': [[1150, 'form']],
            'res_id': self.ids[0],
            'context': {'active_id': self.ids[0]},
            'domain': []
        }

    def button_write(self):

        self.write({'is_devide': self.is_devide, 'is_load': self.is_load, 'is_gantt': self.is_gantt,
                    'uom_id': self.uom_id.id, 'uos_id': self.uos_id.id})
        return True
    #
    # def onchange_uom(self, cursor, user, ids, uom_id, uom_po_id):
    #     if uom_id and uom_po_id:
    #         uom_obj = self.pool.get('product.uom')
    #         uom = uom_obj.browse(cursor, user, [uom_id])[0]
    #         uom_po = uom_obj.browse(cursor, user, [uom_po_id])[0]
    #         if uom.category_id.id != uom_po.category_id.id:
    #             return {'value': {'uom_po_id': uom_id}}
    #     return False
    #
    # ##    def _check_ean_key(self, cr, uid, ids, context=None):
    # ##        for product in self.read(cr, uid, ids, ['ean13'], context=context):
    # ##            if not check_ean(product['ean13']):
    # ##                return False
    # ##        return True
    # ##
    # ##    _constraints = [(_check_ean_key, 'You provided an invalid "EAN13 Barcode" reference. You may use the "Internal Reference" field instead.', ['ean13'])]
    #
    # def on_order(self, cr, uid, ids, orderline, quantity):
    #     pass
    #
    # def name_get(self, cr, user, ids, context=None):
    #     if context is None:
    #         context = {}
    #     if isinstance(ids, (int, long)):
    #         ids = [ids]
    #     if not len(ids):
    #         return []
    #
    #     def _name_get(d):
    #         name = d.get('name', '')
    #         code = context.get('display_default_code', True) and d.get('default_code', False) or False
    #         if code:
    #             name = '[%s] %s' % (code, name)
    #         return (d['id'], name)
    #
    #     partner_id = context.get('partner_id', False)
    #     if partner_id:
    #         partner_ids = [partner_id, self.pool['res.partner'].browse(cr, user, partner_id,
    #                                                                    context=context).commercial_partner_id.id]
    #     else:
    #         partner_ids = []
    #
    #     # all user don't have access to seller and partner
    #     # check access and use superuser
    #     self.check_access_rights(cr, user, "read")
    #     self.check_access_rule(cr, user, ids, "read", context=context)
    #
    #     result = []
    #     for product in self.browse(cr, SUPERUSER_ID, ids, context=context):
    #         variant = ", ".join([v.name for v in product.attribute_value_ids])
    #         name = variant and "%s (%s)" % (product.name, variant) or product.name
    #         sellers = []
    #         if partner_ids:
    #             sellers = filter(lambda x: x.name.id in partner_ids, product.seller_ids)
    #         if sellers:
    #             for s in sellers:
    #                 seller_variant = s.product_name and (
    #                         variant and "%s (%s)" % (s.product_name, variant) or s.product_name
    #                 ) or False
    #                 mydict = {
    #                     'id': product.id,
    #                     'name': seller_variant or name,
    #                     'default_code': s.product_code or product.default_code,
    #                 }
    #                 result.append(_name_get(mydict))
    #         else:
    #             mydict = {
    #                 'id': product.id,
    #                 'name': name,
    #                 'default_code': product.default_code,
    #             }
    #             result.append(_name_get(mydict))
    #     return result
    #
    # def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
    #     if not args:
    #         args = []
    #     if name:
    #         positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
    #         ids = []
    #         if operator in positive_operators:
    #             ids = self.search(cr, user, [('default_code', '=', name)] + args, limit=limit, context=context)
    #             if not ids:
    #                 ids = self.search(cr, user, [('ean13', '=', name)] + args, limit=limit, context=context)
    #         if not ids and operator not in expression.NEGATIVE_TERM_OPERATORS:
    #             # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
    #             # on a database with thousands of matching products, due to the huge merge+unique needed for the
    #             # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
    #             # Performing a quick memory merge of ids in Python will give much better performance
    #             ids = self.search(cr, user, args + [('default_code', operator, name)], limit=limit, context=context)
    #             if not limit or len(ids) < limit:
    #                 # we may underrun the limit because of dupes in the results, that's fine
    #                 limit2 = (limit - len(ids)) if limit else False
    #                 ids += self.search(cr, user, args + [('name', operator, name), ('id', 'not in', ids)], limit=limit2,
    #                                    context=context)
    #         elif not ids and operator in expression.NEGATIVE_TERM_OPERATORS:
    #             ids = self.search(cr, user, args + ['&', ('default_code', operator, name), ('name', operator, name)],
    #                               limit=limit, context=context)
    #         if not ids and operator in positive_operators:
    #             ptrn = re.compile('(\[(.*?)\])')
    #             res = ptrn.search(name)
    #             if res:
    #                 ids = self.search(cr, user, [('default_code', '=', res.group(2))] + args, limit=limit,
    #                                   context=context)
    #     else:
    #         ids = self.search(cr, user, args, limit=limit, context=context)
    #     result = self.name_get(cr, user, ids, context=context)
    #     return result
    #
    # #
    # # Could be overrided for variants matrices prices
    # #
    # def price_get(self, cr, uid, ids, ptype='list_price', context=None):
    #     products = self.browse(cr, uid, ids, context=context)
    #     return self.pool.get("product.template")._price_get(cr, uid, products, ptype=ptype, context=context)
    #
    # def copy(self, cr, uid, id, default=None, context=None):
    #     if context is None:
    #         context = {}
    #
    #     if default is None:
    #         default = {}
    #
    #     product = self.browse(cr, uid, id, context)
    #     if context.get('variant'):
    #         # if we copy a variant or create one, we keep the same template
    #         default['product_tmpl_id'] = product.product_tmpl_id.id
    #     elif 'name' not in default:
    #         default['name'] = _("%s (copy)") % (product.name,)
    #
    #     return super(product_product, self).copy(cr, uid, id, default=default, context=context)
    #
    # ##    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
    # ##        if context is None:
    # ##            context = {}
    # ##        if context.get('search_default_categ_id'):
    # ##            args.append((('categ_id', 'child_of', context['search_default_categ_id'])))
    # ##        return super(product_product, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
    #
    # def open_product_template(self, cr, uid, ids, context=None):
    #     """ Utility method used to add an "Open Template" button in product views """
    #     product = self.browse(cr, uid, ids[0], context=context)
    #     return {'type': 'ir.actions.act_window',
    #             'res_model': 'product.template',
    #             'view_mode': 'form',
    #             'res_id': product.product_tmpl_id.id,
    #             'target': 'new'}
    #
    # def create(self, cr, uid, vals, context=None):
    #     if context is None:
    #         context = {}
    #     ctx = dict(context or {}, create_product_product=True)
    #     return super(product_product, self).create(cr, uid, vals, context=ctx)
    #
    # def need_procurement(self, cr, uid, ids, context=None):
    #     return False
    #
    # def _compute_uos_qty(self, cr, uid, ids, uom, qty, uos, context=None):
    #     '''
    #     Computes product's invoicing quantity in UoS from quantity in UoM.
    #     Takes into account the
    #     :param uom: Source unit
    #     :param qty: Source quantity
    #     :param uos: Target UoS unit.
    #     '''
    #     if not uom or not qty or not uos:
    #         return qty
    #     uom_obj = self.pool['product.uom']
    #     product_id = ids[0] if isinstance(ids, (list, tuple)) else ids
    #     product = self.browse(cr, uid, product_id, context=context)
    #     if isinstance(uos, (int, long)):
    #         uos = uom_obj.browse(cr, uid, uos, context=context)
    #     if isinstance(uom, (int, long)):
    #         uom = uom_obj.browse(cr, uid, uom, context=context)
    #     if product.uos_id:  # Product has UoS defined
    #         # We cannot convert directly between units even if the units are of the same category
    #         # as we need to apply the conversion coefficient which is valid only between quantities
    #         # in product's default UoM/UoS
    #         qty_default_uom = uom_obj._compute_qty_obj(cr, uid, uom, qty,
    #                                                    product.uom_id)  # qty in product's default UoM
    #         qty_default_uos = qty_default_uom * product.uos_coeff
    #         return uom_obj._compute_qty_obj(cr, uid, product.uos_id, qty_default_uos, uos)
    #     else:
    #         return uom_obj._compute_qty_obj(cr, uid, uom, qty, uos)
    #


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'
    _rec_name = 'ean'
    _order = 'sequence'

    name = fields.Text(string='Description')
    qty = fields.Float('Quantity by Package',
                       help="The total number of products you can put by pallet or box.")
    ul = fields.Many2one('product.ul', string='Package Logistic Unit', required=True)
    # default='_get_1st_ul'
    ul_qty = fields.Integer(string='Package by layer', help='The number of packages by layer')
    ul_container = fields.Many2one('product.ul', string='Pallet Logistic Unit')
    rows = fields.Integer(string='Number of Layers', required=True,
                          help='The number of layer on a pallet or box', default=3, )
    product_tmpl_id = fields.Many2one('product.template', 'Product', select=1, ondelete='cascade', required=True)
    ean = fields.Char(string='EAN', size=14, help="The EAN code of the package unit.")
    code = fields.Char(string='Code', help="The code of the transport unit.")
    weight = fields.Float('Total Package Weight',
                          help='The weight of a full package, pallet or box.')

    # def _check_ean_key(self, cr, uid, ids, context=None):
    #     for pack in self.browse(cr, uid, ids, context=context):
    #         if not check_ean(pack.ean):
    #             return False
    #     return True
    #
    # _constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean'])]
    #
    # def name_get(self, cr, uid, ids, context=None):
    #     if not len(ids):
    #         return []
    #     res = []
    #     for pckg in self.browse(cr, uid, ids, context=context):
    #         p_name = pckg.ean and '[' + pckg.ean + '] ' or ''
    #         p_name += pckg.ul.name
    #         res.append((pckg.id,p_name))
    #     return res
    #
    # def _get_1st_ul(self, cr, uid, context=None):
    #     cr.execute('select id from product_ul order by id asc limit 1')
    #     res = cr.fetchone()
    #     return (res and res[0]) or False
    #
    # def checksum(ean):
    #     salt = '31' * 6 + '3'
    #     sum = 0
    #     for ean_part, salt_part in zip(ean, salt):
    #         sum += int(ean_part) * int(salt_part)
    #     return (10 - (sum % 10)) % 10
    # checksum = staticmethod(checksum)


class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'
    # def _calc_qty(self, cr, uid, ids, fields, arg, context=None):
    #     result = {}
    #     for supplier_info in self.browse(cr, uid, ids, context=context):
    #         for field in fields:
    #             result[supplier_info.id] = {field:False}
    #         qty = supplier_info.min_qty
    #         result[supplier_info.id]['qty'] = qty
    #     return result

    name = fields.Many2one('res.partner', string='Supplier', required=True,
                           ondelete='cascade', help="Supplier of this product")
    # domain = [('supplier', '=', True)],
    # 'product_uom': fields.related('product_tmpl_id', 'uom_po_id', type='many2one', relation='product.uom', string="Supplier Unit of Measure", readonly="1", help="This comes from the product form."),
    # qty = fields.Float(compute='_calc_qty', store=True, string='Quantity', multi="qty", help="This is a quantity which is converted into Default Unit of Measure.")
    pricelist_ids = fields.One2many('pricelist.partnerinfo', 'suppinfo_id', string='Supplier Pricelist', copy=True)
    # 'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'product.supplierinfo', context=c),


class PriceListPartnerInfo(models.Model):
    _name = 'pricelist.partnerinfo'
    _order = 'min_quantity asc'

    name = fields.Char(string='Description')
    suppinfo_id = fields.Many2one('product.supplierinfo', string='Partner Information', required=True,
                                  ondelete='cascade')
    min_quantity = fields.Float(string='Quantity', required=True, help="The minimal quantity to trigger this rule, "
                                                                       "expressed in the supplier Unit of Measure if "
                                                                       "any or in the default Unit of Measure of the "
                                                                       "product otherrwise.")
    price = fields.Float('Unit Price', required=True, help="This price will be considered as a price for the supplier "
                                                           "Unit of Measure if any or the default Unit of Measure of "
                                                           "the product otherwise")
    # digits_compute=dp.get_precision('Product Price'),
# class res_currency(osv.osv):
#     _inherit = 'res.currency'
#
#     def _check_main_currency_rounding(self, cr, uid, ids, context=None):
#         cr.execute('SELECT digits FROM decimal_precision WHERE name like %s',('Account',))
#         digits = cr.fetchone()
#         if digits and len(digits):
#             digits = digits[0]
#             main_currency = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
#             for currency_id in ids:
#                 if currency_id == main_currency.id:
#                     if float_compare(main_currency.rounding, 10 ** -digits, precision_digits=6) == -1:
#                         return False
#         return True
#
#     _constraints = [
#         (_check_main_currency_rounding, 'Error! You cannot define a rounding factor for the company\'s main currency that is smaller than the decimal precision of \'Account\'.', ['rounding']),
#     ]
#
# class decimal_precision(osv.osv):
#     _inherit = 'decimal.precision'
#
#     def _check_main_currency_rounding(self, cr, uid, ids, context=None):
#         cr.execute('SELECT id, digits FROM decimal_precision WHERE name like %s',('Account',))
#         res = cr.fetchone()
#         if res and len(res):
#             account_precision_id, digits = res
#             main_currency = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id
#             for decimal_precision in ids:
#                 if decimal_precision == account_precision_id:
#                     if float_compare(main_currency.rounding, 10 ** -digits, precision_digits=6) == -1:
#                         return False
#         return True
#
#     _constraints = [
#         (_check_main_currency_rounding, 'Error! You cannot define the decimal precision of \'Account\' as greater than the rounding factor of the company\'s main currency', ['digits']),
#     ]
#
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
