"""
Resource locator

Defines a ServiceLocator class and creates a module level instance.

You can call the module as a global instance of ServiceLocator.

"""

import sys

from pyglet.event import EventDispatcher


class Locator:

    def __init__(self):
        self.output = Output()
        self.testhub = TestHub()


class Output:

    def __init__(self):
        self.clear()

    def write(self, a, end='\n'):
        self.text += a + end

    def clear(self):
        self.text = ''


class TestHub(EventDispatcher):

    def test(self):
        self.dispatch_event('on_test')

TestHub.register_event_type('on_test')

sys.modules[__name__] = Locator()
