# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    'name': 'LatinChain Platform (Pi Network Games Engine and Platform for Odoo)',
    'category': 'Website/Website',
    'sequence': 54,
    'summary': 'Pi Network Games Engine and Platform for Odoo',
    'version': '2.1',
    "author": "César Cordero Rodríguez <cesar.cordero.r@gmail.com>",
    "website": "https://cr-innova.negocio.site/",
    "contributors": [
        "César Cordero Rodríguez <cesar.cordero.r@gmail.com>",
    ],
    "license": "",
    'description': """
Pi Hackathon winners: https://dev-rockcesar.blogspot.com/2021/05/pi-apps-published.html

Pi, Pi Network and the Pi logo are trademarks of the Pi Community Company.

LatinChain Platform (Pi Network Games Engine and Platform for Odoo)
-----------------

Games Leaders board, Pi API Platform integration, Games.

Pi is a new digital currency developed by Stanford PhDs, with over 18 million members worldwide (at July 2021). To claim your Pi, follow this link https://minepi.com/rockcesar and use my username (rockcesar) as your invitation code.

Referal link: https://minepi.com/rockcesar
Referal code: rockcesar

Documentation: https://developers.minepi.com

Pi Developers: https://developers.minepi.com/

Repository: https://github.com/rockcesar/PiNetworkDevelopments

Institutional Repository: https://github.com/pi-apps/LatinChain

Odoo Developments: https://github.com/rockcesar/odoo_addons

Check our apps published: https://dev-rockcesar.blogspot.com/2021/05/pi-apps-published.html

To test, you have to use Pi Browser.

Main page: /""",
    'depends': ['website', 'portal', 'web', 'website_pinetwork_odoo'],
    'data': [
        'views/website_pinetwork_templates.xml',
        'views/website_pinetwork_templates_sudoku.xml',
        'views/website_pinetwork_templates_snake.xml',
        'views/website_pinetwork_templates_chess.xml',
        'views/website_pinetwork_templates_mainpage.xml',
        'views/website_debranding_templates.xml',
        'views/website_pinetwork_templates_modal.xml',
        'views/website_pinetwork_templates_rules.xml',
        'data/data.xml',
    ],
    'images': ['static/description/icon.png'],
    'qweb': [],
    'installable': True,
    'auto_install': True,
}
