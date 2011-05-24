# -*- coding: utf-8 -*-
"""
    models
    ~~~~~~~~~~~~~~~~~~~~

    Top-level models for the entire app.

    :copyright: 2011 by Google, Inc.
    :license: Apache 2.0, see LICENSE for more details.
"""

from google.appengine.ext import db
from google.appengine.ext import blobstore

USER_ROLES = ('Permit Approver', 'Applicant', 'Spectator')
CASE_STATES = ('Incomplete', 'Submitted', 'Commented', 'Approved', 'Denied')
CASE_ACTIONS = ('Create', 'Update', 'Submit', 'Comment', 'Approve', 'Deny')

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
    
class CaseAction(db.Model):
    name = db.StringProperty(required=True, choices=CASE_ACTIONS)
    actor = db.ReferenceProperty(User, required=True)
    case = db.ReferenceProperty(Case, required=True)
    notes = db.TextProperty(required=False)

class Document(db.Model):
    """Going to be immutable once they are created."""
    filename = db.StringProperty(required=True)
    action = db.ReferenceProperty(CaseAction, required=True)
    uploaded_by = db.ReferenceProperty(User, required=True)
    uploaded_time = db.DateTimeProperty(required=True, auto_now_add=True)
    # Either comments or notes or both will be present.
    contents = blobstore.BlobReferenceProperty(required=False)  
    notes = db.TextProperty(required=False)


