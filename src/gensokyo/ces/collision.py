import abc

from gensokyo import primitives
from gensokyo import ces
from gensokyo.ces import pos


class Hitbox(pos.SlavePosition):

    def __init__(self, master, hb):
        self.hb = hb
        super().__init__(master)

    def setpos(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.x, self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.center = value

    def collide(self, other):
        return self.hb.collide(other.hb)


class CollisionSystem(ces.System, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError
