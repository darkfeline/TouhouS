import logging
from weakref import WeakSet

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import text

__all__ = ['Graphics']
logger = logging.getLogger(__name__)


class GraphicsLevel(tuple):

    layers = tuple()

    def __new__(cls):
        t = super().__new__(
            Batch(),
            dict((cls.layers[i], OrderedGroup(i)) for i in
                 range(len(cls.layers))),
            dict((cls.layers[i], WeakSet()) for i in range(len(cls.layers))))
        t.batch, t.groups, t.labels = t


class Graphics:

    def __init__(self, window):
        self.stack = []

    def draw(self):
        self.window.clear()
        logger.debug('%s drawing', self)
        try:
            s = self.stack[-1]
        except IndexError:
            pass
        else:
            s.batch.draw()
            for layer in s.labels:
                for l in s.labels[layer]:
                    l.draw()

    def add_sprite(self, sprite, group):
        logger.debug("Adding sprite %s %s", sprite, group)
        for l in reversed(self.stack):
            if group in l.layers:
                if isinstance(sprite, text.Label):
                    _add_label(l, sprite, group)
                else:
                    _add_sprite(l, sprite, group)
                break


def _add_label(level, label, group):
    level.labels[group].add(label)
    #_set_label_group(label, level.groups[group])
    #label.batch = level.batch
    #label._own_batch = False


def _add_sprite(level, sprite, group):
    sprite.group = level.groups[group]
    sprite.batch = level.batch


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)
