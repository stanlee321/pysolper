# -*- coding: utf-8 -*-
"""
    integrator.handlers
    ~~~~~~~~~~~~~~~~~~~~

    Tipfy app for the Integrators permit flow. 

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfyext.jinja2 import Jinja2Mixin


class HelloWorldHandler(RequestHandler):
    def get(self):
        """PySolPer !"""
        return Response('Hello, Integrator!')


class PrettyHelloWorldHandler(RequestHandler, Jinja2Mixin):
    def get(self):
        """Announces our existence, with finesse!."""
        context = {
            'message': 'Hello, Integrator!',
        }
        return self.render_response('pysolper.html', **context)
