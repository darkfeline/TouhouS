import logging

from gensokyo.ecs import pos
from gensokyo import sprite

logger = logging.getLogger(__name__)


class Sprite(pos.SlavePosition, sprite.Sprite):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    @property
    def pos(self):
        return (self.sprite.x, self.sprite.y)

    def setpos(self, pos):
        self.sprite.x, self.sprite.y = pos
