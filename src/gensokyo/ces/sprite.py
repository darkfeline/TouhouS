import logging

from pyglet import sprite, text

from gensokyo.ces import pos

logger = logging.getLogger(__name__)


class BaseSprite(pos.SlavePosition):

    def __init__(self, graphics, constructor, group, *args, **kwargs):
        logger.debug('New BaseSprite: %s %s %s %s', constructor, group,
                     args, kwargs)
        self.sprite = constructor(*args, **kwargs)
        self.group = group
        graphics.dispatch_event('on_add_sprite', self.sprite, group)

    @property
    def pos(self):
        return (self.sprite.x, self.sprite.y)

    def setpos(self, pos):
        self.sprite.x, self.sprite.y = pos

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
