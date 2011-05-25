# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='home.HomeHandler'),
    Rule('/applicant/home', name='applicant_home', handler='applicant.HomeHandler'),
]
