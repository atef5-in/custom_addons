# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError


# import logging
#
# _logger = logging.getLogger(__name__)
#
# _RISK_STATE = [('draft', 'Draft'), ('active', 'Active'), ('closed', 'Closed')]


class RiskManagementCategory(models.Model):
    _name = 'risk.management.category'
    _description = 'Risk log category table'

    def _get_qty1(self):

        current = self[0]
        tt = 0
        for rec in current.line_id:
            tt = tt + rec.ps

            current.total_1 = tt

    def _get_qty2(self):

        current = self[0]
        tt = 0
        for rec in current.line_id:
            tt = tt + rec.aerien
            current.total_2 = tt

    def _get_qty3(self):

        current = self[0]
        tt = 0
        for rec in current.line_id:
            tt = tt + rec.souterrain
            current.total_3 = tt

    def _get_qty4(self):

        current = self[0]
        tt = 0
        for rec in current.line_id:
            tt = tt + rec.double_aerien
            current.total_4 = tt

    def _get_qty5(self):

        current = self[0]
        tt = 0
        for rec in current.line_id:
            tt = tt + rec.double_conduit
            current.total_5 = tt

    # def _get_user(self, cr, uid, context=None):
    #     res = []
    #     current = self.browse(cr, uid, ids[0], context=context)
    #     employee_id = current.employee_id.user_id.id
    #     res.append(employee_id)
    #     return res

    # def domain_users(self, cr, uid, ids, field_name, arg, context=None):
    #     domain = False
    #     user = self.pool.get('res.users').browse(cr, uid, uid, context).employee_id.id
    #     domain = [('employee_id', '=', user)]
    #
    #     return domain

    def get_value_ids(self):

        user = self.env['res.users'].browse(self.env.user.id).employee_id.id
        value_obj = self.env['risk.management.response.category']
        value_ids = value_obj.search([('employee_id', '=', user)])

        return dict([(id, value_ids) for id in self.ids])

    #    def default_get(self, cr, uid, fields, context=None):
    ##        if context is None: context = {}
    ##        res = super(risk_management_risk_category, self).default_get(cr, uid, fields, context=context)
    ##        line_id = context.get('line_id', False)
    ##        if  'line_id' in fields:
    ##            query = """
    ##                select id  from risk_management_risk_response_category where parent_id = %s and employee_id=%s"""
    ##            cr.execute(query, ids[0],28,)
    ##            result = cr.dictfetchall()
    ##            res.update(line_id=[(4,elem) for elem in result])
    ##        raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%line_id)
    ##        return res
    # def get_domain_useer_id(self, cr, uid, ids, context=None):
    #     user = self.pool.get('res.users').browse(cr, uid, uid, context).employee_id.id
    #
    #     return {'domain': {'employee_id': [('id', '=', user)]}}

    name = fields.Char(string='Risk Category')
    wiz_id = fields.Many2one('base.group.merge.line', string='Wizard')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    project_id = fields.Many2one('project.project', string='Wizard')
    zone = fields.Integer(string='Zone')
    secteur = fields.Integer(string='Secteur')
    task_id = fields.Many2one('project.task', string='Wizard')
    employee_id = fields.Many2one('hr.employee', string='Wizard')
    wizard_id = fields.Many2one('base.group.merge.automatic.wizard', string='Wizard')
    state = fields.Selection([('draft', 'Brouillon'),
                              ('done', 'Traité')],
                             string='Status', copy=False, default='draft')
    date = fields.Date(string='Last Action', default=fields.datetime.now)
    line_id = fields.One2many('risk.management.response.category', 'parent_id',
                              domain=[('is_me', '=', True)])
    line_id1 = fields.One2many('risk.management.response.category', compute='get_value_ids')
    total_1 = fields.Float(compute='_get_qty1', string='Company Currency')
    total_2 = fields.Float(compute='_get_qty2', string='Company Currency')
    total_3 = fields.Float(compute='_get_qty3', string='Company Currency')
    total_4 = fields.Float(compute='_get_qty4', string='Company Currency')
    total_5 = fields.Float(compute='_get_qty5', string='Company Currency')

    # 'line_id': lambda self, cr, uid, context: self.get_value_ids(cr, uid, [0], '', '', context)[0],


