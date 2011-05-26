# -*- coding: utf-8 -*-
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for Applicant functionality.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from google.appengine.ext import blobstore
from tipfy.app import Response
from tipfy.handler import RequestHandler
from tipfy.sessions import SessionMiddleware
from tipfyext.jinja2 import Jinja2Mixin
import config
import models


class HomeHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self):
        """Home Page for an Approver."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user or not user.can_approve:
            return self.redirect('/')

        cases = models.Case.query_submitted()
        cases = list(cases.order('state').run())
        cases.sort(key=lambda c: c.last_modified, reverse=True)

        context = {
            'user': user,
            'cases': cases,
        }
        context.update(config.config)

        return self.render_response('approver_home.html', **context)


class CaseApproveHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def post(self, id):
        """Approve a case."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user or not user.can_approve:
            return self.redirect('/')

        notes = self.request.form.get('notes')
        case = models.Case.get_by_id(id)
        case.approve(user, notes)

        return self.redirect('/approver/home')


class CaseDetailsHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self, id):
        """Show details of a case and allow editing it."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user or not user.can_approve:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
        actions = models.CaseAction.query_by_case(case).order('-timestamp')
        documents = models.CaseAction.query_updates_by_case(case)
	documents = documents.order('-timestamp')

        context = {
            'user': user,
            'case': case,
            'actions': actions,
            'documents': documents,
            'uploadables': models.PURPOSES,
            'upload_url': 'bogus',
        }
        context.update(config.config)

        return self.render_response('case.html', **context)

