# -*- coding: utf-8 -*-
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for Applicant functionality. 

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfy.sessions import SessionMiddleware
from tipfyext.jinja2 import Jinja2Mixin
import config
import models


class HomeHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self):
        """Home Page for an Applicant."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        cases = models.Case.query_by_user(user)
        cases.order('state').order('-last_modified').run()

        context = {
            'user': user, 
            'cases': list(cases), 
        }
        context.update(config.config)

        return self.render_response('applicant_home.html', **context)
