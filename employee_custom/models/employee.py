# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


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

    def _get_latest_contract(self):
        obj_contract = self.env['hr.contract']
        for emp in self:
            contract_ids = obj_contract.search([('employee_id', '=', emp.id), ], order='date_start')
            if contract_ids:
                emp.contract_id = contract_ids[-1:][0]
            else:
                emp.contract_id = False

    def _contracts_count(self):
        self.contracts_count = self.env['hr.contract'].search_count([('employee_id', '=', self.ids[0])])
        print(self.contracts_count)

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
    academic_ids = fields.One2many('hr.academic', 'employee_id', string='Affectations Département', )
    remuneration_ids = fields.One2many('hr.curriculum', 'employee_id', 'Rénumération', copy=True)
    date_pay = fields.Date("Date of Payment")  # check the name
    otherid = fields.Char('Other Id')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    tva = fields.Selection([('yes', 'Avec TPS/TVQ'), ('no', 'Sans TPS/TVQ')], string='tva')
    department_id = fields.Many2one('hr.department', string='Department')
    address_id = fields.Many2one('res.partner', string='Working Address')
    address_home_id = fields.Many2one('res.partner', string='Home Address')
    bank_account_id = fields.Many2one('res.partner.bank', 'Bank Account Number',
                                      domain="[('partner_id','=',address_home_id)]",
                                      help="Employee bank salary account")
    work_phone = fields.Char(string='Work Phone', readonly=False)
    mobile_phone = fields.Char(string='Work Mobile', readonly=False)
    work_email = fields.Char(string='Work Email', size=240)
    work_location = fields.Char(string='Office Location')
    notes = fields.Text('Notes')
    parent_id = fields.Many2one('hr.employee', string='Manager')
    category_ids = fields.Many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id',
                                    string='Tags')
    dep_ids = fields.Many2many('product.category', 'depart_category_rel', 'emp_id', 'depart_id', string='Tags')
    resource_id = fields.Many2one('resource.resource', string='Resource', ondelete='cascade', required=True,
                                  auto_join=True)
    coach_id = fields.Many2one('hr.employee', string='Coach')
    job_id = fields.Many2one('hr.job', string='Job Title')
    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary(string='Photo',
                          help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    # image_medium = fields.Binary(compute='_get_image', inverse='_set_image',
    #     string="Medium-sized photo",  multi="_get_image",
    #     store = {
    #         'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #     },
    #     help="Medium-sized photo of the employee. It is automatically "\
    #          "resized as a 128x128px image, with aspect ratio preserved. "\
    #          "Use this field in form views or some kanban views.")
    # image_small = fields.Binary(compute='_get_image', inverse='_set_image',
    #     string="Small-sized photo", multi="_get_image",
    #     store = {
    #         'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
    #     },
    #     help="Small-sized photo of the employee. It is automatically "\
    #          "resized as a 64x64px image, with aspect ratio preserved. "\
    #          "Use this field anywhere a small image is required.")
    passport_id = fields.Char('Passport No')
    is_resp = fields.Boolean('Color Index')
    is_super = fields.Boolean('Color Index')
    is_coor = fields.Boolean('Color Index')
    # 'city': fields.related('address_id', 'city', type='char', string='City'),
    # 'login': fields.related('user_id', 'login', type='char', string='Login', readonly=1),
    # 'last_login': fields.related('user_id', 'date', type='datetime', string='Latest Connection', readonly=1),
    lat = fields.Float(string=u'Latitude', digits=(9, 6))
    lng = fields.Float(string=u'Longitude', digits=(9, 6))
    map = fields.Text()
    soc = fields.Char(string='soc')
    tps = fields.Char(string='tps')
    tvq = fields.Char(string='tvq')
    adress1 = fields.Char('adress1')
    adress2 = fields.Char('adress2')
    adress3 = fields.Char('adress3')
    prov = fields.Char(string='prov')
    affect = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('manuel', 'Choix Manuel'),
    ],
        string='Status', copy=False)
    bons = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('manuel', 'Choix Manuel'),
    ],
        string='Status', copy=False)
    facture = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('manuel', 'Choix Manuel'),
    ],
        string='Status', copy=False)
    workflow = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
        ('manuel', 'Choix Manuel'),
    ],
        string='Status', copy=False)
    manager = fields.Boolean(string='Is a Manager')
    medic_exam = fields.Date(string='Medical Examination Date')
    place_of_birth = fields.Char(string='Place of Birth')
    children = fields.Integer(string='Number of Children')
    vehicle = fields.Char(string='Company Vehicle')
    vehicle_distance = fields.Integer('Home-Work Dist.', help="In kilometers")
    contract_ids = fields.One2many('hr.contract', 'employee_id', string='Contracts')
    contract_id = fields.Many2one('hr.contract', compute='_get_latest_contract', string='Contract',
                                  help='Latest contract of the employee')
    contracts_count = fields.Integer(compute='_contracts_count', string='Contrats')
    experience_ids = fields.One2many('hr.experience', 'employee_id', string='Expérience Professionnelles')
    certification_ids = fields.One2many('hr.certification', 'employee_id', string='Certifications')
    product_id = fields.Many2one('product.product', string=' Professional Experiences', )
    journal_id = fields.Many2one('account.analytic.journal', string=' Professional Experiences', )

    # def _get_default_image(self, cr, uid, context=None):
    #     image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
    #     return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))
    #
    # defaults = {
    #     'image': _get_default_image,
    # }
    #
    # def _broadcast_welcome(self, cr, uid, employee_id, context=None):
    #     """ Broadcast the welcome message to all users in the employee company. """
    #     employee = self.browse(cr, uid, employee_id, context=context)
    #     partner_ids = []
    #     _model, group_id = self.pool['ir.model.data'].get_object_reference(cr, uid, 'base', 'group_user')
    #     if employee.user_id:
    #         company_id = employee.user_id.company_id.id
    #     elif employee.company_id:
    #         company_id = employee.company_id.id
    #     elif employee.job_id:
    #         company_id = employee.job_id.company_id.id
    #     elif employee.department_id:
    #         company_id = employee.department_id.company_id.id
    #     else:
    #         company_id = self.pool['res.company']._company_default_get(cr, uid, 'hr.employee', context=context)
    #     res_users = self.pool['res.users']
    #     user_ids = res_users.search(
    #         cr, SUPERUSER_ID, [
    #             ('company_id', '=', company_id),
    #             ('groups_id', 'in', group_id)
    #         ], context=context)
    #     partner_ids = list(set(u.partner_id.id for u in res_users.browse(cr, SUPERUSER_ID, user_ids, context=context)))
    #     self.message_post(
    #         cr, uid, [employee_id],
    #         body=_('Welcome to %s! Please help him/her take the first steps with Odoo!') % (employee.name),
    #         partner_ids=partner_ids,
    #         subtype='mail.mt_comment', context=context
    #     )
    #     return True
    #
    # def create(self, cr, uid, data, context=None):
    #     context = dict(context or {})
    #     if context.get("mail_broadcast"):
    #         context['mail_create_nolog'] = True
    #
    #     employee_id = super(hr_employee, self).create(cr, uid, data, context=context)
    #
    #     if context.get("mail_broadcast"):
    #         self._broadcast_welcome(cr, uid, employee_id, context=context)
    #     return employee_id
    #
    # def unlink(self, cr, uid, ids, context=None):
    #     resource_ids = []
    #     for employee in self.browse(cr, uid, ids, context=context):
    #         resource_ids.append(employee.resource_id.id)
    #     super(hr_employee, self).unlink(cr, uid, ids, context=context)
    #     return self.pool.get('resource.resource').unlink(cr, uid, resource_ids, context=context)
    #
    @api.onchange('address')
    def onchange_address_id(self):
        if self.address:
            address = self.env['res.partner'].browse(self.address)
            return {'value': {'work_phone': address.phone, 'mobile_phone': address.mobile}}
        return {'value': {}}

    # @api.onchange('company_id')
    # def onchange_company(self):
    #     address_id = False
    #     if self.company_id:
    #         company_id = self.env['res.company'].browse(self.company_id.id)
    #         address = self.env['res.partner'].address_get([company_id.partner_id.id], ['default'])
    #         address_id = address and address['default'] or False
    #     return {'value': {'address_id': address_id}}

    @api.onchange('departement_id')
    def onchange_department_id(self):
        value = {'parent_id': False}
        if self.department_id:
            department = self.env['hr.department'].browse(self.department_id)
            value['parent_id'] = department.manager_id.id
        return {'value': value}

    @api.onchange('user_id')
    def onchange_user(self):
        work_email = False
        if self.user_id:
            work_email = self.env['res.users'].browse(self.user_id.id).email
        return {'value': {'work_email': work_email}}

    # def action_follow(self, cr, uid, ids, context=None):
    #     """ Wrapper because message_subscribe_users take a user_ids=None
    #         that receive the context without the wrapper. """
    #     return self.message_subscribe_users(cr, uid, ids, context=context)
    #
    # def action_unfollow(self, cr, uid, ids, context=None):
    #     """ Wrapper because message_unsubscribe_users take a user_ids=None
    #         that receive the context without the wrapper. """
    #     return self.message_unsubscribe_users(cr, uid, ids, context=context)
    #
    # def get_suggested_thread(self, cr, uid, removed_suggested_threads=None, context=None):
    #     """Show the suggestion of employees if display_employees_suggestions if the
    #     user perference allows it. """
    #     user = self.pool.get('res.users').browse(cr, uid, uid, context)
    #     if not user.display_employees_suggestions:
    #         return []
    #     else:
    #         return super(hr_employee, self).get_suggested_thread(cr, uid, removed_suggested_threads, context)
    #
    # def _message_get_auto_subscribe_fields(self, cr, uid, updated_fields, auto_follow_fields=None, context=None):
    #     """ Overwrite of the original method to always follow user_id field,
    #     even when not track_visibility so that a user will follow it's employee
    #     """
    #     if auto_follow_fields is None:
    #         auto_follow_fields = ['user_id']
    #     user_field_lst = []
    #     for name, field in self._fields.items():
    #         if name in auto_follow_fields and name in updated_fields and field.comodel_name == 'res.users':
    #             user_field_lst.append(name)
    #     return user_field_lst
    #
    # def _check_recursion(self, cr, uid, ids, context=None):
    #     level = 100
    #     while len(ids):
    #         cr.execute('SELECT DISTINCT parent_id FROM hr_employee WHERE id IN %s AND parent_id!=id',(tuple(ids),))
    #         ids = filter(None, map(lambda x:x[0], cr.fetchall()))
    #         if not level:
    #             return False
    #         level -= 1
    #     return True
    #
    # _constraints = [
    #     (_check_recursion, 'Error! You cannot create recursive hierarchy of Employee(s).', ['parent_id']),
    # ]
    #


