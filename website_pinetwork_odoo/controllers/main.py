# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

import requests

import logging
_logger = logging.getLogger(__name__)

class PiNetworkController(http.Controller):
    @http.route('/pinetwork', type='http', auth="public", website=True)
    def index(self, **kw):
        return http.request.render('website_pinetwork_odoo.pinetwork', {})
        
    @http.route('/pi-api', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_api(self, **kw):
        
        if kw['action'] == "approve":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/approve'
            obj = {}
        elif kw['action'] == "complete":
            url = 'https://api.minepi.com/v2/payments/' + kw['paymentId'] + '/complete'
            obj = {'txid': kw['txid']}
        
        re = requests.post(url,data=obj,headers={'Authorization':'Key <your Server API Key>'})
        
        try:
            result = re.json()
        except Exception:
            result = {"error": "SERVER MESSAGE: " + str(re)}
        
        return json.dumps(result)
