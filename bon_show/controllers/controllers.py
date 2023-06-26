# -*- coding: utf-8 -*-
# from odoo import http


# class BonShow(http.Controller):
#     @http.route('/bon_show/bon_show', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bon_show/bon_show/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bon_show.listing', {
#             'root': '/bon_show/bon_show',
#             'objects': http.request.env['bon_show.bon_show'].search([]),
#         })

#     @http.route('/bon_show/bon_show/objects/<model("bon_show.bon_show"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bon_show.object', {
#             'object': obj
#         })
