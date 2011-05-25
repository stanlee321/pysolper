# -*- coding: utf-8 -*-
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for Document functionality.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfy.sessions import SessionMiddleware
from tipfyext.jinja2 import Jinja2Mixin
import config
import models


class AddDocumentHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self, id):
        """Add a document to a case."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
        # TODO: upload document and notes to this case

        return self.redirect('/case/details/%s' % case.key().id())

