# -*- coding: utf-8 -*-
# from odoo import http


# class FlowWizard(http.Controller):
#     @http.route('/flow_wizard/flow_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/flow_wizard/flow_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('flow_wizard.listing', {
#             'root': '/flow_wizard/flow_wizard',
#             'objects': http.request.env['flow_wizard.flow_wizard'].search([]),
#         })

#     @http.route('/flow_wizard/flow_wizard/objects/<model("flow_wizard.flow_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('flow_wizard.object', {
#             'object': obj
#         })
