# def default_get(self, fields_list):
#     # print('default_get', default_get)
#     move_line1 = []
#     res = super(EbMergegroups, self).default_get(fields_list)
#     # print('before', res)
#     active_ids = self.env.context.get('active_ids')
#     # print('active_ids', active_ids, 'active_model', self.env.context.get('active_model'))
#     if self.env.context.get('active_model') == 'project.task.work' and active_ids:
#         vv = []
#
#         for active_id in active_ids:
#             work = self.env['project.task.work'].browse(active_id)
#             dd = []
#             if work.kit_id:  # we will note enter in this bloc (not kit)
#                 kit_list = self.env['project.task.work'].search(
#                     [('project_id', '=', work.project_id.id), ('zone', '=', work.zone)
#                         , ('secteur', '=', work.secteur), ('kit_id', '=', work.kit_id.id),
#                      ('product_id.name', 'not ilike', '%correction%'), ('product_id.name', 'not ilike', '%cont%')
#                         , ('product_id.name', 'not ilike', '%gestion client%')
#                      ])
#                 for kit_list_id in kit_list.ids:
#
#                     work1 = self.env['project.task.work'].browse(kit_list_id)
#                     if work.is_copy is False:
#                         if work1.is_copy is False:
#                             if work1.id not in vv:
#                                 vv.append(work1.id)
#                     else:
#                         if work1.is_copy is not False:
#                             if work1.rank == work1.rank:
#                                 if work1.id not in vv:
#                                     vv.append(work1.id)
#                 res['work_ids'] = vv
#             else:
#                 res['work_ids'] = active_ids
#             #  print('res', res)
#             r = []
#             pref = ''
#             test = ''
#             list = []
#             list1 = []
#             proj = []
#             gest_id2 = False
#             emp_id2 = False
#             for jj in active_ids:
#
#                 work = self.env['project.task.work'].browse(jj)
#                 #  user = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).id to_verify (correct one)
#                 user = self.env['hr.employee'].search([('id', '=', self.env.user.id)], limit=1).id
#                 user1 = self.env.user.id
#                 if work.project_id.id not in proj:
#                     proj.append(work.project_id.id)
#
#                 ##                tt=self.env['project.task.work.line'].search([('work_id','=',jj),('state','=','affect')]).ids
#                 # print(work.state)
#                 if work.state == 'pending':
#                     raise UserError('Action impossible,Travaux Suspendus!')
#                 if work.state == 'draft':
#                     raise UserError('Action impossible, Travaux Non Affectés!')
#                 if len(proj) > 1:
#                     raise UserError('Action impossible, Déclaration se fait uniquement sur un projet!')
#                 if len(active_ids) > 1:
#                     pref = '/'
#                 done = 0
#                 if work.gest_id.user_id.id == self.env.user.id or self.env.user.id == 1:
#                     done = 1
#                 else:
#                     done = 0
#                 done1 = 0
#                 if work.employee_id.user_id.id == self.env.user.id or self.env.user.id == 1:
#                     done1 = 1
#                 else:
#                     done1 = 0
#                 if work.affect_cor_list and str(user1) in work.affect_cor_list:
#                     type1 = 'correction'
#                     emp_id2 = user
#
#                 elif work.affect_con_list and str(user1) in work.affect_con_list:
#                     type1 = 'controle'
#                     gest_id2 = user
#                 else:
#                     type1 = 'bon'
#                     # print('work.state:', work.state)
#                     if work.state == 'close':
#                         raise UserError('Action impossible, Travaux Cloturés!')
#                     if work.state == 'valid':
#                         raise UserError('Action impossible, Travaux Terminés!')
#                 # raise osv.except_osv(_('Action impossible!'),_("%s")%user)
#                 test = test + pref + str(work.project_id.name) + ' - ' + str(work.task_id.sequence) + ' - ' + str(
#                     work.sequence)
#                 res.update({'states': test, 'employee_id': work.employee_id.id,
#                             'gest_id': work.gest_id.id,
#                             'project_id': work.project_id.id,
#                             'zo': work.zo, 'sect': work.sect, 'categ_id': work.categ_id.id,
#                             'coordin_id': work.gest_id3.id, 'coordin_id1': work.coordin_id1.id,
#                             'coordin_id2': work.coordin_id2.id, 'coordin_id3': work.coordin_id3.id,
#                             'coordin_id4': work.coordin_id4.id, 'coordin_id5': work.coordin_id5.id,
#                             'type1': type1, 'gest_id2': gest_id2, 'emp_id2': emp_id2})
#                 ##for kk in tt:
#                 ##  pr_lines.append((0,0, {gest_id3
#                 values = {}
#
#                 art = {}
#
#                 ##newline= self.env['project.task.work.line'].create(
#                 ##'aggr_ids': line.id,
#                 list_intervention = []
#                 # print("middle :", res)
#                 poteau = 0
#
#                 tt = self.env['project.task.work'].search([
#                     ('project_id', '=', work.project_id.id),
#                     ('categ_id', '=', work.categ_id.id),
#                     # correct : uncomment    to_verify
#                     # ('name', 'ilike', 'qualit'),
#                     ('etape', '=', work.etape)
#                 ]
#                 ).ids
#                 for ji in tt:
#                     work = self.env['project.task.work'].browse(ji)
#                     move_line1 = {
#                         'product_id': work.product_id.id,
#                         'employee_id': work.gest_id.id,
#                         'state': 'draft',
#                         'work_id': work.id,
#                         'task_id': work.task_id.id,
#                         'categ_id': work.categ_id.id,
#                         ##'hours': work.hours,
#                         'date_start_r': work.date_start_r,
#                         'date_end_r': work.date_end_r,
#                         'poteau_t': work.poteau_t,
#                         'poteau_r': poteau,
#                         ##'poteau_r': work.poteau_r,
#                         ## 'hours_r': work.hours_r,
#                         ##'color1': work.color1,
#                         ## 'total_t':work.color1*7 ,  ##*work.employee_id.contract_id.wage
#
#                         # 'project_id': work.task_id.project_id.id, The correct one
#                         'project_id': work.project_id.id,
#
#                         ##'amount_line': work.employee_id.contract_id.wage*work.hours_r,
#                         ## 'wage': work.employee_id.contract_id.wage,
#                         'gest_id': work.gest_id.id,
#                         'uom_id': work.uom_id.id,
#                         'uom_id_r': work.uom_id_r.id,
#
#                         'zone': work.zone,
#                         'secteur': work.secteur,
#
#                     }
#                 if tt:
#                     list1.append([0, 0, move_line1])
#                 for task in active_ids:
#                     work = self.env['project.task.work'].browse(task)
#                     context = self._context
#                     current_uid = context.get('uid')
#                     res_user = self.env['res.users'].browse(current_uid)
#                     categ_ids = self.env['hr.academic'].search([('employee_id', '=', res_user.employee_id.id)])
#                     jj = []
#                     if categ_ids:
#                         for ll in categ_ids.ids:
#                             dep = self.env['hr.academic'].browse(ll)
#                             jj.append(dep.categ_id.id)
#                     # if work.categ_id.id not in jj:
#                     #     raise UserError(
#                     #         'Action impossible!, Vous n\'etes pas autorisé à exécuter cette action sur un '
#                     #         'département externe')
#             # the codes above are hard coded, need to be deleted after
#             # res = {'date_start_r': '2023-06-03', 'done1': True, 'state': 'draft', 'state1': 'draft'}
#             res['work_ids'] = list1
#     # print('after', res)  # to_remove
#     return res
#
#
# class project_work(osv.osv):
#     _name = "project.task.work"
#     _description = "Project Task Work"
#
#     def default_get(self, cr, uid, ids, context=None):
#         res = {}
#         next_sequence = 10000
#         done = 0
#         done1 = 0
#         r = []
#         if cr.dbname == 'TEST95':
#             connection = py.connect(host='localhost',
#                                     user='root',
#                                     passwd='',
#                                     db='rukovoditel_en', use_unicode=True, charset="utf8")
#             cursor = connection.cursor()
#         if context:
#             context_keys = context.keys()
#             next_sequence = 1
#             if 'work_ids' in context_keys:
#                 if len(context.get('work_ids')) > 0:
#                     next_sequence = next_sequence + len(context.get('work_ids')) * 10
#             done = 0
#             done = 1
#             for rec in self.browse(cr, uid, ids, context=context):
#
#                 if rec.line_ids.wizard_id:
#                     done = 1
#                 if rec.line_ids.paylist_id:
#                     done1 = 1
#
#         res.update({'sequence': next_sequence, 'done': done})
#         return res
#
#     def _default_done(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         ##
#
#         for rec in self.browse(cr, uid, ids, context=context):
#             if cr.dbname == 'TEST95':
#
#                 if rec.product_id.is_gantt is True:
#
#                     sql = ("select field_250 from app_entity_26 WHERE id = %s")
#                     cr.execute(sql, (rec.id,))
#                     datas = cr.fetchone()
#
#                     if datas and datas[0] > 1:
#                         ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
#                         temp = datetime.fromtimestamp(int(datas[0])).strftime('%Y-%m-%d')
#
#                         cr.execute('update project_task_work set date_start=%s where id=%s', (temp, rec.id))
#                         ##cr.execute('update project_task_work set  date_start=%s where  id = %s ' , (date_start,ids[0]))
#                     sql1 = ("select field_251 from app_entity_26 WHERE id = %s")
#                     cr.execute(sql1, (rec.id,))
#                     datas1 = cr.fetchone()
#
#                     if datas1 and datas1[0] > 1:
#                         ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
#                         temp1 = datetime.fromtimestamp(int(datas1[0])).strftime('%Y-%m-%d')
#                         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
#                         cr.execute('update project_task_work set date_end=%s where id=%s', (temp1, rec.id))
#                     sql2 = ("select field_269 from app_entity_26 WHERE id = %s")
#                     cr.execute(sql2, (rec.id,))
#                     datas2 = cr.fetchone()
#
#                     if datas2 and datas2[0] > 1:
#
#                         ##tt=time.strftime("%Y-%m-%d", time.localtime(int(datas[0]))) ()
#                         if datas2 != '':
#                             temp2 = datas2[0]
#                             ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%tt)
#                             cr.execute('update project_task_work set employee_id=%s where id=%s',
#                                        (temp2 or None, rec.id))
#
#             if rec.line_ids:
#
#                 for kk in rec.line_ids.ids:
#
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.done is True:
#                         result[rec.id] = 1
#                         break
#                     else:
#                         result[rec.id] = 0
#             ##                        exit
#             ##                    else:
#             ##                        result[rec.id] =0
#             else:
#                 result[rec.id] = 0
#
#         return result
#
#     def _default_done1(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#
#         for rec in self.browse(cr, uid, ids, context=context):
#             if rec.line_ids:
#
#                 for kk in rec.line_ids.ids:
#
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.done1 is True:
#                         result[rec.id] = 1
#                         break
#                     else:
#                         result[rec.id] = 0
#             ##                        exit
#             ##                    else:
#             ##                        result[rec.id] =0
#             else:
#                 result[rec.id] = 0
#
#         return result
#
#     def _default_done2(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#
#         for rec in self.browse(cr, uid, ids, context=context):
#             if rec.line_ids:
#
#                 for kk in rec.line_ids.ids:
#
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.group_id:
#                         result[rec.id] = 1
#                         break
#
#                     else:
#                         result[rec.id] = 0
#
#             ##                        exit
#             ##                    else:
#             ##                        result[rec.id] =0
#             else:
#                 result[rec.id] = 0
#
#         return result
#
#     def _default_done3(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#
#         for rec in self.browse(cr, uid, ids, context=context):
#             if rec.line_ids:
#
#                 for kk in rec.line_ids.ids:
#
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.group_id2:
#                         result[rec.id] = 1
#                         break
#
#                     else:
#                         result[rec.id] = 0
#
#             ##                        exit
#             ##                    else:
#             ##                        result[rec.id] =0
#             else:
#                 result[rec.id] = 0
#
#         return result
#
#     def _default_flow(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         current = ids[0]
#         list = []
#         for rec in self.browse(cr, uid, ids, context=context):
#             cr.execute('select id from base_flow_merge_line where work_id= %s', (rec.id,))
#             work_ids = cr.fetchone()
#             if work_ids:
#                 result[rec.id] = 1
#             else:
#                 result[rec.id] = 0
#
#         return result
#
#     def _check_color(self, cr, uid, ids, field_name, arg, context):
#
#         res = {}
#         for record in self.browse(cr, uid, ids, context):
#             color = 0
#             if record.statut in ('Soumise', 'A l''étude', 'Envoyé'):
#                 color = 9
#             elif record.statut in (u'Approuvé Partiel', u'Approuvé'):
#                 color = 5
#             elif record.statut in ('Refus Partiel', u'Refusé'):
#                 color = 2
#             elif record.statut == u'Incomplet':
#                 color = 3
#             elif record.statut in ('9032', u'Déviation', u'En résiliation'):
#                 color = 7
#             elif record.statut in ('Encours', '', 'Sans valeur'):
#                 color = 6
#             elif record.statut in ('Non requis', 'Annulé'):
#                 color = 1
#             elif record.statut == u'Travaux Prép.':
#                 color = 8
#
#             res[record.id] = color
#         return res
#
#     def _get_planned(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         cr.execute(
#             "SELECT work_id, COALESCE(SUM(hours_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
#             (tuple(ids),))
#         hours = dict(cr.fetchall())
#         ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
#         for rec in self.browse(cr, uid, ids, context=context):
#             result[rec.id] = hours.get(rec.id, 0.0)
#         return result
#
#     def _get_sum(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         ##cr.execute("SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE state in %s and project_task_work_line.work_id IN %s GROUP BY work_id",(('valid','paid'),tuple(ids),))
#         cr.execute(
#             "SELECT work_id, COALESCE(SUM(total_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
#             (tuple(ids),))
#
#         hours = dict(cr.fetchall())
#         ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
#         for rec in self.browse(cr, uid, ids, context=context):
#             result[rec.id] = hours.get(rec.id, 0.0)
#         return result
#
#     def _get_qty(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         cr.execute(
#             "SELECT work_id, COALESCE(SUM(poteau_r), 0.0) FROM project_task_work_line WHERE project_task_work_line.work_id IN %s GROUP BY work_id",
#             (tuple(ids),))
#         hours = dict(cr.fetchall())
#         ##,COALESCE(SUM(total_hours), 0.0), COALESCE(SUM(effective_hours), 0.0)
#         for rec in self.browse(cr, uid, ids, context=context):
#             result[rec.id] = hours.get(rec.id, 0.0)
#         return result
#
#     def _get_qty_r_affect(self, cr, uid, ids, field_name, arg, context=None):
#
#         x = {}
#         for record in self.browse(cr, uid, ids):
#             cr.execute(
#                 "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
#                 (record.task_id.id, str(record.zone), str(record.secteur)))
#             q3 = cr.fetchone()
#             ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%record.zone)
#             if q3:
#                 x[record.id] = record.poteau_i - q3[0]
#             else:
#                 x[record.id] = record.poteau_i
#         return x
#
#     def _get_qty_affect(self, cr, uid, ids, field_name, arg, context=None):
#
#         x = {}
#         for record in self.browse(cr, uid, ids):
#             cr.execute(
#                 "select COALESCE(SUM(poteau_t), 0.0) from project_task_work where task_id=%s and cast(zone as varchar) =%s and cast(secteur as varchar) =%s and state in ('affect','tovalid','valid')",
#                 (record.task_id.id, str(record.zone), str(record.secteur)))
#             q3 = cr.fetchone()
#             ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%record.zone)
#             if q3:
#                 x[record.id] = q3[0]
#             else:
#                 x[record.id] = 0
#         return x
#
#     def get_domain_useer_id(self, cr, uid, ids, context=None):
#         mach = []
#         lids = self.pool.get('hr.employee').search(cr, uid, [('id', '=', 37)])
#         return {'domain': {'employee_id': [('id', 'in', lids)]}}
#
#     def _disponible(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         for book in self.browse(cr, uid, ids, context=context):
#             if book.gest_id and book.gest_id.user_id:
#                 if book.gest_id.user_id.id == uid or uid == 1 or 100 in book.gest_id.user_id.groups_id.ids:  ##or book..user_id.id==uid:
#                     result[book.id] = True
#                 else:
#                     result[book.id] = False
#             else:
#                 result[book.id] = False
#         return result
#
#     def _isinter(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         current = self.browse(cr, uid, ids, context=context)
#         for book in current:
#             result[book.id] = False
#             if book.line_ids:
#                 tt = []
#                 for kk in book.line_ids.ids:
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.group_id2:
#                         if rec_line.group_id2.ids not in tt:
#                             tt.append(rec_line.group_id2.ids)
#                 if tt:
#                     for kk in tt:
#                         cr.execute('update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
#                                    (uid, tuple(kk)))
#                     test = self.pool.get('base.group.merge.automatic.wizard').search(cr, uid, [('id', 'in', tt), (
#                         'state', '<>', 'draft')])
#                     if test:
#                         result[book.id] = True
#         return result
#
#     def _iscontrol(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         current = self.browse(cr, uid, ids, context=context)
#         for book in current:
#             result[book.id] = False
#             if book.line_ids:
#                 tt = []
#                 for kk in book.line_ids.ids:
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.group_id2:
#                         if rec_line.group_id2.id not in tt:
#                             tt.append(rec_line.group_id2.id)
#                 if tt:
#
#                     test = self.pool.get('base.group.merge.automatic.wizard').search(cr, uid, [('id', 'in', tt), (
#                         'state1', '<>', 'draft')])
#
#                     if test:
#                         result[book.id] = True
#
#                     test1 = self.pool.get('project.task.work.line').search(cr, uid,
#                                                                            [('work_id2', '=', book.id or False)])
#                     ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%test1)
#                     if test1:
#                         for jj in test1:
#                             rec_line = self.pool.get('project.task.work.line').browse(cr, uid, jj, context=context)
#                             if rec_line.group_id2:
#                                 if rec_line.group_id2.id not in tt:
#                                     tt.append(rec_line.group_id2.id)
#                         result[book.id] = True
#
#         return result
#
#     def _iscorr(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#         current = self.browse(cr, uid, ids, context=context)
#         for book in current:
#             result[book.id] = False
#             if book.line_ids:
#                 tt = []
#                 for kk in book.line_ids.ids:
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                     if rec_line.group_id2:
#                         if rec_line.group_id2.ids not in tt:
#                             tt.append(rec_line.group_id2.ids)
#                 if tt:
#                     for kk in tt:
#                         cr.execute('update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
#                                    (uid, tuple(kk)))
#                     test = self.pool.get('base.group.merge.automatic.wizard').search(cr, uid, [('id', 'in', tt), (
#                         'state2', '<>', 'draft')])
#                     if test:
#                         result[book.id] = True
#                     test1 = self.pool.get('project.task.work.line').search(cr, uid,
#                                                                            [('work_id2', '=', book.id or False)])
#                     if test1:
#                         for jj in test1:
#                             rec_line = self.pool.get('project.task.work.line').browse(cr, uid, jj, context=context)
#                             if rec_line.group_id2:
#                                 if rec_line.group_id2.id not in tt:
#                                     tt.append(rec_line.group_id2.id)
#                         result[book.id] = True
#         return result
#
#     def _invoice_num(self, cr, uid, ids, field_name, arg, context=None):
#         result = {}
#
#         for rec in self.browse(cr, uid, ids, context=context):
#             ##raise osv.except_osv(_('Errorfgggggggggg !'),_('%s')%(hours.get(rec.id, '')))
#             tt = ''
#             ##            cr.execute(
#             ##            "SELECT project_id, num FROM project_task_work_line WHERE project_task_work_line.project_id = %s order BY project_id",
#             ##            (tuple(rec.id)),)
#             cr.execute(
#                 'SELECT id FROM project_task_work_line WHERE project_task_work_line.work_id = %s order BY work_id',
#                 (rec.id,))
#             hours = cr.fetchall()
#             ## raise osv.except_osv(_('Errorfgggggggggg !'),_('%s')%(hours))
#             for jj in hours:
#                 pp = self.pool.get('project.task.work.line').browse(cr, uid, jj, context=context)
#
#                 if pp.num and pp.num not in tt:
#                     tt = tt + ',' + pp.num
#             result[rec.id] = tt
#
#         ##                else:
#         ##                    result[rec.id] = hours.get(rec.id, '')
#         return result
#
#     _columns = {
#         'fact_num': fields.function(_invoice_num, type='char', string='done'),
#         'name': fields.char('Nom Service', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'ftp': fields.char('Ftp', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'job': fields.char('Job', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'date': fields.datetime('Date Doc', select="1", readonly=True, states={'draft': [('readonly', False)]}, ),
#         'date_r': fields.datetime('N.U', select="1", readonly=True, states={'draft': [('readonly', False)]}, ),
#         'date_p': fields.date('N.U', select="1"),
#         'date_start': fields.date('Date Début', select="1", readonly=True, states={'draft': [('readonly', False)]}, ),
#         'date_end': fields.date('Date Fin', select="1", readonly=True, states={'draft': [('readonly', False)]}, ),
#         'date_start_r': fields.date('Date Début Réelle', select="1", readonly=True,
#                                     states={'affect': [('readonly', False)]}, ),
#         'ex_state': fields.char('ex'),
#         'date_end_r': fields.date('Date Fin Réelle', select="1", readonly=True,
#                                   states={'affect': [('readonly', False)]}, ),
#
#         'r_id': fields.many2one('risk.management.category', 'N.U', readonly=True,
#                                 states={'draft': [('readonly', False)]}, ),
#         'project_id': fields.many2one('project.project', 'Project', ondelete='set null', select=True,
#                                       track_visibility='onchange', change_default=True, readonly=True,
#                                       states={'draft': [('readonly', False)]}, ),
#         'task_id': fields.many2one('project.task', 'Activités', ondelete='cascade', required=True, select="1",
#                                    readonly=True, states={'draft': [('readonly', False)]}, ),
#         'product_id': fields.many2one('product.product', 'T. de Service', ondelete='cascade', select="1",
#                                       readonly=True, states={'draft': [('readonly', False)]}, ),
#         'hours': fields.float('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'etape': fields.char('Etape', readonly=True, states={'draft': [('readonly', False)]}, ),
#         ## 'hours_r': fields.float('Time Spent',readonly=True, states={'draft':[('readonly',False)]},),
#         'categ_id': fields.many2one('product.category', string='Département', readonly=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         'hours_r': fields.function(_get_planned, type='float', string='Company Currency', readonly=True,
#                                    states={'draft': [('readonly', False)]}, ),
#         'partner_id': fields.many2one('res.partner', 'Clients', readonly=True,
#                                       states={'draft': [('readonly', False)]}, ),
#         'kit_id': fields.many2one('product.kit', 'Task', ondelete='cascade', select="1",
#                                   readonly=True, states={'draft': [('readonly', False)]}, ),
#
#         'total_t': fields.float('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'total_r': fields.function(_get_sum, type='float', string='Company Currency', readonly=True,
#                                    states={'draft': [('readonly', False)]}, ),
#         'poteau_t': fields.float('Qté Prévue', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'poteau_i': fields.float('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'poteau_r': fields.function(_get_qty, type='float', string='Company Currency', readonly=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         'poteau_da': fields.function(_get_qty_affect, type='float', string='Company Currency', readonly=True,
#                                      states={'draft': [('readonly', False)]}, ),
#         'poteau_ra': fields.function(_get_qty_r_affect, type='float', string='Company Currency', readonly=True,
#                                      states={'draft': [('readonly', False)]}, ),
#         'poteau_reste': fields.integer('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'total_part': fields.selection([
#             ('partiel', 'Partiel'),
#             ('total', 'Total'),
#         ],
#             'N.U', copy=False, readonly=True, states={'draft': [('readonly', False)]}, ),
#         'sequence': fields.integer('Sequence', select=True, readonly=True, states={'draft': [('readonly', False)]}, ),
#         'state_id': fields.many2one('res.country.state', 'Cité/Ville'),
#
#         'city': fields.char('N.U', readonly=True),
#         'state_id1': fields.many2one('res.country.state', 'N.U'),
#         'state_id2': fields.many2one('res.country.state', 'N.U'),
#         'precision': fields.char('Precision(P)'),
#         'permis': fields.char('Permis(P)'),
#         'date_fin': fields.date('Date Fin (P)'),
#         'prolong': fields.char('Prolongation demandée(P)'),
#         'remarque': fields.text('Remarque'),
#         'date_remis': fields.date('Date Remis(P)'),
#         'date_construt': fields.date('Date Constrution(P)'),
#         'secteur_en': fields.char('Secteur Enfui(P)'),
#         'graphe_t_b': fields.char('Graphe_t_b(P)'),
#         'dct': fields.char('Dct(P)'),
#         'active': fields.boolean('Active'),
#         'anomalie': fields.char('Anomalie(P)'),
#         'action': fields.char('Action(P)'),
#         'pourc_t': fields.float('% Avancement', readonly=True, states={'draft': [('readonly', False)]}, ),
#
#         'pourc_f': fields.float('% Dépense', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'statut1': fields.many2one('project.status', string='Status', select=True),
#         'statut': fields.selection([('Encours', 'Encours'),
#                                     ('Soumise', 'Soumise'),
#                                     ('A l"Etude', 'A l"étude'),
#                                     ('Approuve', 'Approuvé'),
#                                     ('Incomplet', 'Incomplet'),
#                                     ('En Construction', 'En Construction'),
#                                     ('Envoye', 'Envoyé'),
#                                     ('Travaux Pre.', 'Travaux Pré.'),
#                                     ('Refuse', 'Refusé'),
#                                     ('Refus Partiel', 'Refus Partiel'),
#                                     ('Approuve Partiel', 'Approuvé Partiel'),
#                                     ('Travaux Complété', 'Travaux Complété'),
#                                     ('Inspection', 'Inspection'),
#                                     ('Annule', 'Annulé'),
#                                     ('En Resiliation', 'En Résiliation'),
#                                     ('Non Requis', 'Non Requis'),
#                                     ('En TP-derogation approuvee', 'En TP-dérogation approuvée'),
#                                     ('TP completes-avec refus', 'TP complétés-avec refus'),
#
#                                     ('Deviation', 'Déviation'),
#                                     ('9032', 'Approbation demandeur'),
#                                     ('DA', 'Approbation demandeur – Dérogation Approuvé'),
#                                     ('DP', 'Approbation demandeur – Dérogation Partielle'),
#                                     ('DR', 'Approbation demandeur – Dérogation Refusé'),
#                                     ('AD', 'Approbation demandeur – ADR Défavorable'),
#                                     ('TPDP', 'En TP - Dérogation Partielle'),
#                                     ('TPSD', 'En TP - Sans Dérogation'),
#                                     ],
#                                    'Status', copy=False),
#
#         'kanban_color': fields.function(_check_color, 'Couleur', type="integer"),
#         'link_id': fields.one2many('link.type', 'work_id', 'Work done'),
#
#         'zone': fields.integer('Zone (entier)', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'secteur': fields.integer('Secteur (entier)', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'zo': fields.char('Zone', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'sect': fields.char('Secteur', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'user_id': fields.many2one('res.users', 'N.U', select="1", readonly=True,
#                                    states={'draft': [('readonly', False)]}, ),
#         'paylist_id': fields.many2one('hr.payslip', 'N.U', select="1", readonly=True,
#                                       states={'draft': [('readonly', False)]}, ),
#         'gest_id': fields.many2one('hr.employee', 'Coordinateur', readonly=True,
#                                    states={'draft': [('readonly', False)]}, ),
#         'reviewer_id1': fields.many2one('hr.employee', 'Superviseur1', readonly=True,
#                                         states={'draft': [('readonly', False)]}, ),
#         'gest_id2': fields.many2one('hr.employee', 'Coordinateur2', readonly=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         'coordin_id1': fields.many2one('hr.employee', 'Coordinateur1', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id2': fields.many2one('hr.employee', 'Coordinateur2', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id3': fields.many2one('hr.employee', 'Coordinateur3', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id4': fields.many2one('hr.employee', 'Coordinateur4', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id5': fields.many2one('hr.employee', 'Coordinateur5', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id6': fields.many2one('hr.employee', 'Coordinateur6', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id7': fields.many2one('hr.employee', 'Coordinateur7', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id8': fields.many2one('hr.employee', 'Coordinateur8', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id9': fields.many2one('hr.employee', 'Coordinateur9', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'coordin_id10': fields.many2one('hr.employee', 'Coordinateur10', readonly=True,
#                                         states={'draft': [('readonly', False)]}, ),
#         'gest_id3': fields.many2one('hr.employee', 'N.U', readonly=True, copy=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         ## 'emp_ids': fields.one2many('depart_category_rel', 'categ_id', 'Task',readonly=True, states={'draft':[('readonly',False)]}),
#         ## 'emp_ids': fields.many2many('hr.employee', 'depart_category_rel', 'depart_id', 'emp_id', 'Tags',domain="[('depart_id', '=', categ_id)]",),
#         'employee_id': fields.many2one('hr.employee', 'Employés', readonly=True,
#                                        states={'draft': [('readonly', False)]}),
#         'issue_id': fields.many2one('project.issue', 'N.U', select="1", readonly=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         'group_id': fields.many2one('bon.show', 'N.U', select="1", readonly=True,
#                                     states={'draft': [('readonly', False)]}, ),
#         'group_id2': fields.many2one('base.group.merge.automatic.wizard', 'N.U', select="1", readonly=True,
#                                      states={'draft': [('readonly', False)]}, ),
#         'dependency_task_ids': fields.many2many('project.task.work', 'project_task_dependency_work_rel',
#                                                 'dependency_work_id', 'work_id', 'Dependencies'),
#
#         'state': fields.selection([('draft', 'T. Planifiés'),
#                                    ('affect', 'T. Affectés'),
#                                    ('affect_con', 'T. Affectés controle'),
#                                    ('affect_corr', 'T. Affectés corrction'),
#                                    ('tovalid', 'Ret .Encours'),
#                                    ('tovalidcont', 'Cont .Encours'),
#                                    ('validcont', 'Cont .Valides'),
#                                    ('tovalidcorrec', 'Corr .Encours'),
#                                    ('validcorrec', 'Corr .Valides'),
#                                    ('valid', 'T.Terminés'),
#
#                                    ('cancel', 'T. Annulés'),
#                                    ('pending', 'T. Suspendus'),
#                                    ],
#
#                                   'Status', copy=False),
#         'p_done': fields.float('Qté Réalisée', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'note': fields.text('N.U'),
#         'done': fields.function(_default_done, type='boolean', string='Company Currency', readonly=True,
#                                 states={'draft': [('readonly', False)]}, ),
#         'done1': fields.function(_default_done1, type='boolean', string='Company Currency', readonly=True,
#                                  states={'draft': [('readonly', False)]}, ),
#         'done2': fields.function(_default_done2, type='boolean', string='Company Currency', readonly=True,
#                                  states={'draft': [('readonly', False)]}, ),
#         'done3': fields.function(_default_done3, type='boolean', string='Company Currency', readonly=True,
#                                  states={'draft': [('readonly', False)]}, ),
#         'done4': fields.function(_default_flow, type='boolean', string='Company Currency', readonly=True,
#                                  states={'draft': [('readonly', False)]}, ),
#
#         'color': fields.integer('Nbdays', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'color1': fields.integer('Nbdays', readonly=True, states={'affect': [('readonly', False)]}, ),
#         'uom_id': fields.many2one('product.uom', 'Unité Prévue', required=True, readonly=True,
#                                   states={'draft': [('readonly', False)]}, ),
#         'uom_id_r': fields.many2one('product.uom', 'Unité Réelle', readonly=True,
#                                     states={'affect': [('readonly', False)]}, ),
#         'w_id': fields.many2one('base.task.merge.automatic.wizard', 'Company', readonly=True,
#                                 states={'draft': [('readonly', False)]}, ),
#         'pourc': fields.float('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'rank': fields.char('N.U', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'display': fields.boolean('Réalisable'),
#         'is_copy': fields.boolean('Dupliqué?'),
#         'done33': fields.function(_disponible, type='boolean', string='done'),
#         'current_emp': fields.many2one('hr.employee', 'Employé Encours', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'current_gest': fields.many2one('hr.employee', 'Coordinateur Encours', readonly=True,
#                                         states={'draft': [('readonly', False)]}, ),
#         'current_sup': fields.many2one('hr.employee', 'Superviseur Encours', readonly=True,
#                                        states={'draft': [('readonly', False)]}, ),
#         'prior1': fields.float('Prior1', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'prior2': fields.float('Prior2', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'cmnt': fields.char('Prior2', readonly=True, states={'draft': [('readonly', False)]}, ),
#         'work_orig': fields.integer('tache original'),
#         'affect_emp_list': fields.char('employée id'),
#         'affect_e_l': fields.char('employée id'),
#         'affect_emp': fields.char('employée'),
#         'affect_con': fields.char('controle'),
#         'affect_cor': fields.char('corrdinateur'),
#         'affect_con_list': fields.char('controle id'),
#         'affect_cor_list': fields.char('corrdinateur id'),
#         'is_intervenant': fields.function(_isinter, type='boolean', string='intervenant'),
#         'is_control': fields.function(_iscontrol, type='boolean', string='controle'),
#         'is_correction': fields.function(_iscorr, type='boolean', string='correction'),
#
#     }
#
#     _defaults = {
#         'sequence': 1,
#         'state': 'draft',
#         'cmnt': 'Afficher',
#         'zone': 0,
#         'secteur': 0,
#         'active': True,
#         ##'done': 0,
#         'user_id': 1,
#         'gest_id': 16,
#         'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S')
#     }
#
#     _order = "project_id asc"
#
#     def create(self, cr, uid, vals, context=None):
#         if 'hours' in vals and (not vals['hours']):
#             vals['hours'] = 0.00
#         if 'task_id' in vals:
#             cr.execute('update project_task set remaining_hours=remaining_hours - %s where id=%s',
#                        (vals.get('hours', 0.0), vals['task_id']))
#             self.pool.get('project.task').invalidate_cache(cr, uid, ['remaining_hours'], [vals['task_id']],
#                                                            context=context)
#         return super(project_work, self).create(cr, uid, vals, context=context)
#
#     def fields_view_get(self, cr, uid, view_id=None, view_type=None, context=None, toolbar=False, submenu=False):
#
#         res = super(project_work, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type,
#                                                         context=context, toolbar=toolbar, submenu=submenu)
#
#         if view_type == 'form':
#             if len(context) != 6:
#                 this = self.browse(cr, uid, context['active_ids'][0])
#
#                 r = []
#                 dep = self.pool.get('hr.academic').search(cr, uid, [('categ_id', '=', this.categ_id.id)])
#                 ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%dep)
#
#                 if dep:
#                     for nn in dep:
#                         em = self.pool.get('hr.academic').browse(cr, uid, nn, context=context).employee_id.id
#
#                         r.append(em)
#                     # Set all fields read only when coming from an external model
#                 doc = etree.XML(res['arch'])
#                 for node in doc.xpath("//field[@name='employee_id']"):
#                     user_filter = "[('id', 'in'," + str(r) + ")]"
#                     node.set('domain', user_filter)
#
#                     node_name = node.get('name')
#                     setup_modifiers(node, res['fields'][node_name])
#
#                 res['arch'] = etree.tostring(doc)
#
#         return res
#
#     def onchange_place(self, cr, uid, ids, categ_id, employee_id, context=None):
#         res = {}
#         if categ_id:  # on old api it will return id, instead of record
#             r = []
#
#             dep = self.pool.get('hr.academic').search(cr, uid, [('categ_id', '=', categ_id)])
#
#             if dep:
#                 for nn in dep:
#                     em = self.pool.get('hr.academic').browse(cr, uid, nn, context=context).employee_id.id
#
#                     r.append(em)
#             res['domain'] = {'employee_id': [('id', 'in', r)]}
#         return res
#
#     ##    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
#     ##        ##login_user_dpt_id = users_obj.browse(cr, SUPERUSER_ID, uid, context=context).emp_department_id
#     ##        res = super(project_work, self).fields_view_get(cr, uid, view_id, view_type, context=context, toolbar=toolbar, submenu=submenu)
#     ##        eview = etree.fromstring(res['arch'])
#     ##        for node in eview.xpath("//field[@name='employee_id']"):
#     ##            ##if login_user_dpt_id:
#     ##            user_filter =  "[('employee_id', '=',  37 )]"
#     ##            node.set('domain',user_filter)
#     def button_send(self, cr, uid, ids, context=None):
#
#         ##ir_model_data = self.pool.get('ir.model.data')
#
#         ##template_id = ir_model_data.get_object_reference(cr, uid, 'leave_approval_mail2', 'email_template_leave2')[1]
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%template_id)
#         ##self.pool.get('email.template').send_mail(cr, uid, template_id, ids[0], force_send=False, context=context)
#         ##template_id = self.pool.get('email.template').browse(cr, uid, 251, context=context)# see Metadata on debug if you need it
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%template_id)
#         ##template_id.send_mail(ids[0], force_send=True)
#         ## self.pool.get('email.template').send_mail(cr, uid, 11, ids[0], force_send=False, context=context)
#
#         ##id_copy = self.copy(cr, uid, ids[0], {'done': True}, context=context)
#         this = self.browse(cr, uid, ids[0])
#         if this.poteau_r <= 0:
#             raise osv.except_osv(_('Erreur!'), _('Qté Réalisée doit etre déclarée!'))
#         if this.poteau_r > this.poteau_t:
#             raise osv.except_osv(_('Erreur!'), _('Qté Réalisée doit etre inférieure ou égale à la quantité prévue!'))
#
#         ##'total_t'
#         ##cr.execute('update project_task set remaining_hours=remaining_hours - %s + (%s) where id=%s', (vals.get('hours',0.0), work.hours, work.task_id.id))
#
#         self.write(cr, uid, ids, {'state': 'tovalid'}, context=context)
#         return True
#
#     def move_next(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#
#         return {
#             'name': ('Actions Workflow'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             ## 'views':[[1478,'form']],
#             'target': 'new',
#             'auto_search': False,
#             'res_model': 'base.flow.merge.automatic.wizard',
#             ##'res_id': current.paylist_id.id,
#             'context': {'default_project_id': current.project_id.id,
#                         'default_date_start_r': fields.date.context_today(self, cr, uid, context=context),
#                         'default_zone': current.zone
#
#                 , 'default_secteur': current.secteur},
#
#             'domain': []
#         }
#
#     def onchange_poteau_t_x(self, cr, uid, ids, poteau_t, context=None):
#
#         if context is None:
#             context = {}
#         result = {'value': {}}
#         cr.execute('update project_task_work set  poteau_t=%s where  id = %s ', (poteau_t, ids[0]))
#
#         return True
#
#     def onchange_date_start_x(self, cr, uid, ids, date_start, context=None):
#
#         if context is None:
#             context = {}
#         result = {'value': {}}
#         cr.execute('update project_task_work set  date_start=%s where  id = %s ', (date_start, ids[0]))
#
#         return True
#
#     def onchange_date_end_x(self, cr, uid, ids, date_end, context=None):
#
#         if context is None:
#             context = {}
#         result = {'value': {}}
#         cr.execute('update project_task_work set  date_end=%s where  id = %s ', (date_end, ids[0]))
#
#         return True
#
#     def sub_proj_create(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#         ##        if current.gest_id.user_id.id!= uid or uid!=1:
#         ##            raise osv.except_osv(_('Erreur !'), _('Actions Superviseur!'))
#         ##        else:
#         return {
#             'name': ('Création Sous Projet'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             ## 'views':[[1478,'form']],
#             'target': 'popup',
#             'res_model': 'project.project',
#             ##'res_id': current.paylist_id.id,
#             'context': {'default_parent_id1': current.project_id.id,
#                         'default_partner_id': current.project_id.partner_id.id,
#                         'default_date': fields.date.context_today(self, cr, uid, context=context)
#
#                         },
#
#             'domain': []
#         }
#
#     def action_affect(self, cr, uid, ids, context=None):
#
#         return {
#             'name': ('Modification Travaux Permis'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'popup',
#             'res_model': 'base.invoices.merge.automatic.wizard',
#             'view_id': 1677,
#             ## 'res_id': ids[0],
#             'context': {'types_affect': 'intervenant'},
#             'domain': []
#         }
#
#     def button_close(self, cr, uid, ids, context=None):
#         return {'type': 'ir.actions.act_window_close'}
#
#     def onchange_munic(self, cr, uid, ids, state_id, context=None):
#         if state_id:
#             state_obj = self.pool.get('res.country.state')
#             state = state_obj.browse(cr, uid, state_id, context=context)
#             return {'value': {'city': state.region}}
#         return {}
#
#     def button_save(self, cr, uid, ids, context=None):
#
#         line_obj = self.pool.get('project.task.work.line')
#
#         if not ids:
#             raise osv.except_osv(_('Action Non Valide!'), _("Vous devez sélectionner au moins une ligne  !"))
#         parent = line_obj.browse(cr, uid, ids[0])
#         ##self.write(cr, uid, ids, {'note': 'note' }, context=context)
#         for tt in ids:
#             line = line_obj.browse(cr, uid, tt)
#             if line.done is False:
#                 cr.execute('update project_task_work_line set done= %s where id=%s', (True, tt))
#             else:
#                 cr.execute('update project_task_work_line set done= %s where id=%s', (False, tt))
#         ##self.button_save_(cr, uid, [parent.work_id.id], context=context)
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%parent.work_id.id)
#         return {
#             'name': ('Modification Travaux'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'project.task.work',
#             'res_id': parent.work_id.id,
#             'context': {},
#             'domain': []
#         }
#
#     def project_open(self, cr, uid, ids, context=None):
#
#         line_obj = self.pool.get('project.task.work')
#
#         parent = line_obj.browse(cr, uid, ids[0])
#
#         ##self.button_save_(cr, uid, [parent.work_id.id], context=context)
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%parent.work_id.id)
#         return {
#             'name': ('Consultation Projet'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'current',
#             'res_model': 'project.project',
#             'res_id': parent.project_id.id,
#             'view_id': 1758,
#             'context': {},
#             'domain': []
#         }
#
#     def button_save_(self, cr, uid, ids, context=None):
#
#         this = self.browse(cr, uid, ids[0])
#         project_ids = ids[0]
#
#         ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%ids[0])
#         ##self.write(cr, uid, ids, {'note': 'note' }, context=context)
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%ids[0])
#         if this.categ_id.id == 6:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 1616,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#         else:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 330,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#
#     def button_save2_(self, cr, uid, ids, context=None):
#
#         this = self.browse(cr, uid, ids[0])
#         project_ids = ids[0]
#         ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%ids[0]) 1662
#         ##self.write(cr, uid, ids, {'note': 'note' }, context=context)
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%ids[0])
#         if this.categ_id.id == 6:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 1616,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#         else:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 330,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#
#     def button_approve(self, cr, uid, ids, context=None):
#
#         ## self.pool.get('email.template').send_mail(cr, uid, 11, ids[0], force_send=False, context=context)
#         hr_payslip = self.pool.get('hr.payslip')
#         hr_payslip_line = self.pool.get('hr.payslip.line')
#
#         sum1 = 0
#         employee_obj = self.pool.get('hr.employee')
#         ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
#         task_obj = self.pool.get('project.task.work')
#         task_obj_line = self.pool.get('project.task.work.line')
#
#         this = task_obj.browse(cr, uid, ids[0], context)
#
#         line = this.employee_id.id
#         empl = employee_obj.browse(cr, uid, line, context=context)
#         if empl.job_id.id == 1:
#             name = 'Feuille de Temps'
#         else:
#             name = 'Facture'
#
#         ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%this.date[:4])
#
#         cr.execute(
#             "select cast(substr(number, 6, 8) as integer) from hr_payslip where number is not Null and name=%s and EXTRACT(YEAR FROM date_from)=%s  order by number desc limit 1",
#             (name, this.date_start[:4]))
#         q3 = cr.fetchone()
#         if q3:
#             res1 = q3[0] + 1
#         else:
#             res1 = '001'
#         pay_id = hr_payslip.create(cr, uid, {'employee_id': line,
#                                              'date_from': this.date_start,
#                                              'date_to': this.date_start,
#                                              'contract_id': this.employee_id.contract_id.id,
#                                              'name': name,
#                                              'number': str(str(this.date_start[:4]) + '-' + str(str(res1).zfill(3))),
#                                              'struct_id': 1,
#                                              'currency_id': 5,
#                                              ## 'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
#                                              }, context)
#
#         for tt in this.line_ids:
#
#             if tt.state == 'tovalid' and not tt.paylist_id:
#                 ##raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')% tt.paylist_id)
#                 pay_id_line = hr_payslip_line.create(cr, uid, {'employee_id': line,
#                                                                'contract_id': this.employee_id.contract_id.id,
#                                                                'name': ' ',
#                                                                'code': '-',
#                                                                'category_id': 1,
#                                                                'quantity': tt.hours_r,
#                                                                'slip_id': pay_id,
#                                                                'rate': 100,
#                                                                'work_id': tt.work_id.id,
#                                                                ##'contract_id':this.employee_id.contract_id.id,
#
#                                                                'quantity': tt.poteau_r,
#                                                                'salary_rule_id': 1,
#                                                                'amount': this.employee_id.contract_id.wage,
#                                                                ## 'work_phone': applicant.department_id and applicant.department_id.company_id and applicant.department_id.company_id.phone or False,
#                                                                }, context)
#                 ##this_line=task_obj_line.browse(cr, uid, tt.id, context)
#                 task_obj_line.write(cr, uid, tt.id, {'state': 'valid', 'paylist_id': pay_id}, context=context)
#
#         ##self.pool.get('email.template').send_mail(cr, uid, 16, ids[0], force_send=False, context=context)
#
#         task_obj.write(cr, uid, ids[0], {'state': 'valid', 'paylist_id': pay_id}, context=context)
#         return True
#
#     def action_open(self, cr, uid, ids, context=None):
#         project_ids = ids[0]
#         task_obj = self.pool.get('project.task.work')
#         emp_obj = self.pool.get('hr.employee')
#         task = task_obj.browse(cr, uid, project_ids, context=context)
#         r = []
#         dep = self.pool.get('hr.academic').search(cr, uid, [('categ_id', '=', task.categ_id.id)])
#         ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%dep)
#         cr.execute("update hr_employee set vehicle=''")
#         if dep:
#             for nn in dep:
#                 em = self.pool.get('hr.academic').browse(cr, uid, nn, context=context).employee_id.id
#                 emp_obj.write(cr, uid, em, {'vehicle': '1'}, context=context)
#                 r.append(em)
#         task_obj.write(cr, uid, ids[0], {'dep': r}, context=context)
#         if task.categ_id.id == 6:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 1616,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#         else:
#             return {
#                 'name': ('Modification Travaux'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'view_id': 330,
#                 'target': 'new',
#                 'res_model': 'project.task.work',
#                 'res_id': ids[0],
#                 'context': {'active_id': ids[0]},
#                 'domain': [('project_id', 'in', [project_ids])]
#             }
#
#     def action_calendar(self, cr, uid, ids, context=None):
#         current = ids[0]
#         list = []
#         this = self.browse(cr, uid, current, context=context)
#         if not this.employee_id:
#             raise osv.except_osv(_('Error !'), _('Vous devez sélectionner un employé pour consulter son calendrier'))
#         cr.execute('select id from project_task_work where employee_id= %s and id<>%s', (this.employee_id.id, this.id,))
#         work_ids = cr.fetchall()
#         for tt in work_ids:
#             list.append(tt)
#
#         return {
#             'name': ('Modification Travaux'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'calendar',
#             'target': 'popup',
#             'res_model': 'project.task.work',
#             'res_id': ids[0],
#             'context': {},
#             'domain': [('id', 'in', list)]
#         }
#
#     def action_open_flow(self, cr, uid, ids, context=None):
#         current = ids[0]
#         list = []
#         this = self.browse(cr, uid, current, context=context)
#
#         cr.execute('select id from base_flow_merge_line where work_id= %s', (this.id,))
#         work_ids = cr.fetchall()
#         for tt in work_ids:
#             kk = self.pool.get('base.flow.merge.line').browse(cr, uid, tt, context=context)
#             list.append(kk.wizard_id.id)
#
#         return {
#             'name': ('Liste des Actions Workflows'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'target': 'popup',
#             'res_model': 'base.flow.merge.automatic.wizard',
#             'res_id': ids[0],
#             'context': {},
#             'domain': [('id', 'in', list)]
#         }
#
#     def action_open2(self, cr, uid, ids, context=None):
#         project_ids = ids[0]
#         return {
#             'name': ('Modification Travaux Permis'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'project.task.work',
#             'view_id': 1616,
#             'res_id': ids[0],
#             'context': {'active_id': ids[0]},
#             'domain': [('project_id', 'in', [project_ids])]
#         }
#
#     def action_open_group(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#
#         if current.line_ids:
#             for kk in current.line_ids.ids:
#                 rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                 if rec_line.group_id:
#                     if rec_line.group_id.ids not in tt:
#                         tt.append(rec_line.group_id.ids)
#
#         return {
#             'name': ('Consultation Travaux Validés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'views': [[1478, 'form']],
#             'target': 'new',
#             'res_model': 'bon.show',
#             ##  'res_id': current.paylist_id.id,
#             'context': {},
#             'domain': [('id', 'in', tt)]
#         }
#
#     def action_open_group2(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#
#         if current.line_ids:
#             for kk in current.line_ids.ids:
#                 rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                 if rec_line.group_id2:
#                     if rec_line.group_id2.ids not in tt:
#                         tt.append(rec_line.group_id2.ids)
#         if tt:
#             for kk in tt:
#                 cr.execute('update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
#                            (uid, tuple(kk)))
#         ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% tt)
#         return {
#             'name': ('Consultation Travaux Validés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'views': [[1544, 'tree']],
#             'target': 'new',
#             'res_model': 'base.group.merge.automatic.wizard',
#             ##  'res_id': current.paylist_id.id,
#             'context': {},
#             'domain': [('id', 'in', tt)]
#         }
#
#     def action_open_group3(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#         for book in current:
#             test1 = self.pool.get('project.task.work.line').search(cr, uid, [('work_id2', '=', current.id),
#                                                                              ])
#             if test1:
#                 for jj in test1:
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, jj, context=context)
#                     if rec_line.group_id2:
#                         if rec_line.group_id2.ids not in tt:
#                             tt.append(rec_line.group_id2.ids)
#         if current.line_ids:
#             for kk in current.line_ids.ids:
#                 rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                 if rec_line.group_id2:
#                     if rec_line.group_id2.ids not in tt:
#                         tt.append(rec_line.group_id2.ids)
#         if tt:
#             for kk in tt:
#                 cr.execute('update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
#                            (uid, tuple(kk)))
#         ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% tt)
#         return {
#             'name': ('Consultation Travaux Validés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'views': [[1824, 'tree']],
#             'target': 'new',
#             'res_model': 'base.group.merge.automatic.wizard',
#             ##  'res_id': current.paylist_id.id,
#             'context': {},
#             'domain': [('id', 'in', tt), ('state1', '<>', 'draft')]
#         }
#
#     def action_open_group4(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#         for book in current:
#             test1 = self.pool.get('project.task.work.line').search(cr, uid, [('work_id2', '=', current.id),
#                                                                              ])
#             if test1:
#                 for jj in test1:
#                     rec_line = self.pool.get('project.task.work.line').browse(cr, uid, jj, context=context)
#                     if rec_line.group_id2:
#                         if rec_line.group_id2.ids not in tt:
#                             tt.append(rec_line.group_id2.ids)
#         if current.line_ids:
#             for kk in current.line_ids.ids:
#                 rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#                 if rec_line.group_id2:
#                     if rec_line.group_id2.ids not in tt:
#                         tt.append(rec_line.group_id2.ids)
#         if tt:
#             for kk in tt:
#                 cr.execute('update base_group_merge_automatic_wizard set create_uid= %s where id in %s',
#                            (uid, tuple(kk)))
#         ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% tt)
#         return {
#             'name': ('Consultation Travaux Validés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             'views': [[1825, 'tree']],
#             'target': 'new',
#             'res_model': 'base.group.merge.automatic.wizard',
#             ##  'res_id': current.paylist_id.id,
#             'context': {},
#             'domain': [('id', 'in', tt), ('state2', '<>', 'draft')]
#         }
#
#     def action_open_invoice(self, cr, uid, ids, context=None):
#         current = self.browse(cr, uid, ids[0], context=context)
#
#         tt = []
#         if current.line_ids:
#             for kk in current.line_ids.ids:
#
#
# rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
# if rec_line.paylist_id:
#     if rec_line.paylist_id.ids not in tt:
#         tt.append(rec_line.paylist_id.ids)
# return {
#     'name': ('Consultation Facture/F.T'),
#     'type': 'ir.actions.act_window',
#     'view_type': 'form',
#     'view_mode': 'tree,form',
#     ## 'views':[[1478,'form']],
#     'target': 'new',
#     'res_model': 'hr.payslip',
#     ##'res_id': current.paylist_id.id,
#     'context': {},
#     'domain': [('id', 'in', tt)]
# }
#
#
# def action_open_histo(self, cr, uid, ids, context=None):
#     this = self.browse(cr, uid, ids[0], context=context)
#
#     ll = []
#     if this.kit_id:
#         wrk = self.pool.get('project.task.work').search(cr, uid, [('project_id', '=', this.project_id.id),
#                                                                   ('kit_id', '=', this.kit_id.id)
#             , ('zone', '=', this.zone), ('secteur', '=', this.secteur)])
#
#         for jj in wrk:
#             work = self.pool.get('work.histo').search(cr, uid, [('work_id', '=', jj)])
#             if work:
#                 for dd in work:
#                     hist_l = self.pool.get('work.histo.line').search(cr, uid, [('work_histo_id', '=', dd)])
#                     if hist_l:
#                         for nn in hist_l:
#                             work_histo = self.pool.get('work.histo.line').browse(cr, uid, nn)
#                             if work_histo:
#                                 ll.append(work_histo.work_histo_id.id)
#         ## raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% ll)
#         if not ll:
#             raise osv.except_osv(_('Action impossible!'), _("Pas de d'historique pour cette tache"))
#
#         return {
#             'name': ('Historique Tache'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'popup',
#             'res_model': 'work.histo',
#             'res_id': ll[0],
#             'context': {},
#             'domain': []
#         }
#     else:
#         work = self.pool.get('work.histo').search(cr, uid, [('work_id', '=', this.id)])
#         if work:
#             work_histo = self.pool.get('work.histo').browse(cr, uid, work[0])
#             return {
#                 'name': ('Historique Tache'),
#                 'type': 'ir.actions.act_window',
#                 'view_type': 'form',
#                 'view_mode': 'form',
#                 'target': 'popup',
#                 'res_model': 'work.histo',
#                 'res_id': work_histo.id,
#                 'context': {},
#                 'domain': [('work_id', 'in', this.id)]
#             }
#         else:
#             raise osv.except_osv(_('Action impossible!'), _("Pas de d'historique pour cette tache"))
#
#
# def action_invoice(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids[0], context=context)
#     tt = []
#     if current.line_ids:
#         for kk in current.line_ids.ids:
#             rec_line = self.pool.get('project.task.work.line').browse(cr, uid, kk, context=context)
#             if rec_line.wizard_id:
#                 if rec_line.wizard_id.ids not in tt:
#                     tt.append(rec_line.wizard_id.ids)
#
#         return {
#             'name': ('Consultation Bons Validés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'tree,form',
#             ##'views':[[1478,'form']],
#             'target': 'new',
#             'res_model': 'base.invoice.merge.automatic.wizard',
#             ##  'res_id': current.paylist_id.id,
#             'context': {},
#             'domain': [('id', 'in', tt)]
#         }
#
#
# def action_issue(self, cr, uid, ids, context=None):
#     project_ids = ids[0]
#     current = self.browse(cr, uid, ids[0], context=context)
#
#     if current.issue_id:
#         return {
#             'name': ('Gestion des Incidents et Anomalies'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'project.issue',
#             'res_id': current.issue_id.id,
#             'context': {},
#             'domain': [('work_id', 'in', [project_ids])]
#         }
#     else:
#         return {
#             'name': ('Gestion des Incidents et Anomalies'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'target': 'new',
#             'res_model': 'project.issue',
#             # 'res_id': ids[0],date_deadline
#             'context': {'default_work_id': ids[0],
#                         'default_date_deadline': fields.date.context_today(self, cr, uid, context=context),
#                         'default_employee_id': current.employee_id.id or False
#                 , 'default_project_id': current.project_id.id, 'default_task_id': current.task_id.id,
#                         'default_gest_id': current.gest_id.id
#                 , 'default_name': current.project_id.number + '-' + str(current.task_id.sequence).zfill(
#                     3) + '-' + str(current.sequence).zfill(3)},
#             'domain': []
#         }
#
#
# def action_issue2(self, cr, uid, ids, context=None):
#     this_obj = self.pool.get('base.group.merge.automatic.wizard')
#     current = self.browse(cr, uid, ids[0], context=context)
#     ##        'default_work_id': ids[0],'default_date_deadline': fields.date.context_today(self,cr,uid,context=context),'default_employee_id':current.employee_id.id or False
#     ##                            ,'default_project_id':current.project_id.id,'default_task_id':current.task_id.id,'default_gest_id':current.gest_id.id
#     ##                            ,'default_name': current.project_id.number+'-'+str(current.task_id.sequence).zfill(3)+'-'+str(current.sequence).zfill(3)
#
#     ## current=self.browse(cr, uid, ids[0], context=context)
#     if current.project_id.r_id:
#         return {
#             'name': ('Plans des Relevés'),
#             'type': 'ir.actions.act_window',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'view_id': 1662,
#             'target': 'new',
#             'res_model': 'risk.management.category',
#             'res_id': current.project_id.r_id.id,
#
#             'nodestroy': True,
#             ## 'context': {'default_name':current.project_id.number +' / ' +current.name,'default_project_id':current.project_id.id,'default_task_id':current.task_id.id,'default_work_id':current.id,'default_employee_id':current.employee_id.id  },
#             'domain': []
#         }
#
#
# ##        else:
# ##
# ##            return{
# ##                    'name'          :   ('Plans des Relevés'),
# ##                    'type'          :   'ir.actions.act_window',
# ##                    'view_type'     :   'form',
# ##                    'view_mode'     :   'form',
# ##                    'view_id': 1662,
# ##                    'target'        :   'new',
# ##                    'res_model'     :   'risk.management.category',
# ##                    #'res_id': ids[0],date_deadline
# ##
# ##                    'nodestroy': True,
# ##                    'context': {'default_name':current.project_id.number +' / ' +current.name,'default_project_id':current.project_id.id,'default_task_id':current.task_id.id,'default_work_id':current.id,'default_employee_id':current.employee_id.id},
# ##                    'domain'        :   []
# ##                }
# def action_copy(self, cr, uid, id, default=None, context=None):
#     # your changes
#     if default is None:
#         default = {}
#     for tt in self.browse(cr, uid, id, context=context):
#         ## for tt in current.work_ids:
#         ##if not default.get('name'):
#         ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% tt.name)
#         packaging_obj = self.pool.get('project.task.work')
#         ##default['name'] = _("%s (copy)") % tt.dst_task_id.name
#
#         ##test= packaging_obj.copy_data(cr, uid, tt.dst_task_id.id, default, context)
#         ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")% test)
#         cr.execute('select sequence from project_task_work where task_id=%s order by sequence desc limit 1',
#                    (tt.task_id.id,))
#         res = cr.fetchone()
#         packaging_obj.write(cr, uid, id[0], {'poteau_t': tt.poteau_t / 2}, context=context)
#         cte = packaging_obj.create(cr, uid, {
#             'project_id': tt.project_id.id,
#             'sequence': res[0] + 1,
#             'task_id': tt.task_id.id,
#             'product_id': tt.product_id.id,
#             'categ_id': tt.categ_id.id,
#             'state_id': tt.state_id.id or False,
#             'city': tt.city or False,
#             'name': tt.name + ' * ',
#             'date_start': tt.date_start,
#             'date_end': tt.date_end,
#             'poteau_t': tt.poteau_t / 2,
#             'poteau_i': tt.poteau_i,
#             'color': tt.color,
#             'hours': tt.hours,
#             'total_t': tt.color * 7,  ##*work.employee_id.contract_id.wage
#             'project_id': tt.task_id.project_id.id,
#
#             'gest_id': tt.gest_id.id,
#             'uom_id': tt.uom_id.id,
#             'uom_id_r': tt.uom_id_r.id,
#             'ftp': tt.ftp,
#             'zone': tt.zone,
#             'secteur': tt.secteur,
#             'state': 'draft'
#
#         }, context=context)
#
#         ##test=self.pool.get('project.task').copy_data(cr,uid, tt.dst_task_id.id,default=default,context=context)
#     return cte
#
#
# def button_invoice(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'paid'}, context=context)
#     return True
#
#
# def button_write(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids, context=context)
#     if not current.employee_id.user_id:
#         raise osv.except_osv(_('Erreur'), _('Vous devez affecter un utilisateur Odoo à la ressource choisie'))
#     self.write(cr, uid, ids,
#                {'employee_id': current.employee_id.id, 'state': 'affect', 'user_id': current.employee_id.user_id.id,
#                 'gest_id': current.gest_id.id, 'employee_id': current.employee_id.id}, context=context)
#     return True
#
#
# def button_write1(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids, context=context)
#     ##        if current.poteau_r<1:
#     ##            raise osv.except_osv(_('Erreur'),_('La Quantité Réalisée doit etre supérieur à 0')) len(project_id)
#     task_obj = self.pool.get('project.task.work.line')
#
#     ##        cr.execute('select id from project_task_work_line where done= %s and work_id = %s ', (True, current.id))
#     ##        project_id= cr.fetchall()
#     ##        ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%len(current.line_ids) )
#     ##        ##,'task_id':current.work_id.task_id.id,'project_id':current.work_id.task_id.project_id.id
#     ##        if  len(project_id)==0:
#     ##            for tt in current.line_ids:
#     ##
#     ##                cr.execute('update project_task_work_line set project_id= %s where id=%s', (current.task_id.project_id.id, tt.id))
#     ##                cr.execute('update project_task_work_line set task_id= %s where id=%s', (current.task_id.id, tt.id))
#     ##                cr.execute('update project_task_work_line set state= %s where id=%s', ('tovalid', tt.id))
#     ##
#     ##        else:
#     ##            for tt in project_id:
#     ##
#     ##
#     ##                cr.execute('update project_task_work_line set project_id= %s where id=%s', (current.task_id.project_id.id, tt))
#     ##                cr.execute('update project_task_work_line set task_id= %s where id=%s', (current.task_id.id, tt))
#     ##                cr.execute('update project_task_work_line set state= %s where id=%s and  state=%s and  done=%s', ('tovalid', tt,'affect',False))
#
#     self.write(cr, uid, ids, {'state': 'tovalid'}, context=context)
#     return True
#
#
# def button_write2(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids, context=context)
#     ##        if current.poteau_r<1:
#     ##            raise osv.except_osv(_('Erreur'),_('La Quantité Réalisée doit etre supérieur à 0')) len(project_id)
#     task_obj = self.pool.get('project.task.work.line')
#
#     ##        cr.execute('select id from project_task_work_line where done= %s and work_id = %s', (True, current.id))
#     ##        project_id= cr.fetchall()
#     ##        ##raise osv.except_osv(_('Transfert impossible!'),_("Pas de Stock suffisant pour l'article %s  !")%len(current.line_ids) )
#     ##
#     ##        if  len(project_id)==0:
#     ##            for tt in current.line_ids:
#     ##
#     ##                cr.execute('update project_task_work_line set project_id= %s where id=%s', (current.task_id.project_id.id, tt.id))
#     ##                cr.execute('update project_task_work_line set task_id= %s where id=%s', (current.task_id.id, tt.id))
#     ##
#     ##                cr.execute('update project_task_work_line set state= %s where id=%s', ('tovalid', tt.id))
#     ##
#     ##        else:
#     ##            for tt in project_id:
#     ##
#     ##
#     ##                cr.execute('update project_task_work_line set project_id= %s where id=%s', (current.task_id.project_id.id, tt))
#     ##                cr.execute('update project_task_work_line set task_id= %s where id=%s', (current.task_id.id, tt))
#     ##                cr.execute('update project_task_work_line set state= %s where id=%s and state=%s', ('tovalid', tt,'affect'))
#
#     ##self.write(cr, uid, ids, {'state':'tovalid' }, context=context)
#
#     return True
#
#
# def button_cancel_affect(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids, context=context)
#
#     self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
#     return True
#
#
# def button_cancel_write(self, cr, uid, ids, context=None):
#     current = self.browse(cr, uid, ids[0], context=context)
#     if current.state == 'affect':
#         self.write(cr, uid, ids, {'state': 'draft'}, context=context)
#     elif current.state == 'tovalid':
#         self.write(cr, uid, ids, {'state': 'affect'}, context=context)
#
#     return {'name': "Modification Travaux",
#             'res_model': "project.task.work",
#             'src_model': "project.task.work",
#             'view_mode': "form",
#             'target': "new",
#             'key2': "client_action_multi",
#             'multi': "True",
#             'res_id': ids[0],
#             'type': 'ir.actions.act_window',
#             }
#
#
# def button_cancel_invoice(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'tovalid'}, context=context)
#     return True
#
#
# def button_pause(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'pending'}, context=context)
#     return True
#
#
# def button_done(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'close'}, context=context)
#     return True
#
#
# def button_cancel(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'cancel'}, context=context)
#     return True
#
#
# def button_draft(self, cr, uid, ids, context=None):
#     self.write(cr, uid, ids, {'state': 'draft'}, context=context)
#     return True
#
#
# def onchange_date_to_(self, cr, uid, ids, date_to, date_from):
#     """
#     Update the number_of_days.
#     """
#
#     # date_to has to be greater than date_from
#     if (date_from and date_to) and (date_from > date_to):
#         raise osv.except_osv(_('Warning!'), _('The start date must be anterior to the end date.'))
#
#     result = {'value': {}}
#     holiday_obj = self.pool.get('hr.holidays')
#     hours_obj = self.pool.get('training.holiday.year')
#     ##this=self.browse(cr, uid, ids[0])
#     for work in self.browse(cr, uid, ids):
#
#         # Compute and update the number of days
#
#         if (date_to and date_from) and (date_from <= date_to):  ##'%Y-%m-%d %H:%M:%S'
#             DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
#             from_dt = dt.datetime.strptime(date_from, DATETIME_FORMAT)
#             to_dt = dt.datetime.strptime(date_to, DATETIME_FORMAT)
#             timedelta = to_dt - from_dt
#             diff_day = holiday_obj._get_number_of_days(cr, uid, date_from, date_to)
#             year = hours_obj.search(cr, uid, [('year', '=', str(date_from[:4]))])
#             if year:
#                 hr = hours_obj.browse(cr, uid, year[0], context=context).hours
#             else:
#                 hr = 7
#             result['value']['color1'] = round(math.floor(diff_day)) + 1
#             result['value']['hours_r'] = (round(math.floor(diff_day)) + 1) * hr
#             result['value']['total_r'] = (
#                                              (round(math.floor(
#                                                  diff_day)) + 1)) * hr * work.employee_id.contract_id.wage
#
#         else:
#
#             result['value']['color1'] = 0
#             result['value']['total_r'] = 0
#
#     return result
#
#
# def onchange_date_to(self, cr, uid, ids, date_to, date_from, context):
#     """
#     Update the number_of_days.
#     """
#
#     # date_to has to be greater than date_from
#     if (date_from and date_to) and (date_from > date_to):
#         raise osv.except_osv(_('Warning!'), _('The start date must be anterior to the end date.'))
#
#     result = {'value': {}}
#     this = self.browse(cr, uid, ids[0])
#     holiday_obj = self.pool.get('hr.holidays')
#     hours_obj = self.pool.get('training.holiday.year')
#     ##        for work in self.browse(cr, uid, ids):
#     ##            raise osv.except_osv(_('Error !'), _('No period defined for this date: %s ')%work.employee_id.contract_id.wage)
#
#     # Compute and update the number of days
#
#     if (date_to and date_from) and (date_from <= date_to):  ##'%Y-%m-%d %H:%M:%S'
#         DATETIME_FORMAT = "%Y-%m-%d"
#         from_dt = dt.datetime.strptime(date_from, DATETIME_FORMAT)
#         to_dt = dt.datetime.strptime(date_to, DATETIME_FORMAT)
#         timedelta = to_dt - from_dt
#         diff_day = holiday_obj._get_number_of_days(cr, uid, date_from, date_to)
#         year = hours_obj.search(cr, uid, [('year', '=', str(date_from[:4]))])
#         if year:
#             hr = hours_obj.browse(cr, uid, year[0], context=context).hours
#         else:
#             hr = 7
#
#         result['value']['color'] = round(math.floor(diff_day)) + 1
#         result['value']['hours'] = (round(math.floor(diff_day)) + 1) * hr
#         result['value']['total_t'] = ((round(math.floor(diff_day)) + 1)) * hr * this.employee_id.contract_id.wage
#
#     else:
#
#         result['value']['color'] = 0
#         result['value']['total_t'] = 0
#
#     return result
#
#
# def copy(self, cr, uid, id, default=None, context=None):
#     if default is None:
#         default = {}
#     if 'name' not in default:
#         job = self.browse(cr, uid, id, context=context)
#     ## default['name'] = _("%s (copy)") % (job.name)
#     return super(project_work, self).copy(cr, uid, id, default=default, context=context)
#
#
# def write(self, cr, uid, ids, vals, context=None):
#     if 'hours' in vals and (not vals['hours']):
#         vals['hours'] = 0.00
#     if 'hours' in vals:
#         task_obj = self.pool.get('project.task')
#         for work in self.browse(cr, uid, ids, context=context):
#             cr.execute('update project_task set remaining_hours=remaining_hours - %s + (%s) where id=%s',
#                        (vals.get('hours', 0.0), work.hours, work.task_id.id))
#             task_obj.invalidate_cache(cr, uid, ['remaining_hours'], [work.task_id.id], context=context)
#     return super(project_work, self).write(cr, uid, ids, vals, context)
#
#
# def unlink(self, cr, uid, ids, context=None):
#     task_obj = self.pool.get('project.task')
#     if cr.dbname == 'TEST95':
#         connection = py.connect(host='localhost',
#                                 user='root',
#                                 passwd='',
#                                 db='rukovoditel_en',
#                                 use_unicode=True, charset="utf8")
#         cursor = connection.cursor()
#     res_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
#     dep = self.pool.get('hr.academic').search(cr, uid, [('employee_id', '=', res_user.employee_id.id)])
#     ## raise osv.except_osv(_('Error !'), _('No period defined for this date: %s !\nPlease create one.')%dep)
#     r = []
#     if dep:
#         for nn in dep:
#             em = self.pool.get('hr.academic').browse(cr, uid, nn, context=context).categ_id.id
#             r.append(em)
#
#     dep_ids = res_user.employee_id.academic_ids
#     ##        for work in self.browse(cr, uid, ids):
#     ##            if work:
#     ##                if work.categ_id:
#     ##                    if work.categ_id.id not in r:
#     ##                        raise osv.except_osv(_('Erreur !'), _('Vous n''etes pas autorisé à exécuter cette action sur un département externe'))
#     ##
#     ##                        ##                if work.is_copy is not  True and uid!= 1:
#     ##                        ##                    raise osv.except_osv(_('Suppression Impossible !'), _('Seules les lignes dupliquées peuvent etre supprimées!'))
#     ##                        ##                if work.state  != 'draft':
#     ##                        ##                    raise osv.except_osv(_('Suppression Impossible !'), _('Seules les lignes Brouillons peuvent etre supprimées!'))
#     ##
#     ##
#     ##                    cr.execute('update project_task set remaining_hours=remaining_hours + %s where id=%s',
#     ##                               (work.hours, work.task_id.id))
#     ##                    task_obj.invalidate_cache(cr, uid, ['remaining_hours'], [work.task_id.id], context=context)
#     if cr.dbname == 'TEST95':
#         sql1 = ("delete from  app_entity_26  WHERE id = %s")
#
#         cursor.execute(sql1, (work.id,))
#         connection.commit()
#     return super(project_work, self).unlink(cr, uid, ids, context=context)
