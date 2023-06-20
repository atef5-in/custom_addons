# -*- coding: utf-8 -*-
# from odoo import http


# class CountryCustom(http.Controller):
#     @http.route('/country_custom/country_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/country_custom/country_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('country_custom.listing', {
#             'root': '/country_custom/country_custom',
#             'objects': http.request.env['country_custom.country_custom'].search([]),
#         })

#     @http.route('/country_custom/country_custom/objects/<model("country_custom.country_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('country_custom.object', {
#             'object': obj
#         })
