"""
rails provides a set "animation" movement for entities.  It is mutually
exclusive with physics.

"""

from functools import wraps
import math

from gensokyo import ces
from gensokyo import locator


def _move_start(f, pos):
    x, y = pos
    @wraps(f)
    def wrapper(*args, **kwargs):
        a, b = f(*args, **kwargs)
        return a + x, b + y
    return wrapper


def convert_rails(rails, start_pos):
    """
    ('straight', dest, time)
    ('pivot', center, arc, time)
    ('curve', param, time)

    ('straight', vector, time)
    ('pivot', center, angular_vel, time)
    ('curve', param, time)

    """
    r = []
    pos = start_pos
    time = 0
    for segment in rails:
        dt = segment[-1] - time
        assert dt > 0
        if segment[0] == 'straight':
            dx = segment[1][0] / dt
            dy = segment[1][1] / dt
            @_move_start(pos)
            def f(time):
                return dx * time, dy * time
            pos = segment[1]
        elif segment[0] == 'pivot':
            arc, time = segment[2:]
            alpha = math.atan(pos[1] / pos[0])
            vel = arc / time
            def f(time):
                beta = alpha + vel * time
                return math.cos(beta), math.sin(beta)
            pos = f(time)
        elif segment[0] == 'curve':
            param = segment[1]
            f = _move_start(param, pos)
            pos = param(pos)
        time = segment[-1]
        r.append((f, time))
    return r


class Rails(ces.Component):

    def __init__(self, rails):
        self.rails = convert_rails(rails)
        self.time = 0

    def __getitem__(self, key):
        step = 0
        try:
            while self.time >= self.rails[step][-1]:
                step += 1
        except IndexError:
            raise IndexError(key + " is beyond end of rails")
        else:
            return self.rails[step]


class RailSystem(ces.System):

    req_components = (Rails, ces.Position)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            for r in entity.get(Rails):
                r.time += dt
                func = r[r.time][0]
                pos = func(r.time)
                for p in entity.get(ces.Position):
                    p.x, p.y = pos
