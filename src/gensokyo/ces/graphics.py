import logging

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet import sprite, text
from pyglet import event

from gensokyo import locator
from gensokyo import ces
from gensokyo.ces import observer

logger = logging.getLogger(__name__)


class GraphicsLevel:

    map = tuple()

    def __init__(self):
        self.batch = Batch()
        self.groups = dict(
            (self.map[i], OrderedGroup(i)) for i in range(len(self.map)))
        self.labels = set()

    def on_draw(self):
        locator.window.clear()
        self.draw()
        return event.EVENT_HANDLED

    def on_add_sprite(self, sprite, group):
        if group in self.map:
            self.add_sprite(sprite, group)
            return event.EVENT_HANDLED

    def draw(self):
        self.batch.draw()
        for l in self.labels:
            l.draw()

    def add_sprite(self, sprite, group):
        logger.debug("Adding sprite {} {}".format(sprite, group))
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

GraphicsLevel.register_event_type('on_add_sprite')


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)


class GraphicsObject(ces.Position):

    def __init__(self, constructor, group, *args, **kwargs):
        logger.debug('New GraphicsObject: {} {} {} {}'.format(
            constructor, group, args, kwargs))
        self.sprite = constructor(*args, **kwargs)
        self.group = group
        locator.graphics.dispatch_event(
            'on_add_sprite', self.sprite, group)

    @property
    def pos(self):
        return (self.sprite.x, self.sprite.y)

    @pos.setter
    def pos(self, value):
        self.sprite.x, self.sprite.y = value


class Sprite(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(sprite.Sprite, *args, **kwargs)


class Label(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(text.Label, *args, **kwargs)

    @property
    def label(self):
        return self.sprite