#     def button_back(self, cr, uid, ids, context=None):
#
#         current = self.browse(cr, uid, ids[0], context=context)
#         group = self.pool.get('base.group.merge.line')
#         pt1 = 0
#         pt2 = 0
#         pt3 = 0
#         tt = self.pool.get('base.group.merge.line').search(cr, uid, (
#         [('wizard_id', '=', current.wizard_id.id), ('product_id.default_code', '=', '115-RR')]))
#         tt1 = self.pool.get('base.group.merge.line').search(cr, uid, (
#         [('wizard_id', '=', current.wizard_id.id), ('product_id.default_code', '=', '116-RA')]))
#         tt0 = self.pool.get('base.group.merge.line').search(cr, uid, (
#         [('wizard_id', '=', current.wizard_id.id), ('product_id.default_code', '=', '117-IT')]))
#         for rk in current.line_id:
#             if rk.inj is False:
#                 pt1 = pt1 + rk.aerien + rk.ps + rk.souterrain + rk.double_aerien + rk.double_conduit
#                 pt2 = pt2 + rk.aerien + rk.ps + rk.souterrain
#                 pt3 = pt3 + rk.aerien + rk.double_aerien
#                 self.pool.get('risk.management.response.category').write(cr, uid, rk.id, {'inj': 1,
#                                                                                           'employee_id': current.employee_id.id},
#                                                                          context=context)
#         ##        cr.execute('select product_id from base_group_merge_line  where wizard_id =%s and work_id=%s' , (current.wizard_id.id ,tt1[0]))
#         ##        q3=cr.fetchone()
#         if not current.project_id.r_id:
#             cr.execute('update project_project set  r_id=%s where id =%s', (current.id, current.project_id.id))
#
#         ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt1[0])
#         if tt:
#             cr.execute('update base_group_merge_line set  poteau_r=%s where id=%s', (pt1 / 1000, tt[0]))
#         if tt1:
#             cr.execute('update base_group_merge_line set  poteau_r=%s where id=%s', (pt2 / 1000, tt1[0]))
#         if tt0:
#             cr.execute('update base_group_merge_line set  poteau_r=%s where id=%s', (pt3 / 1000, tt0[0]))
#
#         return {
#             'name': ('Modification Travaux'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'base.group.merge.automatic.wizard',
#             'res_id': current.wizard_id.id,
#             'context': {},
#             'domain': []
#         }
#
#     def button_save_(self, cr, uid, ids, context=None):
#
#         risk_line = self.pool.get('risk.management.response.category')
#         this = self.browse(cr, uid, ids[0])
#         ##self.pool.get('project.task.work').write(cr, uid, this.project_id.id, {'r_id':this.id }, context=context)
#         for rk in this.line_id:
#             ##risk_line.write(cr, uid, rk.id, {'is_me':True }, context=context)
#             if not rk.wiz_id:
#                 risk_line.write(cr, uid, rk.id, {'wiz_id': this.wiz_id.id}, context=context)
#         if not this.project_id.r_id:
#             cr.execute('update project_project set  r_id=%s where id =%s', (this.id, this.project_id.id))
#         ##self.write(cr, uid, this.id, {'state': 'affect'}, context=context)
#         return {
#             'name': ('Déclaration des Bons'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'risk.management.category',
#             'res_id': ids[0],
#             'context': {},
#             'domain': []
#         }
#
#     def button_approve(self, cr, uid, ids, context=None):
#
#         risk_line = self.pool.get('risk.management.response.category')
#         this = self.browse(cr, uid, ids[0])
#         self.pool.get('risk.management.category').write(cr, uid, this.id, {'state': 'done'}, context=context)
#
#         ##self.write(cr, uid, this.id, {'state': 'affect'}, context=context)
#         return {
#             'name': ('Déclaration des Bons'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'risk.management.category',
#             'res_id': ids[0],
#             'context': {},
#             'domain': []
#         }
#
#     def button_close(self, cr, uid, ids, context=None):
#         return {'type': 'ir.actions.act_window_close'}
#
#


class RiskManagementResponseCategory(models.Model):
    _name = 'risk.management.response.category'
    _description = 'Risk log response category table'
    _rec_name = 'plan'

    # def _default_done(self, cr, uid, ids, field_name, arg, context=None):
    #     result = {}
    #
    #     for rec in self.browse(cr, uid, ids, context=context):
    #         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.%s')%(rec.employee_id.user_id.id,uid))
    #         if rec.employee_id.user_id.id == uid:
    #             result[rec.id] = 1
    #
    #         else:
    #             result[rec.id] = 0
    #
    #     return result

    plan = fields.Char(string='Risk Category')
    rue = fields.Char(string='Risk Category')
    aerien = fields.Float(string='Risk Category', domain=[('is_me', '=', 1)])
    ps = fields.Float(string='Risk Category')
    souterrain = fields.Float(string='Risk Category')
    double_aerien = fields.Float(string='Risk Category')
    double_conduit = fields.Float(string='Risk Category')
    type = fields.Selection([('threat', 'Threat'), ('opportunity', 'Opportunity')], string='Type')
    name = fields.Char(string='Response Category')
    work_id = fields.Many2one('project.task.work', string='Wizard')
    project_id = fields.Many2one('project.project', string='Wizard')
    task_id = fields.Many2one('project.task', string='Wizard')
    parent_id = fields.Many2one('risk.management.category', string='Assigned to')
    employee_id = fields.Many2one('hr.employee', string='Assigned to')
    wiz_id = fields.Many2one('base.group.merge.line', string='Wizard')
    date = fields.Date(string='Last Action')
    inj = fields.Boolean(string='Last Action')
    is_me = fields.Boolean(string='Last Action', default=True)


