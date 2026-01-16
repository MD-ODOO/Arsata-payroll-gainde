#-*- coding:utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import UserError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class ReportBulletin(models.AbstractModel):
    _name = 'report.arsata_payroll.report_bulletin'

    @api.model
    def _get_payslip_imposable(self, lines):
        total_gain = 0.0
        total_brut = 0.0
        res = []
        for line in lines:
            if line.appears_on_payslip and line.category_id.code in ('INDM','BASE'):
                if line.total != 0.0:
                    res.append(line)
                    total_gain += line.total
                    total_brut += line.total
        return res, total_gain, total_brut

    @api.model
    def _get_payslip_cotisation(self, lines):
        total_charg_pat = 0.0
        total_charg_sal = 0.0
        res = []
        for line in lines:
            if line.appears_on_payslip and line.category_id.code in ('COMP','SALC','IR'):
                if line.total != 0.0:
                    res.append(line)
                    if line.category_id.code == 'COMP':
                        total_charg_pat += line.total
                    else:
                        total_charg_sal += line.total
        return res, total_charg_pat, total_charg_sal

    @api.model
    def _get_payslip_non_imposable(self, lines):
        res = []
        total_gain = 0.0
        total_brut = 0.0
        for line in lines:
            if line.appears_on_payslip and line.category_id.code == 'NOIMP':
                if line.total != 0.0:
                    res.append(line)
                    total_gain += line.total
                    total_brut += line.total
        return res, total_gain, total_brut

    @api.model
    def _get_payslip_retenu(self, lines):
        res = []
        total_charg_sal = 0.0
        for line in lines:
            if line.appears_on_payslip and line.category_id.code == 'DED':
                if line.total != 0.0:
                    res.append(line)
                    total_charg_sal += line.total
        return res, total_charg_sal

    @api.model
    def get_val_annuel(self, date_from, employee_id):
        Payslip = self.env['hr.payslip']
        year = fields.Date.from_string(date_from).year

        sal_brut_an = 0.0
        sal_brut_imp_an = 0.0
        charg_pat_an = 0.0
        charg_sal_an = 0.0
        heure_travail_an = 0.0

        payslips = Payslip.search([('employee_id','=',employee_id)])
        for slip in payslips:
            if slip.date_from and fields.Date.from_string(slip.date_from).year == year:
                if slip.worked_days_line_ids:
                    heure_travail_an += (173.33 / 30) * slip.worked_days_line_ids[0].number_of_days
                for line in slip.line_ids:
                    if line.category_id.code in ('BRUT','AVN'):
                        sal_brut_imp_an += line.total
                    elif line.category_id.code == 'BTOTAL':
                        sal_brut_an += line.total
                    elif line.category_id.code == 'COMP':
                        charg_pat_an += line.total
                    elif line.category_id.code in ('SALC','IR','DED'):
                        charg_sal_an += line.total
        return {
            'sal_brut_imp_an': sal_brut_imp_an,
            'sal_brut_an': sal_brut_an,
            'charg_pat_an': charg_pat_an,
            'charg_sal_an': charg_sal_an,
            'heure_travail_an': heure_travail_an,
        }
