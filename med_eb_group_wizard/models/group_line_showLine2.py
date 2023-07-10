import time
import itertools
from odoo import netsvc
from lxml import etree
from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning, RedirectWarning
from odoo.tools import float_compare
# from odoo.addons import decimal_precision as dp
from odoo import fields, models
from odoo import api, SUPERUSER_ID
from datetime import datetime as dt
import math


class GroupLineShowLine2(models.Model):
    _name = "group_line.show.line2"
    _description = "group line show line2"

    work_id2 = fields.Many2one('project.task.work', string='Event')  # to_verfy
    work_id = fields.Many2one('project.task.work', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    line_id = fields.Many2one('project.task.work.line', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char('Work summary', readonly=True, states={'draft': [('readonly', False)]})
    ftp = fields.Char('ftp', readonly=True, states={'draft': [('readonly', False)]})
    date = fields.Datetime('Date', readonly=True, states={'draft': [('readonly', False)]})
    date_r = fields.Datetime('Date', readonly=True, states={'draft': [('readonly', False)]})
    date_start = fields.Date('Date', readonly=True, states={'draft': [('readonly', False)]})
    date_end = fields.Date('Date', readonly=True, states={'draft': [('readonly', False)]})
    date_start_r = fields.Date('Date', readonly=True, states={'draft': [('readonly', False)]})
    date_end_r = fields.Date('Date', readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    project_id = fields.Many2one('project.project', 'Project',
                                 ondelete='set null',
                                 select=True,
                                 track_visibility='onchange',
                                 change_default=True, readonly=True, states={'draft': [('readonly', False)]})
    task_id = fields.Many2one('project.task', 'Task', ondelete='cascade', required=True, select=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    product_id = fields.Many2one('product.product', 'Task', ondelete='cascade', required=True, select=True,
                                 readonly=True, states={'draft': [('readonly', False)]})
    hours = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    hours_r = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    poteau_r = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    etape = fields.Char('etap', readonly=True, states={'draft': [('readonly', False)]})
    categ_id = fields.Many2one('product.category', string='Tags', readonly=True,
                               states={'draft': [('readonly', False)]})
    total_t = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    poteau_t = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    poteau_i = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    poteau_reste = fields.Float('Time Spent', readonly=True, states={'draft': [('readonly', False)]})
    total_part = fields.Selection([
        ('partiel', 'Partiel'),
        ('total', 'Total'),
    ], 'Status', copy=False, readonly=True, states={'draft': [('readonly', False)]})
    sequence = fields.Integer('Sequence', select=True, readonly=True, states={'draft': [('readonly', False)]})
    state_id = fields.Many2one('res.country.state', 'Alias', readonly=True, states={'draft': [('readonly', False)]})
    city = fields.Char('Char', readonly=True)
    state_id1 = fields.Many2one('res.country.state', 'Alias')
    state_id2 = fields.Many2one('res.country.state', 'Alias')
    precision = fields.Char('precision')
    permis = fields.Char('permis')
    date_fin = fields.Date('Date')
    prolong = fields.Char('prolong')
    remarque = fields.Text('remarque')
    date_remis = fields.Date('Date')
    date_construt = fields.Date('Date')
    secteur_en = fields.Char('secteur Enfui')
    graphe_t_b = fields.Char('graphe_t_b')
    dct = fields.Char('gct')
    anomalie = fields.Char('gct')
    action = fields.Char('action')
    statut = fields.Selection([
        ('soumise', 'Soumise'),
        ('etude', "A l'étude"),
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
        ('3032', '3032'),
    ], 'Status', copy=False)
    corr = fields.Selection([
        ('oui', 'Oui'),
        ('non', 'Non'),
    ], 'Status', copy=False)
    facturable = fields.Selection([
        ('facturable', 'Facturable'),
        ('nfacturable', 'Non Facturable'),
    ], 'Status', copy=False)
    b1 = fields.Boolean('Work summary', readonly=True, states={'draft': [('readonly', False)]})
    zone = fields.Integer('Color Index', readonly=True, states={'draft': [('readonly', False)]})
    secteur = fields.Integer('Color Index', readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', 'Done by', select=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    paylist_id = fields.Many2one('hr.payslip', 'Done by', select=True, readonly=True,
                                 states={'draft': [('readonly', False)]})
    gest_id = fields.Many2one('hr.employee', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    emp_id2 = fields.Many2one('hr.employee', 'Task', readonly=True, states={'draft': [('readonly', False)]})
    issue_id = fields.Many2one('project.issue', 'Done by', select=True, readonly=True,
                               states={'draft': [('readonly', False)]})
    group_id = fields.Many2one('base.group.merge.automatic.wizard', 'Done by', select=True, readonly=True,
                               states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'T. Planifiés'),
        ('draft', 'T. Affectés'),
        ('tovalid', 'T.Encours'),
        ('valid', 'T.Terminés'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
    ], 'Status', copy=False, readonly=True, states={'draft': [('readonly', False)]})
    note = fields.Text('Work summary', readonly=True, states={'draft': [('readonly', False)]})
    color = fields.Integer('Nbdays', readonly=True, states={'draft': [('readonly', False)]})
    color1 = fields.Integer('Nbdays', readonly=True, states={'draft': [('readonly', False)]})
    uom_id = fields.Many2one('product.uom', 'Unit of Measure', required=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    uom_id_r = fields.Many2one('product.uom', 'Unit of Measure', readonly=True,
                               states={'draft': [('readonly', False)]})
    project_id2 = fields.Many2one('project.project', 'Task', readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('product_id')
    def onchange_product_id(self):
        product_obj = self.env['product.product']
        vals = {}

        if self.product_id:
            prod = product_obj.browse(self.product_id.id)
            vals.update({'categ_id': prod.categ_id.id, 'uom_id': prod.uom_id.id})

        return {'value': vals}

    def kit_open(self):
        line_obj = self.env['base.group.merge.line']
        parent = self

        return {
            'name': ('Consultation Kit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'product.kit',
            'res_id': parent.kit_id.id,
            'context': {},
            'domain': [],
            'target': 'new',
        }

    @api.onchange('date_to', 'date_from', 'employee_id')
    def onchange_date_to_(self):
        """
        Update the number_of_days.
        """

        # date_to has to be greater than date_from
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise UserError(_('Warning!'), _('The start date must be anterior to the end date.'))

        result = {'value': {}}
        holiday_obj = self.env['hr.holidays']
        hours_obj = self.env['training.holiday.year']
        this = self.env['base.group.merge.line']
        employee = self.env['hr.employee'].browse(self.employee_id.id)

        if self.date_to and self.date_from and self.date_from <= self.date_to:  ##'%Y-%m-%d %H:%M:%S'
            DATETIME_FORMAT = "%Y-%m-%d"
            from_dt = dt.datetime.strptime(self.date_from, DATETIME_FORMAT)
            to_dt = dt.datetime.strptime(self.date_to, DATETIME_FORMAT)
            timedelta = to_dt - from_dt
            diff_day = holiday_obj._get_number_of_days(self.date_from, self.date_to)
            year = hours_obj.search([('year', '=', str(self.date_from[:4]))])
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

    def onchange_qty_(self):
        """
        Update the number_of_days.
        """

        employee_obj = self.env['hr.employee']
        academic_obj = self.env['hr.academic']

        empl = self.employee_id

        result = {'value': {}}

        if self.poteau_r:
            wage = 0
            aca = academic_obj.search([('employee_id', '=', self.employee_id.id)])
            if aca:
                for academic in aca:
                    if academic:
                        ligne = academic_obj.browse(academic)
                        if ligne.curr_ids:
                            for ll in ligne.curr_ids:
                                if ll.product_id and ll.uom_id:
                                    if ll.product_id.id == self.product_id.id and ll.uom_id.id == self.uom_id.id:
                                        wage = ll.amount
                                    elif ll.product_id and ll.uom_id2:
                                        if ll.product_id.id == self.product_id.id and ll.uom_id2.id == self.uom_id.id:
                                            wage = ll.amount2
                                elif ll.categ_id and ll.uom_id:
                                    if ll.categ_id.id == self.categ_id.id and ll.uom_id.id == self.uom_id.id:
                                        wage = ll.amount
                                    elif ll.categ_id and ll.uom_id2:
                                        if ll.categ_id.id == self.categ_id.id and ll.uom_id2.id == self.uom_id.id:
                                            wage = ll.amount2
                                else:
                                    raise UserError(_('Error!'),
                                                    _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
                        else:
                            raise UserError(_('Error!'),
                                            _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
                    else:
                        raise UserError(_('Error!'),
                                        _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))
            else:
                raise UserError(_('Error!'),
                                _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))

            if wage == 0:
                raise UserError(_('Error!'),
                                _('Taux horaire Non Défini pour cette configuration, Veuillez consulter le Superviseur SVP!'))

            if self.uom_id.id == 5:
                result['value']['wage'] = wage
                result['value']['total_r'] = self.hours_r * wage
                result['value']['amount_line'] = self.hours_r * wage
            else:
                result['value']['total_r'] = self.poteau_r * wage
                result['value']['amount_line'] = self.poteau_r * wage
                result['value']['wage'] = wage

        return result

    def onchange_hours_(self, hours_r, employee_id, categ_id, product_id, uom_id, poteau_r):
        """
        Update the number_of_days.
        """

        employee_obj = self.env['hr.employee']
        academic_obj = self.env['hr.academic']
        empl = employee_obj.browse(employee_id)

        result = {'value': {}}

        if hours_r:
            wage = 0
            aca = academic_obj.search([('employee_id', '=', employee_id)])
            if aca:
                for record in aca:
                    if record:
                        ligne = academic_obj.browse(record)
                        if ligne.curr_ids:
                            for ll in ligne.curr_ids:
                                if ll.product_id and ll.uom_id:
                                    if ll.product_id.id == product_id and ll.uom_id.id == uom_id:
                                        wage = ll.amount
                                    elif ll.product_id and ll.uom_id2:
                                        if ll.product_id.id == product_id and ll.uom_id2.id == uom_id:
                                            wage = ll.amount2

                                elif ll.product_id and ll.uom_id2:
                                    if ll.product_id.id == product_id and ll.uom_id2.id == uom_id:
                                        wage = ll.amount2

                                elif ll.categ_id and ll.uom_id:
                                    if ll.categ_id.id == categ_id and ll.uom_id.id == uom_id:
                                        wage = ll.amount
                                    elif ll.categ_id and ll.uom_id2:
                                        if ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id:
                                            wage = ll.amount2

                                elif ll.categ_id and ll.uom_id2:
                                    if ll.categ_id.id == categ_id and ll.uom_id2.id == uom_id:
                                        wage = ll.amount2

                                else:
                                    raise UserError(_('Erreur!'),
                                                    _('Taux horaire non défini pour cette configuration. Veuillez consulter le superviseur.'))
                        else:
                            raise UserError(_('Erreur!'),
                                            _('Taux horaire non défini pour cette configuration. Veuillez consulter le superviseur.'))
                    else:
                        raise UserError(_('Erreur!'),
                                        _('Taux horaire non défini pour cette configuration. Veuillez consulter le superviseur.'))
            else:
                raise UserError(_('Erreur!'),
                                _('Taux horaire non défini pour cette configuration. Veuillez consulter le superviseur.'))

            if wage == 0:
                raise UserError(_('Erreur!'),
                                _('Taux horaire non défini pour cette configuration. Veuillez consulter le superviseur.'))

            if uom_id == 5:
                result['value']['wage'] = wage
                result['value']['total_r'] = hours_r * wage
                result['value']['amount_line'] = hours_r * wage
            else:
                result['value']['total_r'] = poteau_r * wage
                result['value']['amount_line'] = poteau_r * wage
                result['value']['wage'] = wage

        return result

    def button_save_(self):
        this = self
        work_obj = self.env['project.task.work']
        work_line = self.env['project.task.work.line']
        line_obj1 = self.env['group_line.show.line2']

        if not this.line_ids:
            raise UserError(_("Action impossible!"), _("Vous devez avoir au moins une ligne à déclarer!"))

        return {
            'name': ('Déclaration des Bons'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.group.merge.automatic.wizard',
            'view_id': self.env.ref('your_view_id_here').id,  # Replace 'your_view_id_here' with the actual view ID
            'res_id': this.id,
            'context': {},
            'domain': []
        }

    def action_issue(self):
        project_ids = self.id
        current = self

        if current.issue_id:
            return {
                'name': ('Gestion des Incidents et Anomalies'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.issue',
                'res_id': current.issue_id.id,
                'context': {},
                'domain': [('gline_id', 'in', [project_ids])],
                'target': 'new',
            }
        else:
            return {
                'name': ('Gestion des Incidents et Anomalies'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'project.issue',
                'context': {
                    'default_gline_id': project_ids,
                    'default_work_id': current.work_id.id,
                    'default_date_deadline': fields.Date.today(),
                    'default_employee_id': current.employee_id.id or False,
                    'default_project_id': current.project_id.id,
                    'default_task_id': current.task_id.id,
                    'default_gest_id': current.gest_id.id,
                    'default_name': current.project_id.number + '-' + str(current.task_id.sequence).zfill(
                        3) + '-' + str(
                        current.sequence).zfill(3),
                    'default_color': current.group_id.id,
                },
                'domain': [],
                'target': 'new',
            }

#
#     # group_id = fields.Many2one('base.group.merge.automatic.wizard', string="Group")
#     sequence = fields.Integer(string='Assigned')
#     work_id = fields.Many2one('project.task.work', string='groups')
#
#     work_id2 = fields.Many2one('project.task.work', string='Event')  # to verify (added attribute)
#     poteau_t = fields.Float(string='Time Spent', readonly=True,
#                             states={'affect': [('readonly', False)]}, )  # to verify (added attrubute)
#     name = fields.Char('Nom Service')
#     ftp = fields.Char('Ftp')
#     job = fields.Char('Job')
#     date = fields.Datetime('Date Doc')
#     date_r = fields.Datetime(string='N.U', readonly=True, states={'draft': [('readonly', False)]})
#     date_p = fields.Date(string='N.U')
#     date_start = fields.Date(string='Date Début', readonly=True, states={'draft': [('readonly', False)]})
#     date_end = fields.Date(string='Date Fin', readonly=True, states={'draft': [('readonly', False)]})
#     date_start_r = fields.Date(string='Date Début Réelle', readonly=True, states={'affect': [('readonly', False)]})
#     ex_state = fields.Char(string='ex')
#     date_end_r = fields.Date(string='Date Fin Réelle', readonly=True, states={'affect': [('readonly', False)]})
#
#     r_id = fields.Many2one(comodel_name='risk.management.category', string='N.U', readonly=True,
#                            states={'draft': [('readonly', False)]})
#     project_id = fields.Many2one(
#         comodel_name='project.project', string='Project', ondelete='set null',
#         selection_add=True, track_visibility='onchange', readonly=True, states={'draft': [('readonly', False)]},
#         change_default=True
#     )
#
#     task_id = fields.Many2one('project.task', 'Activités', ondelete='cascade', required=True, select="1")
#     product_id = fields.Many2one('product.product', 'T. de Service', ondelete='cascade', select="1",
#                                  readonly=True, states={'draft': [('readonly', False)]})
#     hours = fields.Float(string='N.U', readonly=True, compute='_compute_hours', store=True)
#     etape = fields.Char(string='Etape', readonly=True, states={'draft': [('readonly', False)]})
#     categ_id = fields.Many2one(comodel_name='product.category', string='Département', readonly=True,
#                                states={'draft': [('readonly', False)]})
#     hours_r = fields.Float(string='Company Currency', compute='_compute_planned_hours', readonly=True, store=True,
#                            states={'draft': [('readonly', False)]})
#     partner_id = fields.Many2one(comodel_name='res.partner', string='Clients', readonly=True,
#                                  states={'draft': [('readonly', False)]})
#     kit_id = fields.Many2one(comodel_name='product.kit', string='Task', ondelete='cascade', readonly=True,
#                              states={'draft': [('readonly', False)]})
#
#     user_id = fields.Many2one('res.users', 'Responsible')
#     line_id = fields.Many2one('project.task.work.line', string='Wizard')
#
#     state_id = fields.Many2one('res.country.state', 'Cité/Ville')
#     city = fields.Char('N.U', readonly=True)
#     state_id1 = fields.Many2one('res.country.state', 'N.U')
#     state_id2 = fields.Many2one('res.country.state', 'N.U')
#     precision = fields.Char('Precision(P)')
#     permis = fields.Char('Permis(P)')
#     date_fin = fields.Date('Date Fin (P)')
#     prolong = fields.Char('Prolongation demandée(P)')
#     remarque = fields.Text('Remarque')
#     date_remis = fields.Date('Date Remis(P)')
#     date_construt = fields.Date('Date Construction(P)')
#     secteur_en = fields.Char('Secteur Enfui(P)')
#     graphe_t_b = fields.Char('Graphe_t_b(P)')
#     dct = fields.Char('Dct(P)')
#     active = fields.Boolean('Active', default=True)
#     anomalie = fields.Char('Anomalie(P)')
#     action = fields.Char('Action(P)')
#     pourc_t = fields.Float('% Avancement', readonly=True, states={'draft': [('readonly', False)]})
#     poteau_r = fields.Float(string='Time Spent')
#     pourc_f = fields.Float(string='% Dépense', readonly=True, states={'draft': [('readonly', False)]})
#     statut1 = fields.Many2one('project.status', string='Status')
#     statut = fields.Selection([
#         ('Encours', 'Encours'),
#         ('Soumise', 'Soumise'),
#         ('A l"Etude', 'A l"étude'),
#         ('Approuve', 'Approuvé'),
#         ('Incomplet', 'Incomplet'),
#         ('En Construction', 'En Construction'),
#         ('Envoye', 'Envoyé'),
#         ('Travaux Pre.', 'Travaux Pré.'),
#         ('Refuse', 'Refusé'),
#         ('Refus Partiel', 'Refus Partiel'),
#         ('Approuve Partiel', 'Approuvé Partiel'),
#         ('Travaux Complété', 'Travaux Complété'),
#         ('Inspection', 'Inspection'),
#         ('Annule', 'Annulé'),
#         ('En Resiliation', 'En Résiliation'),
#         ('Non Requis', 'Non Requis'),
#         ('En TP-derogation approuvee', 'En TP-dérogation approuvée'),
#         ('TP completes-avec refus', 'TP complétés-avec refus'),
#         ('Deviation', 'Déviation'),
#         ('9032', 'Approbation demandeur'),
#         ('DA', 'Approbation demandeur – Dérogation Approuvé'),
#         ('DP', 'Approbation demandeur – Dérogation Partielle'),
#         ('DR', 'Approbation demandeur – Dérogation Refusé'),
#         ('AD', 'Approbation demandeur – ADR Défavorable'),
#         ('TPDP', 'En TP - Dérogation Partielle'),
#         ('TPSD', 'En TP - Sans Dérogation'),
#     ], string='Status', copy=False)
#     kanban_color = fields.Integer(compute='_check_color', string='Couleur')
#     link_id = fields.One2many('link.type', 'work_id', string='Work done')
#     zone = fields.Integer(string='Zone (entier)', readonly=True, states={'draft': [('readonly', False)]})
#     secteur = fields.Integer(string='Secteur (entier)', readonly=True, states={'draft': [('readonly', False)]})
#     zo = fields.Char(string='Zone', readonly=True, states={'draft': [('readonly', False)]})
#     sect = fields.Char(string='Secteur', readonly=True, states={'draft': [('readonly', False)]})
#     paylist_id = fields.Many2one('hr.payslip', string='N.U', select="1", readonly=True,
#                                  states={'draft': [('readonly', False)]})
#     gest_id = fields.Many2one('hr.employee', string='Coordinateur', readonly=True,
#                               states={'draft': [('readonly', False)]})
#     reviewer_id1 = fields.Many2one('hr.employee', string='Superviseur1', readonly=True,
#                                    states={'draft': [('readonly', False)]})
#     gest_id2 = fields.Many2one('hr.employee', string='Coordinateur2', readonly=True,
#                                states={'draft': [('readonly', False)]})
#     coordin_id1 = fields.Many2one('hr.employee', string='Coordinateur1', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id2 = fields.Many2one('hr.employee', string='Coordinateur2', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id3 = fields.Many2one('hr.employee', string='Coordinateur3', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id4 = fields.Many2one('hr.employee', string='Coordinateur4', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id5 = fields.Many2one('hr.employee', string='Coordinateur5', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id6 = fields.Many2one('hr.employee', string='Coordinateur6', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id7 = fields.Many2one('hr.employee', string='Coordinateur7', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id8 = fields.Many2one('hr.employee', string='Coordinateur8', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id9 = fields.Many2one('hr.employee', string='Coordinateur9', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     coordin_id10 = fields.Many2one('hr.employee', string='Coordinateur10', readonly=True,
#                                    states={'draft': [('readonly', False)]})
#     gest_id3 = fields.Many2one('hr.employee', string='N.U', readonly=True, copy=True,
#                                states={'draft': [('readonly', False)]})
#     employee_id = fields.Many2one('hr.employee', string='Employés', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     issue_id = fields.Many2one('project.issue', string='N.U', select="1", readonly=True,
#                                states={'draft': [('readonly', False)]})
#     group_id = fields.Many2one('bon.show', string='N.U', select="1", readonly=False,  ondelete='restrict',
#                                states={'draft': [('readonly', False)]})
#     group_id2 = fields.Many2one('base.group.merge.automatic.wizard', string='N.U', select="1", readonly=True,
#                                 states={'draft': [('readonly', False)]})
#     dependency_task_ids = fields.Many2many('project.task.work', 'project_task_dependency_work_rel',
#                                            'dependency_work_id', 'work_id', string='Dependencies')
#     tate = fields.Selection([
#         ('draft', 'T. Planifiés'),
#         ('affect', 'T. Affectés'),
#         ('affect_con', 'T. Affectés controle'),
#         ('affect_corr', 'T. Affectés corrction'),
#         ('tovalid', 'Ret .Encours'),
#         ('tovalidcont', 'Cont .Encours'),
#         ('validcont', 'Cont .Valides'),
#         ('tovalidcorrec', 'Corr .Encours'),
#         ('validcorrec', 'Corr .Valides'),
#         ('valid', 'T.Terminés'),
#         ('cancel', 'T. Annulés'),
#         ('pending', 'T. Suspendus'),
#     ], string='Status', copy=False)
#     p_done = fields.Float('Qté Réalisée', readonly=True, states={'draft': [('readonly', False)]})
#     note = fields.Text('N.U')
#     done = fields.Boolean(compute='_default_done', string='Company Currency', readonly=True,
#                           states={'draft': [('readonly', False)]})
#     done1 = fields.Boolean(compute='_default_done1', string='Company Currency', readonly=True,
#                            states={'draft': [('readonly', False)]})
#     done2 = fields.Boolean(compute='_default_done2', string='Company Currency', readonly=True,
#                            states={'draft': [('readonly', False)]})
#     done3 = fields.Boolean(compute='_default_done3', string='Company Currency', readonly=True,
#                            states={'draft': [('readonly', False)]})
#     done4 = fields.Boolean(compute='_default_flow', string='Company Currency', readonly=True,
#                            states={'draft': [('readonly', False)]})
#
#     color = fields.Integer(string='Nbdays', readonly=True, states={'draft': [('readonly', False)]})
#     color1 = fields.Integer(string='Nbdays', readonly=True, states={'affect': [('readonly', False)]})
#     uom_id = fields.Many2one('product.uom', 'Unité Prévue', readonly=True,
#                              states={'draft': [('readonly', False)]})
#     uom_id_r = fields.Many2one('product.uom', 'Unité Prévue', readonly=True,
#                                states={'draft': [('readonly', False)]})
#     # state = fields.Many2one('product.uom', 'Unité Réelle', readonly=True,
#     #                            states={'affect': [('readonly', False)]})
#     w_id = fields.Many2one('base.task.merge.automatic.wizard', 'Company', readonly=True,
#                            states={'draft': [('readonly', False)]})
#     pourc = fields.Float('N.U', readonly=True, states={'draft': [('readonly', False)]})
#     rank = fields.Char('N.U', readonly=True, states={'draft': [('readonly', False)]})
#     display = fields.Boolean('Réalisable')
#     is_copy = fields.Boolean('Dupliqué?')
#     done33 = fields.Boolean(string='done', compute='_disponible', store=True)
#     current_emp = fields.Many2one('hr.employee', 'Employé Encours', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     current_gest = fields.Many2one('hr.employee', 'Coordinateur Encours', readonly=True,
#                                    states={'draft': [('readonly', False)]})
#     current_sup = fields.Many2one('hr.employee', 'Superviseur Encours', readonly=True,
#                                   states={'draft': [('readonly', False)]})
#     prior1 = fields.Float('Prior1', readonly=True, states={'draft': [('readonly', False)]})
#     prior2 = fields.Float('Prior2', readonly=True, states={'draft': [('readonly', False)]})
#     cmnt = fields.Char('Prior2', readonly=True, states={'draft': [('readonly', False)]})
#     work_orig = fields.Integer('tache original')
#     affect_emp_list = fields.Char('employée id')
#     affect_e_l = fields.Char('employée id')
#     affect_emp = fields.Char('employée')
#     affect_con = fields.Char('controle')
#     affect_cor = fields.Char('corrdinateur')
#     affect_con_list = fields.Char('controle id')
#     affect_cor_list = fields.Char('corrdinateur id')
#     is_intervenant = fields.Boolean('intervenant', compute='_isinter', store=True)
#     is_control = fields.Boolean('controle', compute='_iscontrol', store=True)
#     is_correction = fields.Boolean('correction', compute='_iscorr', store=True)
#     state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
