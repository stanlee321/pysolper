# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~~~~~~~~~~~~~

    Top-level models for the entire app.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""

import datetime
from google.appengine.ext import db
from google.appengine.ext import blobstore
import timesince

USER_ROLES = ('Permit Approver', 'Applicant', 'Spectator')
# Cases may be ordered lexicographically by state, the first three characters
# of the state string will be stripped before display.
CASE_STATES = ('00 Incomplete', '10 Submitted',
               '20 Commented', '30 Approved', '40 Denied')
CASE_ACTIONS = ('Create', 'Update', 'Upload',
                'Submit', 'Comment', 'Approve', 'Deny')


class User(db.Model):
    email = db.EmailProperty(required=True)
    role = db.StringProperty(choices=USER_ROLES, required=False)

    @classmethod
    def get_by_email(cls, email):
        return cls.all().filter('email = ', email).get()


class Case(db.Model):
    address = db.StringProperty(required=True)
    creation_date = db.DateProperty(required=True, auto_now_add=True)
    owner = db.ReferenceProperty(User, required=True)
    state = db.StringProperty(required=True, choices=CASE_STATES)
    email_listeners = db.StringListProperty()

    @classmethod
    def query_by_owner(cls, user):
        """Returns a db.Query."""
        return cls.all().filter('owner = ', user)

    @classmethod
    def create(cls, owner, **k):
        case = cls(state=CASE_STATES[0], owner=owner, **k)
        case.put()
        first_action = CaseAction(action='Create', case=case, actor=owner)
        first_action.put()
        return case

    def submit(self, actor, notes):
        self.state = CASE_STATES[1]
        self.put()
        action = CaseAction(action='Submit', case=self, actor=actor)
	if notes is not None:
	    action.notes = notes
        action.put()

    @property
    def visible_state(self):
        return self.state[3:]

    @property
    def latest_action(self):
        return CaseAction.query_by_case(self).order('-timestamp').get()

    @property
    def last_modified(self):
        return datetime.datetime.now() - self.latest_action.timestamp


class CaseAction(db.Model):
    """Immutable once created."""
    action = db.StringProperty(required=True, choices=CASE_ACTIONS)
    case = db.ReferenceProperty(Case, required=True)
    actor = db.ReferenceProperty(User, required=True)
    purpose = db.StringProperty(required=False)
    notes = db.TextProperty(required=False)
    upload = blobstore.BlobReferenceProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now_add=True, required=True)

    @property
    def timesince(self):
        return timesince.timesince(self.timestamp)

    @classmethod
    def query_by_case(cls, case):
        return cls.all().filter('case = ', case)

    @classmethod
    def upload_document_action(cls, case, purpose, user, blob_info, notes):
        action = cls(action='Update', case=case, actor=user)
	if purpose is not None:
	    action.purpose = purpose
	if notes is not None:
	    action.notes = notes
	if upload is not None:
	    action.upload = upload
        action.put()


