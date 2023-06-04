# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TaskCustom(models.Model):
    _description = 'custom Task'
    _inherit = 'project.task'
    _date_name = "date_start"
    _rec_name = 'id'

    @api.depends_context('uid')
    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('om_hospital.group_super_admin')

    def _get_planned(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(hours), 0.0) FROM project_task_work WHERE project_task_work.task_id IN %s GROUP BY task_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_planned = hours.get(rec.id, 0.0)

    def _get_progress_qty(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.state='valid' and project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            if rec.qte > 0:
                ratio = hours.get(rec.id, 0.0) / rec.qte
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_qty = ratio

    def _get_progress_amount(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            if rec.total > 0:
                ratio = hours.get(rec.id, 0.0) * rec.cout / rec.total
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_amount = round(min(100.0 * ratio, 100), 2)

    def _get_sum(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            if rec.total > 0:
                ratio = hours.get(rec.id, 0.0) * rec.cout
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.total_r = ratio

    def _get_qty(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.poteau_r = hours.get(rec.id, 0.0)

    def _get_effective(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(hours),0) FROM project_task_work WHERE task_id IN %s GROUP BY task_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_effective = hours.get(rec.id, 0.0)

    def _get_remaining(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(hours)) FROM project_task_work WHERE task_id IN %s GROUP BY task_id",
            (tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.total_remaining = hours.get(rec.id, 0.0)

    def _get_hours(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE state in %s and  project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            rec.hours_r = hours.get(rec.id, 0.0)

    def _get_progress(self):

        self.env.cr.execute(
            "SELECT task_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.task_id IN %s GROUP BY task_id",
            (('valid', 'paid'), tuple(self.ids),))
        hours = dict(self.env.cr.fetchall())
        for rec in self:
            if rec.planned_hours > 0:
                ratio = hours.get(rec.id, 0.0) / rec.planned_hours
            else:
                ratio = hours.get(rec.id, 0.0)
            rec.progress_me = round(min(100.0 * ratio, 100), 2)

    def _is_template(self):

        for task in self:
            task.active = True
            if task.project_id:
                if task.project_id.active == False or task.project_id.state == 'template':
                    task.active = False

    is_super_admin = fields.Boolean(string='Is Admin', compute='_compute_is_super_admin')
    active = fields.Boolean(compute='_is_template', store=True, string='Not a Template Task', type='boolean',
                            help="This field is computed automatically and have the same behavior than the boolean "
                                 "'active' field: if the task is linked to a template or unactivated project, "
                                 "it will be hidden unless specifically asked.")
    name = fields.Char(string='Task Summary', track_visibility='onchange', size=128, select=True, readonly=True,
                       states={'draft': [('readonly', False)]}, )
    dc = fields.Char(string='Task Summary', track_visibility='onchange', size=128, select=True,readonly=True,
                     states={'draft': [('readonly', False)]}, )
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]}, )
    priority = fields.Selection([('0', 'Faible'), ('1', 'Normale'), ('2', 'Elevée')], 'Priority', select=True,
                                readonly=True, states={'draft': [('readonly', False)]}, )
    sequence = fields.Integer(string='Sequence', readonly=True, states={'draft': [('readonly', False)]}, )
    stage_id = fields.Many2one('project.task.type', 'Stage', track_visibility='onchange', select=True,
                               domain="[('project_ids', '=', project_id)]", copy=False, )
    categ_ids = fields.Many2many('project.category', string='Tags', )
    kanban_state = fields.Selection(
        [('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')], 'Kanban State',
        track_visibility='onchange',
        help="A task's kanban state indicates special situations affecting it:\n"
             " * Normal is the default situation\n"
             " * Blocked indicates something is preventing the progress of this task\n"
             " * Ready for next stage indicates the task is ready to be pulled to the next stage",
        required=False, copy=False)
    create_date = fields.Datetime('Create Date', index=True, )
    write_date = fields.Datetime(string='Last Modification Date', index=True, )
    # not displayed in the view but it might be useful with base_action_rule module (and it needs to be defined first for that)
    date_start = fields.Date(string='Starting Date', index=True, copy=True, )
    date_end = fields.Date(string='Ending Date', index=True, copy=True, )
    date_deadline = fields.Date(string='Deadline', index=True, copy=True, )
    date_last_stage_update = fields.Datetime(string='Last Stage Update', index=True, copy=False, )
    project_id = fields.Many2one('project.project', string='Project', ondelete='set null', select=True,
                                 track_visibility='onchange', change_default=True, )
    parent_ids = fields.Many2many('project.task', 'project_task_parent_rel', 'task_id', 'parent_id',
                                  string='Parent Tasks')
    child_ids = fields.Many2many('project.task', 'project_task_parent_rel', 'parent_id', 'task_id',
                                 string='Delegated Tasks')
    notes = fields.Text('Notes', )
    hours_r = fields.Float(compute='_get_hours', string='Company Currency', )
    total_r = fields.Float(compute='_get_sum', string='Company Currency', )
    poteau_r = fields.Float(compute='_get_qty', string='poteau_r', )
    total_planned = fields.Float(compute='_get_planned', string='Company Currency', )
    total_effective = fields.Float(compute='_get_effective', string='Company Currency', )
    total_remaining = fields.Float(compute='_get_remaining', string='Company Currency', )
    progress_me = fields.Float(compute='_get_progress', string='Company Currency', )
    product_id = fields.Many2one('product.product', string='Product', ondelete='cascade', select="1", )
    kit_id = fields.Many2one('product.kit', 'Kit ID', ondelete='cascade', select="1", )
    planned_hours = fields.Float(string='Initially Planned Hours',
                                 help='Estimated time to do the task, usually set by the project manager when the '
                                      'task is in draft state.', )
    remaining_hours = fields.Float(string='Remaining Hours', digits=(16, 2),
                                   help="Total remaining time, can be re-estimated periodically by the assignee of "
                                        "the task.", )
    # 'effective_hours': fields.function(_hours_get, string='Hours Spent', multi='hours',
    #                                    help="Computed using the sum of the task work done.",
    #                                    store={
    #                                        'project.task': (lambda self, cr, uid, ids, c={}: ids,
    #                                                         ['work_ids', 'remaining_hours', 'planned_hours'], 10),
    #                                        'project.task.work': (_get_task, ['hours'], 10),
    #                                    }),
    # total_hours = fields.function(_hours_get, string='Total', multi='hours',
    #                                help="Computed as: Time Spent + Remaining Time.",
    #                                store={
    #                                    'project.task': (lambda self, cr, uid, ids, c={}: ids,
    #                                                     ['work_ids', 'remaining_hours', 'planned_hours'], 10),
    #                                    'project.task.work': (_get_task, ['hours'], 10),
    #                                })
    # 'progress': fields.function(_hours_get, string='Working Time Progress (%)', multi='hours', group_operator="avg",
    #                             help="If the task has a progress of 99.99% you should close the task if it's finished or reevaluate the time",
    #                             store={
    #                                 'project.task': (lambda self, cr, uid, ids, c={}: ids,
    #                                                  ['work_ids', 'remaining_hours', 'planned_hours', 'state',
    #                                                   'stage_id'], 10),
    #                                 'project.task.work': (_get_task, ['hours'], 10),
    #                             }),
    # 'delay_hours': fields.function(_hours_get, string='Delay Hours', multi='hours',
    #                                help="Computed as difference between planned hours by the project manager and the total hours of the task.",
    #                                store={
    #                                    'project.task': (lambda self, cr, uid, ids, c={}: ids,
    #                                                     ['work_ids', 'remaining_hours', 'planned_hours'], 10),
    #                                    'project.task.work': (_get_task, ['hours'], 10),
    #                                }),
    reviewer_id = fields.Many2one('hr.employee', string='Reviewer', select=True, track_visibility='onchange', )
    reviewer_id1 = fields.Many2one('hr.employee', 'Reviewer 2', select=True, track_visibility='onchange', )
    coordin_id = fields.Many2one('hr.employee', string='Coordinator', select=True, track_visibility='onchange', )
    coordin_id1 = fields.Many2one('hr.employee', string='Coordinator 2', select=True, track_visibility='onchange', )
    coordin_id2 = fields.Many2one('hr.employee', string='Coordinator 3', select=True, track_visibility='onchange', )
    coordin_id3 = fields.Many2one('hr.employee', string='Coordinator 4', select=True, track_visibility='onchange', )
    coordin_id4 = fields.Many2one('hr.employee', string='Coordinator 5', select=True, track_visibility='onchange', )
    coordin_id5 = fields.Many2one('hr.employee', string='Coordinator 6', select=True, track_visibility='onchange', )
    coordin_id6 = fields.Many2one('hr.employee', string='Coordinator 7', select=True, track_visibility='onchange', )
    coordin_id7 = fields.Many2one('hr.employee', string='Coordinator 8', select=True, track_visibility='onchange',)
    coordin_id8 = fields.Many2one('hr.employee', string='Coordinator 9', select=True, track_visibility='onchange', )
    coordin_id9 = fields.Many2one('hr.employee', string='Coordinator 10', select=True, track_visibility='onchange', )
    coordin_id10 = fields.Many2one('hr.employee', string='Coordinator 11', select=True, track_visibility='onchange', )
    current_ph = fields.Char(string='Phase En cours', )
    pourc = fields.Float(string='Time Spent', )
    pourc_t = fields.Float(string='% Avancement', )
    pourc_f = fields.Float(string='% Dépense', )
    user_id = fields.Many2one('res.users', string='Assigned to', select=True, track_visibility='onchange', )

    partner_id = fields.Many2one('res.partner', string='Customer', )
    work_ids = fields.One2many('project.task.work', 'task_id', string='Work done',
                               copy=False, )
    work_ids2 = fields.One2many('project.task.work', 'task_id', copy=False, )
    company_id = fields.Many2one('res.company', string='Company', )
    zone = fields.Integer(string='Zone', )
    secteur = fields.Integer(string='Secteur', )
    categ_id = fields.Many2one('product.category', string='Tags', )
    color = fields.Integer(string='Color Index', )
    done = fields.Boolean(string='Color Index', )
    ct = fields.Float(string='CT', )
    cp = fields.Float(string='CP', )
    dependency_task_ids = fields.Many2many('project.task', 'project_task_dependency_task_rel',
                                           'dependency_task_id', 'task_id', string='Dependencies')
    cout = fields.Float(string='Cout', )
    qte = fields.Float(string='Quantity', )
    ftp = fields.Char(string='ftp', )
    state_id = fields.Many2one('res.country.state', string='State', readonly=True)
    city = fields.Char('City', )
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, )
    total = fields.Float(string='Total', )
    state = fields.Selection([('template', 'Template'),
                              ('draft', 'Brouillon'),
                              ('open', 'Confirmé'),
                              ('close', 'Terminé'),
                              ('cancelled', 'Annulée'),
                              ('pending', 'Suspendu'),
                              ],
                             string='Status', copy=False)
    etape = fields.Char(string='etap', )
    progress_qty = fields.Float(compute='_get_progress_qty', string='Company Currency')
    progress_amount = fields.Float(compute='_get_progress_amount', string='Company Currency')
    rank = fields.Char(string='Rank', )
    display = fields.Boolean(string='Color Index')
    # 'manager_id': fields.related('project_id', 'analytic_account_id', 'user_id', type='many2one',
    #                              relation='res.users', string='Project Manager')
    # 'user_email': fields.related('user_id', 'email', type='char', string='User Email',
    #                            , )
    # 'delegated_user_id': fields.related('child_ids', 'user_id', type='many2one', relation='res.users',
    #                                     string='Delegated To',
    #                                   , )


class ProjectCategory(models.Model):
    """ Category of project's task (or issue) """
    _name = "project.category"
    _description = "Category of project's task, issue, ..."

    name = fields.Char(string='Name', required=True, translate=True)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    _description = 'Task Stage'
    _order = 'sequence'

    name = fields.Char(string='Stage Name', translate=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence')
    case_default = fields.Boolean('Default for New Projects',
                                  help="If you check this field, this stage will be proposed by default on each new "
                                       "project. It will not assign this stage to existing projects.")
    project_ids = fields.Many2many('project.project', 'project_task_type_rel', 'type_id', 'project_id',
                                   string='Projects')
    fold = fields.Boolean(string='Folded in Kanban View',
                          help='This stage is folded in the kanban view when'
                               'there are no records in that stage to display.')
    categ_id = fields.Many2one('project.category', string='Tags')
    category_id = fields.Many2one('product.category', string='Tags')
    product_id = fields.Many2one('product.product', string='Tags')
    line_id = fields.Many2one('wiz.fees_manual.invoice', string='Tags')
    lines_id = fields.Many2one('agreement.fees.amortization_line', string='Tags')
    qty = fields.Float(string='Quantity')


class ProductKit(models.Model):
    _name = "product.kit"
    name = fields.Char('Name')


class ProductUOM(models.Model):
    _name = "product.uom"
    name = fields.Char('Name')
