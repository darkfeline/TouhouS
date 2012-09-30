#!/usr/bin/env python3

"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

"""

class ServiceLocator:

    def __init__(self):
        self.window = None
        self.rendering = None
        self.key_state = None
        self.game = None
        self.collision = None

    @property
    def em(self):
        return self.game.em

    @property
    def sm(self):
        return self.game.sm
