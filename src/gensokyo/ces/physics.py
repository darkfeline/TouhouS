"""
Physics module
"""

import logging

from gensokyo import ces
from gensokyo.ces import pos

logger = logging.getLogger(__name__)


class Velocity(ces.Component):

    """
    Attributes:

    vel
        velocity
    """

    def __init__(self, vel):
        self.vel = vel


class PhysicsSystem(ces.System):

    def on_update(self, dt):
        entities = ces.intersect(self.world, pos.Position, Velocity)
        p = self.world.cm[pos.Position]
        v = self.world.cm[Velocity]
        for e in entities:
            p[e].pos = tuple(p[e].pos[i] + v[e].vel[i] for i in (0, 1))
