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


class ScreenClearer(ces.System, observer.Drawing):

    def on_draw(self):
        locator.window.clear()


class Graphics(ces.System, event.EventDispatcher, observer.Drawing):

    """
    Make sure to open the ``'graphics'`` channel with this when you
    instantiate

    """

    map = tuple()

    def __init__(self):
        super().__init__()
        self.batch = Batch()
        self.groups = dict(
            (self.map[i], OrderedGroup(i)) for i in range(len(self.map)))
        self.labels = set()

    def on_draw(self):
        self.draw()

    def on_add_sprite(self, sprite, group):
        self.add_sprite(sprite, group)

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
        try:
            sprite.group = self.groups[group]
        except AttributeError:  # sprite already deleted
            return
        sprite.batch = self.batch

Graphics.register_event_type('on_add_sprite')


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
        locator.broadcast['graphics'].dispatch_event(
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
