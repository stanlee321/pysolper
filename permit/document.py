# -*- coding: utf-8 -*-
"""
    applicant
    ~~~~~~~~~~~~~~~~~~~~

    Handlers for Document functionality.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""
from google.appengine.ext import blobstore
from tipfy.app import Response
from tipfy.appengine import blobstore as tipfy_blobstore
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
        upload_url = blobstore.create_upload_url(
            '/document/upload/%s' % case.key().id())

        context = {
            'upload_url': upload_url,
            'user': user,
            'case': case,
        }
        context.update(config.config)

        return self.render_response('document_upload.html', **context)


class UploadHandler(RequestHandler, Jinja2Mixin,
                    tipfy_blobstore.BlobstoreUploadMixin):
    middleware = [SessionMiddleware()]

    def post(self, id):
        """Upload a document."""
        user = models.User.get_by_email(self.session.get('email'))
        if not user:
            return self.redirect('/')

        case = models.Case.get_by_id(id)
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]

        models.CaseAction.upload_document_action(
            case,
            self.request.form.get('purpose'),
            user, blob_info,
            self.request.form.get('notes'))

        response = self.redirect('/case/details/%s' % case.key().id())
        response.data = ''
        return response
