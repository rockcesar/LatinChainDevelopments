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
        return http.request.render('website_pinetwork_games_odoo.mainpage', {})

class PiNetworkController(http.Controller):
    @http.route('/pinetwork', type='http', auth="public", website=True)
    def index(self, **kw):
        return http.request.render('website_pinetwork_games_odoo.pinetwork', {})
    
    @http.route('/sudoku', type='http', auth="public", website=True)
    def sudoku(self, **kw):
        return http.request.render('website_pinetwork_games_odoo.sudoku', {})
    
    @http.route('/snake', type='http', auth="public", website=True)
    def snake(self, **kw):
        return http.request.render('website_pinetwork_games_odoo.snake', {})
        
    @http.route('/chess', type='http', auth="public", website=True)
    def chess(self, **kw):
        return http.request.render('website_pinetwork_games_odoo.chess', {})
        
    @http.route('/pi-api', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_api(self, **kw):
        
        if kw['action'] == "approve":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/approve'
            obj = {}
        elif kw['action'] == "complete":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/complete'
            obj = {'txid': kw['txid']}
            
        admin_app_list = request.env["admin.apps"].search([('app', '=', kw['app_client'])])
        
        if len(admin_app_list) == 0:
            result = {"error": "SERVER MESSAGE: There is not API Key Stored in DB"}
            return json.dumps(result)
        
        re = requests.post(url,data=obj,json=obj,headers={'Authorization': "Key " + admin_app_list[0].admin_key})
        
        try:
            result = re.json()
        except Exception:
            result = {"error": "SERVER MESSAGE: " + str(re)}
        
        return json.dumps(result)