class RiskManagementProximity(models.Model):
    _name = 'risk.management.proximity'
    _description = 'Risk log proximity table'

    name = fields.Char(string='Proximity', required=True)  # 64

# class RiskManagementRisk(models.Model):
#     _name = 'risk.management.risk'
#     _description = 'Risk'
#     _inherit = ['mail.thread', 'ir.needaction_mixin']
#
#     _track = {
#         'state': {
#             'risk.mt_risk_draft': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['draft'],
#             'risk.mt_risk_active': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['active'],
#             'risk.mt_risk_closed': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['closed']
#         }
#     }
#
#     def _risk_response_count(self, cr, uid, ids, field_name, arg, context=None):
#         ret = {}
#         try:
#             for risk in self.browse(cr, uid, ids, context):
#                 ret[risk.id] = len(risk.risk_response_ids)
#         except:
#             pass
#         return ret
#
#     def _calculate_expected_inherent_value(self, cr, uid, ids, field_name, arg, context={}):
#         ret = {}
#         for risk in self.browse(cr, uid, ids):
#             ret[risk.id] = risk.impact_inherent * risk.probability_inherent
#         return ret
#
#     def _calculate_expected_residual_value(self, cr, uid, ids, field_name, arg, context={}):
#         ret = {}
#         for risk in self.browse(cr, uid, ids, context=context):
#             ret[risk.id] = risk.impact_residual * risk.probability_residual
#         return ret
#
#     def set_state_draft(self, cr, uid, id, context=None):
#         return self.write(cr, uid, id, {'state': 'draft'})
#
#     def set_state_active(self, cr, uid, id, context=None):
#         return self.write(cr, uid, id, {'state': 'active'})
#
#     def set_state_closed(self, cr, uid, id, context=None):
#         return self.write(cr, uid, id, {'state': 'closed'})
#
#     _columns = {
#         'name': fields.char('Risk Id', size=64, required=True,
#                             readonly=True, states={'draft': [('readonly', False)]}, select=True,
#                             help="Risk label. Can be changed as long as risk is in state 'draft'."),
#         'description': fields.char('Risk Description', 64, help="Short description of the Risk."),
#         'project_id': fields.many2one('project.project', 'Project', required=True),
#         'author_id': fields.many2one('res.users', 'Author', required=True),
#         'color': fields.integer('Color'),
#         'date_registered': fields.date('Date Registered', required=True,
#                                        help="Date of the Risk registered. Auto populated."),
#         'date_modified': fields.date('Date Modified', help="Date of last update."),
#         'risk_category_id': fields.many2one('risk.management.category', 'Risk Category', required=True,
#                                             help="Risk Category: The type of risk in terms of the project's or business' chosen categories (e.g. Schedule, quality, legal etc.)"),
#         'description_cause': fields.text('Cause'),
#         'description_event': fields.text('Event'),
#         'description_effect': fields.text('Effect'),
#         'impact_inherent': fields.integer('Inherent Impact', required=True,
#                                           help="Impact: The result of a particular threat or opportunity actually occurring, or the anticipation of such a result. This is the pre-response value, common used scales are 1 to 10 or 1 to 100."),
#         'impact_residual': fields.integer('Residual Impact', required=True,
#                                           help="Impact: The result of a particular threat or opportunity actually occurring, or the anticipation of such a result. This is the post-response value, common used scales are 1 to 10 or 1 to 100."),
#         'probability_inherent': fields.integer('Inherent Probability', required=True,
#                                                help="Probability: The evaluated likelihood of a particular threat or opportunity actually happening, including a consideration of the frequency with which this may arise. This is the pre-response value, common used scales are 1 to 10 or 1 to 100."),
#         'probability_residual': fields.integer('Residual Probability', required=True,
#                                                help="Probability: The evaluated likelihood of a particular threat or opportunity actually happening, including a consideration of the frequency with which this may arise. This is the post-response value, common used scales are 1 to 10 or 1 to 100."),
#         'expected_value_inherent': fields.function(_calculate_expected_inherent_value, method=True,
#                                                    string='Expected Inherent Value', store=True,
#                                                    help="Expected Value. Cost of inherent impact * inherent probability. This is the pre-response value."),
#         'expected_value_residual': fields.function(_calculate_expected_residual_value, method=True,
#                                                    string='Expected Residual Value', store=True,
#                                                    help="Expected Value. Cost of residual impact * residual probability. This is the post-response value."),
#         'proximity_id': fields.many2one('risk.management.proximity', 'Proximity',
#                                         help="Proximity: This would typically state how close to the present time the risk event is anticipated to happen (e.g. for project risks Imminent, within stage, within project, beyond project).  Proximity should be recorded in accordance with the project's chosen scales or business continuity time scales."),
#         'risk_response_category_id': fields.many2one('risk.management.response.category', 'Response Category',
#                                                      help="Risk Response Categories: How the project will treat the risk in terms of the project's (or business continuity planning) chosen categories."),
#         'risk_response_ids': fields.one2many('project.task', 'risk_id', 'Response Ids'),
#         'risk_response_count': fields.function(_risk_response_count, type='integer'),
#         # 'state': fields.selection([('draft','Draft'),('active','Active'),('closed','Closed')],'State', readonly=True, help="A risk can have one of these three states: draft, active, closed."),
#         'state': fields.selection(_RISK_STATE, 'State', readonly=True,
#                                   help="A risk can have one of these three states: draft, active, closed."),
#         #    'stage_id': fields.selection([('draft','Draft'),('active','Active'),('closed','Closed')],'State', readonly=True, help="A risk can have one of these three states: draft, active, closed."),
#         'risk_owner_id': fields.many2one('res.users', 'Owner',
#                                          help="Risk Owner: The person responsible for managing the risk (there can be only one risk owner per risk), risk ownership is assigned to a managerial level, in case of business continuity to a C-level manager."),
#     }
#     _defaults = {
#         'author_id': lambda s, cr, uid, c: uid,
#         'date_registered': lambda *a: date.today().strftime('%Y-%m-%d'),
#         'state': 'draft',
#         'impact_inherent': 0,
#         'impact_residual': 0,
#         'probability_inherent': 0,
#         'probability_residual': 0,
#         'name': lambda s, cr, uid, c: s.pool.get('ir.sequence').get(cr, uid, 'risk.management.risk'),
#         'color': '0'
#     }
#
#     def _subscribe_extra_followers(self, cr, uid, ids, vals, context=None):
#         user_ids = [vals[x] for x in ['author_id', 'risk_owner_id'] if x in vals and vals[x] != False]
#         if len(user_ids) > 0:
#             self.message_subscribe_users(cr, uid, ids, user_ids=user_ids, context=context)
#
#         risks = self.read(cr, uid, ids, ['message_follower_ids', 'risk_response_ids'])
#         for risk in risks:
#             if 'risk_response_ids' in risk and risk['risk_response_ids']:
#                 task_ob = self.pool.get('project.task')
#                 task_ob.message_subscribe(cr, uid, risk['risk_response_ids'], risk['message_follower_ids'],
#                                           context=context)
#
#     def write(self, cr, uid, ids, vals, context=None):
#         ret = super(risk_management_risk, self).write(cr, uid, ids, vals, context)
#         self._subscribe_extra_followers(cr, uid, ids, vals, context)
#         return ret
#
#     def create(self, cr, uid, vals, context=None):
#         risk_id = super(risk_management_risk, self).create(cr, uid, vals, context)
#         self._subscribe_extra_followers(cr, uid, [risk_id], vals, context)
#         return risk_id
#
# # class risk_management(models.Model):
# #     _name = 'risk_management.risk_management'
# #     _description = 'risk_management.risk_management'
#
# #     name = fields.Char()
# #     value = fields.Integer()
# #     value2 = fields.Float(compute="_value_pc", store=True)
# #     description = fields.Text()
# #
# #     @api.depends('value')
# #     def _value_pc(self):
# #         for record in self:
# #             record.value2 = float(record.value) / 100


