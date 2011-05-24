# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='home', handler='home.HomeHandler'),
    Rule('/pretty', name='hello-world-pretty', handler='integrator.handlers.PrettyHelloWorldHandler'),
]
