import logging
from weakref import WeakSet

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import sprite
from pyglet import text

__all__ = ['BaseSprite', 'Sprite', 'Label', 'SpriteDrawer', 'Clearer']
logger = logging.getLogger(__name__)


class BaseSprite:

    def __init__(self, constructor, drawer, group, *args, **kwargs):
        logger.debug('New BaseSprite: %s %s %s %s', constructor, group,
                     args, kwargs)
        self.sprite = constructor(*args, **kwargs)
        drawer.add_sprite(self.sprite, group)

    def __del__(self):
        logger.debug("garbage collecting sprite %s", self)
        self.sprite.delete()


class Sprite(BaseSprite):

    def __init__(self, *args, **kwargs):
        super().__init__(sprite.Sprite, *args, **kwargs)


class Label(BaseSprite):

    def __init__(self, *args, **kwargs):
        super().__init__(text.Label, *args, **kwargs)

    @property
    def label(self):
        return self.sprite


class SpriteDrawer:

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
        else:
            raise GroupError

    def on_update(self, dt):
        self.draw()


class DrawerStack(SpriteDrawer):

    def __init__(self):
        self.drawers = []

    def add(self, drawer):
        self.drawers.append(drawer)

    def remove(self, drawer):
        self.drawers.remove(drawer)

    def draw(self):
        for x in self.drawers:
            x.draw()

    def add_sprite(self, sprite, group):
        for x in reversed(self.drawers):
            try:
                x.add_sprite(sprite, group)
            except GroupError:
                pass
            else:
                break


class Clearer:

    def __init__(self, window):
        self.window = window

    def draw(self):
        self.window.clear()

    def on_update(self, dt):
        self.draw()


class GroupError(TypeError):
    pass


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)
