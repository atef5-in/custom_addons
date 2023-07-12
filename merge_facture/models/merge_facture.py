# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import time
from odoo.exceptions import UserError
from odoo.tools.translate import _


class MergeFacturesLine(models.Model):
    _name = 'base.facture.merge.line'
    _order = 'min_id asc'

    @api.depends('poteau_t', 'price')
    def _compute_amount(self):
        self.total = self.price * self.poteau_t

    wizard_id = fields.Many2one('base.facture.wizard', 'Wizard')
    min_id = fields.Integer(string='MinID')
    aggr_ids = fields.Char(string='Ids')
    zone = fields.Integer(string='zone')
    zo = fields.Char(string='zone')
    secteur = fields.Integer(string='secteur')
    secteur_to = fields.Integer(string='secteur')
    date_from = fields.Date(string='Wizard')
    date_to = fields.Date(string='Wizard')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    poteau_t = fields.Float(string='Time Spent')
    is_display = fields.Boolean(string='Display ?')
    plans = fields.Char(string='Plans')
    name = fields.Char(string='Name')
    from_int = fields.Integer(string='MinID')
    to_int = fields.Integer(string='MinID')
    product_id = fields.Many2one('product.product', string='Wizard')
    uom_id = fields.Many2one('product.uom', string='Wizard')
    code = fields.Char(string='name')
    price = fields.Float(string='Wizard')
    total = fields.Float(string='Wizard', store=True, readonly=True, compute='_compute_amount')
    plan_id = fields.Many2one('risk.management.response.category', string='Wizard')
    plan_id2 = fields.Many2one('risk.management.response.category', string='Wizard')
    risk_id = fields.Many2one('risk.management.category', string='Wizard')

    # verify this onchange
    @api.onchange('poteau_t', 'price')
    def onchange_qty(self):
        raise UserError(_('Error !\nNo period defined for this date: %s ') % self.price)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.code = self.product_id.default_code
        self.name = self.product_id.name
        self.uom_id = self.product_id.uom_id.id
    #
    # def onchange_plans(self, cr, uid, ids, plans, context=None):
    #     result = {'value': {}}
    #     total = 0
    #     count = 0
    #     if plans:
    #         if plans.count('-') > 1:
    #             raise osv.except_osv(_('Erreur !'), _('Format Incorrecte!, un seul tiret est autorisé!'))
    #         elif plans.count('-') == 1 and plans.count(';') == 0:
    #             ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%plans.split('-')[0])
    #             tt = self.pool.get('risk.management.response.category').search(cr, uid,
    #                                                                            ([('plan', '=', (plans.split('-')[0]))]))
    #             tt1 = self.pool.get('risk.management.response.category').search(cr, uid, (
    #                 [('plan', '=', (plans.split('-')[1]))]))
    #             if not tt:
    #                 raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #             else:
    #                 t1 = tt[0]
    #             if not tt1:
    #                 raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #             else:
    #                 t2 = tt1[0]
    #             for x in range(t1, t2):
    #                 plan = self.pool.get('risk.management.response.category').browse(cr, uid, x, context=context)
    #                 if plan:
    #                     total = total + plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
    #         elif plans.count('-') == 1 and plans.count(';') > 0:
    #             tt = self.pool.get('risk.management.response.category').search(cr, uid, (
    #                 [('plan', '=', ((plans.split(';')[0]).split('-')[0]))]))
    #             tt1 = self.pool.get('risk.management.response.category').search(cr, uid, (
    #                 [('plan', '=', (plans.split(';')[0]).split('-')[1])]))
    #             if not tt:
    #                 raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #             else:
    #                 t1 = tt[0]
    #             if not tt1:
    #                 raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #             else:
    #                 t2 = tt1[0]
    #             for x in range(t1, t2):
    #
    #                 plan = self.pool.get('risk.management.response.category').browse(cr, uid, x, context=context)
    #                 if plan:
    #                     total = total + plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
    #                 list = (plans.split(';')[1]).split(';')
    #                 for kk in list:
    #                     tt2 = self.pool.get('risk.management.response.category').search(cr, uid, ([('plan', '=', kk)]))
    #                     if not tt2:
    #                         raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #                     else:
    #                         plan = self.pool.get('risk.management.response.category').browse(cr, uid, tt2[0],
    #                                                                                          context=context)
    #                     if plan:
    #                         total = total + plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
    #         elif plans.count('-') == 0 and plans.count(';') > 0:
    #             list = (plans.split(';'))
    #             for kk in list:
    #                 for kk in list:
    #                     tt2 = self.pool.get('risk.management.response.category').search(cr, uid, ([('plan', '=', kk)]))
    #                     if not tt2:
    #                         raise osv.except_osv(_('Erreur !'), _('Element n"est pas dans le tableau de relevé!'))
    #                     else:
    #                         plan = self.pool.get('risk.management.response.category').browse(cr, uid, tt2[0],
    #                                                                                          context=context)
    #                     if plan:
    #                         total = total + plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
    #         else:
    #             raise osv.except_osv(_('Erreur !'),
    #                                  _('Format Incorrecte!, seuls les tirets "-" ou les points virgules ";" sont autorisés!'))
    #
    #     ##result['value']['plans'] =plan1.name+'-'+plan2.name
    #     result['value']['poteau_t'] = total / 1000
    #     return result


