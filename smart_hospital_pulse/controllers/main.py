# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class HospitalVitalsController(http.Controller):

    @http.route('/api/hospital/vitals/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_patient_vitals(self, **kwargs):
        
        ticket_id = kwargs.get('ticket_id')
        heart_rate = kwargs.get('heart_rate')

        if not ticket_id or heart_rate is None:
            return {'status': 'error', 'message': 'Missing ticket_id or heart_rate'}

        ticket = request.env['crm.lead'].sudo().browse(int(ticket_id))
        if not ticket.exists():
            return {'status': 'error', 'message': 'Ticket not found'}

        ticket.write({'patient_heart_rate': int(heart_rate)})
        return {'status': 'success', 'message': 'Vitals updated successfully'}
