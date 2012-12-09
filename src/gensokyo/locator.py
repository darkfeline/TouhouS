"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

You can call the module as a global instance of ServiceLocator.

"""

import sys


class ServiceLocator:

    def __init__(self):
        self.key_state = None
        self.state_tree = None
        self.window = None
        self.graphics = None

sys.modules[__name__] = ServiceLocator()