class HrDepartment(models.Model):
    _name = "hr.department"

    # def _dept_name_get_fnc(self, cr, uid, ids, prop, unknow_none, context=None):
    #     res = self.name_get(cr, uid, ids, context=context)
    #     return dict(res)

    complete_name = fields.Char(compute='_dept_name_get_fnc', string='Name')
    company_id = fields.Many2one('res.company', string='Company', select=True, required=False)
    parent_id = fields.Many2one('hr.department', string='Parent Department', select=True)
    manager_id = fields.Many2one('hr.employee', string='Manager')

    # _defaults = {
    #     'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'hr.department', context=c),
    # }

    # def _check_recursion(self, cr, uid, ids, context=None):
    #     if context is None:
    #         context = {}
    #     level = 100
    #     while len(ids):
    #         cr.execute('select distinct parent_id from hr_department where id IN %s',(tuple(ids),))
    #         ids = filter(None, map(lambda x:x[0], cr.fetchall()))
    #         if not level:
    #             return False
    #         level -= 1
    #     return True
    #
    # _constraints = [
    #     (_check_recursion, 'Error! You cannot create recursive departments.', ['parent_id'])
    # ]
    #
    # def name_get(self, cr, uid, ids, context=None):
    #     if context is None:
    #         context = {}
    #     if not ids:
    #         return []
    #     if isinstance(ids, (int, long)):
    #         ids = [ids]
    #     reads = self.read(cr, uid, ids, ['name','parent_id'], context=context)
    #     res = []
    #     for record in reads:
    #         name = record['name']
    #         if record['parent_id']:
    #             name = record['parent_id'][1]+' / '+name
    #         res.append((record['id'], name))
    #     return res


