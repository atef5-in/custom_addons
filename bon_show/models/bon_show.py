# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time


class BonShow(models.Model):
    _name = 'bon.show'

    def _amount_all(self):

        res = {}
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
                if book.gest_id.user_id.id == self.uid or self.uid == 1:
                    book.done = True
                else:
                    book.done = False
            else:
                book.done = False

    def _disponible1(self):

        for book in self:
            if book.employee_id and book.employee_id.user_id:
                if book.employee_id.user_id.id == self.uid or self.uid == 1:
                    book.done1 = True
                else:
                    book.done1 = False
            else:
                book.done1 = True

    @api.depends_context('uid')
    def _super_admin(self):
        for record in self:
            record._super_admin = self.env.user.has_group('project_custom.group_super_admin')


    categ_id = fields.Many2one('product.category', string='Tags', readonly=True,
                               states={'draft': [('readonly', False)]}, )
    date_from = fields.Date(string='date de', select=True, readonly=True, states={'draft': [('readonly', False)]},
                            default=time.strftime('%Y-01-01'))
    date_to = fields.Date(string=u'date a', select=True, readonly=True, states={'draft': [('readonly', False)]}, )
    # fields.date.context_today
    send = fields.Boolean(string='Litigation', readonly=True, states={'draft': [('readonly', False)]}, )
    partner_id = fields.Many2one('res.partner', 'Nationality', readonly=True,
                                 states={'draft': [('readonly', False)]}, )
    employee_id = fields.Many2one('hr.employee', string='Task', readonly=True,
                                  states={'draft': [('readonly', False)]}, )
    # _get_user1
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
    date = fields.Date(string=u'date a')
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
    sadmin = fields.Boolean(compute='_super_admin', string='done', readonly=True,
                            states={'draft': [('readonly', False)]}, )
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

    def action_open(self):

        return {
            'name': ('Préparation F.T'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'bon.show',
            ##   'view_id': 1616,
            'res_id': self.ids[0],
            'context': {'active_id': self.ids[0]},
        }

    def button_approve(self):

        line_obj1 = self.env['bon.show.line2']
        emp_obj = self.env['hr.employee']
        this = self.browse(cr, uid, ids[0], context)
        self.button_save_()
        for tt in this.line_ids2:
            this_line = line_obj1.browse(tt.id)

            if this_line.line_id:
                if this_line.line_id.done1 is True:
                    raise osv.except_osv(_('Erreur'), _('Les Lignes sont déja facturées!'))

            if this_line.send is False:
                valid = 0
        if this.mail_send is False:
            raise osv.except_osv(_('Erreur'),
                                 _('Vous devez choisir OUI ou NON pour l"envoi de courriel!(Onglet Informations Mail)'))
        if this.mail_send == 'yes':
            if this.notes is False:
                self.write(cr, uid, ids, {'notes': ' '}, context=context)
            if not this.employee_ids:
                raise osv.except_osv(_('Erreur !'), _('Vous devez sélectionner un destinataire.'))
            else:
                kk = ''
                for line in this.employee_ids.ids:
                    emp = emp_obj.browse(cr, uid, line)
                    kk = kk + emp.work_email + ','
                    ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%kk)
                self.write(cr, uid, ids, {'to': kk}, context=context)
                if this.employee_ids1:

                    ll = ''
                    for line in this.employee_ids1.ids:
                        emp = emp_obj.browse(cr, uid, line)
                        ll = ll + emp.work_email + ','
                        ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%kk)
                    self.write(cr, uid, ids, {'cc': ll}, context=context)
                if this.employee_ids2:

                    mm = ''
                    for line in this.employee_ids2.ids:
                        emp = emp_obj.browse(cr, uid, line)
                        mm = mm + emp.work_email + ','
                        ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%kk)
                    self.write(cr, uid, ids, {'cci': mm}, context=context)

            self.pool.get('email.template').send_mail(cr, uid, 29, ids[0], force_send=True, context=context)

        ## if valid==0:
        self.write(cr, uid, ids[0], {'state': 'waiting'}, context=context)
        if this.type == 'Facture':
            dep1 = self.pool.get('bon.show').search(cr, uid, [('employee_id', '=', this.employee_id.id),
                                                              ('name', '=', this.name.replace(" ", "")),
                                                              ('id', '!=', this.id)])
            if dep1:
                raise osv.except_osv(_('Action Impossible!'),
                                     _('Une Facture avec le même numéro existe déjà! Facture N°:%s') % this.name)

        ##        else:
        ##            self.button_approve_s(cr, uid, ids, context)

        return {
            'name': ('Préparation Feuille de Temps/Facture'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'res_model': 'bon.show',
            'res_id': ids[0],
            'context': {},
            'domain': []
        }


class BonShowLine2(models.Model):
    _name = "bon.show.line2"

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
