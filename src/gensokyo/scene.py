from pyglet.graphics import OrderedGroup, Batch
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup
from pyglet.event import EVENT_HANDLED

from gensokyo import manager
from gensokyo import locator


class SceneStack:

    def __init__(self):
        self.stack = []

    @property
    def top(self):
        return self.stack[-1]

    @property
    def view(self):
        return self.top.view

    @property
    def model(self):
        return self.top.model

    def push(self, scene):
        self.stack.append(scene)
        try:
            self.top.init()
        except AttributeError:
            pass

    def pop(self):
        a = self.stack.pop()
        a.delete()

    def update(self, dt):
        """Calls update on top of stack"""
        self.top.update(dt)


class Scene:

    def __init__(self, model, view):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def update(self, dt):
        self.sm.update(dt)

    def delete(self):
        self.sm.delete()


class View:

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
