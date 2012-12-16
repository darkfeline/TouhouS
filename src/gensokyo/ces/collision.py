import abc

from gensokyo import primitives
from gensokyo import ces


class Hitbox(ces.Position):

    def __init__(self, hb):
        self.hb = hb

    @property
    def pos(self):
        if isinstance(self.hb, primitives.Circle):
            return self.hb.x, self.hb.y
        elif isinstance(self.hb, primitives.Rect):
            return self.hb.center

    @pos.setter
    def pos(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.x, self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.center = value


class CollisionSystem(ces.System, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError


def collide(hb1, hb2):
    """
    :param hb1: hitboxes to compare
    :param hb2: hitboxes to compare
    :type hb1: tuple
    :type hb2: tuple
    :rtype: boolean

    """
    for i in range(len(hb1)):
        for j in range(len(hb2)):
            if hb1[i].collide(hb2[j]):
                return True
    return False
