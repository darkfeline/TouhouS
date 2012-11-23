import abc

from gensokyo import primitives
from gensokyo import locator
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


class CollisionSystem(ces.System):

    __meta__ = abc.ABCMeta
    req_components = (Hitbox,)

    def update(self, dt):
        """
        Compare ALL of the hitboxes of entities with a hitbox component.  If
        any of them collide, have the SystemManager dispatch on_collide event
        with a tuple containing the two entities as an argument.

        """
        collided = []
        entities = locator.em.get_with(self.req_components)
        for i, e1 in enumerate(entities):
            for e2 in enumerate(entities[i + 1:]):
                for hb1 in e1.get(Hitbox):
                    for hb2 in e2.get(Hitbox):
                        if _collide(hb1, hb2):
                            collided.append((e1, e2))
        for a in collided:
            self.handle(*a)

    @abc.abstractclassmethod
    def handle(a, b):
        raise NotImplementedError


def _collide(hb1, hb2):
    """
    :param t1: hitboxes to compare
    :param t2: hitboxes to compare
    :type t1: tuple
    :type t2: tuple
    :rtype: boolean

    """
    for i in range(len(hb1)):
        for j in range(len(hb2)):
            if hb1[i].collide(hb2[j]):
                return True
    return False


def _check_types(entities, types):
    """Return True if one entity is one type, and the other is the other"""
    e1, e2 = entities
    t1, t2 = types
    if isinstance(e1, t1) and isinstance(e2, t2) or \
            isinstance(e1, t2) and isinstance(e2, t1):
        return True
    else:
        return False
