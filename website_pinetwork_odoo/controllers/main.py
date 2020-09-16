# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website.controllers.main import Website

class Website(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        super(Website, self).index(**kw)
        return http.request.render('website_pinetwork_odoo.pinetwork', {})
