"""
Physics module

"""

import abc
import logging

from gensokyo import ces
from gensokyo import primitives

logger = logging.getLogger(__name__)


# TODO generalize this
class Physics(ces.Component):

    """
    Physics component.  Each Entity should only have one.

    .. attribute:: vel
        velocity

    """

    def __init__(self, vel=None):
        if vel is None:
            self.vel = primitives.Vector(0, 0)
        elif isinstance(vel, primitives.Vector):
            self.vel = vel
        else:
            raise TypeError


class PhysicsPosition(ces.Position, metaclass=abc.ABCMeta):
    pass


class PhysicsSystem(ces.System):

    req_components = (Physics, PhysicsPosition)

    def on_update(self, dt):
        for entity in self.scene.em.get_with(self.req_components):
            physics, pos = entity.get(self.req_components)
            physics = physics[0]
            logger.debug("Moving Entity %s", entity)
            logger.debug("Physics %s", physics.vel)
            for p in pos:
                p.pos = tuple(p.pos[i] + physics.vel[i] for i in [0, 1])
