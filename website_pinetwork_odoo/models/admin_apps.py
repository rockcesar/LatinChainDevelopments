# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError
import requests
import json

import logging
_logger = logging.getLogger(__name__)

from datetime import datetime

from dateutil.relativedelta import relativedelta, MO

class pi_transactions(models.Model):
    _name = "pi.transactions"
    _description = "Pi Transactions"

    name = fields.Char('Name')
    app_id = fields.Many2one('admin.apps', required=True, ondelete='restrict')
    app = fields.Char(related="app_id.app")
    action = fields.Selection([('approve', 'Approve'), ('complete', 'Complete'), ('cancelled', 'Cancelled')], 'Action', required=True)
    payment_id = fields.Char('PaymentId', required=True)
    txid = fields.Text('TXID')
    txid_url = fields.Text('TXID URL', compute="_compute_txid_url")
    pi_user_id = fields.Char('Pi User ID')
    pi_user = fields.Many2one('pi.users', ondelete='restrict')
    amount = fields.Float('Amount', digits=(50,8))
    memo = fields.Char('Memo')
    to_address = fields.Char('To address')
    developer_approved = fields.Boolean('developer_approved')
    transaction_verified = fields.Boolean('transaction_verified')
    developer_completed = fields.Boolean('developer_completed')
    cancelled = fields.Boolean('cancelled')
    user_cancelled = fields.Boolean('user_cancelled')
    json_result = fields.Text('JSON Result', required=True)
    
    def _compute_txid_url(self):
        for pit in self:
            if pit.txid:
                pit.txid_url = "https://minepi.com/blockexplorer/tx/" + pit.txid
            else:
                pit.txid_url = ""
    
    def check_transactions(self):
        for pit in self:
            url = 'https://api.minepi.com/v2/payments/' + pit.payment_id
            
            re = requests.get(url,headers={'Authorization': "Key " + pit.app_id.admin_key})
            
            try:
                result = re.json()
                
                result_dict = json.loads(str(json.dumps(result)))
                
                if (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and pit.action!="cancelled":
                    pit.write({'action': 'cancelled'})
                elif result_dict['status']['developer_approved'] and not (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and pit.action!="approve":
                    pit.write({'action': 'approve'})
                if result_dict["status"]["transaction_verified"] and result_dict['status']['developer_completed'] and pit.action!="complete":
                    pit.write({'name': "complete. PaymentId: " + pit.payment_id,
                                'action': 'complete',
                                'payment_id': pit.payment_id,
                                'txid': result_dict["transaction"]["txid"],
                                'pi_user_id': result_dict["user_uid"],
                                'amount': result_dict["amount"],
                                'memo': result_dict["memo"],
                                'to_address': result_dict["to_address"]})
                    
                pit.write({'developer_approved': result_dict["status"]["developer_approved"], 
                        'transaction_verified': result_dict["status"]["transaction_verified"], 
                        'developer_completed': result_dict["status"]["developer_completed"], 
                        'cancelled': result_dict["status"]["cancelled"], 
                        'user_cancelled': result_dict["status"]["user_cancelled"],
                        'json_result': str(result_dict)})
                
                if pit.action == "cancelled" and (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and \
                    (datetime.now() - pit.create_date).days >= 1:
                    pit.unlink()
                elif pit.action == "approve" and result_dict["status"]["developer_approved"] and \
                    result_dict["status"]["transaction_verified"] and not result_dict["status"]["developer_completed"] and \
                    not (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']):
                    self.env["admin.apps"].pi_api({'action': "complete", 'txid': result_dict["transaction"]["txid"], 
                                                        'app_client': pit.app, 'paymentId': pit.payment_id})
                elif pit.action == "approve" and result_dict["status"]["developer_approved"] and \
                    not result_dict["status"]["transaction_verified"] and not result_dict["status"]["developer_completed"] and \
                    not (result_dict['status']['cancelled'] or result_dict['status']['user_cancelled']) and \
                    (datetime.now() - pit.create_date).days >= 1:
                    pit.unlink()
                    
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
    admin_key = fields.Char('Admin Key', required=True, groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    sandbox = fields.Boolean('Sandbox', required=True)
    pi_transactions_ids = fields.One2many('pi.transactions', 'app_id')
    pi_users_winners_ids = fields.Many2many('pi.users', 'admin_apps_pi_users_winners_rel', string='Winners')
    pi_users_winners_paid_ids = fields.Many2many('pi.users', 'admin_apps_pi_users_winners_paid_rel', string='Winners Paid', domain="[('id', 'in', pi_users_winners_ids)]")
    pi_users_winners_html = fields.Html('Winners HTML')
    block_points = fields.Boolean('Block points', default=False)
    amount = fields.Float('Amount', digits=(50,8), default=1)
    
    def pi_api(self, kw):
        
        if kw['action'] == "approve":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/approve'
            obj = {}
        elif kw['action'] == "complete":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/complete'
            obj = {'txid': kw['txid']}
            
        admin_app_list = self.env["admin.apps"].sudo().search([('app', '=', kw['app_client'])])
        
        if len(admin_app_list) == 0:
            result = {"result": False, "error": "SERVER MESSAGE: There is not API Key Stored in DB"}
            return json.dumps(result)
        
        re = requests.post(url,data=obj,json=obj,headers={'Authorization': "Key " + admin_app_list[0].admin_key})
        
        try:
            result = re.json()
            
            result_dict = json.loads(str(json.dumps(result)))
            
            if kw['action'] == "approve":
                pi_user = self.env['pi.users'].sudo().search([('pi_user_code', '=', kw['pi_user_code'])])
                self.env["pi.transactions"].sudo().create({'name': kw['action'] + ". PaymentId: " + kw['paymentId'],
                                                                'app_id': admin_app_list[0].id,
                                                                'action': kw['action'],
                                                                'payment_id': kw['paymentId'],
                                                                'json_result': str(result_dict),
                                                                'pi_user_id': result_dict["user_uid"],
                                                                'pi_user': pi_user[0].id,
                                                                'amount': result_dict["amount"],
                                                                'memo': result_dict["memo"],
                                                                'to_address': result_dict["to_address"],
                                                                'developer_approved': result_dict["status"]["developer_approved"], 
                                                                'transaction_verified': result_dict["status"]["transaction_verified"], 
                                                                'developer_completed': result_dict["status"]["developer_completed"], 
                                                                'cancelled': result_dict["status"]["cancelled"], 
                                                                'user_cancelled': result_dict["status"]["user_cancelled"]})
                self.env["pi.transactions"].sudo().search([('action', '=', 'approve'), 
                                                            ('pi_user_id', '=', result_dict["user_uid"])]).check_transactions()
                                                            
                result = {"result": True, "approved": True}
            elif kw['action'] == "complete":
                self.env["pi.transactions"].sudo().search([('payment_id', '=', kw['paymentId'])]).write(
                                                                {'name': kw['action'] + ". PaymentId: " + kw['paymentId'],
                                                                'app_id': admin_app_list[0].id,
                                                                'action': kw['action'],
                                                                'payment_id': kw['paymentId'],
                                                                'txid': kw['txid'],
                                                                'json_result': str(result_dict),
                                                                'pi_user_id': result_dict["user_uid"],
                                                                'amount': result_dict["amount"],
                                                                'memo': result_dict["memo"],
                                                                'to_address': result_dict["to_address"],
                                                                'developer_approved': result_dict["status"]["developer_approved"], 
                                                                'transaction_verified': result_dict["status"]["transaction_verified"], 
                                                                'developer_completed': result_dict["status"]["developer_completed"], 
                                                                'cancelled': result_dict["status"]["cancelled"], 
                                                                'user_cancelled': result_dict["status"]["user_cancelled"]})
                transaction = self.env["pi.transactions"].sudo().search([('payment_id', '=', kw['paymentId'])])
                
                result = {"result": True, "completed": False}
                if len(transaction) > 0 and kw['app_client'] in ['auth_pidoku', 'auth_snake', 'auth_platform', 'auth_example']:
                    if result_dict["status"]["transaction_verified"] and result_dict["status"]["developer_approved"] and result_dict["status"]["developer_completed"]:
                        users = transaction[0].pi_user
                        
                        if len(users) > 0:
                            if (users[0].paid + float(result_dict["amount"])) >= admin_app_list[0].amount:
                                users[0].sudo().write({'unblocked': True})
                                                    
                            users[0].sudo().write({'paid': users[0].paid + float(result_dict["amount"])})
                            
                        result = {"result": True, "completed": True}
            else:
                result = {"result": True, "completed": False, "approved": False}
                
        except Exception:
            result = {"result": False, "error": "SERVER MESSAGE: " + str(re)}
        
        return json.dumps(result)

class pi_users(models.Model):
    _name = "pi.users"
    _description = "Pi Users"
    
    _sql_constraints = [
        # Partial constraint, complemented by a python constraint (see below).
        ('pi_user_unique_key', 'unique (pi_user_code)', 'You can not have two users with the same User code!'),
    ]

    name = fields.Char('Name')
    pi_user_id = fields.Char('Pi User ID', required=True, groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    pi_user_code = fields.Char('Pi User Code', required=True)
    passkey = fields.Char('Pass Key')
    points = fields.Float('Pi User Points', compute="_total_points", store=True, digits=(50,8))
    points_chess = fields.Float('Chess Points', required=True, default=0, digits=(50,8))
    points_sudoku = fields.Float('Sudoku Points', required=True, default=0, digits=(50,8))
    points_snake = fields.Float('Snake Points', required=True, default=0, digits=(50,8))
    points_datetime = fields.Datetime('Points Datetime', compute="_compute_points_datetime", store=True)
    paid = fields.Float('Paid by user', digits=(50,8), groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    paid_in_transactions = fields.Float('Paid by user in transactions', compute="_total_paid_transactions", store=True, digits=(50,8))
    pi_transactions_ids = fields.One2many('pi.transactions', 'pi_user', groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    unblocked = fields.Boolean('Unblocked', compute="_total_paid_transactions", store=True)
    user_agent = fields.Char('User agent')
    last_connection = fields.Datetime(string='Last connection', default="")
    days_available = fields.Integer('Days available', store=True, default=0)
    admin_apps_winners_ids = fields.Many2many('admin.apps', 'admin_apps_pi_users_winners_rel', string='Winners Apps', groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    admin_apps_winners_paid_ids = fields.Many2many('admin.apps', 'admin_apps_pi_users_winners_paid_rel', string='Winners Paid Apps', domain="[('id', 'in', admin_apps_winners_ids)]", groups="website_pinetwork_odoo.group_pi_admin,base.group_system")
    donator = fields.Boolean('Donator', compute="_compute_donator", store=True)
    paid_in_all_donations = fields.Float('Paid by user in donations', compute="_compute_donator", store=True, digits=(50,8))
    
    @api.depends("pi_transactions_ids", "pi_transactions_ids.action", "pi_transactions_ids.app_id", "pi_transactions_ids.app_id.app")
    def _compute_donator(self):
        for i in self:
            i.donator = False
            transaction = self.env['pi.transactions'].search([('id', 'in', i.pi_transactions_ids.ids), ('app_id.app', '=', 'auth_example'), ('action', '=', 'complete')], limit=1)
            
            if len(transaction) == 0:
                i.donator = False
            else:
                i.donator = True
            
            total = 0    
            for j in i.pi_transactions_ids:
                if j.action == "complete" and j.app_id.app == "auth_example":
                    total += j.amount
            
            i.paid_in_all_donations = total
    
    @api.depends("points_chess", "points_sudoku", "points_snake", "paid", "unblocked", "pi_user_id")
    def _total_points(self):
        for i in self:
            i.points = i.points_chess + i.points_sudoku + i.points_snake
            
    @api.depends("points_chess", "points_sudoku", "points_snake")
    def _compute_points_datetime(self):
        for i in self:
            i.points_datetime = datetime.now()
    
    @api.depends("pi_transactions_ids", "pi_transactions_ids.action")
    def _total_paid_transactions(self):
        for i in self:
            total = 0
            for j in i.pi_transactions_ids:
                if j.action == "complete":
                    total += j.amount
            
            i.paid_in_transactions = total
            
            if i.paid_in_transactions > 0:
                i.unblocked = True
                
            transaction = self.env['pi.transactions'].search([('id', 'in', i.pi_transactions_ids.ids), ('action', '=', 'complete')], order="create_date desc", limit=1)
            
            if len(transaction) == 0:
                i.unblocked = False
                i.days_available = 0
            else:
                i.days_available = 30 - (datetime.now() - transaction[0].create_date).days
                
                if i.days_available < 0:
                    i.days_available = 0
                
                if i.days_available == 0:
                    i.unblocked = False

    def check_users(self):
        for piu in self:
            transaction = self.env['pi.transactions'].search([('id', 'in', piu.pi_transactions_ids.ids), ('action', '=', 'complete')], order="create_date desc", limit=1)
            
            if len(transaction) == 0:
                piu.write({'unblocked': False, 'days_available': 0})
            else:
                days_available = 30 - (datetime.now() - transaction[0].create_date).days
                
                if days_available < 0:
                    days_available = 0
                    
                piu.write({'days_available': days_available})
                
                if days_available == 0:
                    piu.write({'unblocked': False})
