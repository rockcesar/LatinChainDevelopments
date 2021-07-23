# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
import requests
import json

import logging
_logger = logging.getLogger(__name__)

class pi_transactions(models.Model):
    _name = "pi.transactions"
    _description = "Pi Transactions"

    name = fields.Char('Name')
    app_id = fields.Many2one('admin.apps', required=True)
    app = fields.Char(related="app_id.app")
    action = fields.Selection([('approve', 'Approve'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], 'Action', required=True)
    payment_id = fields.Char('PaymentId', required=True)
    txid = fields.Text('TXID')
    pi_user_id = fields.Char('Pi User ID')
    amount = fields.Float('Amount')
    memo = fields.Char('Memo')
    to_address = fields.Char('To address')
    json_result = fields.Text('JSON Result', required=True)
    
    def check_transactions(self):
        for pit in self:
            
            url = 'https://api.minepi.com/v2/payments/' + pit.payment_id
            
            re = requests.get(url,headers={'Authorization': "Key " + pit.app_id.admin_key})
            
            try:
                result = re.json()
                
                result_dict = json.loads(str(json.dumps(result)))
                
                if (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and pit.action!="cancelled":
                    pit.write({'action': 'cancelled', 'json_result': str(result_dict)})
                elif result_dict['status']['developer_approved'] and not (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and pit.action!="approve":
                    pit.write({'action': 'approve', 'json_result': str(result_dict)})
                if result_dict['status']['developer_completed']  and pit.action!="complete":
                    pit.write({'action': 'complete', 'json_result': str(result_dict)})
                    
            except Exception:
                _logger.info(str(re))

class admin_apps(models.Model):
    _name = "admin.apps"
    _description = "Admin Pi App"
    
    _sql_constraints = [
        # Partial constraint, complemented by a python constraint (see below).
        ('admin_apps_unique_key', 'unique (app)', 'You can not have two app with the same App code!'),
    ]

    name = fields.Char('Name')
    app = fields.Char('App code', required=True)
    admin_key = fields.Char('Admin Key', required=True)
    sandbox = fields.Boolean('Sandbox', required=True)
    pi_transactions_ids = fields.One2many('pi.transactions', 'app_id')
