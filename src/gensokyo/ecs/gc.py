"""
Garbage collecting module

This handles deletion of entities which are bounded by the play area, such as
bullets.  When these entities move out of bounds, they will be deleted.

"""

import logging

from gensokyo import ecs
from gensokyo.ecs import pos

logger = logging.getLogger(__name__)


class Presence(pos.SlavePosition):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, master, rect):
        self.rect = rect
        super().__init__(master)

    def setpos(self, value):
        self.rect.center = value


class GarbageCollectSystem(ecs.System):

    def __init__(self, world, area):
        super().__init__(world)
        self.area = area

    def _check_bounds(self, rect):
        """Check if out of bounds"""
        return not rect.collide(self.area)

    def on_update(self, dt):
        entities = ecs.intersect(self.world, Presence)
        logger.debug('gc found %s', entities)
        pres = self.world.cm[Presence]
        for e in entities:
            if self._check_bounds(pres[e].rect):
                logger.debug('deleting %s', e)
                self.world.remove_entity(e)
