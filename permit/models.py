# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~~~~~~~~~~~~~

    Top-level models for the entire app.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""

import datetime
import logging
import urllib
from google.appengine.ext import db
from google.appengine.ext import blobstore
import timesince

USER_ROLES = ('Applicant', 'Permit Approver')
# Cases may be ordered lexicographically by state, the first three characters
# of the state string will be stripped before display.

CASE_STATES = {'incomplete': '00 Incomplete',
               'submitted': '10 Submitted For Review',
	       'under_review': '20 Review Under Way',
	       'needs_work': '30 Needs Work',
	       'approved': '40 Approved',
	       'denied': '50 Rejected',
	      }

APPLICANT_EDITABLE = set(CASE_STATES[x]
                         for x in 'incomplete submitted needs_work'.split())

CASE_ACTIONS = ('Create', 'Update', 'Submit',
                'Review', 'Reassign', 'Comment', 'Approve', 'Deny')

PURPOSES = (
    'Site Diagram',
    'Electrical Diagram',
    'Diagram Notes'
    )


class User(db.Model):
    email = db.EmailProperty(required=True)
    role = db.StringProperty(choices=USER_ROLES, required=False)

    @classmethod
    def get_by_email(cls, email):
        return cls.all().filter('email = ', email).get()

    @property
    def can_upload(self):
        return self.role == 'Applicant'

    @property
    def can_approve(self):
        return self.role == 'Permit Approver'

    def __eq__(self, other):
        return self.email == other.email

    def __ne__(self, other):
        return self.email != other.email


class Case(db.Model):
    address = db.StringProperty(required=True)
    creation_date = db.DateProperty(required=True, auto_now_add=True)
    owner = db.ReferenceProperty(User, required=True)
    state = db.StringProperty(required=True, choices=CASE_STATES.values())
    email_listeners = db.StringListProperty()

    @classmethod
    def query_by_owner(cls, user):
        """Returns a db.Query."""
        return cls.all().filter('owner = ', user)

    @classmethod
    def query_under_review(cls):
       return cls.all().filter('state = ', CASE_STATES['under_review'])

    @classmethod
    def query_submitted(cls):
        """Returns a db.Query."""
        return cls.all().filter('state = ', CASE_STATES['submitted'])

    @classmethod
    def reviewed_by(cls, user):
       these_cases, other_cases = [], []
       q = cls.query_under_review()
       for case in q.run():
           if case.reviewer == user:
	       these_cases.append(case)
	   else:
	       other_cases.append(case)
       return these_cases, other_cases

    @classmethod
    def create(cls, owner, **k):
        case = cls(state=CASE_STATES['incomplete'], owner=owner, **k)
        case.put()
        first_action = CaseAction.make(action='Create', case=case, actor=owner)
        first_action.put()
        return case

    def submit(self, actor, notes):
        self.state = CASE_STATES['submitted']
        self.put()
        action = CaseAction.make(action='Submit', case=self, actor=actor,
	                    notes=notes)
        action.put()

    def review(self, approver):
	previous_reviewer = self.reviewer
	if previous_reviewer == approver:
	    return
	# reviewer assignment or change requires actual action, state change
        self.state = CASE_STATES['under_review']
	self.put()
	action = CaseAction.make(action='Review', case=self, actor=approver)
	action.put()

    def approve(self, actor, notes):
        self.state = CASE_STATES['approved']
        self.put()
        action = CaseAction.make(action='Approve', case=self, actor=actor,
	                    notes=notes)
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

    @property
    def applicant_can_edit(self):
        return self.state in APPLICANT_EDITABLE

    @property
    def reviewer(self):
       if self.state != CASE_STATES['under_review']:
           return None
       return CaseAction.query_by_case(self, 'Review').get().actor

    @property
    def submit_blockers(self):
        blockers = []
        for purpose in PURPOSES:
            if not self.get_document(purpose):
                blockers.append('Missing %s' % purpose)
        return blockers

    def get_document(self, purpose):
        q = CaseAction.query_by_case(self, 'Update').filter('purpose =', purpose)
        return q.get()


class CaseAction(db.Model):
    """Immutable once created."""
    action = db.StringProperty(required=True, choices=CASE_ACTIONS)
    case = db.ReferenceProperty(Case, required=True)
    actor = db.ReferenceProperty(User, required=True)
    purpose = db.StringProperty(required=False)
    notes = db.TextProperty(required=False)
    upload = blobstore.BlobReferenceProperty(required=False)
    timestamp = db.DateTimeProperty(auto_now_add=True, required=True)

    @classmethod
    def make(cls, **k):
        logging.info('********** ')
        logging.info('********** NEW ACTION: %s', k)
        logging.info('********** ')
        return cls(**k)


    @classmethod
    def query_by_case(cls, case, action=None):
        q = cls.all().filter('case = ', case)
	if action is not None:
	    q.filter('action = ', action)
	return q.order('-timestamp')

    @classmethod
    def upload_document_action(cls, case, purpose, user, blob_info, notes):
        action = cls(action='Update', case=case, actor=user,
	             purpose=purpose, notes=notes, upload=blob_info);
        action.put()

    @property
    def timesince(self):
        return timesince.timesince(self.timestamp)

    @property
    def download_url(self):
        if not self.upload:
            return ''
        return '/document/serve/%s/%s' % (
            urllib.quote(str(self.upload.key())),
            urllib.quote(self.upload.filename))
