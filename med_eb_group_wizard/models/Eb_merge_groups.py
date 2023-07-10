# # -*- coding: utf-8 -*-
#

from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import datetime as dt
import math


#
class EbMergegroups(models.Model):
    _name = "base.group.merge.automatic.wizard"
    _description = "Declararion des bons"
    _rec_name = "id"

    # obj = fields.Char('name')
    # name = fields.Char('name')

    reviewer_id1 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id10 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id9 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id8 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id7 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id6 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id5 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id4 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id3 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id2 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id1 = fields.Many2one('hr.employee', string='Wizard')
    gest_id_ = fields.Many2one('hr.employee', string='Wizard')
    gest_id2 = fields.Many2one('hr.employee', string='Wizard')
    coordin_id = fields.Many2one('hr.employee', string='Wizard')
    emp_id2 = fields.Many2one('hr.employee', string='Wizard')
    gest_id = fields.Many2one('hr.employee', string='Wizard')
    bon_id = fields.Many2one('base.group.merge.automatic.wizard', string='Wizard')
    work_ids = fields.Many2many('project.task.work', string='groups')
    dst_work_ids = fields.Many2one('project.task.work', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")

    line_ids2 = fields.One2many(
        'group_line.show.line2', 'group_id',
        # domain=[('product_id.name', 'ilike', 'qualit')], to uncomment
        string=u"Role lines",
        copy=True)
    line_ids3 = fields.One2many(
        'group_line.show.line2', 'group_id', domain=[('product_id.name', 'ilike', 'correction')], string=u"Role lines",
        copy=True)

    line_ids = fields.One2many(
        'base.group.merge.line', 'wizard_id', string="Role lines", copy=True, )
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    categ_id = fields.Many2one('product.category', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    pay_id = fields.Many2one('hr.payslip', string='Wizard')
    date_start_r = fields.Date(string='Assigned', default=fields.Date.context_today)
    date_end_r = fields.Date(string='Assigned')
    # name = fields.Char(string='Numero Groupement')
    employee_id = fields.Many2one('hr.employee', string='Assigned')
    hours_r = fields.Float(string='Assigned')
    hours = fields.Float(string='Assigned')
    total_t = fields.Float(string='Assigned')
    total_r = fields.Float(string='Assigned')
    poteau_t = fields.Integer(string='Assigned')
    poteau_r = fields.Integer(string='Assigned')
    poteau_reste = fields.Integer(string='Assigned')
    sequence = fields.Integer(string='Assigned')
    zo = fields.Char(string='Assigned')
    sect = fields.Char(string='Assigned')
    secteur = fields.Integer(string='Assigned')
    state = fields.Selection([('draft', 'Brouillon'),
                              ('tovalid', 'Dde Validation'),
                              ('valid', 'Bons Validés'),
                              ('invoiced', 'Bons Facturés'),

                              ], default='draft')
    type1 = fields.Selection([
        ('bon', 'Bon de Production'),
        ('controle', 'Bon de Controle'),
        ('correction', 'Bon de Correction'),

    ])

    active = fields.Boolean('active', default=True)
    state1 = fields.Selection([('draft', 'Brouillon'),
                               ('tovalid', 'Dde Validation'),
                               ('valid', 'Controles Validés'),
                               ('invoiced', 'Bons Facturés'),

                               ], default='draft')
    state2 = fields.Selection([('draft', 'Brouillon'),
                               ('tovalid', 'Dde Validation'),
                               ('valid', 'Corrections Validés'),
                               ('invoiced', 'Bons Facturés'),

                               ], default='draft')
    state3 = fields.Selection([('draft', 'Bon Encours'),

                               ('valid', 'Bon Cloturé'),

                               ], default='draft')

    note = fields.Text(string='Assigned')
    note1 = fields.Text(string='Assigned')
    note2 = fields.Text(string='Assigned')
    note3 = fields.Text(string='Assigned')
    note4 = fields.Text(string='Assigned')
    note5 = fields.Text(string='Assigned')
    note_con = fields.Text(string='Assigned')
    note_corr = fields.Text(string='Assigned')

    to1 = fields.Char(string='char')
    cc1 = fields.Char(string='char')
    cci1 = fields.Char(string='char')
    to2 = fields.Char(string='char')
    cc2 = fields.Char(string='char')
    cci2 = fields.Char(string='char')
    states = fields.Char(string='char')
    ftp = fields.Char(string='FTP')
    num = fields.Char(string='Num')
    sadmin = fields.Boolean(compute='_sadmin', string='Is doctor?')  ##, default=_disponible
    done = fields.Boolean(compute='_disponible', string='Is doctor?')  ##, default=_disponible
    done1 = fields.Boolean(compute='_disponible1', string='Is doctor?', default=False)  ##, default=_disponible
    ##
    # is_kit = fields.Boolean(related="project_id.is_kit", string="Email")

    donecq = fields.Boolean(compute='_disponiblecq', string='Is doctor?')  ##, default=_disponible
    doneco = fields.Boolean(compute='_disponibleco', string='Is doctor?')  ##, default=_disponible
    # dc_ = fields.Boolean(compute='_disponible', string='Is doctor?')  ##, default=_disponible
    # dq_ = fields.Boolean(compute='_disponible', string='Is doctor?')  ##, default=_disponible

    done_ = fields.Boolean(compute='_disponible2', string='Is doctor?')  ##, default=_disponible
    done1_ = fields.Boolean(compute='_compute_done1_', string='done1_')  ##, default=_disponible
    ##
    done__ = fields.Boolean(compute='_disponible3', string='Is doctor?')  ##, default=_disponible
    done1__ = fields.Boolean(compute='_disponible3s', string='Is doctor?')  ##, default=_disponible
    ##

    color1 = fields.Integer(string='Assigned')
    current_uid = fields.Integer(compute='_get_current_user', string='Name')
    uom_id_r = fields.Many2one('product.uom', string='Assigned')
    uom_id = fields.Many2one('product.uom', string='Assigned')
    amount_untaxed = fields.Float(compute='_amount_all', string='Name')
    amount_total = fields.Float(compute='_amount_all', string='Name')
    amount_tvq = fields.Float(compute='_amount_all', string='Name')
    amount_tps = fields.Float(compute='_amount_all', string='Name')
    date_s1 = fields.Date(string='Assigned')
    date_e1 = fields.Date(string='Assigned')
    date_s2 = fields.Date(string='Assigned')
    date_e2 = fields.Date(string='Assigned')
    date_s3 = fields.Date(string='Assigned')
    date_e3 = fields.Date(string='Assigned')
    tp = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Cloturé'),

    ],
        'Status', copy=False)
    to = fields.Char(string='char')
    cc = fields.Char(string='char')
    cci = fields.Char(string='char')
    mail_send = fields.Selection([('yes', 'Oui'),
                                  ('no', 'Non')],
                                 default='no')
    mail_send1 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'Non')],
                                  default='no')
    mail_send2 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'no')],
                                  default='no')
    mail_send3 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'Non')],
                                  default='no')
    mail_send4 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'Non')],
                                  default='no')
    mail_send5 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'Non')],
                                  default='no')
    mail_send6 = fields.Selection([('yes', 'Oui'),
                                   ('no', 'Non')],
                                  default='no')

    employee_ids = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel',
                                    'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids1 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel1',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids2 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel2',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids3 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel3',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids4 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel4',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids5 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel5',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids6 = fields.Many2many('hr.employee', 'base_group_merge_automatic_wizard_hr_employee_rel6',
                                     'base_group_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    kit_id = fields.Many2one('product.kit', string='Kit')

    @api.model
    def default_get(self, fields_list):

        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids')
        if self.env.context.get('active_model') == 'project.task.work' and active_ids:
            vv = []
            for hh in active_ids:
                work = self.env['project.task.work'].browse(hh)

                dd = []
                if work.kit_id:
                    kit_list = self.env['project.task.work'].search([
                        ('project_id', '=', work.project_id.id),
                        ('zone', '=', work.zone),
                        ('secteur', '=', work.secteur),
                        ('kit_id', '=', work.kit_id.id),
                        ('product_id.name', 'not ilike', '%correction%'),
                        ('product_id.name', 'not ilike', '%cont%'),
                        ('product_id.name', 'not ilike', '%gestion client%')
                    ])
                    for kit_list_id in kit_list.ids:
                        work1 = self.env['project.task.work'].browse(kit_list_id)
                        if not work.is_copy and not work1.is_copy and work1.id not in vv:
                            vv.append(work1.id)
                        elif work.is_copy and work1.is_copy and work1.rank == work1.rank and work1.id not in vv:
                            vv.append(work1.id)
                    res['work_ids'] = vv
                else:
                    res['work_ids'] = active_ids
            r = []
            pref = ''
            test = ''
            lst = []
            list1 = []
            proj = []
            gest_id2 = False
            emp_id2 = False
            for jj in active_ids:
                work = self.env['project.task.work'].browse(jj)
                user = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1).id
                user1 = self.env.uid
                if work.project_id.id not in proj:
                    proj.append(work.project_id.id)

                if work.state == 'pending':
                    raise UserError(_('Action impossible!'), _('Travaux Suspendus!'))
                if work.state == 'draft':
                    raise UserError(_('Action impossible!'), _('Travaux Non Affectés!'))
                if len(proj) > 1:
                    raise UserError(_('Action impossible!'), _('Déclaration se fait uniquement sur un projet!'))
                if len(active_ids) > 1:
                    pref = '/'

                done = 1 if work.gest_id.user_id.id == self.env.uid or self.env.uid == 1 else 0
                done1 = 1 if work.employee_id.user_id.id == self.env.uid or self.env.uid == 1 else 0

                if work.affect_cor_list and str(user1) in work.affect_cor_list:
                    type1 = 'correction'
                    emp_id2 = user
                elif work.affect_con_list and str(user1) in work.affect_con_list:
                    type1 = 'controle'
                    gest_id2 = user
                else:
                    type1 = 'bon'
                    if work.state == 'close':
                        raise UserError(_('Action impossible!'), _('Travaux Clotués!'))
                    if work.state == 'valid':
                        raise UserError(_('Action impossible!'), _('Travaux Terminés!'))

                test = test + pref + str(work.project_id.name) + ' - ' + str(work.task_id.sequence) + ' - ' + str(
                    work.sequence)

                res.update({
                    'states': test,
                    'employee_id': work.employee_id.id,
                    'gest_id': work.gest_id.id,
                    'project_id': work.project_id.id,
                    'zo': work.zo,
                    'sect': work.sect,
                    'categ_id': work.categ_id.id,
                    'coordin_id': work.gest_id3.id,
                    'coordin_id1': work.coordin_id1.id,
                    'coordin_id2': work.coordin_id2.id,
                    'coordin_id3': work.coordin_id3.id,
                    'coordin_id4': work.coordin_id4.id,
                    'coordin_id5': work.coordin_id5.id,
                    'type1': type1,
                    'gest_id2': gest_id2,
                    'emp_id2': emp_id2,
                })
                print('res  1 :', res)
                poteau = 0
                tt = self.env['project.task.work'].search([
                    ('project_id', '=', work.project_id.id),
                    ('categ_id', '=', work.categ_id.id),
                    # ('name', 'ilike', 'qualit'),
                    ('etape', '=', work.etape)
                ]).ids
                print('tt :', tt)
                for ji in tt:
                    work = self.env['project.task.work'].browse(ji)
                    move_line1 = {
                        'product_id': work.product_id.id,
                        'employee_id': work.gest_id.id,
                        'state': 'draft',
                        'work_id': work.id,
                        'task_id': work.task_id.id,
                        'categ_id': work.categ_id.id,
                        'date_start_r': work.date_start_r,
                        'date_end_r': work.date_end_r,
                        'poteau_t': work.poteau_t,
                        'poteau_r': poteau,
                        'project_id': work.task_id.project_id.id,
                        'gest_id': work.gest_id.id,
                        'uom_id': work.uom_id.id,
                        'uom_id_r': work.uom_id_r.id,
                        'zone': work.zone,
                        'secteur': work.secteur,
                    }
                    if tt:
                        list1.append((0, 0, move_line1))
                        print('list1 :', list1)
                for task in active_ids:
                    work = self.env['project.task.work'].browse(task)
                    res_user = self.env['res.users'].browse(self.env.uid)
                    categ_ids = self.env['hr.academic'].search([('employee_id', '=', res_user.employee_id.id)])
                    jj = []
                    if categ_ids:
                        for ll in categ_ids.ids:
                            dep = self.env['hr.academic'].browse(ll)
                            jj.append(dep.categ_id.id)
                    # if work.categ_id.id not in jj:
                    #     raise UserError(_('Action impossible!'),
                    #                     _('Vous n''etes pas autorisé à exécuter cette action sur un département externe'))

            res['work_ids'] = list1
            print('res :', res)
            print('work_ids :', self.work_ids)
        return res

    def _compute_done2(self):

        for record in self:
            if record.gest_id.user_id.id == self._uid:
                record.done = True
            else:
                record.done = False

    def _default_done(self):
        for record in self:
            if record.gest_id.user_id.id == self._uid:
                record.doctor = True
            else:
                record.doctor = False

        # Fields**

    ######################## check if logged user is admin  ############################################
    @api.onchange('sadmin')
    def _sadmin(self):
        print('def _sadmin')
        for book in self:
            if self._uid == 1:
                book.sadmin = True
            else:
                book.sadmin = False

    ########################## check if logged user is admin one those user based on ids  and set done to true ##########################
    @api.onchange('done')
    def _disponible(self):
        print('def _disponible_done')
        # simplifed code
        for book in self:
            allowed_user_ids = [45, 114, 26, 47, 83, 1]  # List of allowed user IDs
            if (
                    book.gest_id.user_id.id == self.env.uid
                    or book.coordin_id.user_id.id == self.env.uid
                    or book.coordin_id1.user_id.id == self.env.uid
                    or book.coordin_id2.user_id.id == self.env.uid
                    or book.coordin_id3.user_id.id == self.env.uid
                    or self.env.uid in allowed_user_ids
            ):
                book.done = True
            else:
                book.done = False
        # print('self.done :', self.done)

    ########################## check if logged user is admin one those use is ??? ##########################
    @api.onchange('done1')
    def _disponible1(self):
        print('def _disponible1')
        user_id = self.env.user.id
        print('self.work_ids :', self.work_ids)
        for book in self:
            # to_change_to_6_or_7 [1 is the default]
            print("1")
            if self.work_ids:

                if user_id == 1 or book.employee_id.user_id.id == user_id or str(user_id) in (
                        book.work_ids[0].affect_emp_list or []):
                    book.done1 = True
                else:
                    book.done1 = False

    ########################## check if logged user is admin or corrdinator or his id is 45 ##########################
    @api.onchange('done_')
    def _disponible2(self):
        print('def _disponible2')
        for book in self:
            user = self.env.user.employee_id
            if (
                    book.gest_id.user_id.id == self._uid
                    or user.is_coor is True
                    or self._uid == 1
                    or self._uid == 6  # 45
            ):
                book.done_ = True
            else:
                book.done_ = False

    @api.onchange('done1_')
    def _compute_done1_(self):
        print('def _compute_done1_')
        for book in self:
            user = self.env.user.employee_id
            if book.gest_id2:
                if (
                        book.gest_id.user_id.id == self._uid
                        or book.gest_id2.user_id.id == self._uid
                ):
                    book.done1_ = True
                else:
                    book.done1_ = False
            else:
                if (
                        book.gest_id.user_id.id == self._uid
                        or user.is_coor is True
                        or self._uid == 1
                        or self._uid == 45
                ):
                    book.done1_ = True
                else:
                    book.done1_ = False

    @api.onchange('done__')
    def _disponible3(self):
        print('def _disponible3')
        for book in self:
            user = self.env.user.employee_id
            if (
                    book.gest_id.user_id.id == self._uid
                    # or user.is_coor is True: methode must be implemented
                    or self._uid == 1
                    or self._uid == 45
            ):
                book.done__ = True
            else:
                book.done__ = False

    @api.onchange('donecq')
    def _disponiblecq(self):
        print('def _disponiblecq')
        for book in self:
            user = self.env.user.employee_id
            if (
                    book.employee_id.user_id.id == self._uid
                    or self._uid == 1
            ):
                book.donecq = True
            else:
                book.donecq = False

    #
    @api.onchange('doneco')
    def _disponibleco(self):
        print('def _disponibleco')
        for book in self:
            ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock 3 pour l'article %s  !")% book.gest_id2.name) OK
            user = self.env['res.users'].browse(self._uid).employee_id
            if book.emp_id2.user_id.id == self._uid or self._uid == 1:
                self.doneco = True
            else:

                self.doneco = False

    @api.onchange('done1__')
    def _disponible3s(self):
        print('def _disponible3s')
        for book in self:
            user = self.env.user.employee_id
            if book.emp_id2:
                if (
                        book.gest_id.user_id.id == self._uid
                        or book.emp_id2.user_id.id == self._uid
                ):
                    book.done1__ = True
                else:
                    book.done1__ = False
            else:
                if (
                        book.gest_id.user_id.id == self._uid
                        # or user.is_coor is True
                        or self._uid == 1
                        or self._uid == 45
                ):
                    book.done1__ = True
                else:
                    book.done1__ = False

    @api.onchange('done_c')
    def _disponible3sAAAAAA(self):
        print('_disponible3sAAAAAA')
        for book in self:
            user = self.env.user.employee_id
            if book.emp_id2:
                if book.emp_id2.user_id.id == self._uid:
                    book.done_c = True
                else:
                    book.done_c = False
            else:
                if (
                        book.gest_id.user_id.id == self._uid
                        # or user.is_coor is True
                        or self._uid == 1
                        or self._uid == 45
                ):
                    book.done_c = True
                else:
                    book.done_c = False

    def _get_current_user(self):

        current_login = self.env.user
        self.processing_staff = current_login

    def _amount_all(self):
        tax_obj = self.env['account.tax']
        tvp_obj = tax_obj.browse(8)
        tps_obj = tax_obj.browse(7)

        for group in self:
            group.amount_untaxed = 0.0
            group.amount_tps = 0.0
            group.amount_tvq = 0.0
            group.amount_total = 0.0

            if group.employee_id.job_id.id == 1:
                tvq = 0
                tps = 0
            else:
                tvq = tvp_obj.amount
                tps = tps_obj.amount

            for line in group.line_ids:
                group.amount_untaxed += line.amount_line

            group.amount_tps = group.amount_untaxed * tps
            group.amount_tvq = group.amount_untaxed * tvq
            group.amount_total = group.amount_untaxed + group.amount_tps + group.amount_tvq

    def fields_view_get(self, view_id=None, view_type=None, toolbar=False, submenu=False):
        print('fields_view_get')

        res = super(EbMergegroups, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                         toolbar=toolbar, submenu=submenu)
        if 'active_model' not in self.env.context:
            return res
        elif self.env.context['active_model'] == 'project.task.work' and view_type != 'tree':
            for task in self.env.context['active_ids']:
                work = self.env['project.task.work'].browse(task)
                user = self.env.user
                print('user id :', user.id)
                if (work.affect_cor_list != '' and (str(user.id) in (work.affect_cor_list or ' '))) and (
                        str(user.id) not in (work.affect_con_list or ' ')) and (
                        str(user.id) not in (work.affect_emp_list or ' ')):
                    res = super(EbMergegroups, self).fields_view_get(
                        view_id=self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
                        view_type=view_type, toolbar=toolbar, submenu=submenu)

                elif (work.affect_con_list != '' and (str(user.id) in (work.affect_con_list or ' '))) and (
                        str(user.id) not in (work.affect_cor_list or ' ')) and (
                        str(user.id) not in (work.affect_emp_list or ' ')):
                    res = super(EbMergegroups, self).fields_view_get(
                        view_id=self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
                        view_type=view_type, toolbar=toolbar, submenu=submenu)

                elif ((work.affect_emp_list != '' and (str(user.id) in (work.affect_emp_list or ' ')))
                      or work.current_emp.user_id.id == user) and (
                        str(user.id) not in (work.affect_con_list or ' ')) and (
                        str(user.id) not in (work.affect_cor_list or ' ')):
                    res = super(EbMergegroups, self).fields_view_get(
                        view_id=self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
                        view_type=view_type, toolbar=toolbar, submenu=submenu)

                elif ((str(user.id) not in (work.affect_emp_list or ' ')) or work.current_emp.user_id.id == user) and (
                        str(user.id) not in (work.affect_con_list or ' ')) and (
                        str(user.id) not in (work.affect_cor_list or ' ')):

                    raise ValidationError("Vous n'avez aucune affectation pour cette tâche")

                else:
                    res = super(EbMergegroups, self).fields_view_get(
                        view_id=self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
                        view_type=view_type,
                        toolbar=toolbar, submenu=submenu)
                return res
        elif self.env.context['active_model'] == 'base.group.merge.automatic.wizard':
            print('here 3')
            return res
        else:
            return res

    def onchange_date_from(self, categ_id, date_start_r):
        res = {}

        if date_start_r:
            r = []
            z = []
            k = []
            emp = self.env.user
            ##            if emp.employee_id.is_super:
            if emp.employee_id:
                dep1 = self.env['hr.academic'].search([('employee_id', '=', emp.employee_id.id)])
                if dep1:
                    for ll in dep1:
                        c = self.env['hr.academic'].browse(ll).categ_id.id
                        k.append(c)

                    for nn in k:
                        dep = self.env['hr.academic'].search([('categ_id', '=', nn)])
                        if dep:
                            for jj in dep:
                                em = self.env['hr.academic'].browse(jj).employee_id
                                r.append(em.id)
                                if em.is_super is True:
                                    z.append(em.id)
                res['domain'] = {'categ_id': [('id', 'in', k)], 'emp_id2': [('id', 'in', r)],
                                 'gest_id2': [('id', 'in', r)], 'gest_id_': [('id', 'in', r)]}
        return res

    def button_save_(self):
        if not self.line_ids:
            raise UserError(_("Action impossible! Vous devez avoir au moins une ligne à déclarer!"))
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],  # self.ids[0],  # ids[0],
            'context': {},
            'domain': []
        }

    def button_choice(self):
        print('button_choice')
        user = self.env.user
        for line in self.work_ids:
            l1 = line[0]

            if self.type1 == 'bon' and (str(user) in (l1.affect_emp_list or ' ')):

                return {
                    'name': 'Déclaration des Bons',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'res_model': 'base.group.merge.automatic.wizard',
                    'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
                    'res_id': self.ids[0],  # ids[0],
                    'context': {},
                    'domain': []
                }
            elif self.type1 == 'controle' and (str(user) in (l1.affect_con_list or ' ')):
                return {
                    'name': 'Déclaration  Bons Controle',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'res_model': 'base.group.merge.automatic.wizard',
                    'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
                    'res_id': self.ids[0],  # ids[0],
                    'context': {},
                    'domain': []
                }
            elif self.type1 == 'correction' and (str(user) in (l1.affect_cor_list or ' ')):

                return {
                    'name': 'Déclaration Bons Correction',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'res_model': 'base.group.merge.automatic.wizard',
                    'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
                    # self.env.ref('your_view_id3').id,  # Replace 'your_view_id3' with the actual view ID
                    'res_id': self.ids[0],  # ids[0],
                    'context': {},
                    'domain': []
                }
            else:
                raise UserError(_("Error! Pas d'affectation pour ce type de bon!"))

    def button_load_mail(self, ids):

        work_line = self.env['project.task.work']
        this = self
        # emp_obj = self.pool.get('hr.employee')
        # this = self.browse(cr, uid, ids[0])
        # work_obj = self.pool.get('base.group.merge.automatic.wizard')
        kk = []
        kk1 = []
        coordin1 = []
        coordin2 = []
        coordin3 = []
        coordin4 = []
        coordin5 = []
        coordin6 = []
        coordin7 = []
        coordin8 = []
        coordin9 = []
        coordin10 = []
        for line in this.work_ids:
            l1 = line
            if l1.gest_id and l1.gest_id.id not in kk:
                kk.append(l1.gest_id.id)
            if l1.gest_id3 and l1.gest_id3.id not in kk1:
                kk1.append(l1.gest_id3.id)
            if l1.reviewer_id1 and l1.reviewer_id1.id not in kk1:
                kk1.append(l1.reviewer_id1.id)
            if l1.coordin_id1 and l1.coordin_id1.id not in kk1:
                kk1.append(l1.coordin_id1.id)
            if l1.coordin_id2 and l1.coordin_id2.id not in kk1:
                kk1.append(l1.coordin_id2.id)
            if l1.coordin_id3 and l1.coordin_id3.id not in kk1:
                kk1.append(l1.coordin_id3.id)
            if l1.coordin_id4 and l1.coordin_id4.id not in kk1:
                kk1.append(l1.coordin_id4.id)
            if l1.coordin_id5 and l1.coordin_id5.id not in kk1:
                kk1.append(l1.coordin_id5.id)
            if l1.coordin_id6 and l1.coordin_id6.id not in kk1:
                kk1.append(l1.coordin_id6.id)
            if l1.coordin_id7 and l1.coordin_id7.id not in kk1:
                kk1.append(l1.coordin_id7.id)
            if l1.coordin_id8 and l1.coordin_id8.id not in kk1:
                kk1.append(l1.coordin_id8.id)
            if l1.coordin_id9 and l1.coordin_id9.id not in kk1:
                kk1.append(l1.coordin_id9.id)
            if l1.coordin_id10 and l1.coordin_id10.id not in kk1:
                kk1.append(l1.coordin_id10.id)
            for jj in kk:
                this.write({'hr_employee_rel': [(4, jj)]})
            for jj in kk1:
                this.write({'hr_employee_rel1': [(0, 0, {'employee_id': jj})]})

        return {
            'name': 'Affectation les Travaux',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],  # ids[0],
            'domain': []
        }

    def button_load_mail1(self):
        work_line = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        this = self[0]
        work_obj = self.env['base.group.merge.automatic.wizard']
        kk = []
        kk1 = []
        kk2 = []
        for line in this.work_ids:
            l1 = work_line.browse(line.id)
            if l1.gest_id and l1.gest_id.id not in kk:
                kk.append(l1.gest_id.id)
            for jj in kk:
                self.env.cr.execute("""
                    INSERT INTO base_group_merge_automatic_wizard_hr_employee_rel3
                    VALUES (%s,%s)""", (this.id, jj))

            if l1.reviewer_id1 and l1.reviewer_id1.id not in kk1:
                kk1.append(l1.reviewer_id1.id)

            if l1.coordin_id1 and l1.coordin_id1.id not in kk1:
                kk1.append(l1.coordin_id1.id)

            if l1.coordin_id2 and l1.coordin_id2.id not in kk1:
                kk1.append(l1.coordin_id2.id)

            if l1.coordin_id3 and l1.coordin_id3.id not in kk1:
                kk1.append(l1.coordin_id3.id)

            if l1.coordin_id4 and l1.coordin_id4.id not in kk1:
                kk1.append(l1.coordin_id4.id)

            if l1.coordin_id5 and l1.coordin_id5.id not in kk1:
                kk1.append(l1.coordin_id5.id)

            if l1.coordin_id6 and l1.coordin_id6.id not in kk1:
                kk1.append(l1.coordin_id6.id)

            if l1.coordin_id7 and l1.coordin_id7.id not in kk1:
                kk1.append(l1.coordin_id7.id)

            if l1.coordin_id8 and l1.coordin_id8.id not in kk1:
                kk1.append(l1.coordin_id8.id)

            if l1.coordin_id9 and l1.coordin_id9.id not in kk1:
                kk1.append(l1.coordin_id9.id)

            if l1.coordin_id10 and l1.coordin_id10.id not in kk1:
                kk1.append(l1.coordin_id10.id)
            for jj in kk1:
                self.env.cr.execute("""
                    INSERT INTO base_group_merge_automatic_wizard_hr_employee_rel4
                    VALUES (%s,%s)""", (this.id, jj))

        return {
            'name': 'Déclaration Bon Controle',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            # self.env.ref('module_name.view_id').id,  # Replace 'module_name' with the actual module name
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],

            'domain': []
        }

    def button_load_mail2(self):
        work_line = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        this = self[0]
        work_obj = self.env['base.group.merge.automatic.wizard']
        kk = []
        kk1 = []
        kk2 = []

        for line in this.work_ids:
            l1 = work_line.browse(line.id)
            if l1.gest_id and l1.gest_id.id not in kk:
                kk.append(l1.gest_id.id)
            for jj in kk:
                self.env.cr.execute("""
                                INSERT INTO  base_group_merge_automatic_wizard_hr_employee_rel5
                                VALUES (%s,%s)""", (this.id, jj))

            if l1.gest_id3 and l1.gest_id3.id not in kk1:
                kk1.append(l1.gest_id3.id)
            if l1.reviewer_id1 and l1.reviewer_id1.id not in kk1:
                kk1.append(l1.reviewer_id1.id)
            if l1.coordin_id1 and l1.coordin_id1.id not in kk1:
                kk1.append(l1.coordin_id1.id)
            if l1.coordin_id2 and l1.coordin_id2.id not in kk1:
                kk1.append(l1.coordin_id2.id)
            if l1.coordin_id3 and l1.coordin_id3.id not in kk1:
                kk1.append(l1.coordin_id3.id)
            if l1.coordin_id4 and l1.coordin_id4.id not in kk1:
                kk1.append(l1.coordin_id4.id)
            if l1.coordin_id5 and l1.coordin_id5.id not in kk1:
                kk1.append(l1.coordin_id5.id)
            if l1.coordin_id6 and l1.coordin_id6.id not in kk1:
                kk1.append(l1.coordin_id6.id)
            if l1.coordin_id7 and l1.coordin_id7.id not in kk1:
                kk1.append(l1.coordin_id7.id)
            if l1.coordin_id8 and l1.coordin_id8.id not in kk1:
                kk1.append(l1.coordin_id8.id)
            if l1.coordin_id9 and l1.coordin_id9.id not in kk1:
                kk1.append(l1.coordin_id9.id)
            if l1.coordin_id10 and l1.coordin_id10.id not in kk1:
                kk1.append(l1.coordin_id10.id)
            for jj in kk1:
                self.env.cr.execute("""
                    INSERT INTO base_group_merge_automatic_wizard_hr_employee_rel6
                    VALUES (%s,%s)""", (this.id, jj))
        return {
            'name': 'Déclaration Bon Correction',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            # self.env.ref('module_name.view_id').id,  # Replace 'module_name' with the actual module name,
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self[0].id,

            'domain': []
        }

    def onchange_mail2(self, employee_ids):
        vals = {'employee_ids': False}
        return {'value': vals}

    def onchange_assign(self, employee_id, ):
        vals = {}

        moi = self.env.user.employee_id.name
        if employee_id:
            raise ValidationError(
                'N"oubliez pas de cliquer sur le bouton "Confirmez l"assignation" pour confirmer cette assignation  '
                'Cher/Chère %s :)' % moi)
        return True

    def button_approve_s1(self):

        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'state1': 'valid'})
        type_ = False
        for task in self.line_ids2:

            if not task.b1:
                move_line = {
                    'product_id': task.work_id.product_id.id,
                    'employee_id': task.employee_id.id,
                    'state': 'draft',
                    'work_id': task.work_id.id,
                    'work_id2': task.work_id2.id,
                    'task_id': task.work_id.task_id.id,
                    'group_id2': self.id,
                    'ftp': task.ftp,
                    'sequence': task.work_id.sequence,
                    'done3': True,
                    ##'hours': work.hours,
                    'date': task.date_start_r,
                    'date_start_r': task.date_start_r,
                    'date_end_r': task.date_end_r,
                    'poteau_t': task.poteau_t,
                    'poteau_r': task.poteau_r,
                    'total_r': task.poteau_r,
                    'categ_id': task.work_id.categ_id.id,
                    ##'poteau_r': work.poteau_r,
                    'hours_r': task.hours_r,
                    'color1': task.color1,
                    ## 'total_t':work.color1*7 ,  ##*work.employee_id.contract_id.wage
                    'project_id': task.work_id.task_id.project_id.id,
                    'partner_id': task.work_id.task_id.project_id.partner_id.id,
                    ## 'total_r':  line_w.amount_line,

                    ##                    'amount_line':  line_w.amount_line,
                    ##                    'wage':  line_w.wage,
                    'gest_id': task.gest_id.id,
                    'uom_id': task.work_id.uom_id.id,
                    'uom_id_r': task.uom_id_r.id,

                    'zone': task.work_id.zone,
                    'secteur': task.work_id.secteur,

                }
                one = work_line.create(move_line)
                # to_uncomment
                # if task.total_part_cont == 'total':
                #     type_ = True

                wk = work_obj.browse(task.work_id.id)
                wk.write({
                    'poteau_r': wk.poteau_r + task.poteau_r,
                    'poteau_i': wk.poteau_i + task.poteau_r,
                    'current_emp': False,
                })
                line_obj1.write(task.id, {'b1': True, 'line_id': one})

            wk = work_obj.browse(task.work_id.id)
            wk.write({
                'current_emp': False,
            })
            for line in self.work_ids:
                ll = work_obj.browse(line.id)
                if ll.affect_con_list and type_ and self.line_ids2.create_uid:
                    ll.write({
                        'affect_con_list': ll.affect_con_list.replace(str(self.line_ids2.create_uid.id), ''),
                        'current_emp': False,
                    })
                elif ll.affect_con_list and not type_:
                    ll.write({
                        'current_emp': False,
                    })
                else:
                    ll.write({
                        'current_emp': False,
                    })
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            # self.env.ref('module_name.view_id').id,  # Replace 'module_name' with the actual module name,
            'res_id': self.ids[0],
            'context': {},
            'domain': [],
        }

    def button_approve_s2(self):

        this = self[0]
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        self.write({'state2': 'valid'})
        line_obj1 = self.env['group_line.show.line2']
        for task in this.line_ids3:
            type_ = False
            if not task.b1:
                move_line = {
                    'product_id': task.work_id.product_id.id,
                    'employee_id': task.employee_id.id,
                    'state': 'draft',
                    'work_id': task.work_id.id,
                    'work_id2': task.work_id2.id,
                    'task_id': task.work_id.task_id.id,
                    'group_id2': this.id,
                    'ftp': task.ftp,
                    'sequence': task.work_id.sequence,
                    'done3': True,
                    'categ_id': task.work_id.categ_id.id,
                    'date': task.date_start_r,
                    'date_start_r': task.date_start_r,
                    'date_end_r': task.date_end_r,
                    'poteau_t': task.poteau_t,
                    'poteau_r': task.poteau_r,
                    'total_r': task.poteau_r,
                    'hours_r': task.hours_r,
                    'color1': task.color1,
                    'project_id': task.work_id.task_id.project_id.id,
                    'partner_id': task.work_id.task_id.project_id.partner_id.id,
                    'gest_id': task.gest_id.id,
                    'uom_id': task.work_id.uom_id.id,
                    'uom_id_r': task.uom_id_r.id,
                    'zone': task.work_id.zone,
                    'secteur': task.work_id.secteur,
                    'zo': 'Zone ' + str(task.work_id.zone).zfill(2),
                    'sect': 'Secteur ' + str(task.work_id.secteur).zfill(2),
                }
                one = work_line.create(move_line)

                if task.total_part_corr == 'total':
                    type_ = True
                wk = work_obj.browse(task.work_id.id)
                wk.write({
                    'poteau_r': wk.poteau_r + task.poteau_r,
                    'poteau_i': wk.poteau_i + task.poteau_r,
                    'state': 'validcorrec',
                    'current_emp': False,
                })
                line_obj1.write(task.id, {'b1': True, 'line_id': one})

        for ww in this.work_ids:
            if type_:
                work_obj.write(ww.id, {
                    'current_emp': False,
                    'state': 'validcorrec',
                })
            else:
                work_obj.write(ww.id, {
                    'current_emp': False,
                    'state': 'validcorrec',
                })

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_close_(self):

        this = self[0]
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        this.write({'state3': 'valid'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def forcer_ouverture(self):

        self.write({'num': '1'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_update1_(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'num': '1'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_update2_(self):
        this = self[0]
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'num': '2'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_update3_(self):
        this = self[0]
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        this.write({'num': '3'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': this.id,
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_applyupdate1_(self):
        line_obj = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        if self.num == '1':
            for line_w in self.line_ids:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif self.num == '2':
            for line_w in self.line_ids2:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif self.num == '3':
            for line_w in self.line_ids3:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })

        self.write({'num': ''})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_applyupdate2_(self):
        line_obj = self.env['base.group.merge.line']
        this = self[0]
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']

        if this.num == '1':
            for line_w in this.line_ids:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif this.num == '2':
            for line_w in this.line_ids2:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif this.num == '3':
            for line_w in this.line_ids3:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })

        this.write({'num': ''})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': this.id,
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_applyupdate3_(self):
        line_obj = self.env['base.group.merge.line']
        this = self[0]
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']

        if this.num == '1':
            for line_w in this.line_ids:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif this.num == '2':
            for line_w in this.line_ids2:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })
        elif this.num == '3':
            for line_w in this.line_ids3:
                if line_w.line_id:
                    work_line.write({
                        'poteau_r': line_w.poteau_r,
                        'hours_r': line_w.hours_r,
                    })

        this.write({'num': ''})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': this.id,
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_open_(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']

        self.write({'state3': 'draft'})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'target': 'new',
            'context': {},
            'domain': [],
        }

    def button_workflow(self):

        return {
            'name': 'Action Workflow',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.flow.merge.automatic.wizard',
            # 'view_id': self.env.ref('your_module_name.your_view_id').id,  # Replace with the actual view ID
            # 'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'target': 'popup',
            'context': {'default_project_id': self.project_id.id},
            'domain': [],
        }

    # button_bon_controle
    def affecter_bon_controle(self):
        return {
            'name': 'Affectation Controle',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'view_id': self.env.ref('module_yasmine.affectation_controle_view_id').id,
            'target': 'popup',
            'context': {
                'default_group_id': self.ids[0],  # this.id
                'default_types_affect': 'control',
                'default_project_id': self.project_id.id,
            },
            'domain': [],
        }

    def button_bon_correction(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']

        return {
            'name': 'Affectation Correction',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'view_id': self.env.ref('module_yasmine.affectation_controle_view_id').id,
            'target': 'popup',
            'context': {
                'default_group_id': self.ids[0],  # This.id
                'default_types_affect': 'correction',
                'default_project_id': self.project_id.id,
            },
            'domain': [],
        }

    def button_force_state(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'state': 'tovalid'})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],  # This.id
            'context': {},
            'domain': [],
        }

    def button_force_state1(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'state1': 'tovalid'})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],  # This.id
            'context': {},
            'domain': [],
        }

    def button_force_state2(self):
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        self.write({'state2': 'tovalid'})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': [],
        }

    def button_open1(self):
        if not self.line_ids2:
            raise UserError(_("Action impossible! Vous devez avoir au moins une ligne de controle à déclarer!"))

        for task in self.line_ids2:
            if not task.date_start_r:
                if self.date_s2:
                    task.write({'date_start_r': self.date_s2})
            if not task.date_end_r:
                if self.date_e2:
                    task.write({'date_end_r': self.date_e2})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            # self.env.ref('your_module_name.your_view_id').id,  # Replace with the actual view ID
            'res_id': self.ids[0],
            'context': {},
            'domain': [],
        }

    def action_open(self):
        if self.gest_id.user_id.id == self.env.user.id and self.state == 'tovalid':
            self.write({'done': True})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'popup',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': True},
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
            'domain': [],
        }

    def action_open1(self):
        print('action_open1')
        if self.gest_id.user_id.id == self.env.user.id and self.state == 'tovalid':
            self.write({'done': True})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'popup',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': True},
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
            'domain': [],
        }

    def action_open2(self):
        print("action_open2")
        if self.gest_id.user_id.id == self.env.user.id and self.state == 'tovalid':
            self.write({'done': True})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'popup',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': True},
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
            'domain': [],
        }

    def action_open11(self):
        if self.gest_id.user_id.id == self.env.user.id and self.state == 'tovalid':
            self.write({'done': True})

        for task in self.line_ids:
            if self.ftp:
                task.write({'ftp': self.ftp})
            if not task.date_start_r:
                if self.date_s1:
                    task.write({'date_start_r': self.date_s1})
            if not task.date_end_r:
                if self.date_e1:
                    task.write({'date_end_r': self.date_e1})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_open2(self):
        if not self.line_ids2:
            raise UserError(_("Action impossible! Vous devez avoir au moins une ligne de corrections à déclarer!"))

        for task in self.line_ids2:
            if not task.date_start_r:
                if self.date_s3:
                    task.write({'date_start_r': self.date_s3})
            if not task.date_end_r:
                if self.date_e3:
                    task.write({'date_end_r': self.date_e3})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_cancel(self):
        work_obj = self.env['project.task.work']
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']

        this = self
        ## for tt in this.line_ids:
        ##     if tt.line_id:
        ##         tt.line_id.unlink()
        ## this.unlink()
        ## self.write({'state': 'draft'})

        return True

    def button_close(self):
        self.write({'done': False})
        return {'type': 'ir.actions.act_window_close'}

    # button_reopen
    def annuler_bon(self):
        line_obj1 = self.env['base.group.merge.line']
        current = self
        if current.line_ids:
            for tt in current.line_ids:
                this_line = line_obj1.browse(tt.id)
                this_line.write({'state': 'draft'})
                self.env['project.task.work'].write(tt.work_id.id, {
                    'affect_e_l': tt.work_id.affect_e_l or '' + ',' + str(current.employee_id.user_id.login),
                    'affect_emp_list': tt.work_id.affect_emp_list or '' + ',' + str(current.employee_id.user_id.id),
                    'affect_emp': current.employee_id.id})
        self.write({'state': 'draft'})
        return True

    def button_reopen1(self):
        current = self
        self.write({'state1': 'draft'})
        if current.work_ids:
            for tt in current.work_ids:
                self.env['project.task.work'].write(tt.id, {
                    'affect_con_list': tt.affect_con_list + ',' + str(current.gest_id2.user_id.id),
                    'affect_emp': current.gest_id2.id})
        return True

    def button_reopen2(self):

        current = self
        self.write({'state2': 'draft'})
        if current.work_ids:
            for tt in current.work_ids:
                self.env['project.task.work'].write(tt.id, {
                    'affect_con_list': tt.affect_con_list + ',' + str(current.gest_id2.user_id.id),
                    'affect_emp': current.gest_id2.id})
        return True

    def button_import(self):
        print("button_import")

        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        show_ = self.env['group_line.show.line2']
        this = self

        if this.state2 == 'valid':
            self.write({'state2': 'draft'})

        if this.state2 != 'draft':
            raise UserError(_('Erreur!'), _('Import n"est possible qu"en statut Brouillon!'))

        if this.state3 != 'draft':
            raise UserError(_('Error !'), _('Bon deja cloturé'))

        for tt in self.ids:
            print("button_import 2")
            line = line_obj.browse(tt)
            # found = False
            cnt = 0
            gest = self.env.user.employee_id.id
            work = line.work_ids[0]

            print('work :', work)
            if work.kit_id:
                print("button_import 3")
                found = False
                for hh in work.kit_id.type_id.ids:
                    pr = self.env['product.product'].browse(hh)
                    if pr.default_code == '420-PP':
                        found = True
                        break
                if found:
                    print("button_import 3.1")
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.default_code', '=', '421-PP'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])

                if not found:
                    for hh in work.kit_id.type_id.ids:
                        pr = self.env['product.product'].browse(hh)
                        if pr.default_code == '410-DB':
                            found = True
                            break
                    if found:
                        tt = self.env['project.task.work'].search(
                            [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                             ('product_id.default_code', '=', '411-DB'), ('zone', '=', work.zone),
                             ('secteur', '=', work.secteur), ('is_copy', '=', False)])

                if not found:
                    for hh in work.kit_id.type_id.ids:
                        pr = self.env['product.product'].browse(hh)
                        if pr.default_code == '430-DC':
                            found = True
                            break
                    if found:
                        tt = self.env['project.task.work'].search(
                            [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                             ('product_id.default_code', '=', '431-DC'), ('zone', '=', work.zone),
                             ('secteur', '=', work.secteur), ('is_copy', '=', False)])
                if not found:
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.name', 'ilike', 'correct'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])

            else:
                print("button_import 4")
                if work.product_id.default_code == '420-PP':
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.default_code', '=', '421-PP'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])
                elif work.product_id.default_code == '410-DB':
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.default_code', '=', '411-DB'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])
                elif work.product_id.default_code == '430-DC':
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.default_code', '=', '431-DC'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])
                else:
                    tt = self.env['project.task.work'].search(
                        [('project_id', '=', work.project_id.id), ('categ_id', '=', work.categ_id.id),
                         ('product_id.name', 'ilike', 'correct'), ('zone', '=', work.zone),
                         ('secteur', '=', work.secteur), ('is_copy', '=', False)])

            ##    raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
            ##  raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
            if tt:
                print("button_import 5")
                ji = tt[0]
                work1 = self.env['project.task.work'].browse(ji)
                cnt += 1
                move_line1 = {
                    'product_id': work1.product_id.id,
                    'employee_id': gest,
                    'state': 'draft',
                    'work_id': work1.id,
                    'work_id2': work.id,
                    'task_id': work1.task_id.id,
                    'categ_id': work1.categ_id.id,
                    'sequence': cnt,
                    'date_start_r': work1.date_start_r,
                    'date_end_r': work1.date_end_r,
                    'poteau_t': work1.poteau_t,
                    'project_id': work1.task_id.project_id.id,
                    'gest_id': gest,
                    'uom_id': work1.product_id.uom_id.id,
                    'uom_id_r': work1.product_id.uom_id.id,
                    'zone': work1.zone,
                    'secteur': work1.secteur,
                }

                if tt:
                    print("button_import 6")
                    one = show_.create(move_line1)
                    show_.write(one, {'group_id': line.id})

            self.write({'employee_id': gest})

            for ww in this.work_ids:
                ww.write({'state': 'tovalidcont'})
            return {
                'name': 'Déclaration des Bons',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'base.group.merge.automatic.wizard',
                'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
                # self.env.ref('module_name.view_id').id,  # Replace 'module_name' with your module name
                'res_id': self.ids[0],  # ids[0],
                'context': {},
                'domain': []
            }

    def button_import2(self):
        line_obj = self.env['base.group.merge.automatic.wizard']
        # line_obj1 = self.env['base.group.merge.line']
        # work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        show_ = self.env['group_line.show.line2']
        # list1 = []

        if self.state1 == 'valid':
            self.write({'state1': 'draft'})
        if self.state1 != 'draft':
            raise UserError(_('Error!'), _('Action possible qu"en statut brouillon.'))
        if self.state3 != 'draft':
            raise UserError(_('Error!'), _('Bon deja cloturé'))
        print('1')
        gest = self.env.user.employee_id.id
        for tt in self.ids:
            line = line_obj.browse(tt)
            cnt = 0
            print('2')
            for kk in line.work_ids.ids:
                work = work_.browse(kk)
                print('3')
                if work.kit_id:
                    print('4')
                    tt = work_.search([('project_id', '=', work.project_id.id),
                                       ('categ_id', '=', work.categ_id.id),
                                       # ('product_id.name', 'ilike', 'contr'),
                                       ('zone', '=', work.zone),
                                       ('secteur', '=', work.secteur),
                                       ('is_copy', '=', False)])
                else:
                    tt = work_.search([('project_id', '=', work.project_id.id),
                                       ('categ_id', '=', work.categ_id.id),
                                       # ('name', 'ilike', 'contr'),
                                       ('zone', '=', work.zone),
                                       ('secteur', '=', work.secteur),
                                       ('is_copy', '=', False)
                                       ])
                    print('tt', tt)
                for ji in tt:
                    cnt += 1
                    print('6')
                    work1 = work_.browse(ji.id)
                    print('work1', work1)
                    move_line1 = {
                        'product_id': work1.product_id.id,
                        'employee_id': gest,
                        'state': 'draft',
                        'work_id': work1.id,
                        'work_id2': work.id,
                        'task_id': work1.task_id.id,
                        'categ_id': work1.categ_id.id,
                        'date_start_r': work1.date_start_r,
                        'date_end_r': work1.date_end_r,
                        'poteau_t': work1.poteau_t,
                        'sequence': cnt,
                        'project_id': work1.task_id.project_id.id,
                        'gest_id': gest,
                        'uom_id': work1.product_id.uom_id.id,
                        'uom_id_r': work1.product_id.uom_id.id,
                        'zone': work1.zone,
                        'secteur': work1.secteur,
                        'group_id': line.id
                    }
                    print('8')
                    if tt:
                        print('9')
                        bon_show = self.env['bon.show']
                        bon_show.create({'group_id': line.id})  # to delete

                        # move_line1['group_id'] = line.id
                        one = show_.create(move_line1)
                        # one.write({'group_id': line.id})

        self.write({'mail_send': '', 'employee_id': gest})
        for ww in self.work_ids:
            ww.write({'state': 'tovalidcorrec'})
            print('10')
        return {
            'name': 'Declaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_import_(self):
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        # work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        # show_ = self.env['group_line.show.line2']
        # list1 = []
        if self.state != 'draft':
            raise UserError(_('Error!'), _('Action possible qu"en statut brouillon.'))
        if self.state3 != 'draft':
            raise UserError(_('Error!'), _('Bon deja cloturé'))
        for iterator_id in self.ids:
            line = line_obj.browse(iterator_id)
            cnt = 0
            for iterator_work_id in line.work_ids.ids:
                work = work_.browse(iterator_work_id)
                # to_verify
                # if '115' in work.product_id.default_code or '116' in work.product_id.default_code or '117' in work.product_id.default_code:
                #     record = True
                # else:
                #     record = False
                record = False
                res_user = self.env.user
                move_line = {
                    'product_id': work.product_id.id,
                    'employee_id': res_user.employee_id.id,
                    'state': 'draft',
                    'work_id': work.id,
                    'task_id': work.task_id.id,
                    'categ_id': work.categ_id.id,
                    'date_start_r': self.date_s1,
                    'date_end_r': self.date_e1,
                    'total_part': self.tp,
                    'poteau_t': work.poteau_t,
                    'ftp': self.ftp,
                    'project_id': work.task_id.project_id.id,
                    'is_service': record,
                    'gest_id': work.gest_id.id,
                    'uom_id': work.product_id.uom_id.id,
                    'uom_id_r': work.product_id.uom_id.id,
                    'wizard_id': line.id,
                    'zone': work.zone,
                    'secteur': work.secteur,
                }

                if iterator_id:
                    one = line_obj1.create(move_line)

        # self.write({'mail_send': '', 'employee_id': res_user.employee_id.id})
        for iterator_work_id in self.work_ids:
            work_.write({'current_emp': iterator_work_id.employee_id.id})

        # line_obj1 = self.env['hr.employee'].search([])
        # for obj1 in line_obj1:
        #     print('ici:', obj1.id)
        # print ('sate1', self.state1, 'done_', self.done1_, 'state', self.state)
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],  # self.ids[0],  # ids[0],
            'context': {},
            'domain': []
        }

    def button_approve(self):
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        list = []
        if not self.mail_send:
            raise UserError('Erreur Vous devez choisir OUI ou NON pour l\"envoi de courriel!')

        for tt in self:
            line = line_obj.browse(tt.id)

            if not line.line_ids:
                raise UserError('Action impossible! Vous devez avoir au moins une ligne à déclarer!')

            for jj in self.line_ids:
                list_ = []
                if not jj.date_start_r and not self.date_s1:
                    raise UserError('Action impossible! "La date de début est obligatoire!')
                if jj.date_end_r and jj.date_end_r > fields.Date.today():
                    raise UserError('Warning! Date fin doit être antérieure à la date d\'aujourd\'hui')
                if not jj.total_part:
                    raise UserError('Action impossible! Choix déclaration Totale/Partielle obligatoire! ')
                if self.date_s1 and not jj.date_start_r:
                    jj.date_start_r = self.date_s1
                if self.ftp and not jj.ftp:
                    jj.ftp = self.ftp
                if self.date_e1 and not jj.date_end_r:
                    jj.date_end_r = self.date_e1
                if self.tp and not jj.total_part:
                    jj.total_part = self.tp
                if jj.total_part == 'total':
                    if jj.work_id.affect_emp_list:
                        jj.work_id.write({
                            'affect_emp_list': jj.work_id.affect_emp_list.replace(str(jj.employee_id.user_id.id),
                                                                                  '') if jj.work_id.affect_emp_list else '',
                            'affect_e_l': jj.work_id.affect_e_l.replace(str(jj.employee_id.user_id.login),
                                                                        '') if jj.work_id.affect_e_l else '',
                            'current_emp': False
                        })
                for kk in line.line_ids.ids:
                    line_w = line_obj1.browse(kk)
                    if line_w:
                        move_line = {
                            'product_id': line_w.work_id.product_id.id,
                            'employee_id': line_w.employee_id.id,
                            'state': 'draft',
                            'work_id': line_w.work_id.id,
                            'task_id': line_w.work_id.task_id.id,
                            # 'group_id2': line.id,
                            'ftp': line_w.ftp,
                            'sequence': line_w.work_id.sequence,
                            'categ_id': line_w.work_id.categ_id.id,
                            'date': line_w.date_start_r,
                            'date_start_r': line_w.date_start_r,
                            'date_end_r': line_w.date_end_r,
                            'poteau_t': line_w.poteau_t,
                            'poteau_r': line_w.poteau_r,
                            'total_r': line_w.amount_line,
                            'hours_r': line_w.hours_r,
                            'color1': line_w.color1,
                            'project_id': line_w.work_id.task_id.project_id.id,
                            # 'amount_line': line_w.amount_line,
                            'wage': line_w.wage,
                            'gest_id': line_w.work_id.gest_id.id,
                            'uom_id': line_w.work_id.uom_id.id,
                            'uom_id_r': line_w.uom_id_r.id,
                            'zone': line_w.work_id.zone,
                            'secteur': line_w.work_id.secteur,
                        }
                        one = work_line.create(move_line)
                        line_obj1.write({'id': kk, 'line_id': one.id})
        # the code bellow must be reviewed
        for ww in self.work_ids:
            if ww.state == 'affect':
                ww.write({'state': 'tovalid'})

            res_user = self.env['res.users'].browse(self._uid)
            wk_histo = self.env['work.histo'].search([('work_id', '=', ww.id)])

            if wk_histo and len(wk_histo) == 1:
                wk_histo_id = wk_histo.id
                self.env['work.histo.line'].create({
                    'type': 'db',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': wk_histo_id,
                    'date': fields.Datetime.now(),
                    'coment1': self.note or False,
                    'id_object': self.ids[0],
                })
            else:
                histo = self.env['work.histo'].create({
                    'task_id': ww.task_id.id,
                    'work_id': ww.id,
                    'categ_id': ww.categ_id.id,
                    'product_id': ww.product_id.id,
                    'name': ww.task_id.name,
                    'date': ww.date_start,
                    'create_a': ww.date_start,
                    'zone': ww.zo or 0,
                    'secteur': ww.sect or 0,
                    'project_id': ww.project_id.id,
                    'partner_id': ww.project_id.partner_id.id,
                })
                self.env['work.histo.line'].create({
                    'type': 'db',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': histo.id,
                    'date': fields.Datetime.now(),
                    'coment1': self.note or False,
                    'id_object': self.ids[0]
                })
        # Send email here
        # if self.mail_send == 'yes':
        #     if not self.note:
        #         self.note = ' '
        #     kk = ''
        #     for line in self.employee_ids:
        #         emp = line
        #         kk = kk + emp.work_email + ','
        #     self.to = kk
        #
        #     if self.employee_ids1:
        #         ll = ''
        #         for line in self.employee_ids1:
        #             emp = line
        #             ll = ll + emp.work_email + ','
        #         self.cc = ll
        #
        #     if self.employee_ids2:
        #         mm = ''
        #         for line in self.employee_ids2:
        #             emp = line
        #             mm = mm + emp.work_email + ','
        #         self.cci = mm
        #
        # template = self.env.ref('module_name.email_template_id')
        # template.send_mail(self.ids[0], force_send=True)
        self.write({'state': 'tovalid'})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_approve1(self):
        print('button_approve1')
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        this = self

        if not self.mail_send1:
            raise UserError('Erreur Vous devez choisir OUI ou NON pour l"envoi de courriel!')

        if not self.line_ids2:
            raise UserError('Action impossible! Vous devez avoir au moins une ligne de contrôle à déclarer!')

        for tt in self.line_ids2:
            if tt.date_end_r:
                print('tt.date_end_r', tt.date_end_r)
                if tt.date_end_r > fields.Date.today():
                    raise UserError('Warning! La date de fin doit être antérieure à la date d\'aujourd\'hui')

            if not tt.date_start_r:
                raise UserError("Action impossible! La date de début est obligatoire!")

            # to_uncomment
            # if tt.total_part_cont == 'total':
            #     for ww in self.work_ids:
            #         ww.write({
            #             'affect_con_list': ww.affect_con_list.replace(str(self.gest_id2.user_id.id), '')
            #         })

        for ww in self.work_ids:
            ww.write({'state': 'tovalidcont'})
            res_user = self.env['res.users'].browse(self.env.uid)
            wk_histo = self.env['work.histo'].search([('work_id', '=', ww.id)])

            if wk_histo and len(wk_histo) == 1:
                wk_histo_id = wk_histo.id
                self.env['work.histo.line'].create({
                    'type': 'db_con',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': wk_histo_id,
                    'date': fields.Datetime.now(),
                    'coment1': self.note2 or False,
                    'id_object': self.ids[0],
                })
            else:
                histo = self.env['work.histo'].create({
                    'task_id': ww.task_id.id,
                    'work_id': ww.id,
                    'categ_id': ww.categ_id.id,
                    'product_id': ww.product_id.id,
                    'name': ww.task_id.name,
                    'date': ww.date_start,
                    'create_a': ww.date_start,
                    'zone': ww.zo or 0,
                    'secteur': ww.sect or 0,
                    'project_id': ww.project_id.id,
                    'partner_id': ww.project_id.partner_id.id,
                })
                self.env['work.histo.line'].create({
                    'type': 'db_con',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': histo.id,
                    'date': fields.Datetime.now(),
                    'coment1': self.note2 or False,
                    'id_object': self.ids[0],
                })
        if self.mail_send1 == 'yes':
            kk = ''
            for line in self.employee_ids3:
                emp = line
                kk = kk + emp.work_email + ','
            self.to1 = kk

            ll = ''
            for line in self.employee_ids4:
                emp = line
                ll = ll + emp.work_email + ','
            self.cc1 = ll

            if self.state == 'draft':
                self.env['email.template'].sudo().send_mail(36, self.ids[0], force_send=True)
            else:
                self.env['email.template'].sudo().send_mail(27, self.ids[0], force_send=True)

        self.state1 = 'tovalid'

        return {
            'name': 'Déclaration des Bons de Controle',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
            # self.env.ref('module_name.view_id').id
            'res_id': self.ids[0],  # ids[0],
            'context': {},
            'domain': []
        }

    # #
    def button_approve2(self):
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        work_ = self.env['project.task.work']
        emp_obj = self.env['hr.employee']

        if not self.mail_send2:
            raise UserError("Erreur Vous devez choisir OUI ou NON pour l'envoi de courriel ")

        if not self.line_ids3:
            raise UserError(" Action impossible! Vous devez avoir au moin une ligne de correction à déclarer!")

        for tt in self.line_ids3:
            if tt.date_end_r:
                print('tt.date_end_r', tt.date_end_r)
                if tt.date_end_r > fields.Date.today():
                    raise UserError("Warning! Date fin doit etre antérieur au date d'aujourd'hui")
            if not tt.date_start_r:
                raise UserError("Action impossible! La date de début est obligatoire!")
            if not tt.facturable:
                raise UserError("Action impossible!', Vous devez définir si cette correction est facturable ou non!")

            if tt.total_part_corr == 'total':
                for ww in self.work_ids:
                    ww.write({
                        'affect_cor_list': ww.affect_cor_list.replace(str(self.emp_id2.user_id.id), '')
                    })
        for ww in self.work_ids:
            res_user = self.env['res.users'].browse(self.env.uid)
            wk_histo = self.env['work.histo'].search([('work_id', '=', ww.id)])

            if wk_histo:
                if len(wk_histo) == 1:
                    wk_histo_id = wk_histo.id
                    self.env['work.histo.line'].create({
                        'type': 'db_corr',
                        'create_by': res_user.employee_id.name,
                        'work_histo_id': wk_histo_id,
                        'date': fields.Datetime.now(),
                        'coment1': self.note4 or False,
                        'id_object': self.ids[0],
                    })
                else:
                    histo = self.env['work.histo'].create({
                        'task_id': ww.task_id.id,
                        'work_id': ww.id,
                        'categ_id': ww.categ_id.id,
                        'product_id': ww.product_id.id,
                        'name': ww.task_id.name,
                        'date': ww.date_start,
                        'create_a': ww.date_start,
                        'zone': ww.zo or 0,
                        'secteur': ww.sect or 0,
                        'project_id': ww.project_id.id,
                        'partner_id': ww.project_id.partner_id.id,
                    })
                self.env['work.histo.line'].create({
                    'type': 'db_corr',
                    'create_by': res_user.employee_id.name,
                    'work_histo_id': histo.id,
                    'date': fields.Datetime.now(),
                    'coment1': self.note4 or False,
                    'id_object': self.ids[0],
                })
            ww.write({'state': 'tovalidcorrec'})
        if self.mail_send2 == 'yes':
            kk = ''
            for line in self.employee_ids5:
                emp = line
                kk = kk + emp.work_email + ','
            self.to2 = kk

            ll = ''
            for line in self.employee_ids6:
                emp = line
                ll = ll + emp.work_email + ','
            self.cc2 = ll

            if self.state == 'draft':
                self.env['email.template'].sudo().send_mail(37, self.ids[0], force_send=True)
            else:
                self.env['email.template'].sudo().send_mail(28, self.ids[0], force_send=True)

        self.state2 = 'tovalid'

        return {
            'name': 'Déclaration des Bons de Correction',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    # button_approve_s
    def valider_bon(self):

        hr_payslip = self.env['hr.payslip']
        # hr_payslip_line = self.env['hr.payslip.line']
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        employee_obj = self.env['hr.employee']
        task_obj = self.env['project.task.work']
        task_obj_line = self.env['project.task.work.line']
        files = self.env['base.group.merge.automatic.wizard']

        sum1 = 0
        line = self.employee_id.id
        empl = employee_obj.browse(line)

        for tt in self.line_ids:
            self_line = line_obj1.browse(tt.id)

            line_obj1.write(tt.id, {'state': 'valid', 'bon_id': self.id})
            task_obj_line.write(self_line.line_id.id, {'state': 'valid', 'done3': True})

            if tt.total_part == 'total' and tt.work_id.affect_emp_list:
                tt.work_id.write({
                    'current_emp': False,
                    'affect_emp_list': tt.work_id.affect_emp_list.replace(str(tt.employee_id.user_id.id), ''),
                    'affect_e_l': tt.work_id.affect_e_l.replace(str(tt.employee_id.user_id.login),
                                                                '') if tt.work_id.affect_e_l else '',
                })
            elif tt.total_part == 'total':
                tt.work_id.write({
                    'current_emp': False,
                })
        self.write({'state': 'valid', 'done': False})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'res_id': self.ids[0],  # ids[0],
            'context': {},
            'domain': []
        }

    def button_switch_(self, cr, uid, ids, context=None):

        hr_payslip = self.env['hr.payslip']
        hr_payslip_line = self.env['hr.payslip.line']
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        employee_obj = self.env['hr.employee']
        task_obj = self.env['project.task.work']
        line_obj2 = self.env['group_line.show.line2']

        sum1 = 0
        ##        if this.state !='valid':
        ##            raise osv.except_osv(_('Error !'), _('Switch n"est possible qu"après validation Bon!'))
        if not self.gest_id_:
            raise UserError('Vous devez assigner une ressource!')

        for kk in self.line_ids2:
            if not kk.b1:
                line_obj2.write(kk.id, {'gest_id2': self.gest_id_.id})
        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,
            'res_id': self.ids[0],  # ids[0],
            'context': {},
            'domain': []
        }

    def button_switch(self):
        print('button_switch')
        hr_payslip = self.env['hr.payslip']
        hr_payslip_line = self.env['hr.payslip.line']
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        employee_obj = self.env['hr.employee']
        task_obj = self.env['project.task.work']
        line_obj2 = self.env['group_line.show.line2']
        emp_obj = self.env['hr.employee']
        task_obj_line = self.env['project.task.work.line']
        files = self.env['base.group.merge.automatic.wizard']

        this = self
        sum1 = 0

        self.write({'state1': 'draft'})

        if not this.gest_id2:
            raise UserError(_('Vous devez assigner une ressource!'))

        if not this.mail_send3:
            raise UserError(_('Choix obligatoire d"envois d"email pour le controleur!'))

        if this.mail_send3 == 'yes':
            self.write({'employee_ids': False})
            if this.note is False:
                self.write({'note': ' '})
            else:
                kk = ''
                for line in this.employee_ids3.ids:
                    emp = emp_obj.browse(line)
                    kk = kk + emp.work_email + ','
                self.write({'to1': kk})

                if this.employee_ids4:
                    ll = ''
                    for line in this.employee_ids4.ids:
                        emp = emp_obj.browse(line)
                        ll = ll + emp.work_email + ','
                    self.write({'cc1': ll})

                self.env['email.template'].send_mail(30, this.id, force_send=True)
            for tt in this.work_ids:
                task_obj.write(tt.id, {'gest_id2': this.gest_id2.id})

            for kk in this.line_ids2:
                if not kk.b1:
                    line_obj2.write(kk.id, {'gest_id': this.gest_id2.id})
            for ww in this.work_ids:
                task_obj.write(ww.id, {'state': 'tovalidcont', 'current_emp': this.gest_id2.id})

            return {
                'name': 'Déclaration des Bons',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'base.group.merge.automatic.wizard',
                'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_control_form').id,
                # self.env.ref('module_name.view_id').id,
                'res_id': self.ids[0],  # ids[0],
                'context': {},
                'domain': []
            }

    def button_switch1(self, cr, uid, ids, context=None):
        hr_payslip = self.env['hr.payslip']
        hr_payslip_line = self.env['hr.payslip.line']
        line_obj = self.env['base.group.merge.automatic.wizard']
        line_obj1 = self.env['base.group.merge.line']
        work_line = self.env['project.task.work.line']
        emp_obj = self.env['hr.employee']
        employee_obj = self.env['hr.employee']
        task_obj = self.env['project.task.work']
        line_obj2 = self.env['group_line.show.line2']
        task_obj_line = self.env['project.task.work.line']
        files = self.env['base.group.merge.automatic.wizard']
        self.write({'state2': 'draft'})
        self.write({'state2': 'draft'})

        if not self.emp_id2:
            raise UserError('Vous devez affecter un superviseur!')

        if not self.mail_send4:
            raise UserError('Choix obligatoire d"envois d"email pour le correcteur!')

        if self.mail_send3 == 'yes':
            self.write({'employee_ids': False})
            if self.note is False:
                self.write({'note': ' '})
            else:
                kk = ''
                for line in self.employee_ids5.ids:
                    emp = emp_obj.browse(line)
                    kk = kk + emp.work_email + ','
                self.write({'to2': kk})

                if self.employee_ids6:
                    ll = ''
                    for line in self.employee_ids6.ids:
                        emp = emp_obj.browse(line)
                        ll = ll + emp.work_email + ','
                    self.write({'cc2': ll})

                self.env['email.template'].send_mail(31, self.ids[0], force_send=True)
        for tt in self.work_ids:
            task_obj.write(tt.id, {'gest_id3': self.emp_id2.id})

        for kk in self.line_ids3:
            if not kk.b1:
                line_obj2.write(kk.id, {'employee_id': self.emp_id2.id})

        for ww in self.work_ids:
            task_obj.write(ww.id, {'state': 'tovalidcorrec', 'current_emp': self.emp_id2.id})

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('med_eb_group_wizard.declaration_de_bon_correction_form').id,
            # self.env.ref('module_name.view_id').id,
            'res_id': ids[0],  # self.ids[0],
            'context': {},
            'domain': []
        }

    # @api.multi
    # def copy(self, default=None):
    #     return super(ProjectWork, self).copy(default=default)

    def action_copy(self, default=None):
        if default is None:
            default = {}
        cte = False
        for current in self:
            for tt in current.work_ids:
                packaging_obj = self.env['project.task.work']
                vals = {
                    'task_id': tt.task_id.id,
                    'product_id': tt.product_id.id,
                    'name': tt.name + ' * ',
                    'date_start': tt.date_start,
                    'date_end': tt.date_end,
                    'poteau_t': tt.poteau_t,
                    'color': tt.color,
                    'total_t': tt.color * 7,
                    'project_id': tt.task_id.project_id.id,
                    'gest_id': tt.gest_id.id,
                    'uom_id': tt.uom_id.id,
                    'uom_id_r': tt.uom_id_r.id,
                    'ftp': tt.ftp,
                    'zone': tt.zone,
                    'secteur': tt.secteur,
                    'state': 'draft'
                }
                cte = packaging_obj.create(vals)

        return cte

    # @api.model
    # def create(self, vals):
    #
    #     if self.env.context['active_model'] == 'project.task.work' and 'active_ids' in self.env.context:
    #         return {
    #             'name': 'Déclaration des Bons',
    #             'type': 'ir.actions.act_window',
    #             'view_type': 'form',
    #             'view_mode': 'form',
    #             # 'target': 'new',
    #             'res_model': 'base.group.merge.automatic.wizard',
    #             'view_id': self.env.ref('med_eb_group_wizard.declaration_bons_form').id,  # 1543,
    #             'res_id': self.ids[0],
    #             'context': {},
    #             'domain': []
    #         }
    #     else:
    #         return

    # EB: {'lang': 'en_US', 'tz': 'Africa/Tunis', 'uid': 7, 'allowed_company_ids': [1], 'active_ids': [6], 'active_model': 'project.task.work'}
    # EB: {'lang': 'en_US', 'tz': 'Africa/Tunis', 'uid': 7, 'allowed_company_ids': [1], 'active_ids': [6], 'active_model': 'project.task.work'}
    # def action_group(self, cr, uid, id, default=None, context=None):
    #     # your changes
    #     if default is None:
    #         default = {}
    #     num = 0
    #     list1 = []
    #
    #     for current in self.browse(cr, uid, id, context=context):
    #         sum1 = 0
    #         for tt in current.work_ids:
    #             ##if not default.get('name'):
    #             ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% tt.name)
    #             line = tt.employee_id.id
    #             if not (line in list1):
    #                 list1.append(line)
    #
    #             if tt.employee_id.id != list1[0]:
    #                 raise osv.except_osv(_('Choix Invalide!'),
    #                                      _("Seuls les Travaux d'un seul intervenant sont autorisés!"))
    #             if tt.state != 'tovalid':
    #                 raise osv.except_osv(_('Choix Invalide!'), _("Seuls les Travaux 'A Facturer' sont autorisés!"))
    #             num = num + 1
    #
    #             hr_payslip = self.pool.get('hr.payslip')
    #             hr_payslip_line = self.pool.get('hr.payslip.line')
    #             employee_obj = self.pool.get('hr.employee')
    #             ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
    #             task_obj = self.pool.get('project.task.work')
    #             empl = employee_obj.browse(cr, uid, list1[0], context=context)
    #
    #             if empl.job_id.id == 1:
    #                 name = 'Feuille de Temps'
    #             else:
    #                 name = 'Facture'
    #
    #             if num == 1:
    #                 cr.execute(
    #                     "select cast(substr(number, 6, 8) as integer) from hr_payslip where number is not Null and name=%s and EXTRACT(YEAR FROM date_from)=%s  order by cast(substr(number, 6, 8) as integer) desc limit 1",
    #                     (name, tt.date[:4],))
    #                 q3 = cr.fetchone()
    #                 if q3:
    #                     res1 = q3[0] + 1
    #                 else:
    #                     res1 = '001'
    #                 pay_id = hr_payslip.create(cr, uid, {'employee_id': tt.employee_id.id,
    #                                                      'date_from': tt.date,
    #                                                      'date_to': tt.date,
    #                                                      'contract_id': tt.employee_id.contract_id.id,
    #                                                      'name': name,
    #                                                      'number': str(
    #                                                          str(tt.date[:4]) + '-' + str(str(res1).zfill(3))),
    #                                                      'struct_id': 1,
    #                                                      'currency_id': 5,
    #                                                      ## 'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
    #                                                      }, context)
    #             task_obj.write(cr, uid, tt.id, {'state': 'valid', 'paylist_id': pay_id}, context=context)
    #             pay_id_line = hr_payslip_line.create(cr, uid, {'employee_id': tt.employee_id.id,
    #                                                            'contract_id': tt.employee_id.contract_id.id,
    #                                                            'name': ' ',
    #                                                            'code': '-',
    #                                                            'category_id': 1,
    #                                                            'quantity': tt.hours_r,
    #                                                            'slip_id': pay_id,
    #                                                            'rate': 100,
    #                                                            'work_id': tt.id,
    #                                                            ##'contract_id':this.employee_id.contract_id.id,
    #
    #                                                            'quantity': tt.poteau_r,
    #                                                            'salary_rule_id': 1,
    #                                                            'amount': tt.wage,
    #                                                            ## 'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
    #                                                            }, context)
    #
    #     return pay_id

    # def unlink(self):
    #     for proj in self:
    #         if proj.state != 'draft':
    #             raise UserError('Action Impossible! Seules Les Bons Brouillons peuvent etre supprimés!')
    #
    #     return super(EbMergegroups, self).unlink()

    # def action_copy3(self):
    #     packaging_obj = self.env['project.task']
    #     packaging_copy = packaging_obj.copy(self.dst_task_id.id)
    #     packaging_copy.write({'name': 'dfsdf'})
    #     return True
