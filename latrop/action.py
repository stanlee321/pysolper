# -*- coding: utf-8 -*-
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for latrop Action functionality.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfy.sessions import SessionMiddleware
from tipfyext.jinja2 import Jinja2Mixin
import config
import models


class AddActionHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self):
        """Add a message about an action."""
        juris = self.request.args.get('juris')
        msg = self.request.args.get('msg')
	models.LatropMessage.create(juris, msg)

        return 'OK'
