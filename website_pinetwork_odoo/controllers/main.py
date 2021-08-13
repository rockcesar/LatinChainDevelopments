# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

import requests

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.website.controllers.main import Website

"""
class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        super(Website, self).index(**kw)
        return http.request.render('website_pinetwork_odoo.mainpage', {})
"""

class PiNetworkBaseController(http.Controller):
    @http.route('/mainpage', type='http', auth="public", website=True)
    def index(self, **kw):
                    
        return http.request.render('website_pinetwork_odoo.mainpage')
    
    @http.route('/example', type='http', auth="public", website=True)
    def example(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_first_app')])
        
        if len(admin_app_list) == 0:
            sandbox = False
        else:
            sandbox = admin_app_list[0].sandbox
        
        return http.request.render('website_pinetwork_odoo.example', {'sandbox': sandbox})
        
    @http.route('/pi-api', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_api(self, **kw):
        return request.env["admin.apps"].pi_api(kw)
        
    @http.route('/pi-points', type='http', auth="public", website=True, csrf=True, methods=['POST'])
    def pi_points(self, **kw):
        pi_users_list = request.env["pi.users"].sudo().search([('pi_user_id', '=', kw['pi_user_id'])])
        
        if len(pi_users_list) == 0:
            request.env["pi.users"].sudo().create({'name': kw['pi_user_code'],
                                                    'pi_user_id': kw['pi_user_id'],
                                                    'pi_user_code': kw['pi_user_code'],
                                                    'points': kw['points'],
                                                })
        else:
            pi_users_list[0].sudo().write({'name': kw['pi_user_code'],
                                                    'pi_user_id': kw['pi_user_id'],
                                                    'pi_user_code': kw['pi_user_code'],
                                                    'points': pi_users_list[0].points + float(kw['points']),
                                                })
        
        return json.dumps({'result': True})
        
    @http.route('/get-points', type='http', auth="public", website=True)
    def get_points(self, **kw):
        pi_users_list = request.env["pi.users"].sudo().search([], limit=50, order="points desc")
        
        return http.request.render('website_pinetwork_odoo.list_points', {'pi_users_list': pi_users_list})
