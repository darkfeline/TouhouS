"""
Physics module

"""

import abc

from gensokyo import ces
from gensokyo.ces import observer
from gensokyo import primitives
from gensokyo import locator


# TODO generalize this
class Physics(ces.Component):

    """
    Physics component.  Each Entity should only have one.

    .. attribute:: vel
        velocity
    .. attribute:: acc
        acceleration

    """

    def __init__(self, vel=None):
        if vel is None:
            self.vel = primitives.Vector(0, 0)
        elif isinstance(vel, primitives.Vector):
            self.vel = vel
        else:
            raise TypeError
        self.acc = primitives.Vector(0, 0)


class PhysicsPosition(ces.Position):

    __meta__ = abc.ABCMeta


class PhysicsSystem(ces.System, observer.Updating):

    req_components = (Physics, PhysicsPosition)

    def on_update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            phys, pos = entity.get(self.req_components)
            for phy in phys:
                for p in pos:
                    p.pos = tuple(p.pos[i] + phy.vel[i] for i in [0, 1])
                phy.vel += phy.acc
