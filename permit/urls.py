# -*- coding: utf-8 -*-
"""URL definitions."""
from tipfy.routing import Rule

rules = [
    Rule('/', name='hello-integrator', handler='integrator.handlers.HelloWorldHandler'),
    Rule('/pretty', name='hello-world-pretty', handler='integrator.handlers.PrettyHelloWorldHandler'),
]
