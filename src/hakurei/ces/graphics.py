from pyglet import sprite, text
from gensokyo import locator

from hakurei import ces


class GraphicsObject(ces.Position):

    def __init__(self, type, group, *args, **kwargs):
        self.sprite = type(*args, **kwargs)
        self.group = group
        locator.sm.dispatch_event('add_sprite', self.sprite, group)

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    def delete(self):
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
