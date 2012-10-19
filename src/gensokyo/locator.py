#!/usr/bin/env python3

"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

You can call the module as a global instance of ServiceLocator.

"""

import sys


class ServiceLocator:

    def __init__(self):
        self.window = None
        self.key_state = None
        self.scene_stack = None

    @property
    def view(self):
        return self.scene_stack.view

    @property
    def model(self):
        return self.scene_stack.model

    @property
    def em(self):
        return self.model.em

    @property
    def tm(self):
        return self.model.tm

    @property
    def gm(self):
        return self.model.gm

    @property
    def sm(self):
        return self.model.sm

sys.modules[__name__] = ServiceLocator()
