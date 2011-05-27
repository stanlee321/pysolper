# -*- coding: utf-8 -*-
"""
    home
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for the home page.

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
        """Home Page, show latest 5 messages."""
        latest = models.LatropMessages.get_all().fetch(5)
        context = {
            'latest': latest,
        }
        context.update(config.config)

        return self.render_response('home.html', **context)
