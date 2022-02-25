# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

import requests

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.website.controllers.main import Website

from odoo.addons.portal.controllers.portal import CustomerPortal

from random import choice

from datetime import datetime

"""
class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        super(Website, self).index(**kw)
        return http.request.render('website_pinetwork_odoo.mainpage', {})
"""

winner_domain = [('unblocked', '=', True), ('points_chess', '>=', 20), ('points_sudoku', '>', 18), ('points_snake', '>', 20), ('points', '>', 200)]
leaders_domain = [('unblocked', '=', True)]

class CustomerPortalInherit(CustomerPortal):
    @http.route('/my/security', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def security(self, **post):
        return request.redirect('/')

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
    
    @http.route('/get-external-user', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def get_external_user(self, **kw):
        pi_users_list = request.env["pi.users"].sudo().search([('pi_user_code', '=', kw['pi_user_code'])])
        
        if len(pi_users_list) == 0:
            return json.dumps({'result': False})
        
        return json.dumps({'result': True, 'pi_user_code': pi_users_list[0].pi_user_code,
                            'points': pi_users_list[0].points, 'points_chess': pi_users_list[0].points_chess, 
                            'points_sudoku': pi_users_list[0].points_sudoku,
                            'points_snake': pi_users_list[0].points_snake, 'unblocked': pi_users_list[0].unblocked})
    
    @http.route('/get-user', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def get_user(self, **kw):
        re = requests.get('https://api.minepi.com/v2/me',data={},json={},headers={'Authorization': "Bearer " + kw['accessToken']})
        
        try:
            result = re.json()
            
            result_dict = json.loads(str(json.dumps(result)))
            
            if not (result_dict['uid'] == kw['pi_user_id'] and result_dict['username'] == kw['pi_user_code']):
                _logger.info("Authorization failed")
                return json.dumps({'result': False})
        except Exception:
            _logger.info("Authorization error")
            return json.dumps({'result': False})
        
        pi_users_list = request.env["pi.users"].sudo().search([('pi_user_code', '=', kw['pi_user_code'])])
        
        if len(pi_users_list) == 0:
            return json.dumps({'result': False})
        
        passkey = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789%^*(-_=+)') for i in range(10)])
        
        pi_users_list[0].sudo().write({'passkey': passkey})
        
        return json.dumps({'result': True, 'pi_user_id': pi_users_list[0].pi_user_id, 'pi_user_code': pi_users_list[0].pi_user_code,
                            'points': pi_users_list[0].points, 'points_chess': pi_users_list[0].points_chess, 
                            'points_sudoku': pi_users_list[0].points_sudoku,
                            'points_snake': pi_users_list[0].points_snake, 'unblocked': pi_users_list[0].unblocked,
                            'days_available': pi_users_list[0].days_available,
                            'passkey': passkey})
        
    @http.route('/pi-api', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_api(self, **kw):
        re = requests.get('https://api.minepi.com/v2/me',data={},json={},headers={'Authorization': "Bearer " + kw['accessToken']})
        
        try:
            result = re.json()
            
            result_dict = json.loads(str(json.dumps(result)))
            
            if not (result_dict['uid'] == kw['pi_user_id'] and result_dict['username'] == kw['pi_user_code']):
                _logger.info("Authorization failed")
                return json.dumps({'result': False})
        except Exception:
            _logger.info("Authorization error")
            return json.dumps({'result': False})
        
        return request.env["admin.apps"].pi_api(kw)
        
    @http.route('/pi-points', type='http', auth="public", website=True, csrf=False, methods=['POST'])
    def pi_points(self, **kw):
        admin_apps_block_list = request.env["admin.apps"].sudo().search([('app', '=', "auth_platform"), ('block_points', '=', True)])
        
        if len(admin_apps_block_list) > 0 and float(kw['points']) != 0:
            return json.dumps({'result': False})
        
        re = requests.get('https://api.minepi.com/v2/me',data={},json={},headers={'Authorization': "Bearer " + kw['accessToken']})
        #_logger.info(kw['accessToken'])
        try:
            result = re.json()
            
            result_dict = json.loads(str(json.dumps(result)))
            
            if not (result_dict['uid'] == kw['pi_user_id'] and result_dict['username'] == kw['pi_user_code']):
                _logger.info("Authorization failed")
                return json.dumps({'result': False})
        except Exception:
            _logger.info("Authorization error")
            return json.dumps({'result': False})
        
        pi_users_list = request.env["pi.users"].sudo().search([('pi_user_code', '=', kw['pi_user_code'])])
        
        if len(pi_users_list) == 0:
            request.env["pi.users"].sudo().create({'name': kw['pi_user_code'],
                                                    'pi_user_id': kw['pi_user_id'],
                                                    'pi_user_code': kw['pi_user_code'],
                                                    'points': 0,
                                                    'points_chess': 0,
                                                    'points_sudoku': 0,
                                                    'points_snake': 0,
                                                    'paid': 0,
                                                    'unblocked': False,
                                                    'user_agent': request.httprequest.environ.get('HTTP_USER_AGENT', ''),
                                                    'last_connection': datetime.now(),
                                                })
        else:
            #if 'passkey' not in kw:
            #    _logger.info("PASSKEY NOT PRESENT")
            #    return json.dumps({'result': False})
                
            #if kw['passkey'] != pi_users_list[0].passkey:
            #    _logger.info("PASSKEY DOESN'T MATCH: " + str(kw['passkey']))
            #    return json.dumps({'result': False})
            
            values = {'name': kw['pi_user_code'],
                                'pi_user_id': kw['pi_user_id'],
                                'pi_user_code': kw['pi_user_code'],
                                'user_agent': request.httprequest.environ.get('HTTP_USER_AGENT', ''),
                                'last_connection': datetime.now(),
                            }
            
            if pi_users_list[0].unblocked:
                #if float(kw['points']) > 0:
                #    pi_users_winnners_count = request.env["pi.users"].sudo().search_count(winner_domain)
                #    
                #    if pi_users_winnners_count >= 10:
                #        return json.dumps({'result': False})
                
                if 'app_client' in kw:
                    if kw['app_client'] == "auth_platform":
                        values.update({'points_chess': pi_users_list[0].points_chess + float(kw['points'])})
                    elif kw['app_client'] == "auth_pidoku":
                        values.update({'points_sudoku': pi_users_list[0].points_sudoku + float(kw['points'])})
                    elif kw['app_client'] == "auth_snake":
                        values.update({'points_snake': pi_users_list[0].points_snake + float(kw['points'])})
            elif not pi_users_list[0].unblocked and float(kw['points']) > 0:
                return json.dumps({'result': False})
                    
            pi_users_list[0].sudo().write(values)
        
        return json.dumps({'result': True})
        
    @http.route('/get-points/<string:pi_user_code>', type='http', auth="public", website=True)
    def get_points_user(self, pi_user_code, **kw):
        pi_users_verified_count = request.env["pi.users"].sudo().search_count(leaders_domain)
        
        pi_users_count = request.env["pi.users"].sudo().search_count([])
        
        pi_users_list = request.env["pi.users"].sudo().search(leaders_domain, limit=50, order="points desc,unblocked desc,points_datetime asc")
        
        pi_user = request.env["pi.users"].sudo().search([('pi_user_code', '=', pi_user_code)])
        
        return http.request.render('website_pinetwork_odoo.list_points', {'pi_users_verified_count': pi_users_verified_count, 'pi_users_count': pi_users_count, 'pi_users_list': pi_users_list, 'pi_user': pi_user})
        
    @http.route('/get-points/', type='http', auth="public", website=True)
    def get_points(self, **kw):
        pi_users_verified_count = request.env["pi.users"].sudo().search_count(leaders_domain)
        
        pi_users_count = request.env["pi.users"].sudo().search_count([])
        
        pi_users_list = request.env["pi.users"].sudo().search(leaders_domain, limit=50, order="points desc,unblocked desc,points_datetime asc")
        
        return http.request.render('website_pinetwork_odoo.list_points', {'pi_users_verified_count': pi_users_verified_count, 'pi_users_count': pi_users_count, 'pi_users_list': pi_users_list})
    
    @http.route('/get-winners/<string:pi_user_code>', type='http', auth="public", website=True)
    def get_winners_user(self, pi_user_code, **kw):
        pi_users_verified_count = request.env["pi.users"].sudo().search_count(leaders_domain)
        
        pi_users_count = request.env["pi.users"].sudo().search_count([])
        
        pi_users_list = request.env["pi.users"].sudo().search(winner_domain, limit=10, order="points desc,unblocked desc,points_datetime asc")
        
        pi_user = request.env["pi.users"].sudo().search([('pi_user_code', '=', pi_user_code)])
        
        return http.request.render('website_pinetwork_odoo.list_winners', {'pi_users_verified_count': pi_users_verified_count, 'pi_users_count': pi_users_count, 'pi_users_list': pi_users_list, 'pi_user': pi_user})
        
    @http.route('/get-winners/', type='http', auth="public", website=True)
    def get_winners(self, **kw):
        pi_users_verified_count = request.env["pi.users"].sudo().search_count(leaders_domain)
        
        pi_users_count = request.env["pi.users"].sudo().search_count([])
        
        pi_users_list = request.env["pi.users"].sudo().search(winner_domain, limit=10, order="points desc,unblocked desc,points_datetime asc")
        
        return http.request.render('website_pinetwork_odoo.list_winners', {'pi_users_verified_count': pi_users_verified_count, 'pi_users_count': pi_users_count, 'pi_users_list': pi_users_list})

    @http.route('/get-winners/<string:pi_user_code>', type='http', auth="public", website=True)
    def get_winners_user(self, pi_user_code, **kw):
        pi_users_verified_count = request.env["pi.users"].sudo().search_count(leaders_domain)
        
        pi_users_count = request.env["pi.users"].sudo().search_count([])
        
        pi_users_list = request.env["pi.users"].sudo().search(winner_domain, limit=10, order="points desc,unblocked desc,points_datetime asc")
        
        pi_user = request.env["pi.users"].sudo().search([('pi_user_code', '=', pi_user_code)])
        
        return http.request.render('website_pinetwork_odoo.list_winners', {'pi_users_verified_count': pi_users_verified_count, 'pi_users_count': pi_users_count, 'pi_users_list': pi_users_list, 'pi_user': pi_user})
        
    @http.route('/get-credits/', type='http', auth="public", website=True)
    def get_credits(self, **kw):
        pi_users_count = request.env["pi.users"].sudo().search([('pi_transactions_ids.app_id.app', '=', 'auth_example')])

        counter = 0
        for i in pi_users_count:
            if self.env['pi.transactions'].sudo().search_count([('id', 'in', i.pi_transactions_ids.ids), ('app_id.app', '=', 'auth_example'), ('action', '=', 'complete')]) > 0:
                counter += 1
        
        return http.request.render('website_pinetwork_odoo.list_credits', {'pi_users_count': counter})

    @http.route('/get-credits-data/', type='http', auth="public", website=True, methods=['POST'], csrf=False)
    def get_credits_data(self, **kw):
        #_logger.info(str(kw))
        
        draw = kw['draw'];
        row = kw['start'];
        rowperpage = kw['length'];
        columnIndex = kw["order[0][column]"]
        columnName = kw["columns[0][data]"]
        columnSortOrder = kw["order[0][dir]"]
        searchValue = kw["search[value]"]
        
        pi_users_count = request.env["pi.users"].sudo().search([('pi_transactions_ids.app_id.app', '=', 'auth_example')])
        
        counter = 0
        for i in pi_users_count:
            if self.env['pi.transactions'].sudo().search_count([('id', 'in', i.pi_transactions_ids.ids), ('app_id.app', '=', 'auth_example'), ('action', '=', 'complete')]) > 0:
                counter += 1
        
        pi_users_count_filter = request.env["pi.users"].sudo().search([('pi_transactions_ids.app_id.app', '=', 'auth_example'), ('pi_user_code', 'like', '%' + searchValue + '%')])
        
        counter_filter = 0
        for i in pi_users_count_filter:
            if self.env['pi.transactions'].sudo().search_count([('id', 'in', i.pi_transactions_ids.ids), ('app_id.app', '=', 'auth_example'), ('action', '=', 'complete')]) > 0:
                counter_filter += 1
        
        pi_users_list = request.env["pi.users"].sudo().search([('pi_transactions_ids.app_id.app', '=', 'auth_example'), ('pi_user_code', 'like', '%' + searchValue + '%')], order="unblocked desc, " + columnName + " " + columnSortOrder, limit=int(rowperpage), offset=int(row))
        
        counter_filter = 0
        for i in pi_users_list:
            if self.env['pi.transactions'].sudo().search_count([('id', 'in', i.pi_transactions_ids.ids), ('app_id.app', '=', 'auth_example'), ('action', '=', 'complete')]) == 0:
                del i
        
        data = []
        for i in pi_users_list:
            verified = ""
            if i.unblocked:
                verified = "(verified)"
            else:
                verified = ""
            data.append({'pi_user_code': i.pi_user_code + " " + verified})
        
        return json.dumps({'draw': int(draw), 'aaData': data, "iTotalRecords": pi_users_count, "iTotalDisplayRecords": pi_users_count_filter})
        
    @http.route('/validation-key.txt', type='http', auth="public", website=True, csrf=False)
    def validation_txt(self, **kw):
        return "440b3e77563e4151952010f7a7768ae060bb0408c33604322acca070824ce31fc8bdb73cc819e4acd4600d7f8aabce29ff4242fb00a1ae79bca414c11b7ad0b4"
