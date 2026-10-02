# -*- coding: utf-8 -*-
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    patient_heart_rate = fields.Integer(string="Patient Heart Rate (bpm)", default=70)
    is_critical_iot_alert = fields.Boolean(string="Critical IoT Alert", default=False)

    def write(self, vals):
        res = super(CrmLead, self).write(vals)

        if 'patient_heart_rate' in vals:
            for ticket in self:
                hr = vals.get('patient_heart_rate', ticket.patient_heart_rate)
                
                if hr < 40 or hr > 140:
                    super(CrmLead, ticket).write({
                        'priority': '3',
                        'is_critical_iot_alert': True
                    })
                    
                    
                    ticket.message_post(
                        body="⚠️ SYSTEM OVERRIDE: CRITICAL VITALS DETECTED. IMMEDIATE INTERVENTION REQUIRED!",
                        subtype_xmlid="mail.mt_note"
                    )
                else:
                    super(CrmLead, ticket).write({
                        'is_critical_iot_alert': False
                    })
        return res
