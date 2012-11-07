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
    def scene(self):
        return self.scene_stack.top

    @property
    def em(self):
        return self.scene.em

    @property
    def tm(self):
        return self.scene.tm

    @property
    def gm(self):
        return self.scene.gm

    @property
    def sm(self):
        return self.scene.sm

sys.modules[__name__] = ServiceLocator()
