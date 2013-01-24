import logging

from pyglet import sprite, text

from gensokyo import ces

logger = logging.getLogger(__name__)


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
