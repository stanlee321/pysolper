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
from tipfy.sessions import SessionMiddleware
from tipfyext.jinja2 import Jinja2Mixin

class HomeHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self):
        """Home Page, assumes no state!."""
        # Get user from session or CGI params.
        if self.request.args.get('logout'):
            user = None
            if 'user' in self.session:
                del self.session['user']
        else:
            user = self.request.args.get('email', None)
            if user:
                # set user in session
                self.session['user'] = user 
            else:
                # try to get user from session
                user = self.session.get('user', None) 
                
        context = {
            'jurisdiction': 'City of Light',
            'user': user, 
        }

        return self.render_response('home.html', **context)
