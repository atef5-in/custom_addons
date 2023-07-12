# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class EbMergeInvoices(models.Model):
    _name = "base.invoices.merge.automatic.wizard"
    _description = "Merge invoicess"



    def default_get(self, fields_list):

        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids')

        if self.env.context.get('active_model') == 'base.group.merge.automatic.wizard':
            tt = self.env['base.group.merge.automatic.wizard'].browse(self.env.context.get('active_ids'))
            active_ids = tt.work_ids.ids
            vv = []

            for hh in active_ids:
                work = self.env['project.task.work'].browse(hh)

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
                        if not work.is_copy:
                            if not work1.is_copy:
                                vv.append(work1.id)
                        else:
                            if work1.is_copy is not False:
                                if work.rank == work1.rank:
                                    vv.append(work1.id)
                    res['work_ids'] = vv
                else:
                    res['work_ids'] = active_ids

            r = []
            l = []
            pref = ''
            test = ''
            state = 'draft'
            self.env.cr.execute(
                'select cast(substr(name, 5, 7) as integer)  from base_invoices_merge_automatic_wizard where name is not Null  and categ_id=1  and EXTRACT(YEAR FROM create_date)=%s   order by cast(name as integer) desc limit 1',
                (str(datetime.today().year),))
            q3 = self.env.cr.fetchone()

            if q3:
                res1 = q3[0] + 1
            else:
                res1 = '001'

            for jj in tt.work_ids.ids:
                work = self.env['project.task.work'].browse(jj)
                if work.state == 'close':
                    raise UserError(_('Erreur!\nTravaux clotués!'))
                if len(active_ids) > 1:
                    pref = '/'
                done = 0
                if work.gest_id.user_id.id == self.env.user.id:
                    done = 1
                else:
                    done = 0
                if work.state != 'draft':
                    state = 'affect'
                r.append(work.categ_id.id)
                if r:
                    for kk in r:
                        dep = self.env['hr.academic'].search([('categ_id', '=', kk)])
                        if dep:
                            for nn in dep.ids:
                                em = self.env['hr.academic'].browse(nn).employee_id.id
                                l.append(em)
                cat = work.categ_id.id
                test = test + pref + str(work.project_id.name) + ' - ' + str(work.task_id.sequence) + ' - ' + str(
                    work.sequence)
                res.update({'states': test, 'employee_id': work.employee_id.id, 'gest_id': work.gest_id.id,
                            'categ_id': work.categ_id.id,
                            'project_id': work.project_id.id, 'zone': work.zone, 'secteur': work.secteur,
                            'state': state, 'dep': r})  ##,'categ_id':work.categ_id.id
                if cat == 1:
                    res.update({'name': str(str(fields.Date.today().strftime('%Y%m%d'))[:4] + str(res1).zfill(3))})

        elif self.env.context.get('active_model') != 'project.task.work':
            res = super().default_get(fields_list)
            ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisantdffd pour l'article %s  !")%  self.env.context.get('active_ids'))

            tt = self.env['base.flow.merge.automatic.wizard'].browse(self.env.context.get('active_ids'))
            active_ids = tt.work_ids.ids
            vv = []
            dd = []

            for hh in active_ids:
                work = self.env['project.task.work'].browse(hh)

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
                    for hh in kit_list.ids:
                        work1 = self.env['project.task.work'].browse(hh)
                        if not work.is_copy:
                            if not work1.is_copy:
                                vv.append(work1.id)
                        else:
                            if work1.is_copy is not False:
                                if work.rank == work1.rank:
                                    vv.append(work1.id)
                    res['work_ids'] = vv
                else:
                    res['work_ids'] = active_ids

            r = []
            l = []
            pref = ''
            test = ''
            list = []
            state = 'draft'
            self.env.cr.execute(
                'select cast(substr(name, 5, 7) as integer)  from base_invoices_merge_automatic_wizard where name is not Null  and categ_id=1  and EXTRACT(YEAR FROM create_date)=%s   order by cast(name as integer) desc limit 1',
                (str(datetime.today().year),))
            q3 = self.env.cr.fetchone()

            if q3:
                res1 = q3[0] + 1
            else:
                res1 = '001'

            for jj in tt.work_ids.ids:
                print('jj:', jj)
                work = self.env['project.task.work'].browse(jj)

                ##                tt=self.env['project.task.work.line'].search([('work_id','=',jj),('state','=','affect')]).ids

                if work.state == 'close':
                    raise UserError(_('Erreur!\nTravaux clotués!'))

                ##                if work.employee_id:
                ##                    raise osv.except_osv(_('Erreur!'),_("Travaux Déja affectés aux ressources!"))
                if len(active_ids) > 1:
                    pref = '/'
                done = 0
                if work.gest_id.user_id.id == self.env.user.id:
                    done = 1
                else:
                    done = 0
                if work.state != 'draft':
                    state = 'affect'
                r.append(work.categ_id.id)
                if r:
                    for kk in r:
                        dep = self.env['hr.academic'].search([('categ_id', '=', kk)])
                        if dep:
                            for nn in dep.ids:
                                em = self.env['hr.academic'].browse(nn).employee_id.id
                                l.append(em)
                cat = work[0].categ_id.id
                print(cat)
                test = test + pref + str(work.project_id.name) + ' - ' + str(work.task_id.sequence) + ' - ' + str(
                    work.sequence)
                res.update({
                    'states': test,
                    'employee_id': work.employee_id.id,
                    'gest_id': work.gest_id.id,
                    'categ_id': work.categ_id.id,
                    'project_id': work.project_id.id,
                    'zone': work.zone,
                    'secteur': work.secteur,
                    'state': state,
                    'dep': r
                })
                if cat == 1:
                    res.update({
                        'name': str(str(datetime.today().year) + str(res1).zfill(3))
                    })

        if self.env.context.get('active_model') == 'project.task.work':
            active_ids = self.env.context.get('active_ids')
            tt = self.env['project.task.work'].browse(active_ids)

            for work in tt:
                if 'correction' in work.product_id.name or 'gestion client' in work.product_id.name or u'Contrôle' in work.product_id.name:
                    raise UserError(_("Action impossible!\nImpossible d'affecter ce type de tache à partir de ce menu!"))

                vv = []

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
                    for kit_work in kit_list:
                        if not work.is_copy and not kit_work.is_copy:
                            vv.append(kit_work.id)
                        elif kit_work.is_copy and work.rank == kit_work.rank:
                            vv.append(kit_work.id)

                    res['work_ids'] = vv
                else:
                    res['work_ids'] = active_ids

                if work.state == 'valid':
                    raise UserError(_('Erreur!\nTravaux clotués!'))

        ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisantdffd pour l'article %s  !")% tt)
        ##        raise osv.except_osv(_('Error !'),
        ##                                         _('You cannot validate this journal entry because account "%s" does not belong to chart of accounts "%s"!') % (tt, tt))

        if self.env.context.get('active_model') == 'project.task.work' and active_ids:
            # active_ids = self.env.context.get('active_ids')

            for hh in active_ids:
                work = self.env['project.task.work'].browse(hh)
                print(work)
                vv = []

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
                    for kit_work in kit_list:
                        if not work.is_copy and not kit_work.is_copy:
                            vv.append(kit_work.id)
                        elif kit_work.is_copy and work.rank == kit_work.rank:
                            vv.append(kit_work.id)

                    res['work_ids'] = vv
                else:
                    print("2.1")
                    res['work_ids'] = active_ids

            r = []
            l = []
            pref = ''
            test = ''
            state = 'draft'

            self.env.cr.execute(
                'SELECT CAST(SUBSTRING(name, 5, 7) AS INTEGER) FROM base_invoices_merge_automatic_wizard WHERE name IS NOT NULL AND categ_id=1 AND EXTRACT(YEAR FROM create_date)=%s ORDER BY CAST(name AS INTEGER) DESC LIMIT 1',
                (str(datetime.today().year),))

            q3 = self.env.cr.fetchone()
            print(q3)
            if q3:
                res1 = q3[0] + 1
            else:
                res1 = '001'

            for jj in active_ids:
                work = self.env['project.task.work'].browse(jj)

                if work.state == 'close':
                    raise UserError(_('Erreur!\nTravaux clotués!'))

                if len(active_ids) > 1:
                    pref = '/'

                if work.state != 'draft':
                    state = 'affect'

                r.append(work.categ_id.id)

                if r:
                    for kk in r:
                        dep = self.env['hr.academic'].search([('categ_id', '=', kk)])
                        if dep:
                            for nn in dep.ids:
                                em = self.env['hr.academic'].browse(nn).employee_id.id
                                l.append(em)
                cat = work[0].categ_id.id
                test = test + pref + str(work.project_id.name) + ' - ' + str(work.task_id.sequence) + ' - ' + str(
                    work.sequence)

                res.update({
                    'states': test,
                    'employee_id': work.employee_id.id,
                    'gest_id': work.gest_id.id,
                    'categ_id': cat,
                    'project_id': work.project_id.id,
                    'zone': work.zone,
                    'secteur': work.secteur,
                    'state': state,
                    'dep': r,
                })
                if cat == 1:
                    res.update({'name': str(str(datetime.today().year) + str(str(res1).zfill(3)))})

        return res

    def _amount_all(self):

        tax_obj = self.env['account.tax']

        tvp_obj = tax_obj.browse(8)
        tps_obj = tax_obj.browse(7)

        for invoice in self:
            invoice.amount_untaxed = sum(line.amount_line for line in invoice.line_ids)
            if invoice.employee_id.job_id.id == 1:
                tvq = 0
                tps = 0
            else:
                tvq = tvp_obj.amount
                tps = tps_obj.amount
            invoice.amount_tps = invoice.amount_untaxed * tps
            invoice.amount_tvq = invoice.amount_untaxed * tvq
            invoice.amount_total = invoice.amount_untaxed + invoice.amount_tps + invoice.amount_tvq

    name = fields.Char(string='name', readonly=True, )
    gest_id = fields.Many2one('hr.employee', string='Wizard', readonly=True, states={'draft': [('readonly', False)]})
    work_ids = fields.Many2many('project.task.work', string='Invoices', readonly=True,
                                states={'draft': [('readonly', False)]})
    user_id = fields.Many2one('res.users', string='Assigned', readonly=True, states={'draft': [('readonly', False)]})
    dst_work_id = fields.Many2one('project.task.work', string='Destination Task')
    dst_project = fields.Many2one('project.project', string="Project")
    group_id = fields.Many2one('base.group.merge.automatic.wizard', string="Project")
    line_ids = fields.One2many(
        'base.invoices.merge.line', 'wizard_id', string="Role lines", copy=True,
        readonly=True, states={'draft': [('readonly', False)]})
    # link_ids = fields.One2many('link.line', 'affect_id', string="Work done")
    project_id = fields.Many2one('project.project', string='Wizard', readonly=True,
                                 states={'draft': [('readonly', False)]})
    task_id = fields.Many2one('project.task', string='Wizard', readonly=True, states={'draft': [('readonly', False)]})
    work_id = fields.Many2one('project.task.work', string='Wizard', readonly=True,
                              states={'draft': [('readonly', False)]})
    pay_id = fields.Many2one('hr.payslip', string='Wizard', readonly=True, states={'draft': [('readonly', False)]})
    date_start_r = fields.Date(string='Assigned')
    date_end_r = fields.Date(string='Assigned')
    employee_id = fields.Many2one('hr.employee', string='Assigned',
                                  readonly=True, states={'draft': [('readonly', False)]})
    employee_id2 = fields.Many2one('hr.employee', string='Assigned')
    hours_r = fields.Float(string='Assigned')
    total_t = fields.Float(string='Assigned')
    total_r = fields.Float(string='Assigned')
    poteau_t = fields.Float(string='Assigned')
    poteau_r = fields.Float(string='Assigned')
    poteau_i = fields.Float(string='Assigned')
    poteau_reste = fields.Float(string='Assigned')
    sequence = fields.Integer(string='Assigned')
    zone = fields.Integer(string='Assigned')
    secteur = fields.Integer(string='Assigned')
    state = fields.Selection([
        ('draft', 'Planif. Trav.'),
        ('affect', 'Travaux Affectés'),
        ('tovalid', 'Validaion Super.'),
        ('valid', 'Factures Br.'),
        ('paid', 'Factures Val.'),
        ('cancel', 'T. Annulés'),
        ('pending', 'T. Suspendus'),
        ('close', 'Traité')], default='draft')
    note = fields.Text(string='Assigned')
    states = fields.Char(string='char', readonly=True, states={'draft': [('readonly', False)]})
    ftp = fields.Char(string='char')
    dep = fields.Char(string='char', readonly=True, states={'draft': [('readonly', False)]})
    done = fields.Boolean(string='Is doctor?', compute='_disponible')
    objet = fields.Char(string='char')
    color1 = fields.Integer(string='Assigned')
    uom_id_r = fields.Many2one('product.uom', string='Assigned')
    uom_id = fields.Many2one('product.uom', string='Assigned')
    amount_untaxed = fields.Float(compute='_amount_all', string='Name', default=0, )
    amount_total = fields.Float(compute='_amount_all', string='Name')
    amount_tvq = fields.Float(compute='_amount_all', string='Name')
    amount_tps = fields.Float(compute='_amount_all', string='Name')
    categ_id = fields.Many2one('product.category', string='Wizard')
    to = fields.Char(string='char')
    cc = fields.Char(string='char')
    cci = fields.Char(string='char')
    mail_send = fields.Selection([('yes', 'Oui'), ('no', 'Non')])
    employee_ids = fields.Many2many('hr.employee', 'base_invoices_merge_automatic_wizard_hr_employee_rel',
                                    'base_invoices_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids1 = fields.Many2many('hr.employee', 'base_invoices_merge_automatic_wizard_hr_employee_rel1',
                                     'base_invoices_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids2 = fields.Many2many('hr.employee', 'base_invoices_merge_automatic_wizard_hr_employee_rel2',
                                     'base_invoices_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    employee_ids3 = fields.Many2many('hr.employee', 'base_invoices_merge_automatic_wizard_hr_employee_rel3',
                                     'base_invoices_merge_automatic_wizard_id', 'hr_employee_id', string='Legumes')
    types_affect = fields.Selection([
        ('intervenant', 'Production'),
        ('controle', 'Contrôle'),
        ('correction', 'Correction')
    ], string="Type d'affectation", default='intervenant')
    intervenant_id = fields.Many2one('hr.employee', string='Intervenant')
    time = fields.Float(string='Temps de gestion')
    time_ch = fields.Char(string='Temps de gestion')

    def _compute_done2(self):
        print('_compute_done2')
        for record in self:
            if record.gest_id.user_id.id == self.env.user.id:
                record.done = True
            else:
                raise UserError(_("Transfert impossible!\nPas de stock suffisant pour l'article %s !") % record.name)
                record.done = False

    def _disponible(self):
        print('_disponible')
        for book in self:
            if book.gest_id.user_id.id == self.env.user.id:
                print('self.env.user.id:', self.env.user.id)
                book.done = True
            else:
                book.done = False

    @api.model
    def _get_current_user(self):
        print("_get_current_user")
        for record in self:
            record.done = False  # (self.env.user.id == record.gest_id.user_id.id)

    @api.onchange('categ_id', 'project_id', 'zone', 'secteur')
    def onchange_place(self):

        res = {}

        if self.categ_id:
            r = []
            k = []
            dep = self.env['hr.academic'].search([('categ_id', '=', self.categ_id.id)])

            if dep:
                for academic in dep:
                    em = academic.employee_id.id
                    k.append(academic.id)
                    r.append(em)
            res['domain'] = {
                # 'employee_id2': [('id', 'in', r)],
                'work_ids': [
                    ('categ_id', '=', self.categ_id.id),
                    ('project_id', '=', self.project_id.id),
                    ('zone', '=', self.zone),
                    ('secteur', '=', self.secteur)
                ]
            }
        print('res:', res)
        return res

    @api.model
    def action_merge(self):
        names = []

        # Write the name of the destination task because it will be overwritten
        if self.dst_work_id:
            names.append(self.dst_work_id.name)
        else:
            raise UserError(_('You must select a Destination Work'))

        desc = []

        # Also write the description of the destination task because it will be overwritten
        desc.append(self.dst_work_id.description)

        for invoice in self.invoices_ids:
            if invoice.id != self.dst_work_id.id:
                for name in invoice:
                    names.append(name.name)
                    desc.append(name.description)

        # Transfer messages from work_ids to dst_work_id
        for message in self.work_ids:
            for msg_id in message.message_ids:
                msg_id.write({'res_id': self.dst_work_id.id})

        plan_hours = self.dst_work_id.planned_hours

        for hour in self.work_ids:
            for time in hour:
                plan_hours += time.planned_hours

        # Write to dst_work_id full planned hours from all works
        self.dst_work_id.write({'planned_hours': plan_hours})

        # Actual writing to the tasks
        transformed_names = ', '.join(names)
        self.dst_work_id.write({'name': transformed_names})

        transformed_desc = ', '.join(desc)
        self.dst_work_id.write({'description': transformed_desc})

        # Posting a note in the merged and archived tasks
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        for work in self.work_ids:
            work.message_post(body="This work has been merged into: %s/#id=%s&amp;view_type=form&amp;model=project.task"
                                   % (base_url, self.dst_work_id.id))

        self.work_ids.write({'active': False})

        # Explicitly write the dst_work_id as active for security reasons
        self.dst_work_id.write({'active': True})

        # Check if user has been assigned and if not raise an error
        if self.user_id:
            # Write the Assigned To user_id
            self.dst_work_id.write({'user_id': self.user_id.id})
        elif self.dst_work_id.user_id:
            self.dst_work_id.write({'user_id': self.dst_work_id.user_id.id})
        else:
            raise Warning(
                "There is no user assigned to the merged work, and the destination work doesn't have an assigned user.")

        return True

    def button_close(self):
        return {'type': 'ir.actions.act_window_close'}

    def action_open(self):
        print("action_open")
        current = self.ids[0]
        work_ids = []
        for tt in self.work_ids.ids:
            work_ids.append(tt)
        return {
            'name': 'Taches Affectées',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree',
            'target': 'current',
            'res_model': 'project.task.work',
            'context': {
                'default_active_ids': work_ids,
                'default_ids': work_ids,
            },
            'domain': [('id', 'in', work_ids)],
        }

    # def button_cancel(self):
    #     work_obj = self.env['project.task.work']
    #     line_obj = self.env['base.invoices.merge.automatic.wizard']
    #     line_obj1 = self.env['base.invoices.merge.line']
    #     work_line = self.env['project.task.work']
    #     emp_obj = self.env['hr.employee']
    #     for rec in self:
    #         for tt in rec.work_ids:
    #             for msg_id in tt.ids:
    #                 wk = work_obj.browse(msg_id)
    #                 if rec.types_affect == 'intervenant':
    #                     if rec.employee_id2 and str(wk.affect_emp_list).find(
    #                             str(rec.employee_id2.user_id.id)) != -1 and wk.state == 'affect':
    #                         work_line.write({'state': 'draft'})
    #                         work_line.write({
    #                             'job': '',
    #                             'current_emp': False,
    #                             'employee_id': False,
    #                             'state': 'draft'
    #                         })
    #                         work_obj.write({
    #                             'affect_emp_list': wk.affect_emp_list.replace(str(rec.employee_id2.user_id.id), ''),
    #                             'affect_e_l': wk.affect_e_l.replace(str(rec.employee_id2.user_id.login), ''),
    #                             'affect_emp': wk.affect_emp.replace(
    #                                 str(rec.employee_id2.name if rec.employee_id2 else ''), '')
    #                         })
    #                     else:
    #                         raise UserError(
    #                             _("Champs Intervenant vide ou employée n'existe pas dans liste des intervenants"))
    #                 elif rec.types_affect == 'controle':
    #                     if rec.employee_id2 and str(wk.affect_con).find(str(rec.employee_id2.name)) != -1:
    #                         work_obj.write(wk, {
    #                             'affect_con_list': wk.affect_con_list.replace(str(rec.employee_id2.id), ''),
    #                             'affect_con': wk.affect_con.replace(str(rec.employee_id2.name), '')
    #                         })
    #                     else:
    #                         raise UserError(
    #                             _("Champs Intervenant vide ou employée n'existe pas dans liste des controleurs"))
    #                 elif rec.types_affect == 'correction':
    #                     if rec.employee_id2 and str(wk.affect_cor).find(str(rec.employee_id2.name)) != -1:
    #                         work_obj.write(wk, {
    #                             'affect_cor_list': wk.affect_cor_list.replace(str(rec.employee_id2.id), ''),
    #                             'affect_cor': wk.affect_cor.replace(str(rec.employee_id2.name), '')
    #                         })
    #                     else:
    #                         raise UserError(
    #                             _("Champs Intervenant vide ou employée n'existe pas dans liste des correcteurs"))
    #
    #                 if self.env.cr.dbname == 'DEMOddddddd':
    #                     sql = "SELECT field_250 FROM app_entity_26 WHERE id = %s"
    #                     self.env.cr.execute(sql, (wk.id,))
    #                     datas = self.env.cr.fetchone()
    #                     if datas:
    #                         sql1 = "UPDATE app_entity_26 SET field_269=%s WHERE id = %s"
    #                         self.env.cr.execute(sql1, ('', wk.id))
    #                         sql2 = "UPDATE app_entity_26 SET field_244=%s WHERE id = %s"
    #                         self.env.cr.execute(sql2, ('72', wk.id))
    #                     self.env.cr.commit()
    #             line_obj1.write({'state': 'draft'})
    #     if rec.mail_send == 'yes':
    #         if rec.note is False:
    #             rec.write({'note': ' '})
    #         if not rec.employee_ids:
    #             raise UserError(_("Vous devez sélectionner un destinataire."))
    #         else:
    #             kk = ''
    #             for line in rec.employee_ids.ids:
    #                 emp = emp_obj.browse(line)
    #                 kk += emp.work_email + ','
    #             rec.write({'to': kk})
    #             if rec.employee_ids1:
    #                 ll = ''
    #                 for line in rec.employee_ids1.ids:
    #                     emp = emp_obj.browse(line)
    #                     ll += emp.work_email + ','
    #                 rec.write({'cc': ll})
    #             if rec.employee_ids2:
    #                 mm = ''
    #                 for line in rec.employee_ids2.ids:
    #                     emp = emp_obj.browse(line)
    #                     mm += emp.work_email + ','
    #                 rec.write({'cci': mm})
    #     rec.write({'state': 'draft'})
    #     line_obj.write({'state': 'draft'})
    #     view = self.env['sh.message.wizard']
    #     view_id = view and view.id or False
    #
    #     return {
    #         'name': 'Affectation les Travaux',
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'base.invoices.merge.automatic.wizard',
    #         'res_id': rec.id,
    #         'context': {'default_state': 'draft'},
    #         'views': [(view_id, 'form')],
    #         'view_id': view_id,
    #         'target': 'new',
    #     }

        # return {
        #     'name': 'Annualtaion d"affectation faite avec Succès',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'sh.message.wizard',
        #     'views': [(view_id, 'form')],
        #     'view_id': view_id,
        #     'target': 'new',
        #     'context': self.env.context,
        # }

    def button_cancel(self):
        print("button cancel")
        work_obj = self.env['project.task.work']
        line_obj = self.env['base.invoices.merge.automatic.wizard']
        line_obj1 = self.env['base.invoices.merge.line']
        work_line = self.env['project.task.work']
        emp_obj = self.env['hr.employee']
        this = self

        for tt in this.work_ids:
            for msg_id in tt.ids:
                wk = work_obj.browse(msg_id)
                if this.types_affect == 'intervenant':
                    print('employee_id2:', this.employee_id2)
                    print('wk.affect_emp_list:', wk.affect_emp_list)
                    if this.employee_id2 and str(wk.affect_emp_list).find(
                            str(this.employee_id2.user_id.id)) != -1 and wk.state == 'affect':
                        work_line.write({'state': 'draft'})
                        work_line.write({
                            'job': '',
                            'current_emp': False,
                            'employee_id': False,
                            'state': 'draft',
                        })

                        work_obj.write({
                            'affect_emp_list': wk.affect_emp_list.replace(str(this.employee_id2.user_id.id), ''),
                            'affect_e_l': wk.affect_e_l.replace(str(this.employee_id2.user_id.login), ''),
                            'affect_emp': wk.affect_emp.replace(
                                str(this.employee_id2.name if this.employee_id2 else ''), ''),
                        })
                    else:
                        raise ValidationError(
                            _("Champs Intervenant vide ou employée n'existe pas dans liste des intervenants"))
                elif this.types_affect == 'controle':
                    if this.employee_id2 and str(wk.affect_con).find(str(this.employee_id2.name)) != -1:
                        work_obj.write({
                            'affect_con_list': wk.affect_con_list.replace(str(this.employee_id2.id), ''),
                            'affect_con': wk.affect_con.replace(str(this.employee_id2.name), ''),
                        })
                    else:
                        raise ValidationError(
                            _("Champs Intervenant vide ou employée n'existe pas dans liste des controleurs"))
                elif this.types_affect == 'correction':
                    if this.employee_id2 and str(wk.affect_cor).find(str(this.employee_id2.name)) != -1:
                        work_obj.write({
                            'affect_cor_list': wk.affect_cor_list.replace(str(this.employee_id2.id), ''),
                            'affect_cor': wk.affect_cor.replace(str(this.employee_id2.name), ''),
                        })
                    else:
                        raise ValidationError(
                            _("Champs Intervenant vide ou employée n'existe pas dans liste des correcteurs"))

                for rec in self:
                    if self.env.cr.dbname == 'DEMOddddddd':
                        sql = "SELECT field_250 FROM app_entity_26 WHERE id = %s"
                        self.env.cr.execute(sql, (wk.id,))
                        datas = self.env.cr.fetchone()

                        if datas:
                            sql1 = "UPDATE app_entity_26 SET field_269 = %s WHERE id = %s"
                            self.env.cr.execute(sql1, ('', wk.id))

                            sql2 = "UPDATE app_entity_26 SET field_244 = %s WHERE id = %s"
                            self.env.cr.execute(sql2, ('72', wk.id))

                        self.env.cr.commit()

                line_obj1.browse(tt.id).write({'state': 'draft'})

            # line_obj1.write({'state': 'draft'})

        if this.mail_send == 'yes':
            if not this.note:
                this.note = ' '
            if not this.employee_ids:
                raise ValidationError(_('Erreur ! Vous devez sélectionner un destinataire.'))
            else:
                kk = ''
                for line in this.employee_ids.ids:
                    emp = emp_obj.browse(line)
                    kk = kk + emp.work_email + ','
                this.to = kk
                if this.employee_ids1:
                    ll = ''
                    for line in this.employee_ids1.ids:
                        emp = emp_obj.browse(line)
                        ll = ll + emp.work_email + ','
                    this.cc = ll
                if this.employee_ids2:
                    mm = ''
                    for line in this.employee_ids2.ids:
                        emp = emp_obj.browse(line)
                        mm = mm + emp.work_email + ','
                    this.cci = mm

        this.state = 'draft'
        self.env['email.template'].sudo().browse(33).send_mail(this.id, force_send=True)

        line_obj.write({'state': 'draft'})

        view = self.env.ref('module_name.sh_message_sh_message_wizard')
        view_id = view and view.id or False

        return {
            'name': 'Affectation les Travaux',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'res_id': this.id,
            'context': {'default_state': 'draft'},
            'target': 'new',
            'domain': []
        }
    # def action_calendar(self, cr, uid, ids, context=None):
    #     current = ids[0]
    #     list = []
    #     l = []
    #     this = self.browse(cr, uid, current, context=context)
    #     if this.employee_id2:
    #         cr.execute('select id from project_task_work where employee_id= %s and state=%s',
    #                    (this.employee_id2.id, 'affect',))
    #         work_ids = cr.fetchall()
    #     else:
    #         dep = self.pool.get('hr.academic').search(cr, uid, [('categ_id', '=', this.categ_id.id)])
    #         if dep:
    #             for nn in dep:
    #                 em = self.pool.get('hr.academic').browse(cr, uid, nn).employee_id.id
    #
    #                 l.append(em)
    #         today_date = datetime.today()
    #         from_d = today_date - relativedelta(months=2)
    #         to_d = today_date + relativedelta(months=2)
    #
    #         cr.execute(
    #             'select id from project_task_work where employee_id in %s and state not in %s and employee_id is not null and date_start>=%s and date_start<=%s',
    #             (tuple(l), ('valid', 'cancel', 'pending'), from_d, to_d,))
    #         work_ids = cr.fetchall()
    #     ##     raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%len(work_ids))
    #     ##            raise osv.except_osv(_('Error !'), _('Vous devez sélectionner un employé pour consulter son calendrier'))
    #
    #     for tt in work_ids:
    #         list.append(tt)
    #
    #     return {
    #         'name': ('Calendrier Ressources'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'timeline',
    #         ##  'target'        :   'popup',
    #         'nodestroy': True,
    #
    #         'target': 'popup',
    #         'res_model': 'project.task.work',
    #         ## 'res_id': ids[0],
    #         'context': {'default_active_ids': list, 'default_ids': list},
    #         'domain': [('id', 'in', list)]
    #     }
    #
    # def action_calendar(self):
    #     current = self.ids[0]
    #     work_ids = []
    #     employee_id2 = self.employee_id2
    #
    #     if employee_id2:
    #         work_ids = self.env['project.task.work'].search(
    #             [('employee_id', '=', employee_id2.id), ('state', '=', 'affect')]).ids
    #     else:
    #         l = []
    #         dep = self.env['hr.academic'].search([('categ_id', '=', self.categ_id.id)])
    #         if dep:
    #             for nn in dep:
    #                 em = nn.employee_id.id
    #                 l.append(em)
    #
    #         today_date = datetime.today()
    #         from_d = today_date - relativedelta(months=2)
    #         to_d = today_date + relativedelta(months=2)
    #
    #         work_ids = self.env['project.task.work'].search([
    #             ('employee_id', 'in', l),
    #             ('state', 'not in', ('valid', 'cancel', 'pending')),
    #             ('employee_id', '!=', False),
    #             ('date_start', '>=', from_d),
    #             ('date_start', '<=', to_d)
    #         ]).ids
    #
    #     list_ids = work_ids
    #
    #     return {
    #         'name': ('Calendrier Ressources'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'timeline',
    #         'nodestroy': True,
    #         'target': 'popup',
    #         'res_model': 'project.task.work',
    #         'context': {
    #             'default_active_ids': list_ids,
    #             'default_ids': list_ids
    #         },
    #         'domain': [('id', 'in', list_ids)]
    #     }

    def button_save_(self):
        this = self
        work_obj = self.env['base.invoices.merge.automatic.wizard']
        work_line = self.env['project.task.work']

        for line in this.work_ids:
            line = line

        return {
            'name': ('Affectation les Travaux'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'res_id': this.id,
            'context': {},
            'domain': []
        }

    def button_load_mail(self):
        this = self
        work_obj = self.env['base.invoices.merge.automatic.wizard']
        kk = []

        if this.employee_id2 and this.employee_id2.id not in kk:
            kk.append(this.employee_id2.id)

        for jj in kk:
            self.env.cr.execute("INSERT INTO base_invoices_merge_automatic_wizard_hr_employee_rel VALUES (%s,%s)",
                                (this.id, jj))

        return {
            'name': ('Affectation les Travaux'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('eb_invoices_wizard.your_view_id').id,  # Replace with the actual view ID
            'target': 'new',
            'res_model': 'base.invoices.merge.automatic.wizard',
            'res_id': this.id,
            'domain': []
        }

    def message_(self):
        view = self.env.ref('sh_message.sh_message_wizard')  # Replace with the actual view ID

        return {
            'name': 'Affectation faite avec Succès',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': self.env.context
        }

    def button_approve(self):
        print("button_approve")
        line_obj = self.env['base.invoices.merge.automatic.wizard']
        line_obj1 = self.env['base.invoices.merge.line']
        work_line = self.env['project.task.work']
        wl = self.env['project.task.work.line']
        link_line = self.env['link.line']
        emp_obj = self.env['hr.employee']
        res_user = self.env['res.users'].browse(self.env.uid)
        this = self
        for line in this.work_ids:
            line = self.env['project.task.work'].browse(line.id)
            if this.employee_id2 and this.types_affect == 'intervenant' and line.state == 'draft':
                line.write({'state': 'affect'})

            for msg_id in line.ids:
                wk = self.env['project.task.work'].browse(msg_id)
                wk_histo = self.env['work.histo'].search([('work_id', '=', msg_id)])
                wk11 = ''
                wk21 = ''
                wk31 = ''
                wk1 = ''
                wk2 = ''
                wk3 = ''
                wk111 = ''

                if wk.affect_emp is False:
                    wk1 = ''
                else:
                    wk1 = wk.affect_emp or '' + ', '
                    wk11 = wk.affect_emp_list or '' + ', '
                    wk111 = wk.affect_e_l or '' + ', '

                if wk.affect_con is False:
                    wk2 = '0,'
                else:
                    wk2 = wk.affect_con or '' + ', '
                    wk21 = wk.affect_con_list or '' + ', '

                if wk.affect_cor is False:
                    wk3 = '0, '
                else:
                    wk3 = wk.affect_cor or '' + ', '
                    wk31 = wk.affect_cor_list or '' + ', '

                if this.employee_id2 and this.types_affect == 'intervenant':
                    if wk.state == 'draft':
                        wk.write({'state': 'affect'})

                    wk.write({
                        'affect_emp': wk1 + this.employee_id2.name,
                        'affect_emp_list': wk11 + str(this.employee_id2.user_id.id),
                        'affect_e_l': wk111 + str(this.employee_id2.user_id.login),
                        'current_emp': this.employee_id2.id,
                        'employee_id': this.employee_id2.id,
                        'display': True
                    })

                    if wk_histo:
                        if len(wk_histo) == 1:
                            wk_histo_id = wk_histo.id
                            self.env['work.histo.line'].create({
                                'type': 'affect_inter',
                                'execute_by': this.employee_id2.name,
                                'create_by': res_user.employee_id.name,
                                'work_histo_id': wk_histo_id,
                                'date': fields.Datetime.now(),
                                'coment1': this.note or False,
                                'id_object': self.ids[0],
                            })
                    else:
                        histo = self.env['work.histo'].create({
                            'task_id': wk.task_id.id,
                            'work_id': wk.id,
                            'categ_id': wk.categ_id.id,
                            'product_id': wk.product_id.id,
                            'name': wk.task_id.name,
                            'create_a': wk.date_start,
                            'date': wk.date_start,
                            'zone': wk.zo or 0,
                            'secteur': wk.sect or 0,
                            'project_id': wk.project_id.id,
                            'partner_id': wk.project_id.partner_id.id,
                        })
                        self.env['work.histo.line'].create({
                            'type': 'affect_inter',
                            'execute_by': this.employee_id2.name,
                            'create_by': res_user.employee_id.name,
                            'work_histo_id': histo.id,
                            'date': fields.Datetime.now(),
                            'coment1': this.note or False,
                            'id_object': self.ids[0],
                        })
                elif this.employee_id2 and this.types_affect == 'controle':
                    if wk.state == 'affect':
                        wk.write({'state': 'tovalidcont'})

                    wk.write({
                        'affect_con': wk2 + this.employee_id2.name,
                        'affect_con_list': wk21 + str(this.employee_id2.user_id.id),
                    })

                    if this.group_id:
                        this.group_id.write({'gest_id2': this.employee_id2.id, 'note_con': this.note})

                    if wk_histo:
                        if len(wk_histo) == 1:
                            wk_histo_id = wk_histo.id
                            self.env['work.histo.line'].create({
                                'type': 'affect_control',
                                'execute_by': this.employee_id2.name,
                                'create_by': res_user.employee_id.name,
                                'work_histo_id': wk_histo_id,
                                'date': fields.Datetime.now(),
                                'coment1': this.note or False,
                                'id_object': self.ids[0],
                            })
                    else:
                        histo = self.env['work.histo'].create({
                            'task_id': wk.task_id.id,
                            'work_id': wk.id,
                            'categ_id': wk.categ_id.id,
                            'product_id': wk.product_id.id,
                            'name': wk.task_id.name,
                            'date': wk.date_start,
                            'create_a': wk.date_start,
                            'zone': wk.zo or 0,
                            'secteur': wk.sect or 0,
                            'project_id': wk.project_id.id,
                            'partner_id': wk.project_id.partner_id.id,
                        })
                        self.env['work.histo.line'].create({
                            'type': 'affect_control',
                            'execute_by': this.employee_id2.name,
                            'create_by': res_user.employee_id.name,
                            'work_histo_id': histo.id,
                            'date': fields.Datetime.now(),
                            'coment1': this.note or False,
                            'id_object': self.ids[0],
                        })
                elif this.employee_id2 and this.types_affect == 'correction':
                    wk.write({
                        'state': 'affect_corr',
                        'affect_cor': wk3 + this.employee_id2.name,
                        'affect_cor_list': wk31 + str(this.employee_id2.user_id.id),
                    })

                    if this.group_id:
                        this.group_id.write({'emp_id2': this.employee_id2.id, 'note_corr': this.note})

                    if wk_histo:
                        if len(wk_histo) == 1:
                            wk_histo_id = wk_histo.id
                            self.env['work.histo.line'].create({
                                'type': 'affect_corr',
                                'execute_by': this.employee_id2.name,
                                'create_by': res_user.employee_id.name,
                                'work_histo_id': wk_histo_id,
                                'date': fields.Datetime.now(),
                                'coment1': this.note or False,
                                'id_object': self.ids[0],
                            })
                    else:
                        histo = self.env['work.histo'].create({
                            'task_id': wk.task_id.id,
                            'work_id': wk.id,
                            'categ_id': wk.categ_id.id,
                            'product_id': wk.product_id.id,
                            'name': wk.task_id.name,
                            'date': wk.date_start,
                            'create_a': wk.date_start,
                            'zone': wk.zo or 0,
                            'secteur': wk.sect or 0,
                            'project_id': wk.project_id.id,
                            'partner_id': wk.project_id.partner_id.id,
                        })
                        self.env['work.histo.line'].create({
                            'type': 'affect_corr',
                            'execute_by': this.employee_id2.name,
                            'create_by': res_user.employee_id.name,
                            'work_histo_id': histo.id,
                            'date': fields.Datetime.now(),
                            'coment1': this.note or False,
                            'id_object': self.ids[0],
                        })

                if this.date_start_r:
                    wk.write({'date_start': this.date_start_r})
                if this.name:
                    wk.write({'job': this.name})
                if this.date_end_r:
                    wk.write({'date_end': this.date_end_r})
                if this.poteau_t:
                    wk.write({'poteau_t': this.poteau_t})
                if this.ftp:
                    link_id = {
                        'name': 'FTP Affectation',
                        'ftp': this.ftp,
                        'work_id': wk.id
                    }
                    one = link_line.create(link_id)
                if this.note:
                    wk.write({'note': this.note})
                if wk.employee_id:
                    self._cr.execute('update project_task_work set current_emp =%s where id=%s ',
                                     (wk.employee_id.id, wk.id))
                    result = {}

            self.write({'state': 'affect'})

            vals = self.time_ch.split(':')
            t, hours = divmod(float(vals[0]), 24)
            t, minutes = divmod(float(vals[1]), 60)
            minutes = minutes / 60.0

            total = hours + minutes

            res_user = self.env['res.users'].browse(self._uid)
            if self.work_ids:
                for rec in self.work_ids[0]:
                    base_group = self.env['base.group.merge.automatic.wizard'].create({
                        'create_date': fields.Date.today(),
                        'date_start_r': fields.Date.today(),
                        'project_id': rec.project_id.id,
                        'zo': rec.zone,
                        'sect': rec.secteur,
                        'gest_id': rec.gest_id.id,
                        'state': 'valid',
                        'active': True,
                        'name': 'gestion affectation'
                    })
                    base_group_id = base_group.id

                    product = 80  # Default value
                    if rec.categ_id.id == 3:
                        product = 156
                    elif rec.categ_id.id == 1:
                        product = 80
                    elif rec.categ_id.id == 4:
                        product = 218
                    elif rec.categ_id.id == 6:
                        product = 174
                    elif rec.categ_id.id == 7:
                        product = 197
                    elif rec.categ_id.id == 8:
                        product = 132
                    elif rec.categ_id.id == 5:
                        product = 132

                    self.env['base.group.merge.line'].create({
                        'create_date': fields.Date.today(),
                        'date_start_r': fields.Date.today(),
                        'date_end_r': fields.Date.today(),
                        'product_id': product,
                        'project_id': rec.project_id.id,
                        'hours_r': total,
                        'uom_id_r': 5,
                        'uom_id': 5,
                        'wizard_id': base_group_id,
                        'color1': 1,
                        'employee_id': res_user.employee_id.id,
                        'categ_id': rec.categ_id.id,
                        'zone': rec.zone or 0,
                        'secteur': rec.secteur or 0
                    })

                    move_line = {
                        'employee_id': res_user.employee_id.id,
                        'state': 'valid',
                        'work_id': rec.id,
                        'task_id': rec.task_id.id,
                        'sequence': rec.sequence,
                        'uom_id': 5,
                        'date_start_r': fields.Date.today(),
                        'date_end_r': fields.Date.today(),
                        'categ_id': rec.categ_id.id,
                        'hours_r': total,
                        'color1': 1,
                        'project_id': rec.project_id.id,
                        'gest_id': rec.gest_id.id,
                        'zone': rec.zone,
                        'secteur': rec.secteur,
                    }
                    self.env['base.invoices.merge.automatic.wizard'].create(move_line)

            # if self.mail_send == 'yes':
            #     if not self.note:
            #         self.note = ' '
            #     if not self.employee_ids:
            #         raise ValidationError(_('Erreur ! Vous devez sélectionner un destinataire.'))
            #     else:
            #         kk = ''
            #         for line in self.employee_ids.ids:
            #             emp = self.env['hr.employee'].browse(line)
            #             kk = kk + emp.work_email + ','
            #         self.to = kk
            #         if self.employee_ids1:
            #             ll = ''
            #             for line in self.employee_ids1.ids:
            #                 emp = self.env['hr.employee'].browse(line)
            #                 ll = ll + emp.work_email + ','
            #             self.cc = ll
            #         if self.employee_ids2:
            #             mm = ''
            #             for line in self.employee_ids2.ids:
            #                 emp = self.env['hr.employee'].browse(line)
            #                 mm = mm + emp.work_email + ','
            #             self.cci = mm
            #
            # if self.employee_id2 and self.types_affect == 'intervenant':
            #     self.env['mail.template'].sudo().browse(25).send_mail(self.id, force_send=True)
            #     ##Ne pas oublier d'ajouter la condition par bon
            # elif self.employee_id2 and self.types_affect == 'controle' and self.group_id:
            #     self.env['mail.template'].sudo().browse(30).send_mail(self.id, force_send=True)
            # elif self.employee_id2 and self.types_affect == 'controle' and not self.group_id:
            #     self.env['mail.template'].sudo().browse(34).send_mail(self.id, force_send=True)
            # elif self.employee_id2 and self.types_affect == 'correction' and self.group_id:
            #     self.env['mail.template'].sudo().browse(31).send_mail(self.id, force_send=True)
            # elif self.employee_id2 and self.types_affect == 'correction' and not self.group_id:
            #     self.env['mail.template'].sudo().browse(35).send_mail(self.id, force_send=True)
            #
            # for rec in self.work_ids:
            #     for line in self.link_ids:
            #         self.env['link.line'].create({
            #             'ftp': line.ftp,
            #             'name': line.name,
            #             'work_id': rec.id,
            #             'affect_id': line.id,
            #             'source': 'affectation',
            #             'id_record': self.id
            #         })

            return {
                'name': 'Affectation les Travaux',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'base.invoices.merge.automatic.wizard',
                'res_id': self.id,
                'context': {'default_state': 'affect'},
            }


class ProjectTaskWorkLine(models.Model):
    _inherit = 'project.task.work.line'

    wizard_id = fields.Many2one('base.invoices.merge.automatic.wizard', string='Event')

