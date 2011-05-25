# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='home.HomeHandler'),
    Rule('/applicant/home', handler='applicant.HomeHandler'),
    Rule('/case/create', handler='applicant.CreateCaseHandler'),
    Rule('/case/details/<int:id>', handler='applicant.CaseDetailsHandler'),
]
