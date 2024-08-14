# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json

import requests

from werkzeug.utils import redirect

import logging
_logger = logging.getLogger(__name__)

from odoo.addons.website.controllers.main import Website

from datetime import datetime, timedelta

class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        #super(Website, self).index(**kw)
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            no_footer = True
            total_transactions_daily_count = 0
            total_users_daily_count = 0
            pi_main_user = False
            points_latin_amount = 1
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            if mainnet in ['Mainnet ON', 'Mainnet OFF']:
                no_footer = False
            else:
                no_footer = True
            total_transactions_daily_count = int(admin_app_list[0].total_transactions_daily_count)
            total_users_daily_count = int(admin_app_list[0].total_users_daily_count)
            pioneers_streaming = admin_app_list[0].pioneers_streaming
            pi_main_user = admin_app_list[0].pi_main_user
            points_latin_amount = admin_app_list[0].points_latin_amount
        
        return http.request.render('website_pinetwork_games_odoo.mainpage', {'points_latin_amount': points_latin_amount, 'pi_main_user': pi_main_user, 'pioneers_streaming': pioneers_streaming, 'total_transactions_daily_count': total_transactions_daily_count, 'total_users_daily_count': total_users_daily_count, 'no_footer': True, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})

class PiNetworkController(http.Controller):
    @http.route('/radioforus', type='http', auth="public", website=True)
    def radioforus(self, **kw):
        
        link_back = "https://mainnet.radioforus.com"
        if 'link_back' not in kw:
            if 'HTTP_REFERER' in http.request.httprequest.environ and 'HTTP_HOST' in http.request.httprequest.environ:
                if "https://radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://test.latin-chain.com/radioforus?link_back=https://radioforus.com")
                elif "https://mainnet.radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://latin-chain.com/radioforus?link_back=https://mainnet.radioforus.com")
            else:
                if http.request.httprequest.environ['HTTP_HOST'] == "latin-chain.com":
                    link_back = "https://mainnet.radioforus.com"
                elif http.request.httprequest.environ['HTTP_HOST'] == "test.latin-chain.com":
                    link_back = "https://radioforus.com"
        else:
            link_back = kw['link_back']
        
        """
        link_back = "https://mainnet.radioforus.com"
        if 'link_back' not in kw:
            if 'HTTP_REFERER' in http.request.httprequest.environ and 'HTTP_HOST' in http.request.httprequest.environ:
                if "https://radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://" + http.request.httprequest.environ['HTTP_HOST'] + "/radioforus?link_back=https://radioforus.com")
                elif "https://mainnet.radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://" + http.request.httprequest.environ['HTTP_HOST'] + "/radioforus?link_back=https://mainnet.radioforus.com")
        else:
            link_back = kw['link_back']
        """
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_example')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            points_latin_amount = 1
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            points_latin_amount = admin_app_list[0].points_latin_amount
        
        return http.request.render('website_pinetwork_games_odoo.radioforus', {'points_latin_amount': points_latin_amount, 'link_back': link_back, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})
    
    @http.route('/get-transactions-radioforus/', type='http', auth="public", website=True)
    def get_transactions_radioforus(self, **kw):
        
        link_back = "https://mainnet.radioforus.com"
        if 'link_back' not in kw:
            if 'HTTP_REFERER' in http.request.httprequest.environ and 'HTTP_HOST' in http.request.httprequest.environ:
                if "https://radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://test.latin-chain.com/get-transactions-radioforus?link_back=https://radioforus.com")
                elif "https://mainnet.radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://latin-chain.com/get-transactions-radioforus?link_back=https://mainnet.radioforus.com")
            else:
                if http.request.httprequest.environ['HTTP_HOST'] == "latin-chain.com":
                    link_back = "https://mainnet.radioforus.com"
                elif http.request.httprequest.environ['HTTP_HOST'] == "test.latin-chain.com":
                    link_back = "https://radioforus.com"
        else:
            link_back = kw['link_back']
        
        """
        link_back = "https://mainnet.radioforus.com"
        if 'link_back' not in kw:
            if 'HTTP_REFERER' in http.request.httprequest.environ and 'HTTP_HOST' in http.request.httprequest.environ:
                if "https://radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://" + http.request.httprequest.environ['HTTP_HOST'] + "/get-transactions-radioforus?link_back='https://radioforus.com'")
                elif "https://mainnet.radioforus.com" in http.request.httprequest.environ['HTTP_REFERER']:
                    return redirect("https://" + http.request.httprequest.environ['HTTP_HOST'] + "/get-transactions-radioforus?link_back='https://mainnet.radioforus.com'")
        else:
            link_back = kw['link_back']
        """
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            mainnet = ""
            google_adsense = ""
        else:
            sandbox = admin_app_list[0].sandbox
            mainnet = admin_app_list[0].mainnet
            google_adsense = admin_app_list[0].google_adsense
        
        return http.request.render('website_pinetwork_games_odoo.list_transactions_radioforus', {'link_back': link_back, 'sandbox': sandbox, 'mainnet': mainnet, 'google_adsense': google_adsense})
    
    @http.route('/tetris/', type='http', auth="public", website=True)
    def tetris(self, **kw):
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            mainnet = ""
            google_adsense = ""
        else:
            sandbox = admin_app_list[0].sandbox
            mainnet = admin_app_list[0].mainnet
            google_adsense = admin_app_list[0].google_adsense
        
        return http.request.render('website_pinetwork_games_odoo.tetris', {'sandbox': sandbox, 'mainnet': mainnet, 'google_adsense': google_adsense})
    
    @http.route('/mahjong/', type='http', auth="public", website=True)
    def mahjong(self, **kw):
        
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            mainnet = ""
            google_adsense = ""
        else:
            sandbox = admin_app_list[0].sandbox
            mainnet = admin_app_list[0].mainnet
            google_adsense = admin_app_list[0].google_adsense
        
        return http.request.render('website_pinetwork_games_odoo.mahjong', {'sandbox': sandbox, 'mainnet': mainnet, 'google_adsense': google_adsense})
    
    @http.route('/latinchain_x', type='http', auth="public", website=True)
    def latinchain_x(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            announcement_html = ""
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            announcement_html = admin_app_list[0].announcement_html
        
        return http.request.render('website_pinetwork_games_odoo.latinchain_x', {'announcement_html': announcement_html, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})
    
    @http.route('/pinetwork', type='http', auth="public", website=True)
    def index(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_example')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            points_latin_amount = 1
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            points_latin_amount = admin_app_list[0].points_latin_amount
        
        return http.request.render('website_pinetwork_games_odoo.pinetwork', {'points_latin_amount': points_latin_amount, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})
    
    @http.route('/sudoku', type='http', auth="public", website=True)
    def sudoku(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_pidoku')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            points_latin_amount = 1
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            points_latin_amount = admin_app_list[0].points_latin_amount
        
        return http.request.render('website_pinetwork_games_odoo.sudoku', {'points_latin_amount': points_latin_amount, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})
    
    @http.route('/snake', type='http', auth="public", website=True)
    def snake(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_snake')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
        
        return http.request.render('website_pinetwork_games_odoo.snake', {'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 
                                                                        'google_adsense': google_adsense, 'a_ads': a_ads, 
                                                                        'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style,
                                                                        'hide_google_translate': True,
                                                                        'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 
                                                                        'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 
                                                                        'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})
        
    @http.route('/chess', type='http', auth="public", website=True)
    def chess(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            sandbox = False
            amount = False
            google_adsense = ""
            a_ads = ""
            a_ads_data = ""
            a_ads_style = ""
            a_ads_2 = ""
            a_ads_data_2 = ""
            a_ads_style_2 = ""
            a_ads_3 = ""
            a_ads_data_3 = ""
            a_ads_style_3 = ""
            mainnet = ""
            points_latin_amount = 1
        else:
            sandbox = admin_app_list[0].sandbox
            amount = admin_app_list[0].amount
            google_adsense = admin_app_list[0].google_adsense
            a_ads = admin_app_list[0].a_ads
            a_ads_data = admin_app_list[0].a_ads_data
            a_ads_style = admin_app_list[0].a_ads_style
            a_ads_2 = admin_app_list[0].a_ads_2
            a_ads_data_2 = admin_app_list[0].a_ads_data_2
            a_ads_style_2 = admin_app_list[0].a_ads_style_2
            a_ads_3 = admin_app_list[0].a_ads_3
            a_ads_data_3 = admin_app_list[0].a_ads_data_3
            a_ads_style_3 = admin_app_list[0].a_ads_style_3
            mainnet = admin_app_list[0].mainnet
            points_latin_amount = admin_app_list[0].points_latin_amount
        
        return http.request.render('website_pinetwork_games_odoo.chess', {'points_latin_amount': points_latin_amount, 'mainnet': mainnet, 'sandbox': sandbox, 'amount': amount, 'google_adsense': google_adsense, 'a_ads': a_ads, 'a_ads_data': a_ads_data, 'a_ads_style': a_ads_style, 'a_ads_2': a_ads_2, 'a_ads_data_2': a_ads_data_2, 'a_ads_style_2': a_ads_style_2, 'a_ads_3': a_ads_3, 'a_ads_data_3': a_ads_data_3, 'a_ads_style_3': a_ads_style_3})

    @http.route('/modal-vote', type='http', auth="public", website=True, csrf=False)
    def modal_vote(self, **kw):
        
        return http.request.render('website_pinetwork_games_odoo.modal')
        
    @http.route('/modal-rules', type='http', auth="public", website=True, csrf=False)
    def modal_rules(self, **kw):
        admin_app_list = request.env["admin.apps"].sudo().search([('app', '=', 'auth_platform')])
        
        if len(admin_app_list) == 0:
            amount = False
            pi_users_winners_paid_datetime = False
            mainnet = ""
        else:
            amount = admin_app_list[0].amount
            pi_users_winners_paid_datetime = admin_app_list[0].pi_users_winners_paid_datetime
            mainnet = admin_app_list[0].mainnet
        
        return http.request.render('website_pinetwork_games_odoo.rules', {'mainnet': mainnet, 'amount': amount, 'pi_users_winners_paid_datetime': pi_users_winners_paid_datetime})
