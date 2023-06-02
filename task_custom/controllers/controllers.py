# -*- coding: utf-8 -*-
# from odoo import http


# class TaskCustom(http.Controller):
#     @http.route('/task_custom/task_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_custom/task_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_custom.listing', {
#             'root': '/task_custom/task_custom',
#             'objects': http.request.env['task_custom.task_custom'].search([]),
#         })

#     @http.route('/task_custom/task_custom/objects/<model("task_custom.task_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_custom.object', {
#             'object': obj
#         })
