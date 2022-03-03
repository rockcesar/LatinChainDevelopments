'''
Created on Nov 18, 2018

@author: Zuhair Hammadi
'''
from odoo.addons.web.controllers.main import Database
from odoo import http
from werkzeug.exceptions import BadRequest

class MyDatabase(Database):

    @http.route()
    def selector(self, *args, **kwargs):    
        raise BadRequest()
    
    @http.route()
    def manager(self, *args, **kwargs):    
        raise BadRequest()
    
    @http.route()
    def create(self, *args, **kwargs):    
        raise BadRequest()
    
    @http.route()
    def duplicate(self, *args, **kwargs):    
        raise BadRequest()
    
    @http.route()
    def drop(self, *args, **kwargs):    
        raise BadRequest()
    
    @http.route()
    def backup(self, *args, **kwargs):    
        raise BadRequest()                    
        
    @http.route()
    def restore(self, *args, **kwargs):    
        raise BadRequest()                        
    
    @http.route()
    def change_password(self, *args, **kwargs):    
        raise BadRequest()         
    
    @http.route()
    def list(self, *args, **kwargs):    
        raise BadRequest()             