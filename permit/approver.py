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

        open_cases = models.Case.query_submitted()
        open_cases = list(open_cases.order('state').run())
        open_cases.sort(key=lambda c: c.last_modified, reverse=True)

	my_cases, other_cases = models.Case.reviewed_by(user)

        context = {
            'user': user,
            'open_cases': open_cases,
            'num_other_cases': len(other_cases),
	    'my_cases': my_cases,
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


class CaseCommentHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def post(self, id):
        """Comment on a case."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user or not user.can_approve:
            return self.redirect('/')

        notes = self.request.form.get('notes')
        case = models.Case.get_by_id(id)
        case.comment(user, notes)

        return self.redirect('/approver/home')



class CaseReviewHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self, id):
        """Show details of a case and allow editing it."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user or not user.can_approve:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
	case.review(user)
        actions = models.CaseAction.query_by_case(case)
        documents = models.CaseAction.query_by_case(case, 'Update')

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

