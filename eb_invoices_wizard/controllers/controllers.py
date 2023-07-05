# -*- coding: utf-8 -*-
# from odoo import http


# class EbInvoicesWizard(http.Controller):
#     @http.route('/eb_invoices_wizard/eb_invoices_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eb_invoices_wizard/eb_invoices_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eb_invoices_wizard.listing', {
#             'root': '/eb_invoices_wizard/eb_invoices_wizard',
#             'objects': http.request.env['eb_invoices_wizard.eb_invoices_wizard'].search([]),
#         })

#     @http.route('/eb_invoices_wizard/eb_invoices_wizard/objects/<model("eb_invoices_wizard.eb_invoices_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eb_invoices_wizard.object', {
#             'object': obj
#         })
