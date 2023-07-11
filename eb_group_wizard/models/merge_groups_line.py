# -*- coding: utf-8 -*-

from lxml import etree
# from openerp import models, fields, api, _
from odoo import models, fields, api, _
# from openerp.osv import osv
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import datetime as dt
import math


class MergegroupsLine(models.Model):
    _name = 'base.group.merge.line'
    _description = 'base group merge line'
    # _order = 'min_id asc'

    wizard_id = fields.Many2one('base.group.merge.automatic.wizard', string='Wizard')
    wiz_id = fields.Integer(string='Wizard')
    kit_id = fields.Many2one('product.kit', string='Kit')
    r_id = fields.Many2one('risk.management.category', string='Wizard')
    min_id = fields.Integer(string='Wizard')
    aggr_ids = fields.Char('Ids')
    ftp = fields.Char(string='ftp')
    zo = fields.Char(string='Zone')
    name = fields.Char(string='Name')

    line_id = fields.Many2one('project.task.work.line', string='Wizard')
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    # categ to category (to be modified)
    categ_id = fields.Many2one('product.category', string='Tags')
    product_id = fields.Many2one('product.product', string='Tags')
    work_id = fields.Many2one('project.task.work', string='Wizard')

    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    date_start_r = fields.Date(string='Date')
    date_end_r = fields.Date(string='Date')
    date_start = fields.Date(string='Date')
    date_end = fields.Date(string='Date')
    color = fields.Float(string='Time Spent')
    uom_id = fields.Many2one('product.uom', string='Wizard')
    etape = fields.Char(string='Time Spent')
    hours = fields.Float(string='Time Spent')
    poteau_i = fields.Float(string='Time Spent')

    employee_id = fields.Many2one('hr.employee', string='Wizard')
    gest_id = fields.Many2one('hr.employee', string='Wizard')
    hours_r = fields.Float(string='Time Spent')
    total_t = fields.Float(string='Time Spent')
    total_r = fields.Float(string='Time Spent')
    poteau_t = fields.Float(string='Time Spent')
    poteau_r = fields.Float(string='Time Spent')
    wage = fields.Float(string='Time Spent')
    amount_line = fields.Float(string='Time Spent')
    poteau_reste = fields.Float(string='Time Spent')
    sequence = fields.Integer(string='Sequence')
    is_service = fields.Boolean(string='serv')

    zone = fields.Integer('Color Index')
    secteur = fields.Integer('Color Index')
    state = fields.Selection([
        ('draft', 'T. Planifiés'),
        ('affect', 'T. Affectés'),
        ('tovalid', 'Ret Encours'),
        ('tovalidcont', 'Control Encours'),
        ('validcont', 'Control Valides'),
        ('tovalidcorrec', 'Correction Encours'),
        ('validcorrec', 'Correction .Valides'),
        ('valid', 'Bons Validés'),

        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
    ],
        'Status', copy=False)
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Cloturé'),

    ],
        'Status', copy=False)

    note = fields.Text(string='Work summary')
    done = fields.Boolean(string='is done')
    color1 = fields.Integer(string='Nbdays')
    link_id = fields.Many2one('project.task', string='Wizard')
    uom_id_r = fields.Many2one('product.uom', string='Wizard')
    is_display = fields.Boolean(string='Ids')

    def onchange_product_id(self, product_id, context=None):
        product_obj = self.env['product.product']
        vals = {}
        if product_id:
            prod = product_obj.browse(product_id, context=context)
            vals.update({'categ_id': prod.categ_id.id, 'uom_id': prod.uom_id.id})

        return {'value': vals}

    def kit_open(self):
        line_obj = self.env['base.group.merge.line']
        parent = line_obj.browse(self.ids[0])
        return {
            'name': 'Consultation Kit',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'product.kit',
            'res_id': parent.kit_id.id,
            'context': {},
            'domain': []
        }

    #
    def onchange_date_to_(self, date_to, date_from, employee_id):
        """
        Update the number_of_days.
        """
        result = {'value': {}}
        if date_to:
            if str(date_to) > str(fields.Date.today()):
                raise UserError('Date fin doit etre antérieur au date d\'aujourd\'hui')
        # date_to has to be greater than date_from
        if date_from and date_to and date_from > date_to:
            raise UserError('The start date must be anterior to the end date.')

        holiday_obj = self.env['hr.holidays']
        hours_obj = self.env['training.holiday.year']
        this = self.env['base.group.merge.line']
        employee = self.env['hr.employee'].browse(employee_id)

        # Compute and update the number of days

        if date_to and date_from and date_from <= date_to:
            DATETIME_FORMAT = "%Y-%m-%d"
            from_dt = fields.Datetime.from_string(date_from)
            to_dt = fields.Datetime.from_string(date_to)
            timedelta = to_dt - from_dt
            diff_day = holiday_obj._get_number_of_days(date_from, date_to)
            year = hours_obj.search([('year', '=', str(date_from.year))])
            if year:
                hr = hours_obj.browse(year[0]).hours
            else:
                hr = 7
            result['value']['color1'] = round(math.floor(diff_day)) + 1
        else:
            result['value']['color1'] = 0
            result['value']['total_r'] = 0
            result['value']['amount_line'] = 0

        return result

    def onchange_qty_(self, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r):
        """
        Update the number_of_days.
        """
        employee_obj = self.env['hr.employee']
        academic_obj = self.env['hr.academic']
        empl = self.env['hr.employee'].browse(employee_id)

        result = {'value': {}}

        if poteau_r:
            wage = 0
            aca = academic_obj.search([('employee_id', '=', employee_id)])
            if not aca:
                raise UserError(
                    'Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!')

            for academic in aca:
                ligne = academic_obj.browse(academic)
                if not ligne.curr_ids:
                    raise UserError(
                        'Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!')

                for ll in ligne.curr_ids:
                    if ll.product_id and ll.uom_id:
                        if ll.product_id.id == product_id and ll.uom_id.id == uom_id:
                            wage = ll.amount
                        elif ll.product_id and ll.uom_id2:
                            if ll.product_id.id == product_id and ll.uom_id2.id == uom_id:
                                wage = ll.amount2
                    elif ll.categ_id and ll.uom_id:
                        if ll.categ_id.id == categ_id and ll.uom_id.id == uom_id:
                            wage = ll.amount
                        elif ll.categ_id and ll.uom_id2:
                            if ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id:
                                wage = ll.amount2

            if wage == 0:
                raise UserError(
                    'Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!')

            if uom_id == 5:
                result['value']['wage'] = wage
                result['value']['total_r'] = hours_r * wage
                result['value']['amount_line'] = hours_r * wage
            else:
                result['value']['total_r'] = poteau_r * wage
                result['value']['amount_line'] = poteau_r * wage
                result['value']['wage'] = wage

        return result

    def onchange_hours_(self, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r, context=None):
        """
        Update the number_of_days.
        """

        academic_obj = self.env['hr.academic']
        empl = self.env['hr.employee'].browse(employee_id)

        result = {'value': {}}

        if hours_r:
            wage = 0
            aca = academic_obj.search([('employee_id', '=', employee_id)])
            if not aca:
                raise UserError(
                    'Error, Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!')

            for academic in aca:
                ligne = academic_obj.browse(academic)
                if not ligne.curr_ids:
                    raise UserError(
                        'Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!')

                for ll in ligne.curr_ids:
                    if ll.product_id and ll.uom_id:
                        if ll.product_id.id == product_id and ll.uom_id.id == uom_id:
                            wage = ll.amount
                        elif ll.product_id and ll.uom_id2:
                            if ll.product_id.id == product_id and ll.uom_id2.id == uom_id:
                                wage = ll.amount2
                    elif ll.categ_id and ll.uom_id:
                        if ll.categ_id.id == categ_id and ll.uom_id.id == uom_id:
                            wage = ll.amount
                        elif ll.categ_id and ll.uom_id2:
                            if ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id:
                                wage = ll.amount2

            if wage == 0:
                raise UserError('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur '
                                'SVP!')

            if uom_id == 5:
                result['value']['wage'] = wage
                result['value']['total_r'] = hours_r * wage
                result['value']['amount_line'] = hours_r * wage
            else:
                result['value']['total_r'] = poteau_r * wage
                result['value']['amount_line'] = poteau_r * wage
                result['value']['wage'] = wage

        return result

    def button_save_(self, ids):

        this = self.browse(ids[0])
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']
        if not this.line_ids:
            raise UserError('Vous devez avoir au moin une ligne à déclarer!')

        return {
            'name': 'Déclaration des Bons',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            # 'view_id': self.env.ref('module_name.view_id').id,  # Replace 'module_name' with the actual module name and view ID
            'view_id': 1543,
            'res_id': ids[0],
            'context': {},
            'domain': []
        }

    def action_issue(self):
        this_obj = self.env['base.group.merge.automatic.wizard']
        current = self.browse(self.ids[0])
        if current.work_id.project_id.r_id:

            self.env.cr.execute(
                'UPDATE risk_management_category SET wizard_id=%s WHERE id=%s',
                (current.wizard_id.id, current.work_id.project_id.r_id.id))

            self.env.cr.execute(
                'UPDATE risk_management_category SET employee_id=%s WHERE id=%s',
                (self.env.user.employee_id.id or 1, current.work_id.project_id.r_id.id))

            self.env.cr.execute(
                'UPDATE risk_management_response_category SET is_me=True WHERE employee_id=%s AND parent_id=%s',
                (self.env.user.employee_id.id or 1, current.work_id.project_id.r_id.id)
            )
            self.env.cr.execute(
                'UPDATE risk_management_response_category SET is_me=False WHERE employee_id<>%s AND parent_id=%s',
                (self.env.user.employee_id.id or 1, current.work_id.project_id.r_id.id)
            )

            return {
                'name': 'Plans des Relevés',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',

                'target': 'popup',
                'res_model': 'risk.management.category',
                'res_id': current.work_id.project_id.r_id.id,

                'nodestroy': True,
                'context': {'default_wizard_id': current.wizard_id.id,
                            'default_name': current.work_id.project_id.number,
                            'default_project_id': current.work_id.project_id.id,
                            'default_employee_id': self.env.user.employee_id.id or 1},
                'domain': [],
                'flags': {'form': {'action_buttons': False}}
            }
        else:

            return {
                'name': 'Plans des Relevés',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',

                'target': 'popup',
                'res_model': 'risk.management.category',
                # 'res_id': ids[0],date_deadline
                'nodestroy': True,
                'context': {'default_wizard_id': current.wizard_id.id,
                            'default_name': current.work_id.project_id.number,
                            'default_project_id': current.work_id.project_id.id,
                            'default_employee_id': self.env.user.employee_id.id or 1
                            },
                'domain': []

            }

    def unlink(self):

        for proj in self:
            if proj.state != 'draft':
                raise UserError('Action Impossible! , Ligne de Bons Validées')

        return super().unlink()
