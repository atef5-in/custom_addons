# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployeeCategory(models.Model):
    _inherit = "hr.employee.category"
    _description = "Employee Category"

    # def name_get(self, cr, uid, ids, context=None):
    #     if not ids:
    #         return []
    #     reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
    #     res = []
    #     for record in reads:
    #         name = record['name']
    #         if record['parent_id']:
    #             name = record['parent_id'][1]+' / '+name
    #         res.append((record['id'], name))
    #     return res

    # def _name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.name_get(cr, uid, ids, context=context)
    #     return dict(res)

    name = fields.Char(string='Employee Tag', required=True)
    complete_name = fields.Char(compute='_name_get_fnc', string='Name')
    parent_id = fields.Many2one('hr.employee.category', string='Parent Employee Tag', select=True)
    child_ids = fields.One2many('hr.employee.category', 'parent_id', string='Child Categories')
    employee_ids = fields.Many2many('hr.employee', 'employee_category_rel', 'category_id', 'emp_id', 'Employees')

    # def _check_recursion(self, cr, uid, ids, context=None):
    #     level = 100
    #     while len(ids):
    #         cr.execute('select distinct parent_id from hr_employee_category where id IN %s', (tuple(ids), ))
    #         ids = filter(None, map(lambda x:x[0], cr.fetchall()))
    #         if not level:
    #             return False
    #         level -= 1
    #     return True
    #
    # _constraints = [
    #     (_check_recursion, 'Error! You cannot create recursive Categories.', ['parent_id'])
    # ]


