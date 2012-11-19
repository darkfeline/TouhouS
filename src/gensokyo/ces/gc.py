from gensokyo import ces
from gensokyo import locator
from gensokyo import globals


class Presence(ces.Component):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, rect):
        self.rect = rect


class GarbageCollectSystem(ces.System):

    req_components = (Presence,)

    def update(self, dt):
        entities = self.get_with(self.req_components)
        for e in entities:
            if _check_bounds(e):
                locator.em.delete(e)


def _check_bounds(entity):
    """Return True if entity has a Presence component outside of bounds"""
    c = entity.get(Presence)
    if len(c) < 1:
        raise NotImplementedError
    for r in [a.hb for a in c]:
        if (r.bottom > globals.GAME_AREA.top or
                r.top < globals.GAME_AREA.bottom or
                r.left > globals.GAME_AREA.right or
                r.right < globals.GAME_AREA.left):
            return True
    return False
