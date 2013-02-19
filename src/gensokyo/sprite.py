import logging
from weakref import WeakSet

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import text

__all__ = ['SpriteGroup', 'Clearer']
logger = logging.getLogger(__name__)


class SpriteGroup:

    layers = tuple()

    def __init__(self):
        self.batch = Batch()
        self.groups = dict(
            (self.layers[i], OrderedGroup(i)) for i in range(len(self.layers)))
        self.labels = dict(
            (self.layers[i], WeakSet()) for i in range(len(self.layers)))

    def draw(self):
        self.batch.draw()
        for layer in self.labels:
            for l in self.labels[layer]:
                l.draw()

    def add_sprite(self, sprite, group):
        logger.debug("Adding sprite %s %s", sprite, group)
        if group in self.layers:
            if isinstance(sprite, text.Label):
                self.labels[group].add(sprite)
                #_set_label_group(label, self.groups[group])
                #label.batch = self.batch
                #label._own_batch = False
            else:
                sprite.group = self.groups[group]
                sprite.batch = self.batch
            break


class Clearer:

    def __init__(self, window):
        self.window = window

    def draw(self):
        self.window.clear()


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)
