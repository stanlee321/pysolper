# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='home.HomeHandler'),
    Rule('/applicant/home', handler='applicant.HomeHandler'),
    Rule('/case/create', handler='applicant.CreateCaseHandler'),
    Rule('/case/details/<int:id>', handler='applicant.CaseDetailsHandler'),
    Rule('/case/emails/<int:id>', handler='applicant.CaseEmailsHandler'),
    Rule('/case/submit/<int:id>', handler='applicant.CaseSubmitHandler'),
    Rule('/document/serve/<string:key>/<string:filename>',
         handler='document.DownloadHandler'),
    Rule('/document/upload/<int:id>', handler='document.UploadHandler'),
    Rule('/approver/home', handler='approver.HomeHandler'),
    Rule('/approver/case/<int:id>', handler='approver.CaseReviewHandler'),
    Rule('/case/approve/<int:id>', handler='approver.CaseApproveHandler'),
    Rule('/case/comment/<int:id>', handler='approver.CaseCommentHandler'),
]