class HrJob(models.Model):
    _inherit = 'hr.job'
    # _inherit = 'ir.needaction_mixin'

    description = fields.Text(string='Job Description')
    state = fields.Selection([('open', 'Recruitment Closed'), ('recruit', 'Recruitment in Progress')],
                             string='Status', readonly=True, required=True,
                             track_visibility='always', copy=False, default='open',
                             help="By default 'Closed', set it to 'In Recruitment' if recruitment process is going on "
                                  "for this job position.")

    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id, department_id)',
         'The name of the job position must be unique per department in company!'),
        ('hired_employee_check', "CHECK ( no_of_hired_employee <= no_of_recruitment )",
         "Number of hired employee must be less than expected number of employee in recruitment.")
    ]

    # def set_recruit(self, cr, uid, ids, context=None):
    #     for job in self.browse(cr, uid, ids, context=context):
    #         no_of_recruitment = job.no_of_recruitment == 0 and 1 or job.no_of_recruitment
    #         self.write(cr, uid, [job.id], {'state': 'recruit', 'no_of_recruitment': no_of_recruitment}, context=context)
    #     return True
    #
    # def set_open(self, cr, uid, ids, context=None):
    #     self.write(cr, uid, ids, {
    #         'state': 'open',
    #         'no_of_recruitment': 0,
    #         'no_of_hired_employee': 0
    #     }, context=context)
    #     return True
    #
    # def copy(self, cr, uid, id, default=None, context=None):
    #     if default is None:
    #         default = {}
    #     if 'name' not in default:
    #         job = self.browse(cr, uid, id, context=context)
    #         default['name'] = _("%s (copy)") % (job.name)
    #     return super(hr_job, self).copy(cr, uid, id, default=default, context=context)

    # ----------------------------------------
    # Compatibility methods
    # ----------------------------------------
    # _no_of_employee = _get_nbr_employees  # v7 compatibility
    # job_open = set_open  # v7 compatibility
    # job_recruitment = set_recruit  # v7 compatibility

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    # _order = 'name_related'
    # _inherits = {'resource.resource': "resource_id"}

    # def _get_image(self, cr, uid, ids, name, args, context=None):
    #     result = dict.fromkeys(ids, False)
    #     for obj in self.browse(cr, uid, ids, context=context):
    #         result[obj.id] = tools.image_get_resized_images(obj.image)
    #     return result
    #
    # def _set_image(self, cr, uid, id, name, value, args, context=None):
    #     return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

    # we need a related field in order to be able to sort the employee by name
    # 'name_related': fields.related('resource_id', 'name', type='char', string='Name', readonly=True, store=True),
    renumeration_ids = fields.One2many('hr.curriculum', 'employee_id', 'Rénumération', copy=True)
    date_pay = fields.Date("Date of Payment") # check the name
    otherid = fields.Char('Other Id')
    'gender': fields.selection([('male', 'Male'), ('female', 'Female')], 'Gender'),
    'tva': fields.selection([('yes', 'Avec TPS/TVQ'), ('no', 'Sans TPS/TVQ')], 'tva'),
    'marital': fields.selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
    'department_id': fields.many2one('hr.department', 'Department'),
    'address_id': fields.many2one('res.partner', 'Working Address'),
    'address_home_id': fields.many2one('res.partner', 'Home Address'),
    'bank_account_id': fields.many2one('res.partner.bank', 'Bank Account Number', domain="[('partner_id','=',address_home_id)]", help="Employee bank salary account"),
    'work_phone': fields.char('Work Phone', readonly=False),
    'mobile_phone': fields.char('Work Mobile', readonly=False),
    'work_email': fields.char('Work Email', size=240),
    'work_location': fields.char('Office Location'),
    'notes': fields.text('Notes'),
    'parent_id': fields.many2one('hr.employee', 'Manager'),
    'category_ids': fields.many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags'),
    'child_ids': fields.one2many('hr.employee', 'parent_id', 'Subordinates'),
    ##'dep_ids': fields.one2many('product.category', 'employee_id', 'Subordinates'),
    'dep_ids': fields.many2many('product.category', 'depart_category_rel', 'emp_id', 'depart_id', 'Tags'),
    'resource_id': fields.many2one('resource.resource', 'Resource', ondelete='cascade', required=True, auto_join=True),
    'coach_id': fields.many2one('hr.employee', 'Coach'),
    'job_id': fields.many2one('hr.job', 'Job Title'),
    # image: all image fields are base64 encoded and PIL-supported
    'image': fields.binary("Photo",
        help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
    'image_medium': fields.function(_get_image, fnct_inv=_set_image,
        string="Medium-sized photo", type="binary", multi="_get_image",
        store = {
            'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        },
        help="Medium-sized photo of the employee. It is automatically "\
             "resized as a 128x128px image, with aspect ratio preserved. "\
             "Use this field in form views or some kanban views."),
    'image_small': fields.function(_get_image, fnct_inv=_set_image,
        string="Small-sized photo", type="binary", multi="_get_image",
        store = {
            'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        },
        help="Small-sized photo of the employee. It is automatically "\
             "resized as a 64x64px image, with aspect ratio preserved. "\
             "Use this field anywhere a small image is required."),
    'passport_id': fields.char('Passport No'),
    'color': fields.integer('Color Index'),
    'is_resp': fields.boolean('Color Index'),
    'is_super': fields.boolean('Color Index'),
    'is_coor': fields.boolean('Color Index'),
    'city': fields.related('address_id', 'city', type='char', string='City'),
    'login': fields.related('user_id', 'login', type='char', string='Login', readonly=1),
    'last_login': fields.related('user_id', 'date', type='datetime', string='Latest Connection', readonly=1),
    'lat': fields.float(u'Latitude', digits=(9, 6)),
    'lng': fields.float(u'Longitude', digits=(9, 6)),
    'map': fields.dummy(),
    'soc': fields.char('soc'),
    'tps': fields.char('tps'),
    'tvq': fields.char('tvq'),
    'adress1': fields.char('adress1'),
    'adress2': fields.char('adress2'),
    'adress3': fields.char('adress3'),
    'prov': fields.char('prov'),
    'affect': fields.selection([
                               ('yes', 'Oui'),
                               ('no', 'Non'),
                               ('manuel', 'Choix Manuel'),
                               ],
                              'Status',  copy=False),
    'bons': fields.selection([
                               ('yes', 'Oui'),
                               ('no', 'Non'),
                               ('manuel', 'Choix Manuel'),
                               ],
                              'Status',  copy=False),
    'facture': fields.selection([
                               ('yes', 'Oui'),
                               ('no', 'Non'),
                               ('manuel', 'Choix Manuel'),
                               ],
                              'Status',  copy=False),
    'workflow': fields.selection([
                               ('yes', 'Oui'),
                               ('no', 'Non'),
                               ('manuel', 'Choix Manuel'),
                               ],
                              'Status',  copy=False),

    def _get_default_image(self, cr, uid, context=None):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    defaults = {
        'active': 1,
        'image': _get_default_image,
        'color': 0,
    }

    def _broadcast_welcome(self, cr, uid, employee_id, context=None):
        """ Broadcast the welcome message to all users in the employee company. """
        employee = self.browse(cr, uid, employee_id, context=context)
        partner_ids = []
        _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_user')
        if employee.user_id:
            company_id = employee.user_id.company_id.id
        elif employee.company_id:
            company_id = employee.company_id.id
        elif employee.job_id:
            company_id = employee.job_id.company_id.id
        elif employee.department_id:
            company_id = employee.department_id.company_id.id
        else:
            company_id = self.pool['res.company']._company_default_get(cr, uid, 'hr.employee', context=context)
        res_users = self.pool['res.users']
        user_ids = res_users.search(
            cr, SUPERUSER_ID, [
                ('company_id', '=', company_id),
                ('groups_id', 'in', group_id)
            ], context=context)
        partner_ids = list(set(u.partner_id.id for u in res_users.browse(cr, SUPERUSER_ID, user_ids, context=context)))
        self.message_post(
            cr, uid, [employee_id],
            body=_('Welcome to %s! Please help him/her take the first steps with Odoo!') % (employee.name),
            partner_ids=partner_ids,
            subtype='mail.mt_comment', context=context
        )
        return True

    def create(self, cr, uid, data, context=None):
        context = dict(context or {})
        if context.get("mail_broadcast"):
            context['mail_create_nolog'] = True

        employee_id = super(hr_employee, self).create(cr, uid, data, context=context)

        if context.get("mail_broadcast"):
            self._broadcast_welcome(cr, uid, employee_id, context=context)
        return employee_id

    def unlink(self, cr, uid, ids, context=None):
        resource_ids = []
        for employee in self.browse(cr, uid, ids, context=context):
            resource_ids.append(employee.resource_id.id)
        super(hr_employee, self).unlink(cr, uid, ids, context=context)
        return self.pool.get('resource.resource').unlink(cr, uid, resource_ids, context=context)

    def onchange_address_id(self, cr, uid, ids, address, context=None):
        if address:
            address = self.pool.get('res.partner').browse(cr, uid, address, context=context)
            return {'value': {'work_phone': address.phone, 'mobile_phone': address.mobile}}
        return {'value': {}}

    def onchange_company(self, cr, uid, ids, company, context=None):
        address_id = False
        if company:
            company_id = self.pool.get('res.company').browse(cr, uid, company, context=context)
            address = self.pool.get('res.partner').address_get(cr, uid, [company_id.partner_id.id], ['default'])
            address_id = address and address['default'] or False
        return {'value': {'address_id': address_id}}

    def onchange_department_id(self, cr, uid, ids, department_id, context=None):
        value = {'parent_id': False}
        if department_id:
            department = self.pool.get('hr.department').browse(cr, uid, department_id)
            value['parent_id'] = department.manager_id.id
        return {'value': value}

    def onchange_user(self, cr, uid, ids, user_id, context=None):
        work_email = False
        if user_id:
            work_email = self.pool.get('res.users').browse(cr, uid, user_id, context=context).email
        return {'value': {'work_email': work_email}}

    def action_follow(self, cr, uid, ids, context=None):
        """ Wrapper because message_subscribe_users take a user_ids=None
            that receive the context without the wrapper. """
        return self.message_subscribe_users(cr, uid, ids, context=context)

    def action_unfollow(self, cr, uid, ids, context=None):
        """ Wrapper because message_unsubscribe_users take a user_ids=None
            that receive the context without the wrapper. """
        return self.message_unsubscribe_users(cr, uid, ids, context=context)

    def get_suggested_thread(self, cr, uid, removed_suggested_threads=None, context=None):
        """Show the suggestion of employees if display_employees_suggestions if the
        user perference allows it. """
        user = self.pool.get('res.users').browse(cr, uid, uid, context)
        if not user.display_employees_suggestions:
            return []
        else:
            return super(hr_employee, self).get_suggested_thread(cr, uid, removed_suggested_threads, context)

    def _message_get_auto_subscribe_fields(self, cr, uid, updated_fields, auto_follow_fields=None, context=None):
        """ Overwrite of the original method to always follow user_id field,
        even when not track_visibility so that a user will follow it's employee
        """
        if auto_follow_fields is None:
            auto_follow_fields = ['user_id']
        user_field_lst = []
        for name, field in self._fields.items():
            if name in auto_follow_fields and name in updated_fields and field.comodel_name == 'res.users':
                user_field_lst.append(name)
        return user_field_lst

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute('SELECT DISTINCT parent_id FROM hr_employee WHERE id IN %s AND parent_id!=id',(tuple(ids),))
            ids = filter(None, map(lambda x:x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion, 'Error! You cannot create recursive hierarchy of Employee(s).', ['parent_id']),
    ]

