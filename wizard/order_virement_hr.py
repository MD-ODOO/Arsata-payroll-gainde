# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil import relativedelta
import logging

_logger = logging.getLogger(__name__)

class OrdreVirementHR(models.TransientModel):
    _name = 'wizard.ordre.virement.hr'
    _description = "Wizard pour l'ordre de virement RH"

    payslip_ids = fields.Many2many(
        'hr.payslip', 'payslip_wizard_rel', 'wizard_id', 'payslip_id',
        string="Bulletins de Paye", required=True
    )
    date_start = fields.Date(
        string="Date début", 
        default=lambda self: datetime.today().replace(day=1),
        required=True
    )
    date_stop = fields.Date(
        string="Date fin",
        default=lambda self: (datetime.today() + relativedelta.relativedelta(months=+1, day=1, days=-1)),
        required=True
    )
    ordre = fields.Text(string='Message')
    bank_id = fields.Many2one('res.bank', string='Banque')
    # emp_account_id = fields.Many2one('account.account', string="Compte débiteur")
    # treasury_account_id = fields.Many2one('account.account', string="Compte créditeur")
    # journal_id = fields.Many2one('account.journal', string="Journal")
    
    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_ids = self.env.context.get('active_ids')
        active_model = self.env.context.get('active_model')

        if active_model == 'hr.payslip' and active_ids:
            res['payslip_ids'] = [(6, 0, active_ids)]
        return res
    
    def action_print_report(self):
        self.ensure_one()
        return self.env.ref(
        'arsata_payroll.action_report_ordre_virement_hr'
         ).report_action(
        None,  # ← PAS self
        data={
            'payslip_ids': self.payslip_ids.ids,
            'date_start': self.date_start,
            'date_stop': self.date_stop,
            'bank_id': self.bank_id.id if self.bank_id else False,
        }
    )
    
    
