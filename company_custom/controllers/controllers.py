# -*- coding: utf-8 -*-
# from odoo import http


# class CompanyCustom(http.Controller):
#     @http.route('/company_custom/company_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_custom/company_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_custom.listing', {
#             'root': '/company_custom/company_custom',
#             'objects': http.request.env['company_custom.company_custom'].search([]),
#         })

#     @http.route('/company_custom/company_custom/objects/<model("company_custom.company_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_custom.object', {
#             'object': obj
#         })
