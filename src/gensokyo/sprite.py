import abc
import logging
from weakref import WeakSet

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import sprite
from pyglet import text

__all__ = []
logger = logging.getLogger(__name__)

def _public(f):
    __all__.append(f.__name__)
    return f


@_public
class BaseSprite:

    def __init__(self, constructor, drawer, group, *args, **kwargs):
        logger.debug('New BaseSprite: %s %s %s %s', constructor, group,
                     args, kwargs)
        self.sprite = constructor(*args, **kwargs)
        drawer.add_sprite(self.sprite, group)

    def __del__(self):
        logger.debug("garbage collecting sprite %s", self.sprite)
        try:
            self.sprite.delete()
        except AttributeError:  # Failed __init__
            pass


@_public
class Sprite(BaseSprite):

    def __init__(self, drawer, group, *args, **kwargs):
        super().__init__(sprite.Sprite, drawer, group, *args, **kwargs)


@_public
class Label(BaseSprite):

    def __init__(self, drawer, group, *args, **kwargs):
        super().__init__(text.Label, drawer, group, *args, **kwargs)

    @property
    def label(self):
        return self.sprite


@_public
class BaseDrawer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def draw(self):
        raise NotImplementedError

    def on_draw(self):
        self.draw()


@_public
class SpriteDrawer(BaseDrawer):

    def __init__(self, layers):
        self.batch = Batch()
        self.groups = dict(
            (layers[i], OrderedGroup(i)) for i in range(len(layers)))
        self.labels = dict(
            (layers[i], WeakSet()) for i in range(len(layers)))
        self.layers = layers

    def draw(self):
        logger.debug('%r drawing', self)
        self.batch.draw()
        for layer in self.labels:
            for l in self.labels[layer]:
                logger.debug('drawing label %r', l)
                l.draw()

    def add_sprite(self, sprite, group):
        logger.debug("Adding sprite %r to %r", sprite, group)
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
            raise GroupError(group)


@_public
class DrawerStack(SpriteDrawer):

    """
    Order:

    add() to end
    remove() first from front
    draw() self then from front to end
    add_sprite() from end to front then self
    """

    def __init__(self, layers=tuple()):
        super().__init__(layers)
        self.drawers = []

    def add(self, drawer):
        assert isinstance(drawer, BaseDrawer)
        self.drawers.append(drawer)

    def remove(self, drawer):
        self.drawers.remove(drawer)

    def draw(self):
        super().draw()
        for x in self.drawers:
            x.draw()


@_public
class Clearer(BaseDrawer):

    def __init__(self, window):
        self.window = window

    def draw(self):
        self.window.clear()


@_public
class GroupError(TypeError):

    def __init__(self, group):
        self.group = group

    def __str__(self):
        return 'No group named {!s}'.format(self.group)


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)