class HrContractType(models.Model):
    _name = 'hr.contract.type'
    _description = 'Contract Type'
    name = fields.Char(string='Contract Type', required=True)


class HrContract(models.Model):
    _name = 'hr.contract'
    _description = 'Contract'
    name = fields.Char(string='Contract Reference', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    # department_id = fields.related('employee_id','department_id', type='many2one', relation='hr.department', string="Department", readonly=True)
    type_id = fields.Many2one('hr.contract.type', string='Contract Type', required=True)
    job_id = fields.Many2one('hr.job', string='Job Title')
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', default=lambda *a: time.strftime("%Y-%m-%d"))
    trial_date_start = fields.Date(string='Trial Start Date')
    trial_date_end = fields.Date(string='Trial End Date')
    working_hours = fields.Many2one('resource.calendar', 'Working Schedule')
    wage = fields.Float(string='Wage', digits=(16, 2), required=True, help="Basic Salary of the employee")
    advantages = fields.Text(string='Advantages')
    notes = fields.Text(string='Notes')
    permit_no = fields.Char(string='Work Permit No', required=False, readonly=False)
    visa_no = fields.Char(string='Visa No', required=False, readonly=False)
    visa_expire = fields.Date('Visa Expire Date')
    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'quarterly'),
        ('semi-annually', 'semi-annually'),
        ('annually', 'annually'),
        ('weekly', 'weekly'),
        ('bi-weekly', 'bi-weekly'),
        ('bi-monthly', 'bi-monthly'),
        ], string='type de payment')

    # def _get_type(self, cr, uid, context=None):
    #     type_ids = self.pool.get('hr.contract.type').search(cr, uid, [('name', '=', 'Employee')])
    #     return type_ids and type_ids[0] or False
    #
    # _defaults = {
    #     'type_id': _get_type
    # }
    #
    # def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
    #     if not employee_id:
    #         return {'value': {'job_id': False}}
    #     emp_obj = self.pool.get('hr.employee').browse(cr, uid, employee_id, context=context)
    #     job_id = False
    #     if emp_obj.job_id:
    #         job_id = emp_obj.job_id.id
    #     return {'value': {'job_id': job_id}}
    #
    # def _check_dates(self, cr, uid, ids, context=None):
    #     for contract in self.read(cr, uid, ids, ['date_start', 'date_end'], context=context):
    #          if contract['date_start'] and contract['date_end'] and contract['date_start'] > contract['date_end']:
    #              return False
    #     return True

    # _constraints = [
    #     (_check_dates, 'Error! Contract start-date must be less than contract end-date.', ['date_start', 'date_end'])
    # ]


