#!/usr/bin/env python3

"""
Resource locator

Basically global/singleton.
Don't add global variables or other classes.

"""

class ServiceLocator:

    def __init__(self):
        self.window = None
        self.rendering = None
        self.key_state = None
        self.game = None
        self.collision = None
