import abc

from gensokyo import ces
from gensokyo import locator


class BaseInput(ces.System):

    __meta__ = abc.ABCMeta

    def __init__(self):
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
