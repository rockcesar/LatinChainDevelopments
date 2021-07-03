# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError

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
