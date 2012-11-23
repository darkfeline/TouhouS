"""
Garbage collecting module

This handles deletion of entities which are bounded by the play area, such as
bullets.  When these entities move out of bounds, they will be deleted.

Add a Presence to entities that need this feature.  A Presence has a Rect that
will be used to determine if the entity has completely exited the boundaries.

"""

from gensokyo import ces
from gensokyo.ces import observer
from gensokyo import locator


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


class GarbageCollectSystem(ces.System, observer.Updating):

    req_components = (Presence,)

    def __init__(self, area):
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
        entities = self.get_with(self.req_components)
        for e in entities:
            if _check_bounds(e):
                locator.em.delete(e)
