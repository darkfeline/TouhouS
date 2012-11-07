from pyglet.graphics import OrderedGroup, Batch
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet.event import EVENT_HANDLED

from gensokyo import locator
from gensokyo import ces


class Graphics(ces.System):

    map = tuple()

    def __init__(self):
        self.batch = Batch()
        o = (OrderedGroup(i) for i in range(len(self.map)))
        self.groups = dict((self.map[i], o[i]) for i in range(len(self.map)))
        self.labels = set()
        locator.window.push_handlers(self)

    def delete(self):
        locator.window.remove_handlers(self)

    def on_draw(self):
        self.draw()
        return EVENT_HANDLED

    def on_add_sprite(self, sprite, group):
        self.add_sprite(sprite, group)
        return EVENT_HANDLED

    def draw(self):
        self.batch.draw()
        for l in self.labels:
            l.draw()

    def add_sprite(self, sprite, group):
        if isinstance(sprite, Label):
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


def _set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
        TextLayoutForegroundDecorationGroup(2, label.top_group)
