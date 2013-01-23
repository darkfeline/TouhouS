"""
Garbage collecting module

This handles deletion of entities which are bounded by the play area, such as
bullets.  When these entities move out of bounds, they will be deleted.

"""

import logging

from gensokyo import ces
from gensokyo.ces.pos import Position

logger = logging.getLogger(__name__)


class Presence(ces.Component):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, rect):
        self.rect = rect

    def setpos(self, value):
        self.rect.center = value


class GarbageCollectSystem(ces.System):

    def __init__(self, world, area):
        super().__init__(world)
        self.area = area

    def _check_bounds(self, rect):
        assert len(rect) == 2
        if (rect.bottom > self.area.top or
                rect.top < self.area.bottom or
                rect.left > self.area.right or
                rect.right < self.area.left):
            return True
        return False

    def on_update(self, dt):
        entities = ces.intersect(self.world, Position, Presence)
        logger.debug('gc found %s', entities)
        pos = self.world.cm[Position]
        pres = self.world.cm[Presence]
        for e in entities:
            pres[e].setpos(pos[e].pos)
            if self._check_bounds(pres[e].rect):
                logger.debug('deleting %s', e)
                self.world.remove_entity(e)
