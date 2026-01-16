# -*- coding: utf-8 -*-
{
    'name': 'ARSATA Payroll',
    'author': 'Mansour Diop',
    'category': 'Human Resources',
    'summary': 'Module de paie développé par ARSATA CONSULTING',
    'sequence': 9,
    'description': """
Module de paie complet pour Odoo 18.
Inclut la gestion des contrats, des bulletins de paie, des règles de salaire,
des conventions collectives, et les rapports liés aux cotisations sociales.
""",
    'depends': [
        'base',
        'hr',
        'hr_contract',
        'hr_payroll','report_xlsx',
        # 'arsata_base',
        # 'hr_payroll_account'
    ],
    'data': [
       
        # Vues
        
        'views/hr_contract_view.xml',
        'views/periode_paie.xml',
        'views/hr_payroll_view.xml',
        
        'views/convention_view.xml',
        'views/ipres_xlsx.xml',
        'views/xls_ipres.xml',


        'views/report_declaration_retenu.xml',
        # 'views/hr_holidays_status_inherit_view.xml',
       #  'views/cerco_payslip_line_contributor_register.xml',
        'views/report_cotisation_ipres.xml',
       # 'views/report_securite_sociale.xml',
       # 'views/report_declaration_retenu.xml',
        
        # Rapports
        'report/template.xml',
        'report/report_payroll.xml',
         'report/order_payement_hr_report.xml',
        
        # Wizards
        'wizard/ordre_virement_hr_wizard_view.xml',
         # Sécurité
        'security/cerco_security.xml',
        'security/ir.model.access.csv',
        
       
        
    ],
    'demo': [],
        #'data/image.xml',
        # 'data/update_value_wage.xml',  # Tâche planifiée pour mise à jour automatique du salaire
        # 'data/salary_rule_data.xml',
        # 'data/convention_collective_data.xml'
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
