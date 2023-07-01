# -*- coding: utf-8 -*-
# from odoo import http


# class LinkLine(http.Controller):
#     @http.route('/link_line/link_line', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/link_line/link_line/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('link_line.listing', {
#             'root': '/link_line/link_line',
#             'objects': http.request.env['link_line.link_line'].search([]),
#         })

#     @http.route('/link_line/link_line/objects/<model("link_line.link_line"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('link_line.object', {
#             'object': obj
#         })
