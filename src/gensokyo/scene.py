import abc

from pyglet.graphics import OrderedGroup, Batch
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup

from gensokyo import manager


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
        self.top.init()

    def pop(self):
        return self.stack.pop()

    def update(self, dt):
        """Calls update on top of stack"""
        self.top.update(dt)

    def on_draw(self):
        self.top.view.draw()

    def on_key_press(self, symbol, modifiers):
        self.top.model.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.top.model.on_key_release(symbol, modifiers)


class Scene:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def init(self):
        self.model.init()

    def update(self, dt):
        self.model.update(dt)


class Model:

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def init(self):
        pass

    def update(self, dt):
        self.sm.update(dt)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


class AbstractView:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def draw(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_sprite(self, sprite, group):
        raise NotImplementedError


class View(AbstractView):

    map = tuple()

    def __init__(self):
        self.batch = Batch()
        o = (OrderedGroup(i) for i in range(len(self.map)))
        self.groups = dict((self.map[i], o[i]) for i in range(len(self.map)))
        self.labels = set()

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
        #View.set_label_group(label, self.groups[group])
        #label.batch = self.batch
        #label._own_batch = False

    def _add_sprite(self, sprite, group):
        try:
            sprite.group = self.groups[group]
        except AttributeError:  # sprite already deleted
            return
        sprite.batch = self.batch

    @staticmethod
    def set_label_group(label, group):
        label.top_group = TextLayoutGroup(group)
        label.background_group = OrderedGroup(0, label.top_group)
        label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
        label.foreground_decoration_group = \
            TextLayoutForegroundDecorationGroup(2, label.top_group)
