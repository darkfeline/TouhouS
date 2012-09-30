#!/usr/bin/env python3

"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

"""

import sys


class ServiceLocator:

    def __init__(self):
        self.window = None
        self.key_state = None
        self.scene_stack = None
        self.collision = None

    @property
    def view(self):
        return self.scene_stack.view

    @property
    def model(self):
        return self.scene_stack.model

sys.modules[__name__] = ServiceLocator()
