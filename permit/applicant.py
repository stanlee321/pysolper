
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for Applicant functionality.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
import logging
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
        """Home Page for an Applicant."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        cases = models.Case.query_by_owner(user)
        cases = list(cases.order('state'))
        logging.debug(cases)
        cases.sort(key=lambda c: c.last_modified, reverse=True)

        context = {
            'user': user,
            'cases': cases,
        }
        context.update(config.config)

        return self.render_response('applicant_home.html', **context)


class CreateCaseHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self):
        """Create a new case."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        # TODO: add a form!
        case = models.Case.create(
            owner = user,
            address = self.request.args.get('address')
            )

        return self.redirect('/case/details/%s' % case.key().id())


class CaseSubmitHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def post(self, id):
        """Submit a case for approval."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        notes = self.request.form.get('notes')
        case = models.Case.get_by_id(id)
        case.submit(user, notes)

        return self.redirect('/applicant/home')


class CaseDetailsHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self, id):
        """Show details of a case and allow editing it."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
        actions = models.CaseAction.query_by_case(case).order('-timestamp')
        upload_url = blobstore.create_upload_url(
            '/document/upload/%s' % case.key().id())

        context = {
            'user': user,
            'case': case,
            'actions': actions,
            'uploadables': models.PURPOSES,
            'upload_url': upload_url,
        }
        context.update(config.config)

        return self.render_response('case.html', **context)


class CaseEmailsHandler(RequestHandler, Jinja2Mixin):
    middleware = [SessionMiddleware()]

    def get(self, id):
        """Show/change email settings for a case."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
        notifications = models.EmailNotification.query_by_case(case)

        notif_on = {}
	for a in models.NOTIFIABLE_ACTIONS:
	    notif_on[a] = False
	for notif in notifications:
	    if notif.email == user.email:
	        notif_on[notif.action] = True

        logging.info('notif_on: %s', notif_on)

        context = {
            'user': user,
            'case': case,
            'notif': notif_on,
            'actions': models.NOTIFIABLE_ACTIONS,
        }
        context.update(config.config)

        return self.render_response('notifications.html', **context)


