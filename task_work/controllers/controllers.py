# -*- coding: utf-8 -*-
# from odoo import http


# class TaskWork(http.Controller):
#     @http.route('/task_work/task_work', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_work/task_work/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_work.listing', {
#             'root': '/task_work/task_work',
#             'objects': http.request.env['task_work.task_work'].search([]),
#         })

#     @http.route('/task_work/task_work/objects/<model("task_work.task_work"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_work.object', {
#             'object': obj
#         })
