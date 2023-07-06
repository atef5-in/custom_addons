# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import datetime, date, timedelta
import datetime as dt
import math


class BonShow(models.Model):
    _name = 'bon.show'
    _rec_name = 'name'

    def _amount_all(self):

        tax_obj = self.env['account.tax']

        tvp_obj = tax_obj.browse(8)
        tps_obj = tax_obj.browse(7)
        for rec in self:
            rec.amount_untaxed = 0.0
            rec.amount_tvq = 0.0
            rec.amount_tps = 0.0
            rec.amount_total = 0.0
            rec.total_h = 0.0

            if rec.type == 'Facture':
                if rec.employee_id.tva == 'yes':
                    tvq = tvp_obj.amount
                    tps = tps_obj.amount
                else:
                    tvq = 0
                    tps = 0
            elif rec.employee_id.job_id.id == 1 or rec.employee_id.tva == 'no':
                tvq = 0
                tps = 0
            else:
                tvq = tvp_obj.amount
                tps = tps_obj.amount
            for line in rec.line_ids2:
                rec.amount_untaxed += round(line.amount_line, 2)
                rec.total_h += line.hours_r
            rec.amount_tps += round(rec.amount_untaxed, 2) * tps
            rec.amount_tvq += round(rec.amount_untaxed, 2) * tvq
            rec.amount_total += round(rec.amount_tps, 2) + round(
                rec.amount_tvq, 2) + round(rec.amount_untaxed, 2)

    def _disponible(self):

        for book in self:
            if book.gest_id and book.gest_id.user_id:
                if book.gest_id.user_id.id == self.env.user.id or self.env.user.id == 1:
                    book.done = True
                else:
                    book.done = False
            else:
                book.done = False

    def _disponible1(self):

        for book in self:
            if book.employee_id and book.employee_id.user_id:
                if book.employee_id.user_id.id == self.env.user.id or self.env.user.id == 1:
                    book.done1 = True
                else:
                    book.done1 = False
            else:
                book.done1 = True

    def _get_user1(self):

        employee_id = self.env['res.users'].browse(self.env.uid).employee_id
        if employee_id:
            return employee_id.id
        else:
            return False

    @api.depends_context('uid')
    def _super_admin(self):
        for record in self:
            record.sadmin = self.env.user.has_group('project_custom.group_super_admin')

    categ_id = fields.Many2one('product.category', string='Tags', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    date_from = fields.Date(string='date de', select=True, readonly=True, states={'draft': [('readonly', False)]},
                            default=time.strftime('%Y-01-01'))
    date_to = fields.Date(string=u'date a', select=True, readonly=True, states={'draft': [('readonly', False)]},
                          default=lambda *a: time.strftime('%Y-%m-%d'), )
    send = fields.Boolean(string='Litigation', readonly=True, states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', 'Nationality', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    employee_id = fields.Many2one('hr.employee', string='Task', readonly=True,
                                  states={'draft': [('readonly', False)]}, default=lambda self: self._get_user1(), )
    gest_id = fields.Many2one('hr.employee', string='Task', readonly=True, states={'draft': [('readonly', False)]}, )
    project_id = fields.Many2one('project.project', string='Project', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    task_id = fields.Many2one('project.task', 'Nationality', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    work_id = fields.Many2one('project.task.work', 'Nationality', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    product_id = fields.Many2one('product.product', 'Nationality', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    user_id = fields.Many2one('hr.employee', 'Nationality', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    name = fields.Char(string='Nom')
    tps = fields.Char(string='tps', readonly=True, states={'draft': [('readonly', False)]}, )
    tvq = fields.Char(string='tvq', readonly=True, states={'draft': [('readonly', False)]}, )
    line_ids1 = fields.One2many('bon.show.line1', 'bon_id', string='Work done', readonly=True,
                                states={'draft': [('readonly', False)]}, )
    line_ids2 = fields.One2many('bon.show.line2', 'bon_id', string='Work done')
    pay_id = fields.Many2one('hr.payslip', string='Wizard', readonly=True,
                             states={'draft': [('readonly', False)]}, )
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('waiting', 'En Attente Validation'),
        ('open', 'Terminé'),
        ('cancelled', 'Annulée'),
        ('pending', 'Suspendu'),
        ('close', 'Approuvé'),
        ('treat', 'Traité'),
        ('paid', 'Payé'),
    ],
        string='Status', copy=False, default='draft')
    week_no = fields.Selection([
        ('01', '01'),
        ('02', '02'),
        ('03', '03'),
        ('04', '04'),
        ('05', '05'),
        ('06', '06'),
        ('07', '07'),
        ('08', '08'),
        ('09', '09'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52')], string='Status', copy=False, readonly=True, states={'draft': [('readonly', False)]},
        default=str(time.strftime('%W')))
    year_no = fields.Char(string='year', readonly=True, states={'draft': [('readonly', False)]},
                          default=str(time.strftime('%Y')))
    intern = fields.Selection([
        ('intern', 'Employés Uniquement'),
        ('extern', 'Externes Uniquement'),
        ('both', 'Tous'),
    ],
        string='Status', copy=False, readonly=True, states={'draft': [('readonly', False)]}, )
    filter = fields.Selection([
        ('best', 'Meilleur KPI'),
        ('nearest', 'Plus Proche'),
        ('Cheepest', 'Moins Couteux '),
    ],
        string='Status', copy=False, readonly=True, states={'draft': [('readonly', False)]}, )
    date = fields.Date(string=u'date a', default=lambda *a: time.strftime('%Y-%m-%d'))
    # fields.date.context_today
    date_p = fields.Date(string=u'date a', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    amount_untaxed = fields.Float(compute='_amount_all', string='Company Currency',
                                  readonly=True, states={'draft': [('readonly', False)]}, )
    # multi = 'all',
    amount_total = fields.Float(compute='_amount_all', string='Company Currency',
                                readonly=True, states={'draft': [('readonly', False)]}, )
    # multi = 'all',
    amount_tvq = fields.Float(compute='_amount_all', string='Company Currency', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    # , multi = 'all'
    amount_tps = fields.Float(compute='_amount_all', string='Company Currency', readonly=True,
                              states={'draft': [('readonly', False)]}, )
    # , multi = 'all'
    total_h = fields.Float(compute='_amount_all', string='Company Currency', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    # multi = 'all',
    done = fields.Boolean(compute='_disponible', string='done', readonly=True,
                          states={'draft': [('readonly', False)]}, )
    done1 = fields.Boolean(compute='_disponible1', string='done', readonly=True,
                           states={'draft': [('readonly', False)]}, )
    sadmin = fields.Boolean(compute='_super_admin', string='done', )
    notes = fields.Text(string='year', readonly=True, states={'draft': [('readonly', False)]}, )
    type = fields.Char(string='Type', readonly=True, states={'draft': [('readonly', False)]}, )
    to = fields.Char(string='year', readonly=True, states={'draft': [('readonly', False)]}, )
    cc = fields.Char(string='year', readonly=True, states={'draft': [('readonly', False)]}, )
    cci = fields.Char(string='year', readonly=True, states={'draft': [('readonly', False)]}, )
    line_ids = fields.Many2many('project.task.work.line', 'bon_show_project_task_work_line_rel', 'bon_show_id',
                                'project_task_work_line_id', string='Legumes', readonly=True,
                                states={'draft': [('readonly', False)]}, )
    mail_send = fields.Selection([
        ('yes', 'Oui'),
        ('no', 'Non'),
    ],
        string='Status', copy=False, readonly=True, states={'draft': [('readonly', False)]}, )
    employee_ids = fields.Many2many('hr.employee', 'bon_show_hr_employee_rel', 'bon_show_id', 'hr_employee_id',
                                    string='Legumes', readonly=True, states={'draft': [('readonly', False)]}, )
    employee_ids1 = fields.Many2many('hr.employee', 'bon_show_hr_employee_rel1', 'bon_show_id', 'hr_employee_id',
                                     string='Legumes', readonly=True, states={'draft': [('readonly', False)]}, )
    employee_ids2 = fields.Many2many('hr.employee', 'bon_show_hr_employee_rel2', 'bon_show_id', 'hr_employee_id',
                                     string='Legumes', readonly=True, states={'draft': [('readonly', False)]}, )

    def unlink(self):
        for rec in self:
            if rec.state not in ['draft']:
                raise UserError(
                    _('Warning!\nImpossible de supprimer une Facture ou F/T si le statut n"est pas brouillon!'))
            for kk in rec.line_ids2:
                self.env.cr.execute("DELETE FROM bon_show_line2 WHERE bon_id=%s ", (rec.id,))

        return super(BonShow, self).unlink()

    def action_open(self):

        return {
            'name': ('Préparation F.T'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'bon.show',
            'view_id': self.env.ref('bon_show.view_ft_form').id,
            'res_id': self.ids[0],
            'context': {'active_id': self.ids[0]},
        }

    def button_save_(self):

        line_obj1 = self.env['bon.show.line2']
        this = self[0]
        for kk in this.line_ids2:
            work = line_obj1.browse(kk.id)

            employee_obj = self.env['hr.employee']
            academic_obj = self.env['hr.academic']
            roles_obj = self.env['res.users.role']

            empl = employee_obj.browse(this.employee_id.id)

            wage = 0
            aca = academic_obj.search([('employee_id', '=', empl.id)])

            if aca:
                for list in aca:

                    if list:
                        ligne = academic_obj.browse(list)
                        if ligne.curr_ids:

                            for ll in ligne.curr_ids:
                                if ligne.project_id and ll.project_id.id == ligne.project_id.id:
                                    if ll.product_id and ll.uom_id:
                                        if (ll.product_id.id == work.product_id.id):
                                            wage = ll.amount
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})

                                            break
                                        elif ll.product_id and ll.uom_id2:
                                            if (ll.product_id.id == work.product_id.id):
                                                wage = ll.amount2
                                                line_obj1.write(kk.id,
                                                                {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                 'total_r': work.poteau_r * wage,
                                                                 'amount_line': work.poteau_r * wage})
                                                break

                                    elif ll.product_id and ll.uom_id2:
                                        if (ll.product_id.id == work.product_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break

                                    elif ll.categ_id and ll.uom_id:
                                        if (ll.categ_id.id == work.categ_id.id):
                                            wage = ll.amount
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break
                                        elif ll.categ_id and ll.uom_id2:
                                            if (ll.categ_id.id == work.categ_id.id):
                                                wage = ll.amount2
                                                line_obj1.write(kk.id,
                                                                {'wage': wage, 'total_r': work.poteau_r * wage,
                                                                 'uom_id_r': ll.uom_id2.id,
                                                                 'amount_line': work.poteau_r * wage})
                                                break

                                    elif ll.categ_id and ll.uom_id2:
                                        if (ll.categ_id.id == work.categ_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break
                        if ligne.curr_ids:

                            for ll in ligne.curr_ids:
                                if ll.partner_id.id == ligne.partner_id.id:
                                    if ll.product_id and ll.uom_id:
                                        if (ll.product_id.id == work.product_id.id):
                                            wage = ll.amount
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break
                                        elif ll.product_id and ll.uom_id2:
                                            if (ll.product_id.id == work.product_id.id):
                                                wage = ll.amount2
                                                line_obj1.write(kk.id,
                                                                {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                 'total_r': work.poteau_r * wage,
                                                                 'amount_line': work.poteau_r * wage})
                                                break

                                    elif ll.product_id and ll.uom_id2:
                                        if (ll.product_id.id == work.product_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break

                                    elif ll.categ_id and ll.uom_id:
                                        if (ll.categ_id.id == work.categ_id.id):
                                            wage = ll.amount
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break
                                        elif ll.categ_id and ll.uom_id2:
                                            if (ll.categ_id.id == work.categ_id.id):
                                                wage = ll.amount2
                                                line_obj1.write(kk.id,
                                                                {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                 'total_r': work.poteau_r * wage,
                                                                 'amount_line': work.poteau_r * wage})
                                                break

                                    elif ll.categ_id and ll.uom_id2:
                                        if (ll.categ_id.id == work.categ_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break
                        if ligne.curr_ids:

                            for ll in ligne.curr_ids:

                                if ll.product_id and ll.uom_id:
                                    if (ll.product_id.id == work.product_id.id):
                                        wage = ll.amount
                                        line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                'total_r': work.poteau_r * wage,
                                                                'amount_line': work.poteau_r * wage})
                                        break
                                    elif ll.product_id and ll.uom_id2:
                                        if (ll.product_id.id == work.product_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break

                                elif ll.product_id and ll.uom_id2:
                                    if (ll.product_id.id == work.product_id.id):
                                        wage = ll.amount2
                                        line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                'total_r': work.poteau_r * wage,
                                                                'amount_line': work.poteau_r * wage})
                                        break

                                elif ll.categ_id and ll.uom_id:
                                    if (ll.categ_id.id == work.categ_id.id):
                                        wage = ll.amount
                                        line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                'total_r': work.poteau_r * wage,
                                                                'amount_line': work.poteau_r * wage})
                                        break
                                    elif ll.categ_id and ll.uom_id2:
                                        if (ll.categ_id.id == work.categ_id.id):
                                            wage = ll.amount2
                                            line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                    'total_r': work.poteau_r * wage,
                                                                    'amount_line': work.poteau_r * wage})
                                            break

                                elif ll.categ_id and ll.uom_id2:
                                    if (ll.categ_id.id == work.categ_id.id):
                                        wage = ll.amount2
                                        line_obj1.write(kk.id, {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                'total_r': work.poteau_r * wage,
                                                                'amount_line': work.poteau_r * wage})
                                        break

                if wage == 0:

                    roles = roles_obj.search([])
                    for gp in roles:
                        ro = roles_obj.browse(gp)
                        if this.employee_id.id in ro.employee_ids.ids:
                            aca = academic_obj.search([('role_id', '=', ro.id)])

                            if aca:
                                for list in aca:

                                    if list:
                                        ligne = academic_obj.browse(list)

                                        if ligne.curr_ids:
                                            for ll in ligne.curr_ids:
                                                if ligne.project_id and ll.project_id.id == ligne.project_id.id:
                                                    if ll.product_id and ll.uom_id:
                                                        if (ll.product_id.id == work.product_id.id):
                                                            wage = ll.amount
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                                        elif ll.product_id and ll.uom_id2:
                                                            if (ll.product_id.id == work.product_id.id):
                                                                wage = ll.amount2
                                                                line_obj1.write(kk.id, {'wage': wage,
                                                                                        'uom_id_r': ll.uom_id2.id,
                                                                                        'total_r': work.poteau_r * wage,
                                                                                        'amount_line': work.poteau_r * wage})
                                                                break

                                                    elif ll.product_id and ll.uom_id2:
                                                        if (ll.product_id.id == work.product_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break

                                                    elif ll.categ_id and ll.uom_id:
                                                        if (ll.categ_id.id == work.categ_id.id):
                                                            wage = ll.amount
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                                        elif ll.categ_id and ll.uom_id2:
                                                            if (ll.categ_id.id == work.categ_id.id):
                                                                wage = ll.amount2
                                                                line_obj1.write(kk.id, {'wage': wage,
                                                                                        'uom_id_r': ll.uom_id2.id,
                                                                                        'total_r': work.poteau_r * wage,
                                                                                        'amount_line': work.poteau_r * wage})
                                                                break

                                                    elif ll.categ_id and ll.uom_id2:
                                                        if (ll.categ_id.id == work.categ_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                        if ligne.curr_ids:

                                            for ll in ligne.curr_ids:
                                                if ligne.project_id is False and ll.partner_id.id == ligne.partner_id.id:
                                                    if ll.product_id and ll.uom_id:
                                                        if (ll.product_id.id == work.product_id.id):
                                                            wage = ll.amount
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                                        elif ll.product_id and ll.uom_id2:
                                                            if (ll.product_id.id == work.product_id.id):
                                                                wage = ll.amount2
                                                                line_obj1.write(kk.id, {'wage': wage,
                                                                                        'uom_id_r': ll.uom_id2.id,
                                                                                        'total_r': work.poteau_r * wage,
                                                                                        'amount_line': work.poteau_r * wage})
                                                                break

                                                    elif ll.product_id and ll.uom_id2:
                                                        if (ll.product_id.id == work.product_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break

                                                    elif ll.categ_id and ll.uom_id:
                                                        if (ll.categ_id.id == work.categ_id.id):
                                                            wage = ll.amount
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                                        elif ll.categ_id and ll.uom_id2:
                                                            if (ll.categ_id.id == work.categ_id.id):
                                                                wage = ll.amount2
                                                                line_obj1.write(kk.id, {'wage': wage,
                                                                                        'uom_id_r': ll.uom_id2.id,
                                                                                        'total_r': work.poteau_r * wage,
                                                                                        'amount_line': work.poteau_r * wage})
                                                                break

                                                    elif ll.categ_id and ll.uom_id2:
                                                        if (ll.categ_id.id == work.categ_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break
                                        if ligne.curr_ids:

                                            for ll in ligne.curr_ids:

                                                if ll.product_id and ll.uom_id:
                                                    if (ll.product_id.id == work.product_id.id):
                                                        wage = ll.amount
                                                        line_obj1.write(kk.id,
                                                                        {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                         'total_r': work.poteau_r * wage,
                                                                         'amount_line': work.poteau_r * wage})
                                                        break

                                                    elif ll.product_id and ll.uom_id2:
                                                        if (ll.product_id.id == work.product_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break

                                                elif ll.product_id and ll.uom_id2:
                                                    if (ll.product_id.id == work.product_id.id):
                                                        wage = ll.amount2
                                                        line_obj1.write(kk.id,
                                                                        {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                         'total_r': work.poteau_r * wage,
                                                                         'amount_line': work.poteau_r * wage})
                                                        break

                                                elif ll.categ_id and ll.uom_id:
                                                    if (ll.categ_id.id == work.categ_id.id):

                                                        wage = ll.amount
                                                        line_obj1.write(kk.id,
                                                                        {'wage': wage, 'uom_id_r': ll.uom_id.id,
                                                                         'total_r': work.poteau_r * wage,
                                                                         'amount_line': work.poteau_r * wage})
                                                        break

                                                    elif ll.categ_id and ll.uom_id2:
                                                        if (ll.categ_id.id == work.categ_id.id):
                                                            wage = ll.amount2
                                                            line_obj1.write(kk.id,
                                                                            {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                             'total_r': work.poteau_r * wage,
                                                                             'amount_line': work.poteau_r * wage})
                                                            break

                                                elif ll.categ_id and ll.uom_id2:
                                                    if (ll.categ_id.id == work.categ_id.id):
                                                        wage = ll.amount2
                                                        line_obj1.write(kk.id,
                                                                        {'wage': wage, 'uom_id_r': ll.uom_id2.id,
                                                                         'total_r': work.poteau_r * wage,
                                                                         'amount_line': work.poteau_r * wage})
                                                        break

            if work.uom_id_r.id == 5:
                line_obj1.write(kk.id, {'total_r': work.hours_r * wage, 'amount_line': work.hours_r * wage})

        return True

    def button_approve(self):

        line_obj1 = self.env['bon.show.line2']
        emp_obj = self.env['hr.employee']
        this = self[0]
        self.button_save_()
        for tt in this.line_ids2:
            this_line = line_obj1.browse(tt.id)

            if this_line.line_id:
                if this_line.line_id.done1 is True:
                    raise UserError(_('Erreur\nLes Lignes sont déja facturées!'))

            if this_line.send is False:
                valid = 0
        if this.mail_send is False:
            raise UserError(
                _('Erreur\nVous devez choisir OUI ou NON pour l"envoi de courriel!(Onglet Informations Mail)'))
        if this.mail_send == 'yes':
            if this.notes is False:
                self.write({'notes': ' '})
            if not this.employee_ids:
                raise UserError(_('Erreur !\nVous devez sélectionner un destinataire.'))
            else:
                kk = ''
                for line in this.employee_ids.ids:
                    emp = emp_obj.browse(line)
                    kk = kk + emp.work_email + ','
                self.write({'to': kk})
                if this.employee_ids1:

                    ll = ''
                    for line in this.employee_ids1.ids:
                        emp = emp_obj.browse(line)
                        ll = ll + emp.work_email + ','
                    self.write({'cc': ll})
                if this.employee_ids2:

                    mm = ''
                    for line in this.employee_ids2.ids:
                        emp = emp_obj.browse(line)
                        mm = mm + emp.work_email + ','
                    self.write({'cci': mm})

            self.env['email.template'].send_mail(29, force_send=True)

        self.write({'state': 'waiting'})
        if this.type == 'Facture':
            dep1 = self.env['bon.show'].search([('employee_id', '=', this.employee_id.id),
                                                ('name', '=', this.name.replace(" ", "")),
                                                ('id', '!=', this.id)])
            if dep1:
                raise UserError(
                    _('Action Impossible!\nUne Facture avec le même numéro existe déjà! Facture N°:%s') % this.name)

        return {
            'name': ('Préparation Feuille de Temps/Facture'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('bon_show.view_ft_form').id,
            'target': 'current',
            'res_model': 'bon.show',
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_approve_s(self):

        hr_payslip = self.env['hr.payslip']
        hr_payslip_line = self.env['hr.payslip.line']
        bgl_obj = self.env['base.group.merge.line']
        line_obj1 = self.env['bon.show.line2']
        work_line = self.env['project.task.work.line']

        employee_obj = self.env['hr.employee']
        task_obj_line = self.env['project.task.work.line']
        this = self[0]

        line = this.employee_id.id
        empl = employee_obj.browse(line)
        if empl.job_id.id == 1:
            name = 'Feuille de Temps'
        else:
            name = 'Facture'

        self.env.cr.execute(
            "select cast(substr(number, 6, 8) as integer) from hr_payslip where number is not Null and name=%s and EXTRACT(YEAR FROM date_from)=%s  order by number desc limit 1",
            (name, this.date_from.year))
        q3 = self.env.cr.fetchone()
        if q3:
            res1 = q3[0] + 1
        else:
            res1 = '001'

        pay_id = hr_payslip.create({'employee_id': line,
                                    'date_from': this.date_from,
                                    'date_to': this.date_to,
                                    'contract_id': this.employee_id.contract_id.id,
                                    'name': name,
                                    'number': str(str(this.date_from[:4]) + '-' + str(str(res1).zfill(3))),
                                    'struct_id': 1,
                                    'currency_id': 5,
                                    })

        for tt in this.line_ids2:

            this_line = line_obj1.browse(tt.id)
            if tt.work_id:
                name = tt.work_id.name
                code = tt.work_id.product_id.default_code
                unit = tt.uom_id_r.id
            else:
                name = tt.product_id.name
                code = tt.product_id.default_code
                unit = tt.uom_id_r.id
            hr_payslip_line.create({'employee_id': this.employee_id.id,
                                    'contract_id': this.employee_id.contract_id.id,
                                    'name': name,
                                    'code': code,
                                    'category_id': 1,
                                    'quantity': tt.hours_r,
                                    'slip_id': pay_id,
                                    'rate': 100,
                                    'work_id': tt.work_id.id,
                                    'uom_id': unit,
                                    'salary_rule_id': 1,
                                    'amount': tt.wage,
                                    })
            if this_line.send is False:
                work_line.create({'employee_id': this.employee_id.id,
                                  'name': name,
                                  'categ_id': this_line.product_id.categ_id.id,
                                  'project_id': this_line.project_id.id or False,
                                  'partner_id': this_line.partner_id.id or False,
                                  'zo': str(this_line.zone),
                                  'sect': str(this_line.secteur),
                                  'date_start_r': this_line.date_start_r,
                                  'hours_r': this_line.hours_r,
                                  'note': this_line.note,
                                  'state': 'close',
                                  'sequence': 1,
                                  'poteau_r': this_line.poteau_r,
                                  'uom_id_r': this_line.uom_id_r.id or False,
                                  'uom_id': this_line.uom_id_r.id or False,
                                  'date': this.date,
                                  'done1': True,
                                  'done3': True,
                                  })

            task_obj_line.write(this_line.line_id.id,
                                {'state': 'valid', 'paylist_id': pay_id, 'done1': True, 'group_id': this.id})
            if task_obj_line.browse(this_line.line_id.id).group_id2:
                tt = bgl_obj.search([('line_id', '=', this_line.line_id.id)])
                if tt:
                    self.env.cr.execute('update base_group_merge_automatic_wizard set  state=%s where id=%s', (
                        'invoiced', task_obj_line.browse(this_line.line_id.id).group_id2.id), )
        if empl.job_id.id == 1:
            self.env['email.template'].send_mail(32, force_send=True)

        self.write({'state': 'close', 'pay_id': pay_id})

        return True

    def button_reopen(self):

        self.write({'state': 'draft'})
        return {
            'name': ('Préparation Feuille de Temps/Facture'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'bon.show',
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    def button_preview(self):

        list = []
        current = self[0]

        self.env.cr.execute(
            'select id from project_task_work_line where employee_id= %s and date>=%s and date <=%s and done3 is True and done1 is False',
            (current.employee_id.id, current.date_from, current.date_to))
        project_id = self.env.cr.fetchall()

        if current.state != 'draft':
            raise UserError(_("Action Impossible!\nAction possible qu'en statut brouillon!"))

        if project_id:
            for tt in project_id:
                list.append(tt)

        return {
            'name': ('Préparation Feuille de Temps/Facture'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'popup',
            'res_model': 'base.work_line.wizard',
            'context': {'default_work_line_ids': list, 'work_line_ids': list},
            'domain': [('default_work_line_ids', 'in', list)]
        }

    def load_(self):

        """
        Action that shows the list of (non-draft) account moves from
        the selected journals and periods, so the user can review
        the renumbered account moves.
        """

        current = self[0]

        self.env.cr.execute(
            'select id from project_task_work_line where employee_id= %s and date>=%s and date <=%s and done3 is True and done1 is False',
            (current.employee_id.id, current.date_from, current.date_to))
        project_id = self.env.cr.fetchall()

        if current.state != 'draft':
            raise UserError(_("Action Impossible!\nAction possible qu'en statut brouillon!"))
        if project_id:
            for tt in project_id:
                s2 = self.env['project.task.work.line'].browse(tt)
                s3 = self.env['bon.show.line2'].search([('line_id', '=', s2.id)])
                if not s3:
                    if current.employee_id.job_id.name in u'Employé':
                        uom = 5
                        self.write({'type': 'Feuille de Temps'})
                    else:
                        uom = s2.uom_id_r.id
                        self.write({'type': 'Facture'})
                    self.env['bon.show.line2'].create({
                        'task_id': s2.task_id.id,
                        'categ_id': s2.work_id.categ_id.id,
                        'product_id': s2.product_id.id,
                        'name': s2.name,
                        'date_start': s2.date_start,
                        'date_end': s2.date_end,
                        'date_start_r': s2.date_start_r,
                        'date_end_r': s2.date_end_r,
                        'poteau_t': s2.poteau_t,
                        'poteau_r': s2.poteau_r,
                        'color': s2.color,
                        'color1': s2.color1,
                        'hours_r': s2.hours_r,
                        'total_t': s2.total_t,
                        'project_id': s2.work_id.project_id.id,
                        'partner_id': s2.work_id.project_id.partner_id.id,
                        'bon_id': current.id,
                        'gest_id': s2.gest_id.id or False,
                        'employee_id': s2.employee_id.id or False,
                        'uom_id': uom or s2.uom_id.id,
                        'uom_id_r': uom or s2.uom_id.id,
                        'ftp': s2.ftp,
                        'state': s2.state,
                        'work_id': s2.work_id.id,
                        'line_id': s2.id,
                        'zone': s2.zone,
                        'done': True,
                        'send': True,
                        'secteur': s2.secteur,

                    })

        return True

    def button_load_mail(self):

        this = self[0]

        self.env.cr.execute("INSERT INTO bon_show_hr_employee_rel  VALUES (%s,%s)"
                            % (this.id, this.gest_id.id))

        return {
            'name': ('Préparation Feuille de Temps/Facture'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'bon.show',
            'res_id': self.ids[0],
            'context': {},
            'domain': []
        }

    @api.onchange('gest_id', 'employee_id')
    def onchange_gest_id(self):
        result = {'value': {}}
        if self.gest_id and self.employee_id:
            gest_user = self.env['hr.employee'].search([('id', '=', self.gest_id.id)]).user_id.id
            emp_user = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).user_id.id
            if emp_user == self.env.user.id or self.env.user.id == 1:
                result['value']['done1'] = True

            else:
                result['value']['done1'] = False
            if gest_user == self.env.user.id or self.env.user.id == 1:
                result['value']['done'] = True
            else:
                result['value']['done'] = False
            result['value']['tps'] = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).tps
            result['value']['tvq'] = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).tvq
        return result

    ##########################################################################
    # Renumber form/action
    ##########################################################################
    @api.onchange('year_no', 'week_no')
    def onchange_week_(self):

        result = {'value': {}}

        d = date(int(self.year_no), 1, 1)
        if (d.weekday() <= 3):
            d = d - dt.timedelta(d.weekday())
        else:
            d = d + dt.timedelta(7 - d.weekday())
        dlt = dt.timedelta(days=(int(self.week_no) - 1) * 7)

        result['value']['date_from'] = d + dlt
        result['value']['date_to'] = d + dlt + dt.timedelta(days=6)
        return result

    @api.onchange('date', 'employee_id')
    def onchange_date_(self):

        result = {'value': {}}
        emp_user = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).contract_id.schedule_pay

        if self.employee_id and self.date:
            days = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
            delta_day = timedelta(days=1)
            day_count = 0
            if emp_user == 'monthly':
                date_2 = datetime.strptime(str(self.date), "%Y-%m-%d")

                end_date = date_2 + timedelta(days=30)
                df = end_date
                while df.weekday() == days['sun'] or df.weekday() == days['sat']:
                    day_count += 1
                    df += delta_day

            elif emp_user == 'biweekly':
                date_2 = datetime.strptime(str(self.date), "%Y-%m-%d")

                end_date = date_2 + timedelta(days=15)
                df = end_date
                while df.weekday() == days['sun'] or df.weekday() == days['sat']:
                    day_count += 1
                    df += delta_day
            else:
                date_2 = datetime.strptime(str(self.date), "%Y-%m-%d")

                end_date = date_2 + timedelta(days=7)
                df = end_date
                while df.weekday() == days['sun'] or df.weekday() == days['sat']:
                    day_count += 1
                    df += delta_day

            result['value']['date_p'] = df

        return result


class BonShowLine2(models.Model):
    _name = "bon.show.line2"

    def _disponible(self):

        for book in self:
            if self.uid == 1:
                book.done = True

            elif book.bon_id.state == 'draft' and book.send is False:
                book.done = True
            else:
                book.done = False

    bon_id = fields.Many2one('bon.show', string='Task')
    name = fields.Char(string='Work summary', )
    ftp = fields.Char(string='ftp', )
    date = fields.Datetime(string='Date', select="1", )
    date_r = fields.Datetime(string='Date', select="1", )
    date_start = fields.Date(string='Date', select="1", )
    date_end = fields.Date(string='Date', select="1", )
    date_start_r = fields.Date(string='Date', select="1")
    date_end_r = fields.Date(string='Date', select="1")
    employee_id = fields.Many2one('hr.employee', string='Task', )
    partner_id = fields.Many2one('res.partner', string='Task', )
    project_id = fields.Many2one('project.project', 'Project')
    task_id = fields.Many2one('project.task', string='Task')
    work_id = fields.Many2one('project.task.work', string='Nationality')
    group_id = fields.Many2one('base.group.merge.automatic.wizard', string='Nationality')
    product_id = fields.Many2one('product.product', string='Task')
    hours = fields.Float(string='Time Spent', )
    hours_r = fields.Float(string='Time Spent')
    total_t = fields.Float(string='Time Spent')
    amount_line = fields.Float(string='Time Spent')
    wage = fields.Float(string='Time Spent')
    poteau_t = fields.Float(string='Time Spent', )
    poteau_r = fields.Float(string='Time Spent', )
    poteau_reste = fields.Float(string='Time Spent', )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'),
    ],
        string='Status', copy=False, )
    sequence = fields.Integer(string='Sequence', select=True, )
    zone = fields.Integer(string='Color Index', )
    secteur = fields.Integer(string='Color Index', )
    user_id = fields.Many2one('res.users', string='Done by', select="1", )
    paylist_id = fields.Many2one('hr.payslip', string='Done by', select="1", )
    gest_id = fields.Many2one('hr.employee', string='Task', )
    issue_id = fields.Many2one('project.issue', string='Done by', select="1", )
    state = fields.Selection([('draft', 'T. Planifiés'),
                              ('affect', 'T. Affectés'),
                              ('tovalid', 'T. Validés'),
                              ('valid', 'Factures en Attentes'),
                              ('paid', 'Factures Approuvées'),
                              ('cancel', 'T. Annulés'),
                              ('pending', 'T. Suspendus'),
                              ('close', 'Traité')],
                             string='Status', copy=False)
    note = fields.Text(string='Work summary', states={'affect': [('readonly', False)]}, )
    send = fields.Boolean(string='is done', )
    color = fields.Integer(string='Nbdays', )
    color1 = fields.Integer(string='Nbdays', states={'affect': [('readonly', False)]}, )
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True, )
    uom_id_r = fields.Many2one('product.uom', string='Unit of Measure', states={'affect': [('readonly', False)]}, )
    line_id = fields.Many2one('project.task.work.line', string='Tags')
    categ_id = fields.Many2one('product.category', string='Tags')
    done = fields.Boolean(compute='_disponible', string='done', default=1)

    @api.onchange('employee_id', 'bon_id.type')
    def onchange_employee_id(self):
        res = {}
        r = []
        dep1 = self.env['hr.academic'].search([('employee_id', '=', self.employee_id.id)]).ids
        if dep1:
            for ll in dep1:
                c = self.env['hr.academic'].browse(ll).categ_id.id
                r.append(c)
                print(r)
                if r:
                    for nn in r:
                        if self.bon_id.type == 'Feuille de Temps':
                            dep = self.env['product.product'].search([('categ_id', '=', nn), ('is_ft', '=', True)])
                        else:

                            dep = self.env['product.product'].search([('categ_id', '=', nn), ('is_invoice', '=', True)])

                        if dep:
                            for jj in dep:
                                r.append(jj)
            res['domain'] = {'product_id': [('id', 'in', r)]}
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        product_obj = self.env['product.product']
        vals = {}

        if self.product_id:
            prod = product_obj.browse(self.product_id)
            vals.update({'categ_id': prod.categ_id.id, 'uom_id_r': prod.uos_id.id, 'uom_id': prod.uos_id.id})

        return {'value': vals}

    @api.onchange('date_end_r', 'date_start_r', 'employee_id')
    def onchange_date_to_(self):
        """
        Update the number_of_days.
        """

        date_to = self.date_end_r
        date_from = self.date_start_r

        # date_to has to be greater than date_from
        if (date_from and date_to) and (date_from > date_to):
            raise UserError(_('Warning!\nThe start date must be anterior to the end date.'))

        result = {'value': {}}
        holiday_obj = self.env['hr.holidays']

        # Compute and update the number of days

        if (date_to and date_from) and (date_from <= date_to):
            diff_day = holiday_obj._get_number_of_days(date_from, date_to)
            result['value']['color1'] = round(math.floor(diff_day)) + 1

        else:

            result['value']['color1'] = 0
            result['value']['total_r'] = 0
            result['value']['amount_line'] = 0

        return result


class BonShowLine1(models.Model):
    _name = 'bon.show.line1'

    bon_id = fields.Integer(string='Task')
    name = fields.Char(string='Work summary', )
    ftp = fields.Char(string='ftp', )
    date = fields.Datetime(string='Date', select="1", )
    date_r = fields.Datetime(string='Date', select="1", )
    date_start = fields.Date(string='Date', select="1", )
    date_end = fields.Date(string='Date', select="1", )
    date_start_r = fields.Date(string='Date', select="1")
    date_end_r = fields.Date(string='Date', select="1")
    employee_id = fields.Many2one('hr.employee', string='Task')
    project_id = fields.Many2one('project.project', string='Project')
    task_id = fields.Many2one('project.task', string='Task')
    work_id = fields.Many2one('project.task.work', string='Task')
    line_id = fields.Many2one('project.task.work.line', string='Task')
    product_id = fields.Many2one('product.product', string='Task')
    hours = fields.Float(string='Time Spent', )
    etape = fields.Char(string='etap', )
    categ_id = fields.Many2one('product.category', string='Tags', )
    total_t = fields.Float(string='Time Spent', )
    poteau_t = fields.Integer(string='Time Spent', )
    poteau_i = fields.Integer(string='Time Spent', )
    poteau_reste = fields.Integer(string='Time Spent', )
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'),
    ],
        string='Status', copy=False, )
    sequence = fields.Integer(string='Sequence', select=True, )
    state_id = fields.Many2one('res.country.state', string='Alias', )
    city = fields.Char(string='Char', )
    state_id1 = fields.Many2one('res.country.state', string='Alias')
    state_id2 = fields.Many2one('res.country.state', string='Alias')
    precision = fields.Char(string='precision')
    permis = fields.Char(string='permis')
    date_fin = fields.Date(string='Date')
    prolong = fields.Char(string='prolong')
    remarque = fields.Text(string='remarque')
    date_remis = fields.Date(string='Date')
    date_construt = fields.Date(string='Date')
    secteur_en = fields.Char(string='secteur Enfui')
    graphe_t_b = fields.Char(string='graphe_t_b')
    dct = fields.Char(string='gct')
    anomalie = fields.Char(string='gct')
    action = fields.Char(string='action')
    statut = fields.Selection([('soumise', 'Soumise'),
                               ('etude', 'A l''étude'),
                               ('approuve', 'Approuvé'),
                               ('incomplet', 'Incomplet'),
                               ('construction', 'En Construction'),
                               ('envoye', 'Envoyé'),
                               ('travaux_pre', 'Travaux Pré.'),
                               ('refus', 'Refusé'),
                               ('refus_part', 'Refus Partiel'),
                               ('travaux_comp', 'Travaux Complété'),
                               ('inspection', 'Inspection'),
                               ('annule', 'Annulé'),
                               ('deviation', 'Déviation'),
                               ('3032', '3032'), ],
                              string='Status', copy=False)
    zone = fields.Integer(string='Color Index', )
    secteur = fields.Integer(string='Color Index', )
    user_id = fields.Many2one('res.users', string='Done by', select="1", )
    paylist_id = fields.Many2one('hr.payslip', string='Done by', select="1", )
    gest_id = fields.Many2one('hr.employee', string='Task', )
    issue_id = fields.Many2one('project.issue', string='Done by', select="1", )
    group_id = fields.Many2one('base.group.merge.automatic.wizard', 'Done by', select="1", )
    state = fields.Selection([('draft', 'T. Planifiés'),
                              ('affect', 'T. Affectés'),
                              ('tovalid', 'T.Encours'),
                              ('valid', 'T.Terminés'),
                              ('cancel', 'T. Annulés'),
                              ('pending', 'T. Suspendus'),
                              ],

                             string='Status', copy=False)
    note = fields.Text(string='Work summary')
    color = fields.Integer(string='Nbdays')
    color1 = fields.Integer(string='Nbdays')
    uom_id = fields.Many2one('product.uom', string='Unit of Measure', required=True)
    uom_id_r = fields.Many2one('product.uom', string='Unit of Measure')


class HrHolidays(models.Model):
    _name = 'hr.holidays'


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    group_id = fields.Many2one('bon.show', 'group ID', select="1", readonly=True,
                               states={'draft': [('readonly', False)]}, )


class ProjectTaskWorkLine(models.Model):
    _inherit = 'project.task.work.line'

    group_id = fields.Many2one('bon.show', string='Done by', select="1", readonly=True,
                               states={'affect': [('readonly', False)]}, )
