"""
Physics module

"""

import logging

from gensokyo import ces
from gensokyo.ces import pos

logger = logging.getLogger(__name__)


class Physics(ces.Component):

    """
    Physics component

    .. attribute:: vel
        velocity

    """

    def __init__(self, vectors):
        self.v = vectors


class PhysicsSystem(ces.System):

    def __init__(self, env):
        super().__init__(env)

    def on_update(self, dt):
        entities = ces.intersect(self.env, pos.Position, Physics)
        p = self.env.cm[pos.Position]
        v = self.env.cm[Physics]
        for e in entities:
            p[e].pos = tuple(p[e].pos[i] + v[e].v[0][i] for i in (0, 1))
            for i, a in enumerate(v[e].v[1:]):
                v[e].v[i - 1] = tuple(
                    v[e].v[i - 1][j] + v[e].v[i][j] for j in (0, 1))
