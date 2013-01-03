"""
Garbage collecting module

This handles deletion of entities which are bounded by the play area, such as
bullets.  When these entities move out of bounds, they will be deleted.

Add a Presence to entities that need this feature.  A Presence has a Rect that
will be used to determine if the entity has completely exited the boundaries.

"""

import logging

from gensokyo import ces

logger = logging.getLogger(__name__)


class Presence(ces.Position):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, rect):
        self.rect = rect

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value


class GarbageCollectSystem(ces.System):

    req_components = (Presence,)

    def __init__(self, env, area):
        super().__init__(env)
        env.clock.push_handlers(self)
        self.area = area

    def _check_bounds(self, entity):
        """Return True if entity has a Presence component outside of bounds"""
        c = entity.get(Presence)
        if len(c) < 1:
            raise NotImplementedError
        for r in [a.hb for a in c]:
            if (r.bottom > self.area.top or
                    r.top < self.area.bottom or
                    r.left > self.area.right or
                    r.right < self.area.left):
                return True
        return False

    def on_update(self, dt):
        entities = self.env.em.get_with(self.req_components)
        logger.debug('gc found %s', entities)
        for e in entities:
            if self._check_bounds(e):
                logger.debug('deleting %s', e)
                self.env.em.delete(e)
