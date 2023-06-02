# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'hospital Appointment'
    _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string='Patient')
    gender = fields.Selection(related='patient_id.gender')
    doctor_id = fields.Many2one(comodel_name='hospital.doctor', string='Doctor')
    app_time = fields.Datetime(string='Appointment Time')
    booking_date = fields.Date(string='Booking Date')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Important'),
        ('2', 'Urgent'), ], string='Priority')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'), ], default='draft', string='Status')


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.gender = self.patient_id.gender

    def action_done(self):
        self.status = 'done'

    def action_cancel(self):
        self.status = 'cancel'

    def action_in_consultation(self):
        self.status = 'in_consultation'

class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'appointment.pharmacy.lines'

    product_id = fields.Many2one('hospital.medicament', string='Medicament')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')



