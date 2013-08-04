import logging
import abc

from gensokyo import state
from gensokyo.master import Master
from gensokyo import sprite
from gensokyo import resources

from pyglet.window import key
from pyglet.event import EVENT_HANDLED

logger = logging.getLogger(__name__)


class Menu(Master, state.StateMachine):

    def __init__(self, graph, x, y):
        super().__init__(graph)
        self._drawer = MenuDrawer()
        self.x, self.y = x, y

    def init(self, state, *args, **kwargs):
        super().init(state, self.x, self.y, *args, **kwargs)

    def event(self, event, *args, **kwargs):
        if event.startswith('hook_'):
            super().event(event, *args, **kwargs)
        else:
            super().event(event, self.x, self.y, *args, **kwargs)


class BaseMenuPane(state.State, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, master, x, y, *args, **kwargs):
        raise NotImplementedError


@BaseMenuPane.register
class MenuPane(state.State, Master):

    """
    keys
        iterator of strings
    map
        dict mapping menu keys to actions
    """
    _selector_image = resources.selector
    _x_offset = 30
    _y_offset = 40
    keys = None
    map = None

    def __init__(self, master, x, y):
        super().__init__(master)
        self._drawer = MenuDrawer()
        self.x, self.y = x, y
        self.labels = []
        x += self._x_offset
        for key in self.keys:
            label = sprite.Label(self.drawer, 'menu', text=key, x=x, y=y)
            self.labels.append(label)
            y -= self._y_offset
        self.selection = 0
        self.selector = sprite.Sprite(
            self.drawer, 'menu', x=self.x, img=self._selector_image)
        self._reset_selector()

    def enter(self):
        logger.debug('Entering MenuPane %r', self)
        self.master.drawer.add(self.drawer)
        self.rootenv.window.push_handlers(self)

    def exit(self):
        logger.debug('Exiting MenuPane %r', self)
        self.master.drawer.remove(self.drawer)
        self.rootenv.window.remove_handlers(self)

    def _reset_selector(self):
        y = self.y - (self.selection * self._y_offset)
        logger.debug('Resetting selector to y=%r', y)
        self.selector.sprite.y = y

    def down(self):
        logger.debug('Moving selection down')
        self.selection = (self.selection+1) % len(self.keys)
        self._reset_selector()

    def up(self):
        logger.debug('Moving selection up')
        self.selection = (self.selection-1) % len(self.keys)
        self._reset_selector()

    def select(self):
        x = self.map[self.keys[self.selection]]
        if isinstance(x, str):
            self.master.event(x)
        else:
            self.master.event(*x)

    _input = {
        key.UP: up,
        key.DOWN: down,
        key.ENTER: select
    }

    def on_key_press(self, symbol, modifiers):
        if symbol in self._input:
            self._input[symbol](self)
        return EVENT_HANDLED


class MenuDrawer(sprite.DrawerStack):

    def __init__(self):
        super().__init__(('menu',))
