import abc

from gensokyo import primitives
from gensokyo import ces
from gensokyo.ces import pos


class Hitbox(ces.Component):

    def __init__(self, hb):
        self.hb = hb

    def setpos(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.x, self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.center = value


class CollisionSystem(ces.System, metaclass=abc.ABCMeta):

    def on_update(self, dt):
        entities = ces.intersect(self.world, pos.Position, Hitbox)
        p = self.world.cm[pos.Position]
        hb = self.world.cm[Hitbox]
        for e in entities:
            hb[e].setpos(p[e].pos)
        self.process(entities)

    @abc.abstractmethod
    def process(self, entities):
        raise NotImplementedError
