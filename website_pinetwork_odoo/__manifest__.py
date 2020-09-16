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
    'name': 'PiNetwork Hello World for Odoo',
    'category': 'Website/Website',
    'sequence': 54,
    'summary': 'PiNetwork Hello World',
    'version': '2.1',
    "author": "César Cordero Rodríguez <cesar.cordero.r@gmail.com>",
    "website": "https://cr-innova.negocio.site/",
    "contributors": [
        "César Cordero Rodríguez <cesar.cordero.r@gmail.com>",
    ],
    'description': """
PiNetwork Hello World for Odoo
-----------------

This simple application show a PiNetwork Hello World example in the root (/) of the Odoo Server.

Pi is a new digital currency developed by Stanford PhDs, with over 8 million members worldwide (at September 2020). To claim your Pi, follow this link https://minepi.com/rockcesar and use my username (rockcesar) as your invitation code.

I'm developing Pi Apps for the Pi Network Apps Platform, also, watch this video

https://youtu.be/zMUKTWLN5Uk

Referal link: https://minepi.com/rockcesar
Referal code: rockcesar

To put it work, use Odoo 13.

Test the app here: https://developers.minepi.com/about-app

Documentation: https://developers.minepi.com/doc/javascript

Pi Developers: https://developers.minepi.com/""",
    'depends': ['website'],
    'data': [
        'views/website_pinetwork_templates.xml',
    ],
    'images': ['static/description/icon.png'],
    'qweb': [],
    'installable': True,
    'auto_install': True,
}
