# -*- coding: utf-8 -*-
# from odoo import http


# class UsersCustom(http.Controller):
#     @http.route('/users_custom/users_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/users_custom/users_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('users_custom.listing', {
#             'root': '/users_custom/users_custom',
#             'objects': http.request.env['users_custom.users_custom'].search([]),
#         })

#     @http.route('/users_custom/users_custom/objects/<model("users_custom.users_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('users_custom.object', {
#             'object': obj
#         })
