# -*- coding: utf-8 -*-
"""
    home
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for the home page, including login/registration flow.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin


class HomeHandler(RequestHandler, Jinja2Mixin):
    def get(self):
        """Home Page, no state!."""
        context = {
            'jurisdiction': 'City of Light',
        }
        return self.render_response('home.html', **context)
