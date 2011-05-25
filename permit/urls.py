# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='home.HomeHandler'),
    Rule('/applicant/home', handler='applicant.HomeHandler'),
    Rule('/case/create', handler='applicant.CreateCaseHandler'),
    Rule('/case/details/<int:id>', handler='applicant.CaseDetailsHandler'),
    Rule('/case/submit/<int:id>', handler='applicant.CaseSubmitHandler'),
    Rule('/document/serve/<string:key>', handler='document.DownloadHandler'),
    Rule('/document/upload/<int:id>', handler='document.UploadHandler'),
]
