# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

import requests

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.website.controllers.main import Website

class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        super(Website, self).index(**kw)
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_games_odoo.mainpage', {'sandbox': sandbox})

class PiNetworkController(http.Controller):
    @http.route('/pinetwork', type='http', auth="public", website=True)
    def index(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_example')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_games_odoo.pinetwork', {'sandbox': sandbox})
    
    @http.route('/sudoku', type='http', auth="public", website=True)
    def sudoku(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_pidoku')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_games_odoo.sudoku', {'sandbox': sandbox})
    
    @http.route('/snake', type='http', auth="public", website=True)
    def snake(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_snake')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_games_odoo.snake', {'sandbox': sandbox})
        
    @http.route('/chess', type='http', auth="public", website=True)
    def chess(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_games_odoo.chess', {'sandbox': sandbox})
        
    @http.route('/pi-api', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_api(self, **kw):
        
        if kw['action'] == "approve":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/approve'
            obj = {}
        elif kw['action'] == "complete":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/complete'
            obj = {'txid': kw['txid']}
            
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', kw['app_client'])])
        
        if len(admin_app_list) == 0:
            result = {"error": "SERVER MESSAGE: There is not API Key Stored in DB"}
            return json.dumps(result)
        
        re = requests.post(url,data=obj,json=obj,headers={'Authorization': "Key " + admin_app_list[0].admin_key})
        
        try:
            result = re.json()
        except Exception:
            result = {"error": "SERVER MESSAGE: " + str(re)}
        
        return json.dumps(result)
