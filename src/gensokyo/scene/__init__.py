import functools

from gensokyo import state
from gensokyo import ces
from gensokyo import locator


class Scene(state.StateNode, ces.Environment):

    def __init__(self):
        super().__init__()
        self.graphics = None
        self.input = None
        self._update = functools.partial(self.sm.dispatch_event, 'on_update')

    def enter(self):
        locator.push_handlers(on_update=self._update)

    def exit(self):
        locator.remove_handlers(on_update=self._update)