class ProjectTaskWork(models.Model):
    _inherit = 'project.task.work'

    r_id = fields.Many2one('risk.management.category', string='r ID', readonly=True,
                           states={'draft': [('readonly', False)]}, )


class BaseTaskMergeLine(models.Model):
    _inherit = 'base.task.merge.line'

    plan_id = fields.Many2one('risk.management.response.category', string='Wizard')
    plan_id2 = fields.Many2one('risk.management.response.category', string='Wizard')
    risk_id = fields.Many2one('risk.management.category', string='Wizard')

    def onchange_plan_id_(self, plan_id, plan_id2):
        result = {'value': {}}  # Initialisation d'un dictionnaire de résultats

        total = 0  # Initialisation d'une variable pour stocker le total des valeurs calculées

        if plan_id and plan_id2:  # Vérifie si les deux plan_id sont présents
            plan1 = self.env['risk.management.response.category'].browse(
                plan_id)  # Récupère l'enregistrement correspondant à plan_id dans le modèle 'risk.management.response.category'
            plan2 = self.env['risk.management.response.category'].browse(
                plan_id2)  # Récupère l'enregistrement correspondant à plan_id2 dans le modèle 'risk.management.response.category'

            # Parcours de la plage des identifiants de plan entre plan_id et plan_id2 inclus
            for x in range(plan_id, plan_id2 + 1):
                plan = self.env['risk.management.response.category'].browse(
                    x)  # Récupère chaque enregistrement correspondant à un identifiant de plan dans la plage
                if plan:
                    # Accumulation des valeurs des champs spécifiques de l'enregistrement plan dans la variable total
                    total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit

            # Assignation de la valeur calculée au champ 'plans' du dictionnaire de résultats
            result['value']['plans'] = plan1.plan + '-' + plan2.plan

        return result  # Retourne le dictionnaire de résultats contenant les valeurs mises à jour

    def onchange_plans(self, plans):
        result = {'value': {}}  # Initialisation d'un dictionnaire de résultats
        total = 0  # Initialisation d'une variable pour stocker le total des valeurs calculées
        count = 0  # Initialisation d'une variable pour compter

        if plans:  # Vérifie si le champ plans n'est pas vide
            if plans.count('-') > 1:  # Vérifie s'il y a plus d'un tiret dans plans
                raise ValidationError(_('Erreur !\nFormat Incorrecte!, un seul tiret est autorisé!'))
            elif plans.count('-') == 1 and plans.count(
                    ';') == 0:  # Vérifie s'il y a un seul tiret et aucun point-virgule dans plans
                tt = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[0])])
                tt1 = self.env['risk.management.response.category'].search([('plan', '=', plans.split('-')[1])])
                if not tt:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t1 = tt[0]
                if not tt1:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t2 = tt1[0]
                for x in range(t1, t2):
                    plan = self.env['risk.management.response.category'].browse(x)
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            elif plans.count('-') == 1 and plans.count(
                    ';') > 0:  # Vérifie s'il y a un seul tiret et au moins un point-virgule dans plans
                tt = self.env['risk.management.response.category'].search(
                    [('plan', '=', (plans.split(';')[0]).split('-')[0])])
                tt1 = self.env['risk.management.response.category'].search(
                    [('plan', '=', (plans.split(';')[0]).split('-')[1])])
                if not tt:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t1 = tt[0]
                if not tt1:
                    raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                else:
                    t2 = tt1[0]
                for x in range(t1, t2):
                    plan = self.env['risk.management.response.category'].browse(x)
                    if plan:
                        total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
                    lst = (plans.split(';')[1]).split(';')
                    for kk in lst:
                        tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                        if not tt2:
                            raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                        else:
                            plan = self.env['risk.management.response.category'].browse(tt2[0])
                        if plan:
                            total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            elif plans.count('-') == 0 and plans.count(
                    ';') > 0:  # Vérifie s'il n'y a pas de tiret et au moins un point-virgule dans plans
                lst = plans.split(';')
                for kk in lst:
                    for kk in lst:
                        tt2 = self.env['risk.management.response.category'].search([('plan', '=', kk)])
                        if not tt2:
                            raise ValidationError(_('Erreur !\nElement n"est pas dans le tableau de relevé!'))
                        else:
                            plan = self.env['risk.management.response.category'].browse(tt2[0])
                        if plan:
                            total += plan.aerien + plan.ps + plan.souterrain + plan.double_aerien + plan.double_conduit
            else:
                raise ValidationError(_('Erreur !\nFormat Incorrecte!, seuls les tirets "-" ou les points virgules ";" sont autorisés!'))

        result['value'][
            'poteau_t'] = total / 1000  # Calcule la valeur pour le champ 'poteau_t' dans le dictionnaire de résultats
        return result  # Retourne le dictionnaire de résultats contenant les valeurs mises à jour
