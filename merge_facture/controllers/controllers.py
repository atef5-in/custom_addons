# -*- coding: utf-8 -*-
# from odoo import http


# class MergeFacture(http.Controller):
#     @http.route('/merge_facture/merge_facture', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/merge_facture/merge_facture/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('merge_facture.listing', {
#             'root': '/merge_facture/merge_facture',
#             'objects': http.request.env['merge_facture.merge_facture'].search([]),
#         })

#     @http.route('/merge_facture/merge_facture/objects/<model("merge_facture.merge_facture"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('merge_facture.object', {
#             'object': obj
#         })