class HrCurriculum(models.Model):
    _name = 'hr.curriculum'
    _description = "Employee's Curriculum"
    _rec_name = 'employee_id'
    # _inherit = 'ir.needaction_mixin'

    #     # Allow the possibility to attachements to curriculum
    #     # even if it's a diploma, degree...

    name = fields.Char('Name')
    employee_id = fields.Many2one('hr.employee', string='Employee', )
    start_date = fields.Date('Start date')
    end_date = fields.Date('End date')
    description = fields.Text('Description')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 help="Employer, School, University ,Certification Authority")
    location = fields.Char('Location', help="Location")
    expire = fields.Boolean('Expire', help="Expire", default=True)
    product_id = fields.Many2one('product.product', string=' Professional Experiences', )
    project_id = fields.Many2one('project.project', string=' Professional Experiences', )
    categ_id = fields.Many2one('product.category', string=' Professional Experiences', )
    amount = fields.Float(string='Diploma', )
    amount2 = fields.Float(string='Diploma', )
    currency_id = fields.Many2one('res.currency', string=' Professional Experiences', default=5, )
    uom_id = fields.Many2one('product.uom', string=' Professional Experiences', )
    uom_id2 = fields.Many2one('product.uom', string=' Professional Experiences', )
    aca_id = fields.Many2one('hr.academic', string=' Professional Experiences', )
    # status = fields.Selection([
    #     ('valide', 'Valide'),
    #     ('invalide', 'Invalide')], string='Status')
    #
    # def onchange_end_date(self, cr, uid, ids, end_date, context=None):
    #     result = {'value': {}}
    #     DATETIME_FORMAT = "%Y-%m-%d"
    #     if end_date:
    #         if datetime.strptime(end_date, DATETIME_FORMAT) < datetime.now():
    #             result['value']['status'] = 'invalide'
    #         else:
    #             result['value']['status'] = 'valide'
    #
    #     return result


class HrAcademic(models.Model):
    _name = 'hr.academic'
    _inherit = 'hr.curriculum'

    diploma = fields.Char(string='Diploma', translate=True)
    study_field = fields.Char(string='Field of study', translate=True, )
    activities = fields.Text(string='Activities and associations',
                             translate=True)
    role_id = fields.Many2one('res.users.role', string=' Professional Experiences', )
    curr_ids = fields.One2many('hr.curriculum', 'aca_id', string=u"Role lines", copy=True)

    # def onchange_project_id(self, cr, uid, ids, project_id, context=None):
    #     if project_id:
    #         department = self.pool.get('project.project').browse(cr, uid, project_id)
    #         value['partner_id'] = department.partner_id.id
    #     return {'value': value}


class HrExperience(models.Model):
    _name = 'hr.experience'
    _inherit = 'hr.curriculum'

    category = fields.Selection([('professional', 'Professional'),
                                 ('academic', 'Academic'),
                                 ('certification', 'Certification')],
                                'Category', default='professional', help='Category')


class HrCertification(models.Model):
    _name = 'hr.certification'
    _inherit = 'hr.curriculum'

    certification = fields.Char(string='Certification Number', help='Certification Number')


class AccountAnalyticJournal(models.Model):
    _name = 'account.analytic.journal'

