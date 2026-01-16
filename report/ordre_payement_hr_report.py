# -*- coding: utf-8 -*-
import time
from odoo import api, models

import logging
log = logging.getLogger(__name__)

DATE_FORMAT = '%Y-%m-%d'
FRENCH_DATE_FORMAT = '%d/%m/%Y'

class OrdrePayementHRReport(models.AbstractModel):
    _name = 'report.arsata_payroll.report_pay_order'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}

        payslip_ids = data.get('payslip_ids', [])
        payslips = self.env['hr.payslip'].browse(payslip_ids)
        lines = []
        for p in payslips:
            lines.append({
                'employee_name': p.employee_id.name or '',
                'bank_name': p.employee_id.bank_account_id.bank_id.name
                    if p.employee_id.bank_account_id else '',
                'account_number': p.employee_id.bank_account_id.acc_number
                    if p.employee_id.bank_account_id else '',
                'net': p.amount_net or 0.0,
            })

        return {
            'doc_ids': payslip_ids,
            'doc_model': 'hr.payslip',
            'docs': payslips,
            'load_lines': lines,
            'date_start': data.get('date_start'),
            'date_stop': data.get('date_stop'),
        }


    
    def _load_lines(self, payslips):
        result = []
        for payslip in payslips:
           result.append({
            'employee_name': payslip.employee_id.name or '',
            'bank_name': payslip.employee_id.bank_account_id.bank_id.name
                if payslip.employee_id.bank_account_id else '',
            'account_number': payslip.employee_id.bank_account_id.acc_number
                if payslip.employee_id.bank_account_id else '',
            'net': payslip.amount_net or 0.0,
        })
           return result