class EbMergeFactures(models.Model):
    _name = 'base.facture.wizard'
    _description = 'Merge factures'
    _rec_name = 'name'

    # @api.model
    # def default_get(self, fields):
    #     res = super(EbMergeFactures, self).default_get(fields)
    #     active_ids = self.env.context.get('active_ids')
    #     project_list = []
    #     if active_ids:
    #         res['work_ids'] = active_ids
    #         for jj in active_ids:
    #             work = self.env['project.task.work.line'].browse(jj)
    #             project_list.append(work.project_id.id)
    #             res.update({'partner_id': work.partner_id.id, 'project_id': work.project_id.id})
    #         list_wo_no_duplicate = list(set(project_list))
    #         res.update({'partner_id': work.work_id.task_id.partner_id.id, 'project_ids': list_wo_no_duplicate})
    #     return res

    @api.depends('line_ids.total')
    def _compute_amount(self):

        tvq_ = self.env['account.tax'].browse(7)
        tps_ = self.env['account.tax'].browse(8)
        self.amount_untaxed = sum(line.total for line in self.line_ids)
        self.tvq = self.amount_untaxed * tvq_.amount
        self.tps = self.amount_untaxed * tps_.amount
        self.amount_total = self.amount_untaxed + self.tvq + self.tps

    def _compute_progress_gauge(self):
        this = self.browse(self.ids[0])
        data = 0
        total_profitabilite = 0
        for line in this.project_profitability:
            if line and this.line_ids:
                if this.amount_untaxed > 0:
                    total_profitabilite += line.total_depenses
                    data = ((this.amount_untaxed - total_profitabilite) / this.amount_untaxed) * 100
                else:
                    data = 0
                    break
        this.taux_gain = data
        return data

    project_id = fields.Many2one('project.project', string='Wizard')
    project_ids = fields.Many2many('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    date_from = fields.Date(string='Wizard', select=True, default=time.strftime('%Y-01-01'))
    date_to = fields.Date(string='Wizard', select=True, default=datetime.today())
    date_inv = fields.Date(string='Wizard', select=True, default=datetime.today())
    partner_id = fields.Many2one('res.partner', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    categ_id = fields.Many2one('product.category', string='Wizard')
    product_id = fields.Many2one('product.product', string='Wizard')
    choix = fields.Selection([
        ('1', 'Première Subdivision'),
        ('2', 'Deuxième Subdivision')
    ], string='Priority', select=True)
    type = fields.Selection([
        ('1', 'Nouvelle Subdivision'),
        ('2', 'Modification Subdivision Existante'),
        ('3', 'Ajouter Subdivision A Partir d"une Existante')
    ], string='Type', select=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('open', 'Validé')

    ], string='Priority', default='draft', select=True)
    week_no = fields.Selection([
        ('00', '00'),
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
        ('52', '52')], string='Priority', select=True, default=str(time.strftime('%W')))
    exist = fields.Boolean('Ids', default=True)
    clos = fields.Boolean('Ids', default=False)
    year_no = fields.Char(string='Priority', default='N/A')
    name = fields.Char(string='Priority', default='Génération Facture')
    num = fields.Char(string='Priority')
    note = fields.Char(string='Priority')
    task_ids = fields.Many2many('project.task', string='Tasks')  # 'merge_tasks_rel', 'merge_id', 'task_id',)
    work_ids = fields.Many2many('project.task.work.line', string='Tasks')  # 'merge_tasks_rel', 'merge_id', 'task_id',)
    user_id = fields.Many2one('res.users', 'Assigned to', index=True)
    dst_task_id = fields.Many2one('project.task', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")
    zone = fields.Integer(string="zone", default=99)
    secteur = fields.Integer(string="secteur", default=99)
    line_ids = fields.One2many('base.facture.merge.line', 'wizard_id', string=u"Role lines", copy=True)
    keep = fields.Selection([
        ('active', 'Actives'),
        ('inactive', 'Archivées'),
        ('both', 'Actives et Archivées')
    ], string='keep', default='active', select=True)
    tps = fields.Float(string='Journal Entry', readonly=True,
                       states={'draft': [('readonly', False)]}, copy=False)
    tvq = fields.Float(string='Journal Entry', readonly=True,
                       states={'draft': [('readonly', False)]}, copy=False)
    amount_untaxed = fields.Float(string='Subtotal', store=True, readonly=True,
                                  compute='_compute_amount', track_visibility='always')
    # digits = dp.get_precision('Account'),
    amount_total = fields.Float(string='Total', store=True, readonly=True, compute='_compute_amount')
    # digits = dp.get_precision('Account'),
    project_profitability = fields.One2many('project.profitability', 'invoice_id', string='Project profitability')
    progress_gauge = fields.Float(compute='_compute_progress_gauge', string='%', readonly=True, )
    taux_gain = fields.Float(compute='_compute_progress_gauge', string='% Taux Gain', readonly=True, )
    progress_gauge_total = fields.Float(string='%', readonly=True, )

    def rentabilite_projet(self):
        this = self.browse(self.ids[0])
        self.env.cr.execute("delete from project_profitability")
        for rec_project in this.project_ids.ids:
            self.env.cr.execute("INSERT INTO project_profitability (project_id,invoice_id) VALUES (%s,%s)",
                                ((tuple([rec_project])), self.ids[0]))
        line_work_ids = self.env['base.facture.wizard']
        work_line = self.env['project.task.work.line']
        for line in this.work_ids:
            work_line.write(line.id, {'rentability': 0, 'taux_horaire': 0})
        for line in this.project_profitability:
            tarif_client = 0
            total_dep2 = 0
            update = False
            for kk in this:
                for rec in this.work_ids:
                    wage = 0
                    exist = 0
                    if rec.project_id.id == line.project_id.id:
                        employee_obj = self.env['hr.employee']
                        academic_obj = self.env['hr.academic']
                        roles_obj = self.env['res.users.role']
                        empl = employee_obj.browse(rec.employee_id.id)
                        aca = academic_obj.search([('employee_id', '=', empl.id)])
                        if rec.group_id:
                            bon_id = self.env['bon.show'].browse(rec.group_id.id)
                            for line in bon_id.line_ids2:
                                if rec.product_id.id == line.product_id.id and rec.project_id.id == line.project_id.id and rec.date_start_r == line.date_start_r:
                                    wage = line.wage
                                    total_dep = line.amount_line
                                    total_dep2 += line.amount_line
                                    work_line.write(rec.id, {'rentability': total_dep, 'taux_horaire': wage})
                                    break
                        elif aca:
                            for list in aca:
                                if list:
                                    ligne = academic_obj.browse(list)
                                    if ligne.curr_ids:
                                        for ll in ligne.curr_ids:
                                            if ligne.project_id and ll.project_id.id == ligne.project_id.id:
                                                if ll.product_id and ll.uom_id:
                                                    if datetime.strptime(ll.start_date,
                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                        rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                        ll.end_date, "%Y-%m-%d"):
                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                            wage = ll.amount
                                                            total_dep = wage * rec.hours_r
                                                            total_dep2 += wage * rec.hours_r
                                                        else:
                                                            wage = ll.amount
                                                            total_dep = wage * rec.poteau_r
                                                            total_dep2 += wage * rec.poteau_r
                                                        work_line.write(rec.id, {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                        break
                                                    elif ll.product_id and ll.uom_id2:
                                                        if ll.product_id.id == rec.product_id.id:
                                                            if datetime.strptime(ll.start_date,
                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                                ll.end_date, "%Y-%m-%d"):
                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.hours_r
                                                                    total_dep2 += wage * rec.hours_r
                                                                else:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.poteau_r
                                                                    total_dep2 += wage * rec.poteau_r
                                                                work_line.write(rec.id,
                                                                                {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                                break
                                                elif ll.product_id and ll.uom_id2:
                                                    if ll.product_id.id == rec.product_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                                elif ll.categ_id and ll.uom_id:
                                                    if ll.categ_id.id == rec.categ_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                                    elif ll.categ_id and ll.uom_id2:
                                                        if ll.categ_id.id == rec.categ_id.id:
                                                            if datetime.strptime(ll.start_date,
                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                                ll.end_date, "%Y-%m-%d"):
                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.hours_r
                                                                    total_dep2 += wage * rec.hours_r
                                                                else:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.poteau_r
                                                                    total_dep2 += wage * rec.poteau_r
                                                                work_line.write(rec.id,
                                                                                {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                                break
                                                elif ll.categ_id and ll.uom_id2:
                                                    if ll.categ_id.id == rec.categ_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                    if ligne.curr_ids:
                                        for ll in ligne.curr_ids:
                                            if ll.partner_id.id == ligne.partner_id.id:
                                                if ll.product_id and ll.uom_id:
                                                    if ll.product_id.id == rec.product_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                wage = ll.amount
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                wage = ll.amount
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                                    elif ll.product_id and ll.uom_id2:
                                                        if ll.product_id.id == rec.product_id.id:
                                                            if datetime.strptime(ll.start_date,
                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                                ll.end_date, "%Y-%m-%d"):
                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.hours_r
                                                                    total_dep2 += wage * rec.hours_r
                                                                else:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.poteau_r
                                                                    total_dep2 += wage * rec.poteau_r
                                                                work_line.write(rec.id,
                                                                                {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                                break
                                                elif ll.product_id and ll.uom_id2:
                                                    if ll.product_id.id == rec.product_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                                elif ll.categ_id and ll.uom_id:
                                                    if ll.categ_id.id == rec.categ_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                wage = ll.amount
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                wage = ll.amount
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                                    elif ll.categ_id and ll.uom_id2:
                                                        if ll.categ_id.id == rec.categ_id.id:
                                                            if datetime.strptime(ll.start_date,
                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                                ll.end_date, "%Y-%m-%d"):
                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.hours_r
                                                                    total_dep2 += wage * rec.hours_r
                                                                else:
                                                                    exist += 1
                                                                    wage = ll.amount2
                                                                    total_dep = wage * rec.poteau_r
                                                                    total_dep2 += wage * rec.poteau_r
                                                                work_line.write(rec.id,
                                                                                {'rentability': total_dep,
                                                                                 'taux_horaire': wage})

                                                                break

                                                elif ll.categ_id and ll.uom_id2:
                                                    if ll.categ_id.id == rec.categ_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                        continue
                                    if ligne.curr_ids:
                                        for ll in ligne.curr_ids:
                                            if ll.product_id and ll.uom_id:
                                                if ll.product_id.id == rec.product_id.id:
                                                    if datetime.strptime(ll.start_date,
                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                        rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                        ll.end_date, "%Y-%m-%d"):
                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                            wage = ll.amount
                                                            total_dep = wage * rec.hours_r
                                                            total_dep2 += wage * rec.hours_r
                                                        else:
                                                            exist += 1
                                                            wage = ll.amount
                                                            total_dep = wage * rec.poteau_r
                                                            total_dep2 += wage * rec.poteau_r
                                                        work_line.write(rec.id, {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                        break
                                                elif ll.product_id and ll.uom_id2:
                                                    if ll.product_id.id == rec.product_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})
                                                            break
                                            elif ll.product_id and ll.uom_id2:
                                                if ll.product_id.id == rec.product_id.id:
                                                    if datetime.strptime(ll.start_date,
                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                        rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                        ll.end_date, "%Y-%m-%d"):
                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                            exist += 1
                                                            wage = ll.amount2
                                                            total_dep = wage * rec.hours_r
                                                            total_dep2 += wage * rec.hours_r
                                                        else:
                                                            exist += 1
                                                            wage = ll.amount2
                                                            total_dep = wage * rec.poteau_r
                                                            total_dep2 += wage * rec.poteau_r
                                                        work_line.write(rec.id, {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                        break
                                            elif ll.categ_id and ll.uom_id:
                                                if ll.categ_id.id == rec.categ_id.id:
                                                    if datetime.strptime(ll.start_date,
                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                        rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                        ll.end_date, "%Y-%m-%d"):
                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                            exist += 1
                                                            wage = ll.amount
                                                            total_dep = wage * rec.hours_r
                                                            total_dep2 += wage * rec.hours_r
                                                        else:
                                                            exist += 1
                                                            wage = ll.amount
                                                            total_dep = wage * rec.poteau_r
                                                            total_dep2 += wage * rec.poteau_r
                                                        work_line.write(rec.id, {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                        break
                                                elif ll.categ_id and ll.uom_id2:
                                                    if ll.categ_id.id == rec.categ_id.id:
                                                        if datetime.strptime(ll.start_date,
                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                            rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                            ll.end_date, "%Y-%m-%d"):
                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.hours_r
                                                                total_dep2 += wage * rec.hours_r
                                                            else:
                                                                exist += 1
                                                                wage = ll.amount2
                                                                total_dep = wage * rec.poteau_r
                                                                total_dep2 += wage * rec.poteau_r
                                                            work_line.write(rec.id, {'rentability': total_dep,
                                                                                     'taux_horaire': wage})

                                                            break

                                            elif ll.categ_id and ll.uom_id2:
                                                if ll.categ_id.id == rec.categ_id.id:
                                                    if datetime.strptime(ll.start_date,
                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                        rec.date_start_r, "%Y-%m-%d") <= datetime.strptime(
                                                        ll.end_date, "%Y-%m-%d"):
                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                            exist += 1
                                                            wage = ll.amount2
                                                            total_dep = wage * rec.hours_r
                                                            total_dep2 += wage * rec.hours_r
                                                        else:
                                                            exist += 1
                                                            wage = ll.amount2
                                                            total_dep = wage * rec.poteau_r
                                                            total_dep2 += wage * rec.poteau_r
                                                        work_line.write(rec.id, {'rentability': total_dep,
                                                                                 'taux_horaire': wage})
                                                    break

                            if wage == 0:
                                roles = roles_obj.search([])
                                for gp in roles:
                                    ro = roles_obj.browse(gp)
                                    if rec.employee_id.id in ro.employee_ids.ids:
                                        aca = academic_obj.search([('role_id', '=', ro.id)])
                                        if aca:
                                            for list in aca:
                                                if list:
                                                    ligne = academic_obj.browse(list)
                                                    if ligne.curr_ids:
                                                        for ll in ligne.curr_ids:
                                                            if ligne.project_id and ll.project_id.id == ligne.project_id.id:
                                                                if ll.product_id and ll.uom_id:
                                                                    if ll.product_id.id == rec.product_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep2 += wage * rec.hours_r
                                                                                total_dep = wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})
                                                                            break
                                                                    elif ll.product_id and ll.uom_id2:
                                                                        if ll.product_id.id == rec.product_id.id:
                                                                            if datetime.strptime(ll.start_date,
                                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                                rec.date_start_r,
                                                                                "%Y-%m-%d") <= datetime.strptime(
                                                                                ll.end_date, "%Y-%m-%d"):
                                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.hours_r
                                                                                    total_dep2 += wage * rec.hours_r
                                                                                else:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.poteau_r
                                                                                    total_dep2 += wage * rec.poteau_r
                                                                                work_line.write(rec.id,
                                                                                                {
                                                                                                    'rentability': total_dep,
                                                                                                    'taux_horaire': wage})

                                                                                break

                                                                elif ll.product_id and ll.uom_id2:
                                                                    if ll.product_id.id == rec.product_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                                elif ll.categ_id and ll.uom_id:
                                                                    if ll.categ_id.id == rec.categ_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = 0
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                                    elif ll.categ_id and ll.uom_id2:
                                                                        if ll.categ_id.id == this.categ_id.id:
                                                                            if datetime.strptime(ll.start_date,
                                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                                rec.date_start_r,
                                                                                "%Y-%m-%d") <= datetime.strptime(
                                                                                ll.end_date, "%Y-%m-%d"):
                                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.hours_r
                                                                                    total_dep2 += wage * rec.hours_r
                                                                                else:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.poteau_r
                                                                                    total_dep2 += wage * rec.poteau_r
                                                                                work_line.write(rec.id,
                                                                                                {
                                                                                                    'rentability': total_dep,
                                                                                                    'taux_horaire': wage})

                                                                                break

                                                                elif ll.categ_id and ll.uom_id2:
                                                                    if ll.categ_id.id == rec.categ_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                    if ligne.curr_ids:
                                                        for ll in ligne.curr_ids:
                                                            if ligne.project_id is False and ll.partner_id.id == ligne.partner_id.id:
                                                                if ll.product_id and ll.uom_id:
                                                                    if ll.product_id.id == rec.product_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                                    elif ll.product_id and ll.uom_id2:
                                                                        if ll.product_id.id == rec.product_id.id:
                                                                            if datetime.strptime(ll.start_date,
                                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                                rec.date_start_r,
                                                                                "%Y-%m-%d") <= datetime.strptime(
                                                                                ll.end_date, "%Y-%m-%d"):
                                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.hours_r
                                                                                    total_dep2 += wage * rec.hours_r
                                                                                else:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.poteau_r
                                                                                    total_dep2 += wage * rec.poteau_r
                                                                                work_line.write(rec.id,
                                                                                                {
                                                                                                    'rentability': total_dep,
                                                                                                    'taux_horaire': wage})

                                                                                break

                                                                elif ll.product_id and ll.uom_id2:
                                                                    if ll.product_id.id == rec.product_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break

                                                                elif ll.categ_id and ll.uom_id:
                                                                    if ll.categ_id.id == rec.categ_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount
                                                                                total_dep = 0
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                                    elif ll.categ_id and ll.uom_id2:
                                                                        if ll.categ_id.id == rec.categ_id.id:
                                                                            if datetime.strptime(ll.start_date,
                                                                                                 "%Y-%m-%d") <= datetime.strptime(
                                                                                rec.date_start_r,
                                                                                "%Y-%m-%d") <= datetime.strptime(
                                                                                ll.end_date, "%Y-%m-%d"):
                                                                                if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.hours_r
                                                                                    total_dep2 += wage * rec.hours_r
                                                                                else:
                                                                                    exist += 1
                                                                                    wage = ll.amount2
                                                                                    total_dep = wage * rec.poteau_r
                                                                                    total_dep2 += wage * rec.poteau_r
                                                                                work_line.write(rec.id,
                                                                                                {
                                                                                                    'rentability': total_dep,
                                                                                                    'taux_horaire': wage})

                                                                                break

                                                                elif ll.categ_id and ll.uom_id2:
                                                                    if ll.categ_id.id == rec.categ_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                    if ligne.curr_ids:
                                                        for ll in ligne.curr_ids:
                                                            if ll.product_id and ll.uom_id:
                                                                if ll.product_id.id == rec.product_id.id:
                                                                    if datetime.strptime(ll.start_date,
                                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                                        rec.date_start_r,
                                                                        "%Y-%m-%d") <= datetime.strptime(
                                                                        ll.end_date, "%Y-%m-%d"):
                                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                            exist += 1
                                                                            wage = ll.amount
                                                                            total_dep = wage * rec.hours_r
                                                                            total_dep2 += wage * rec.hours_r
                                                                        else:
                                                                            exist += 1
                                                                            wage = ll.amount
                                                                            total_dep = wage * rec.poteau_r
                                                                            total_dep2 += wage * rec.poteau_r
                                                                        work_line.write(rec.id,
                                                                                        {'rentability': total_dep,
                                                                                         'taux_horaire': wage})
                                                                        break
                                                                elif ll.product_id and ll.uom_id2:
                                                                    if ll.product_id.id == rec.product_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.hours_r
                                                                                total_dep2 += wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep = wage * rec.poteau_r
                                                                                total_dep2 += wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})

                                                                            break
                                                            elif ll.product_id and ll.uom_id2:
                                                                if ll.product_id.id == rec.product_id.id:
                                                                    if datetime.strptime(ll.start_date,
                                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                                        rec.date_start_r,
                                                                        "%Y-%m-%d") <= datetime.strptime(
                                                                        ll.end_date, "%Y-%m-%d"):
                                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                            exist += 1
                                                                            wage = ll.amount2
                                                                            total_dep = wage * rec.hours_r
                                                                            total_dep2 += wage * rec.hours_r
                                                                        else:
                                                                            exist += 1
                                                                            wage = ll.amount2
                                                                            total_dep = wage * rec.poteau_r
                                                                            total_dep2 += wage * rec.poteau_r
                                                                        work_line.write(rec.id,
                                                                                        {'rentability': total_dep,
                                                                                         'taux_horaire': wage})
                                                                        break
                                                            elif ll.categ_id and ll.uom_id:
                                                                if ll.categ_id.id == rec.categ_id.id:
                                                                    if datetime.strptime(ll.start_date,
                                                                                         "%Y-%m-%d") <= datetime.strptime(
                                                                        rec.date_start_r,
                                                                        "%Y-%m-%d") <= datetime.strptime(
                                                                        ll.end_date, "%Y-%m-%d"):
                                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                            exist += 1
                                                                            wage = ll.amount
                                                                            total_dep = wage * rec.hours_r
                                                                            total_dep2 += wage * rec.hours_r
                                                                        else:
                                                                            exist += 1
                                                                            wage = ll.amount
                                                                            total_dep = 0
                                                                        work_line.write(rec.id,
                                                                                        {'rentability': total_dep,
                                                                                         'taux_horaire': wage})
                                                                        break

                                                                elif ll.categ_id and ll.uom_id2:

                                                                    if ll.categ_id.id == rec.categ_id.id:
                                                                        if datetime.strptime(ll.start_date,
                                                                                             "%Y-%m-%d") <= datetime.strptime(
                                                                            rec.date_start_r,
                                                                            "%Y-%m-%d") <= datetime.strptime(
                                                                            ll.end_date, "%Y-%m-%d"):
                                                                            if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep2 += wage * rec.hours_r
                                                                                total_dep = wage * rec.hours_r
                                                                            else:
                                                                                exist += 1
                                                                                wage = ll.amount2
                                                                                total_dep2 += wage * rec.poteau_r
                                                                                total_dep = wage * rec.poteau_r
                                                                            work_line.write(rec.id,
                                                                                            {'rentability': total_dep,
                                                                                             'taux_horaire': wage})
                                                                            break

                                                            elif ll.categ_id and ll.uom_id2:
                                                                if ll.categ_id.id == rec.categ_id.id:
                                                                    if str(ll.start_date) <= str(datetime.now()) <= str(
                                                                            ll.end_date):
                                                                        if empl.job_id.id == 1 or ll.uom_id.id == 5:
                                                                            exist += 1
                                                                            wage = ll.amount2
                                                                            total_dep2 += wage * rec.hours_r
                                                                            total_dep = wage * rec.hours_r
                                                                        else:
                                                                            exist += 1
                                                                            wage = ll.amount2
                                                                            total_dep = wage * rec.poteau_r
                                                                            total_dep2 += wage * rec.poteau_r
                                                                        work_line.write(rec.id,
                                                                                        {'rentability': total_dep,
                                                                                         'taux_horaire': wage})

                                                                        break
                        if wage == 0:
                            employee = employee_obj.search([('id', '=', empl.id)])
                            if employee:
                                for list in employee:
                                    if list:
                                        ligne_emp = employee_obj.browse(list)
                                        contract = self.env['hr.contract'].search([('employee_id', '=', list), (
                                            'trial_date_start', '<=',
                                            rec.date_start_r)],
                                                                                  order="id desc")
                                        if len(contract) > 1:
                                            raise UserError(
                                                _('Error !\nVous devez avoir un seul contrat valide pour Mr/Mme %s !') % ligne_emp.name)

                                        else:
                                            contract_valid = self.env['hr.contract'].browse(contract)
                                            if ligne_emp.job_id.id == 1 or rec.uom_id_r.id == 5:
                                                wage = contract_valid.wage
                                                total_dep2 += wage * rec.hours_r
                                                total_dep = wage * rec.hours_r
                                            else:
                                                wage = contract_valid.wage
                                                total_dep = wage * rec.poteau_r
                                                total_dep2 += wage * rec.poteau_r
                                            work_line.write(rec.id,
                                                            {'rentability': total_dep, 'taux_horaire': wage})
            if update == False and tarif_client == 0:
                self.env.cr.execute("""  UPDATE project_profitability
                                               SET total_depenses = %s,
                                                montant_total = %s,
                                                diference = %s,
                                                taux = %s
                                               WHERE project_id = %s AND invoice_id = %s
                                          """,
                                    (tuple([total_dep2]),
                                     tuple([tarif_client]), tuple([tarif_client - total_dep2]),
                                     tuple([0]), tuple([line.project_id.id]), self.ids[0]))
            elif update == False and tarif_client != 0:
                self.env.cr.execute("""  UPDATE project_profitability
                                                   SET total_depenses = %s,
                                                    montant_total = %s,
                                                    diference = %s,
                                                    taux = %s
                                                   WHERE project_id = %s AND invoice_id = %s
                                           """,
                                    (tuple([total_dep2]),
                                     tuple([tarif_client]), tuple([tarif_client - total_dep2]),
                                     tuple([((tarif_client - total_dep2) / tarif_client) * 100]),
                                     tuple([line.project_id.id]),
                                     self.ids[0]))
        if this.line_ids and this.amount_untaxed == 0:
            raise UserError(_('Error !\nVous ne pouvez pas diviser par 0 !!!'))

        else:
            return {
                'name': _("Création Facture"),
                'res_id': self.ids[0],
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'base.facture.wizard',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'context': {}
            }

    #
    #     def rentabilite_projet_total(self, cr, uid, ids, context=None):
    #         this = self.browse(cr, uid, ids[0], context=context)
    #         for project in this.project_ids.ids:
    #             exist = this.project_profitability_total.search([('project_id', '=', project)])
    #             if exist:
    #                 continue
    #             else:
    #                 cr.execute("INSERT INTO project_profitability_total (project_id,invoice_id) VALUES (%s,%s)",
    #                            (tuple([project]), ids[0],))
    #         cr.execute(
    #             "SELECT project_id FROM project_profitability_total WHERE project_id in %s and invoice_id=%s",
    #             (tuple(this.project_ids.ids), ids[0],)
    #         )
    #         test = cr.fetchall()
    #         # raise osv.except_osv(_('Error !'), _('%s') % test)
    #         for line in test:
    #             # raise osv.except_osv(_('Error !'), _('%s') % line)
    #             cr.execute(
    #                 "SELECT project_id, COALESCE(SUM(total_depenses), 0.0) FROM project_profitability WHERE project_id = %s GROUP BY "
    #                 "project_id",
    #                 tuple([line[0]]))
    #             total_dep = dict(cr.fetchall())
    #             cr.execute(
    #                 "SELECT project_id, COALESCE(SUM(montant_total), 0.0) FROM project_profitability WHERE project_id = %s GROUP BY "
    #                 "project_id",
    #                 tuple([line[0]]))
    #             montant_total = dict(cr.fetchall())
    #             # raise osv.except_osv(_('Error !'), _('%s') % montant_total)
    #             if montant_total == {} and total_dep == {}:
    #                 cr.execute("""  UPDATE project_profitability_total
    #                                       SET total_depenses = %s,
    #                                        montant_total = %s,
    #                                        diference = %s,
    #                                        taux = %s
    #                                       WHERE project_id = %s AND invoice_id = %s
    #                                  """,
    #                            (tuple([0]), tuple([0]), tuple([0]),
    #                             tuple([0]), tuple([line[0]]), ids[0]))
    #             elif montant_total == {} or montant_total[line[0]] == 0:
    #                 cr.execute("""  UPDATE project_profitability_total
    #                                       SET total_depenses = %s,
    #                                        montant_total = %s,
    #                                        diference = %s,
    #                                        taux = %s
    #                                       WHERE project_id = %s AND invoice_id = %s
    #                                  """,
    #                            (tuple([total_dep[line[0]]]), tuple([montant_total[line[0]]]),
    #                             tuple([-total_dep[line[0]]]),
    #                             tuple([0]), tuple([line[0]]), ids[0]))
    #             elif total_dep == {}:
    #                 cr.execute("""  UPDATE project_profitability_total
    #                                       SET total_depenses = %s,
    #                                        montant_total = %s,
    #                                        diference = %s,
    #                                        taux = %s
    #                                       WHERE project_id = %s AND invoice_id = %s
    #                                  """,
    #                            (tuple([0]), tuple([montant_total[line[0]]]),
    #                             tuple([montant_total[line[0]]]),
    #                             tuple([100]), tuple([line[0]]), ids[0]))
    #             else:
    #                 cr.execute("""  UPDATE project_profitability_total
    #                                      SET total_depenses = %s,
    #                                       montant_total = %s,
    #                                       diference = %s,
    #                                       taux = %s
    #                                      WHERE project_id = %s AND invoice_id = %s
    #                                 """,
    #                            (tuple([total_dep[line[0]]]), tuple([montant_total[line[0]]]),
    #                             tuple([montant_total[line[0]] - total_dep[line[0]]]),
    #                             tuple([((montant_total[line[0]] - total_dep[line[0]]) / montant_total[
    #                                 line[0]]) * 100]), tuple([line[0]]), ids[0]))
    #
    #         return {
    #             'name': _("Création Facture"),
    #             'res_id': ids[0],
    #             'view_mode': 'form',
    #             'view_id': False,
    #             'view_type': 'form',
    #             'res_model': 'base.facture.wizard',
    #             'type': 'ir.actions.act_window',
    #             'nodestroy': True,
    #             'target': 'current',
    #             'context': {}
    #         }
    #
    #     @api.multi
    #     def action_merge(self):
    #         names = []
    #         # write the name of the destination task because it will overwritten
    #         if self.dst_task_id:
    #             names.append(self.dst_task_id.name)
    #         else:
    #             raise Warning('You must select a Destination Task')
    #
    #         desc = []
    #         # also write the description of the destination task because it will be overwritten
    #         desc.append(self.dst_task_id.description)
    #         for id in self.task_ids:
    #             if id.id != self.dst_task_id.id:
    #                 for name in id:
    #                     names.append(name.name)
    #                     desc.append(name.description)
    #                 # append the names and desc to the empty lists
    #
    #         # transfering the messages from task_ids to dst_task_id
    #         for message in self.task_ids:
    #             for msg_id in message.message_ids:
    #                 msg_id.write({'res_id': self.dst_task_id.id})
    #
    #         # Check for planned hours and if any collect them all and place dst_task_id
    #         plan_hours = self.dst_task_id.planned_hours
    #         for hour in self.task_ids:
    #             for time in hour:
    #                 plan_hours += time.planned_hours
    #         # Write to dst_task_id full planned hours from all tasks
    #         self.dst_task_id.write({'planned_hours': plan_hours})
    #
    #         # actual writing to the tasks
    #         transformed_names = ', '.join([unicode(i) for i in names])
    #         self.dst_task_id.write({'name': transformed_names})
    #
    #         # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), names)
    #
    #         transformed_desc = ', '.join([unicode(i) for i in desc])
    #         self.dst_task_id.write({'description': transformed_desc})
    #
    #         # mapping with lambda prints with BRACKETS []  ---> map(lambda x: x.encode('ascii'), desc)
    #         # Posting a note in the merged and archived tasks
    #         ###################################################################
    #         # get the base url from ir.config_parameter
    #         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         # loop all active tasks
    #         for task in self.task_ids:
    #             # post the link to every task
    #             task.message_post(
    #                 body="This task has been merged into: " '%s/#id=%s&amp;view_type=form&amp;model=project.task' % (
    #                     base_url, self.dst_task_id.id))
    #
    #         self.task_ids.write({'active': False})
    #         # explicitly write the dst_task_id TRUE for ACTIVE for security reasons
    #
    #         self.dst_task_id.write({'active': True})
    #
    #         # Check if user has been assigned and if not raise error
    #
    #         if self.user_id.id:
    #             # write the Assiged TO user_id
    #             self.dst_task_id.write({'user_id': self.user_id.id})
    #         elif self.dst_task_id.user_id.id:
    #             self.dst_task_id.write({'user_id': self.dst_task_id.user_id.id})
    #         else:
    #             # raise UserError(_("There is no user assigned to the merged task, and the destination task doesn't have assigned user too!!!"))
    #             raise Warning(
    #                 'There is no user assigned to the merged task, and the destination task doesn''t have assigned user too!!!')
    #
    #         return True
    #
    #     @api.onchange('poteau_t', 'price')
    #     def onchange_categ_id(self):
    #         raise Warning(
    #             'There is no user assigned to the merged task, and the destination task doesn''t have assigned user too!!!')
    #         return True
    #
    #     @api.onchange('clos')
    #     def onchange_clos(self):
    #         for record in self:
    #             if record.clos is True:
    #                 raise Warning('Attention, Vous aller cloturer le projet d"une façon définitive!!!')
    #
    def button_save_(self):

        sum1 = 0
        tvq_ = self.env['account.tax'].browse(7)
        tps_ = self.env['account.tax'].browse(8)
        for current in self:
            for tt in current.line_ids:
                sum1 = sum1 + tt.total

        self.write({'amount_untaxed': sum1, 'tps': tps_.amount * sum1, 'tvq': tvq_.amount * sum1})
        return True

    def merge_lines(self):
        to_delete = []
        itered = []
        for line in self.line_ids:
            itered.append(line.id)
            line_to_merge = self.line_ids.search([('wizard_id', '=', self.id),

                                                  ('code', '=', line.code),
                                                  ('uom_id', '=', line.uom_id.id),
                                                  ('id', 'not in', itered)], limit=1)
            if line_to_merge:
                to_delete.append(line.id)
                line_to_merge.write({'poteau_t': line_to_merge.poteau_t + line.poteau_t})
        self.write({'line_ids': [(2, x, 0) for x in to_delete]})

    #     @api.multi
    #     def button_merge(self):
    #
    #         product_list = []
    #         for obj in self.line_ids:
    #             if obj[2]:
    #                 if "product_id" in obj[2]:
    #                     if obj[2]['product_id'] not in product_list:
    #                         product_list.append(obj[2]['product_id'])
    #                     list_new = self.line_ids
    #                     new_list = []
    #                     for obj in product_list:
    #                         count = 0
    #                         qty = 0
    #                         for ele in list_new:
    #                             if obj == ele[2]['product_id']:
    #                                 count += 1
    #                                 qty += ele[2]['poteau_t']
    #                                 if count == 1:
    #                                     new_list.append(ele)
    #                         for att in new_list:
    #                             if obj == att[2]['product_id']:
    #                                 att[2]['poteau_t'] = qty
    #                     vals['line_ids'] = new_list
    #
    #         return res
    #
    def button_accept1(self):

        if self.work_ids:
            for zz in self.work_ids.ids:
                kk = self.env['project.task.work.line'].browse(zz)
                if kk.auto is False:
                    self.env.cr.execute(
                        'select id from agreement_fees where partner_id= %s and date_init<=%s and date_end>=%s',
                        (self.partner_id.id, self.date_inv, self.date_inv,))
                    oo = self.env.cr.fetchone()
                    if oo:
                        for ll in self.env['agreement.fees'].browse(oo[0]).line_ids:
                            for nn in ll.ids:
                                tt = self.env['agreement.fees.amortization_line'].browse(nn)
                                sequence = 0
                                for product in tt.product_ids1.ids:
                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })
                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))

                                    sequence = 1
                                for product in tt.product_ids2.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })

                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))
                                    sequence = 1
                                for product in tt.product_ids7.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })

                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))
                                    sequence = 1
                                for product in tt.product_ids3.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })

                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))
                                    sequence = 1
                                for product in tt.product_ids4.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })

                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))
                                    sequence = 1
                                for product in tt.product_ids5.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })
                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))
                                    sequence = 1
                                for product in tt.product_ids6.ids:

                                    jj = self.env['product.product'].browse(product)
                                    if jj.id == kk.product_id.id:
                                        if kk.uom_id.id == 5:
                                            qty = kk.hours_r
                                        else:
                                            qty = kk.hours_r
                                        self.env['base.facture.merge.line'].create({
                                            'wizard_id': self.id,
                                            'poteau_t': qty,
                                            'code': tt.name,
                                            'name': tt.desc,
                                            'uom_id': tt.uom_id.id,
                                            'partner_id': self.partner_id.id,

                                            'product_id': jj.id,
                                            'categ_id': jj.categ_id.id,
                                            'qte': qty,
                                            'price': tt.amount_total,
                                            'total': qty * tt.amount_total,

                                        })

                                        self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                            (kk.id,))

                                    sequence = 1
                                if sequence == 0:
                                    if kk.uom_id.id == 5:
                                        qty = kk.hours_r
                                    else:
                                        qty = kk.hours_r
                                    self.env['base.facture.merge.line'].create({
                                        'wizard_id': self.id,
                                        'poteau_t': qty,
                                        'code': tt.name,
                                        'name': tt.desc,
                                        'uom_id': tt.uom_id.id,
                                        'partner_id': self.partner_id.id,

                                        'product_id': kk.product_id.id,
                                        'categ_id': kk.product_id.categ_id.id,
                                        'qte': qty,
                                        'price': tt.amount_total,
                                        'total': qty * tt.amount_total,

                                    })
                                    self.env.cr.execute('update project_task_work_line set auto=True where id= %s ',
                                                        (kk.id,))
                    else:
                        raise UserError(_('Info !\nPas de contrat lié au projet !'))

        return True

    #     def onchange_week_(self, cr, uid, ids, year_no, week_no, context=None):
    #         result = {'value': {}}
    #
    #         d = date(int(year_no), 1, 1)
    #         if (d.weekday() <= 3):
    #             d = d - dt.timedelta(d.weekday())
    #         else:
    #             d = d + dt.timedelta(7 - d.weekday())
    #         dlt = dt.timedelta(days=(int(week_no) - 1) * 7)
    #
    #         result['value']['date_from'] = d + dlt
    #         result['value']['date_to'] = d + dlt + dt.timedelta(days=6)
    #         return result
    #
    #     def onchange_project_id(self, cr, uid, ids, project_id, context=None):
    #         result = {'value': {}}
    #
    #         d = date(int(year_no), 1, 1)
    #         if project_id:
    #             result['value']['task_ids'] = False
    #             result['value']['work_ids'] = False
    #         return result
    #
    #     def onchange_exist(self, cr, uid, ids, exist, context=None):
    #         if exist is False:
    #             raise osv.except_osv(_('Attention!'),
    #                                  _("Si vous décochez cette option, le systeme ne vérifiera pas l'existance du Projet-Zone-Secteur!"))
    #         return True
    #
    #     @api.multi
    #     def action_copy1(self, default=None):
    #
    #         return super(project_task, self).copy(vals)
    #
    #     def action_copy(self, cr, uid, ids, default=None, context=None):
    #
    #         # your changes
    #         if default is None:
    #             default = {}
    #         for current in self.browse(cr, uid, ids, context=context):
    #             for tt in current.work_ids.ids:
    #                 self.pool.get('project.task.work.line').write(cr, uid, tt,
    #                                                               {'date_inv': current.date_inv, 'num': current.num,
    #                                                                'facture': True}, context=context)
    #         return True
    #
    #     def show_results(self, cr, uid, ids, context=None):
    #
    #         """
    #         Action that shows the list of (non-draft) account moves from
    #         the selected journals and periods, so the user can review
    #         the renumbered account moves.
    #         """
    #
    #         current = self.browse(cr, uid, ids[0], context=context)
    #         cr.execute("delete from base_group_merge_line2 where wiz_id=%s", (current.id,))
    #         res_cpt = []
    #         list = []
    #         if current.project_id:
    #             if not current.task_ids:
    #                 raise osv.except_osv(_('Action impossible!'), _("Vous devez sélectionner les étapes concernées!"))
    #             if not current.line_ids:
    #                 raise osv.except_osv(_('Action impossible!'), _("Vous devez Mentionner les Zones et Secteurs!"))
    #             l = []
    #             for tt in current.task_ids.ids:
    #                 this_p = self.pool.get('project.task').browse(cr, uid, tt, context=context)
    #                 l.append(this_p.name)
    #             cr.execute('select id from project_task_work where project_id= %s and state in %s and etape in %s',
    #                        (current.project_id.id, ('draft', 'affect'), tuple(l)))
    #             ll = cr.fetchall()
    #             for nn in current.work_ids.ids:
    #                 wrk = self.pool.get('project.task.work').browse(cr, uid, nn, context=context)
    #                 res_cpt.append(wrk.id)
    #
    #             pp = set(ll).intersection(res_cpt)
    #             for kk in res_cpt:
    #                 if kk:
    #                     s2 = self.pool.get('project.task.work').browse(cr, uid, kk, context=context)
    #                     sequence_w = 0
    #                     if s2.task_id:
    #                         cr.execute(
    #                             'select sequence from project_task_work where task_id=%s and sequence is not Null order by sequence desc limit 1',
    #                             (s2.task_id.id,))
    #                         res = cr.fetchone()
    #                     for jj in current.line_ids:
    #                         if jj.secteur > jj.secteur_to:
    #                             raise osv.except_osv(_('Action impossible!'),
    #                                                  _("Le secteur de départ doit etre plus petit que le secteur de fin!"))
    #                     for jj in current.line_ids:
    #
    #                         if jj.zone == 0 and jj.secteur > 0:
    #                             for hh in range(jj.secteur, jj.secteur_to + 1):
    #                                 ##sequence_w=sequence_w+1
    #                                 if jj.employee_id:
    #                                     employee = jj.employee_id.id
    #                                 else:
    #                                     employee = s2.employee_id.id or False
    #                                 if jj.date_from:
    #                                     date_from = jj.date_from
    #                                 else:
    #                                     date_from = s2.date_start
    #                                 if jj.date_to:
    #                                     date_to = jj.date_to
    #                                 else:
    #                                     date_to = s2.date_end
    #                                 if jj.poteau_t:
    #                                     poteau_t = jj.poteau_t
    #                                 else:
    #                                     poteau_t = s2.poteau_t
    #                                 if jj.is_display is True:
    #                                     is_display = True
    #                                 else:
    #                                     is_display = False
    #                                 self.pool.get('base.group.merge.line2').create(cr, uid, {
    #                                     'task_id': s2.task_id.id,
    #                                     'categ_id': s2.categ_id.id,
    #                                     'product_id': s2.product_id.id,
    #                                     'name': s2.name + ' - Secteur ' + str(hh),
    #                                     'date_start': date_from,
    #                                     'date_end': date_to,
    #                                     'poteau_i': s2.poteau_t,
    #                                     'poteau_t': poteau_t,
    #                                     'color': s2.color,
    #                                     'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                     'project_id': s2.project_id.id,
    #                                     'etape': s2.etape,
    #                                     'bon_id': current.id,
    #                                     'gest_id': s2.gest_id.id or False,
    #                                     'employee_id': employee,
    #                                     'uom_id': s2.uom_id.id,
    #                                     'uom_id_r': s2.uom_id.id,
    #                                     'ftp': s2.ftp,
    #                                     'state': s2.state,
    #                                     'work_id': s2.id,
    #                                     'sequence': res[0] + 1,
    #                                     'zone': 0,
    #                                     'zo': str(jj.zone),
    #                                     'secteur': hh,
    #                                     'wiz_id': current.id,
    #                                     'is_display': is_display
    #
    #                                 }, context=context)
    #                         elif jj.zone > 0 and jj.secteur > 0:
    #                             for hh in range(jj.zone, jj.zone + 1):
    #                                 for vv in range(jj.secteur, jj.secteur_to + 1):
    #                                     if jj.employee_id:
    #                                         employee = jj.employee_id.id
    #                                     else:
    #                                         employee = s2.employee_id.id or False
    #                                     if jj.date_from:
    #                                         date_from = jj.date_from
    #                                     else:
    #                                         date_from = s2.date_start
    #                                     if jj.date_to:
    #                                         date_to = jj.date_to
    #                                     else:
    #                                         date_to = s2.date_end
    #                                     if jj.poteau_t:
    #                                         poteau_t = jj.poteau_t
    #                                     else:
    #                                         poteau_t = s2.poteau_t
    #                                     if jj.is_display is True:
    #                                         is_display = True
    #                                     else:
    #                                         is_display = False
    #                                     sequence_w = sequence_w + 1
    #                                     self.pool.get('base.group.merge.line2').create(cr, uid, {
    #                                         'task_id': s2.task_id.id,
    #                                         'categ_id': s2.categ_id.id,
    #                                         'product_id': s2.product_id.id,
    #                                         'name': s2.name + ' - Zone ' + str(hh) + ' - Secteur ' + str(vv),
    #                                         'date_start': date_from,
    #                                         'date_end': date_to,
    #                                         'poteau_i': s2.poteau_t,
    #                                         'poteau_t': poteau_t,
    #                                         'color': s2.color,
    #                                         'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                         'project_id': s2.project_id.id,
    #                                         'bon_id': current.id,
    #                                         'gest_id': s2.gest_id.id or False,
    #                                         'employee_id': employee,
    #                                         'uom_id': s2.uom_id.id,
    #                                         'uom_id_r': s2.uom_id.id,
    #                                         'ftp': s2.ftp,
    #                                         'state': s2.state,
    #                                         'work_id': s2.id,
    #                                         'zone': hh,
    #                                         'secteur': vv,
    #                                         'wiz_id': current.id,
    #                                         'sequence': res[0] + 1,
    #                                         'etape': s2.etape,
    #                                         'zo': str(hh),
    #                                         'is_display': is_display
    #
    #                                     }, context=context)
    #                         elif jj.zone > 0 and jj.secteur == 0:
    #                             for hh in range(jj.zone, jj.zone + 1):
    #                                 if jj.employee_id:
    #                                     employee = jj.employee_id.id
    #                                 else:
    #                                     employee = s2.employee_id.id or False
    #                                 if jj.date_from:
    #                                     date_from = jj.date_from
    #                                 else:
    #                                     date_from = s2.date_start
    #                                 if jj.date_to:
    #                                     date_to = jj.date_to
    #                                 else:
    #                                     date_to = s2.date_end
    #                                 if jj.poteau_t:
    #                                     poteau_t = jj.poteau_t
    #                                 else:
    #                                     poteau_t = s2.poteau_t
    #                                 if jj.is_display is True:
    #                                     is_display = True
    #                                 else:
    #                                     is_display = False
    #                                 sequence_w = sequence_w + 1
    #                                 self.pool.get('base.group.merge.line2').create(cr, uid, {
    #                                     'task_id': s2.task_id.id,
    #                                     'categ_id': s2.categ_id.id,
    #                                     'product_id': s2.product_id.id,
    #                                     'name': s2.name + ' - Zone ' + str(hh),
    #                                     'date_start': date_from,
    #                                     'date_end': date_to,
    #                                     'poteau_i': s2.poteau_t,
    #                                     'poteau_t': poteau_t,
    #                                     'color': s2.color,
    #                                     'total_t': s2.total_t,  ##*work.employee_id.contract_id.wage
    #                                     'project_id': s2.project_id.id,
    #                                     'bon_id': current.id,
    #                                     'gest_id': s2.gest_id.id or False,
    #                                     'employee_id': employee,
    #                                     'uom_id': s2.uom_id.id,
    #                                     'uom_id_r': s2.uom_id.id,
    #                                     'ftp': s2.ftp,
    #                                     'state': s2.state,
    #                                     'work_id': s2.id,
    #                                     'zone': hh,
    #                                     'zo': str(jj.hh),
    #                                     'secteur': 0,
    #                                     'wiz_id': current.id,
    #                                     'sequence': res[0] + 1,
    #                                     'etape': s2.etape,
    #                                     'is_display': is_display
    #
    #                                 }, context=context)
    #
    #         return True
    #
    #     @api.onchange('project_id', 'date_from', 'date_to', 'zone', 'secteur', 'categ_id', 'partner_id')
    #     def onchange_categ_id(self):
    #         ids = []
    #         list = []
    #         tt = []
    #         task_ = self.env['project.task']
    #         if self.project_id and self.zone == 99 and self.secteur == 99:
    #             if self.categ_id:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('categ_id', '=', self.categ_id.id),
    #                      ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('facture', '=', False),
    #                      ('done3', '=', True)], order='id asc')
    #             else:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('date', '>=', self.date_from),
    #                      ('date', '<=', self.date_to), ('facture', '=', False), ('done3', '=', True)], order='id asc')
    #         elif self.project_id and self.zone != 99 and self.secteur != 99:
    #             if self.categ_id:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('categ_id', '=', self.categ_id.id),
    #                      ('zone', '=', self.zone), ('secteur', '=', self.secteur), ('date', '>=', self.date_from),
    #                      ('date', '<=', self.date_to), ('facture', '=', False), ('done3', '=', True)], order='id asc')
    #             else:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('date', '>=', self.date_from), ('zone', '=', self.zone),
    #                      ('secteur', '=', self.secteur), ('date', '<=', self.date_to), ('facture', '=', False),
    #                      ('done3', '=', True)], order='id asc')
    #
    #         elif self.project_id and self.zone != 99 and self.secteur == 99:
    #             if self.categ_id:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('categ_id', '=', self.categ_id.id),
    #                      ('zone', '=', self.zone), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
    #                      ('facture', '=', False), ('done3', '=', True)], order='id asc')
    #             else:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('project_id', '=', self.project_id.id), ('date', '>=', self.date_from), ('zone', '=', self.zone),
    #                      ('date', '<=', self.date_to), ('facture', '=', False), ('done3', '=', True)], order='id asc')
    #         elif self.partner_id:
    #             if self.categ_id:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('partner_id', '=', self.partner_id.id), ('categ_id', '=', self.categ_id.id),
    #                      ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('facture', '=', False),
    #                      ('done3', '=', True)], order='id asc')
    #             else:
    #                 tt = self.env['project.task.work.line'].search(
    #                     [('partner_id', '=', self.partner_id.id), ('date', '>=', self.date_from),
    #                      ('date', '<=', self.date_to), ('facture', '=', False), ('done3', '=', True)], order='id asc')
    #
    #         if tt:
    #             ll = tt.ids
    #         else:
    #             ll = []
    #
    #         return {'domain': {'work_ids': [('id', 'in', ll)]}}
    #
    def apply_(self):

        """
        Action that shows the list of (non-draft) account moves from
        the selected journals and periods, so the user can review
        the renumbered account moves.
        """
        current = self.browse(self.ids[0])
        for s3 in current.work_ids.ids:
            if current.clos:
                self.env['project.project'].set_done([current.project_id.id])

            if not current.num:
                raise UserError(_('Action Impossible!\nN° Facture Obligatoire !'))
            self.env['project.task.work.line'].write(s3, {'num': current.num, 'date_inv': current.date_inv,
                                                          'facture': True})

        self.write({'state': 'open'})
        view = self.env['sh.message.wizard']

        view_id = view and view.id or False
        return {
            'name': 'Facture généré avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }

    #
    #     @api.one
    #     def action_copy3(self):
    #         packaging_obj = self.pool.get('project.task')
    #         packaging_copy = packaging_obj.copy_data(self._cr, self._uid, self.dst_task_id.id)
    #         packaging_obj.write({'name': 'dfsdf'})
    #         return True

    def cancel_(self):

        """
        Action that shows the list of (non-draft) account moves from
        the selected journals and periods, so the user can review
        the renumbered account moves.
        """
        current = self.browse(self.ids[0])

        for s3 in current.work_ids.ids:
            self.env['project.task.work.line'].write(s3, {'num': '', 'date_inv': False})

        self.write({'state': 'draft'})
        view = self.env['sh.message.wizard']

        view_id = view and view.id or False
        return {
            'name': 'Annulation faite avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
        }


class ProjectProfitability(models.Model):
    _name = 'project.profitability'
    _description = 'Project Profitability'
#
    total_depenses = fields.Float(string='Total Depenses')
    montant_total = fields.Float(string='Montant total')
    diference = fields.Float('Difference ')
    taux = fields.Float(string='Taux %')
    project_id = fields.Many2one('project.project', string='project')
    invoice_id = fields.Many2one('base.facture.wizard', string='Invoice')
    # progress_amount is a  computed field
    # progress_amout = fields.Float(string='Progress Amount')


