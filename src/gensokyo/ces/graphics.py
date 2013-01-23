import logging
import weakref

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import sprite, text
from pyglet import event

from gensokyo import ces

__all__ = ['Graphics']
logger = logging.getLogger(__name__)


class Graphics:

    map = tuple()

    def __init__(self, window):
        self.batch = Batch()
        self.groups = dict(
            (self.map[i], OrderedGroup(i)) for i in range(len(self.map)))
        self.labels = set()
        self.window = weakref.ref(window)

    def on_draw(self):
        self.window.clear()
        logger.debug('%s drawing', self)
        self.draw()
        return event.EVENT_HANDLED

    def on_add_sprite(self, sprite, group):
        if group in self.map:
            logger.debug('%s adding sprite %s %s', self, sprite, group)
            self.add_sprite(sprite, group)
            return event.EVENT_HANDLED

    def draw(self):
        self.batch.draw()
        for l in self.labels:
            l.draw()

    def add_sprite(self, sprite, group):
        logger.debug("Adding sprite %s %s", sprite, group)
        if isinstance(sprite, text.Label):
            self._add_label(sprite, group)
        else:
            self._add_sprite(sprite, group)

    def _add_label(self, label, group):
        self.labels.add(label)
        #_set_label_group(label, self.groups[group])
        #label.batch = self.batch
        #label._own_batch = False

    def _add_sprite(self, sprite, group):
        sprite.group = self.groups[group]
        sprite.batch = self.batch


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)


class GraphicsObject(ces.Position):

    def __init__(self, graphics, constructor, group, *args, **kwargs):
        logger.debug('New GraphicsObject: %s %s %s %s', constructor, group,
                     args, kwargs)
        self.sprite = constructor(*args, **kwargs)
        self.group = group
        graphics.dispatch_event('on_add_sprite', self.sprite, group)

    @property
    def pos(self):
        return (self.sprite.x, self.sprite.y)

    @pos.setter
    def pos(self, value):
        self.sprite.x, self.sprite.y = value

    def __del__(self):
        logger.debug("deleting sprite %s", self)
        self.sprite.delete()


class Sprite(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(sprite.Sprite, *args, **kwargs)


class Label(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(text.Label, *args, **kwargs)

    @property
    def label(self):
        return self.sprite
