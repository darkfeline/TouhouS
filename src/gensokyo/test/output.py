"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

You can call the module as a global instance of ServiceLocator.

"""

import sys


class Output:

    def __init__(self):
        self.clear()

    def write(self, a, end='\n'):
        self.text += a + end

    def clear(self):
        self.text = ''

sys.modules[__name__] = Output()
