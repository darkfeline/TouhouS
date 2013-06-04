"""
rails provides a set "animation" movement for entities.  It is mutually
exclusive with physics.  Therefore, do not subclass RailPosition and
PhysicsPosition at the same time!

Rails
*****

Rails is a wrapper component for the main representation of the *rails tuple*.
The rails tuple is essentially a piece-wise parametrization of a continuous
path::

    (
        (f, t),
        (f, t)
    )

The parametrization starts at ``t = 0``, and finds the current location
``f(t)``.  Each segment ``(f, t)`` gives the position with function ``f(t)``
for all ``t`` up to the given ``t`` exclusively (i.e., up to but not
including).

However, writing such parametrizations can be tedious, so ``rails`` provides a
convenience function ``convert_rails()``, which takes a *lazy rails tuple*.
The first item is the starting position, and the following items are
*parametrization designations*.  For convenience, ``Rails``'s constructor takes
a lazy tuple.

The first item in a parametrization designation is the designation type, and
the last is the ending time.

Rails instances also keep an internal ``time`` attribute.

Designations
============

    ('straight', dest, time)
        Designates a constant-speed, straight-line parametrization, given an
        absolute destination.  Parametrizes by velocity and time

    ('pivot', center, arc, time)
        Designates a circle pivot around a center, traveling the given arc
        distance by the given point in time.  Parametrizes by angular velocity
        and time.

    ('custom', param, time)
        Designates a custom parametrization.  Given a parametrization relative
        to the origin,  the parametrization is shifted so its starting point is
        the ending position of the previous step.

"""

from functools import wraps
import math

from gensokyo import ecs
from gensokyo.ecs.pos import Position

__all__ = ['Rails', 'RailSystem']


def convert_rails(rails, start):
    """Parametrize rail designations

    ('straight', dest, time)
    -> Parametrize by velocity and time

    ('pivot', center, arc, time)
    -> Parametrize by angular velocity and time

    ('custom', param, time)
    -> Already parametrized

    :param rails: rails designations
    :type rails: tuple

    """
    r = []
    assert len(start) == 2
    pos = start
    time = 0
    for segment in rails:
        dt = segment[-1] - time
        assert dt > 0
        f, pos = _desig[segment[0]](segment, pos, dt)
        time = segment[-1]
        r.append((f, time))
    return r


class Rails(ecs.Component):

    """
    .. attribute:: rails
    .. attribute:: time

    """

    def __init__(self, rails, start):
        self.rails = convert_rails(rails, start)
        self.time = 0
        self.step = 0


class RailSystem(ecs.System):

    def on_update(self, dt):
        entities = ecs.intersect(self.world, Position, Rails)
        p = self.world.cm[Position]
        r = self.world.cm[Rails]
        for e in entities:
            rails = r[e]
            rails.time += dt
            try:
                while rails.time >= rails.rails[rails.step][1]:
                    r[e].step += 1
            except IndexError:
                continue
            else:
                func, t = r[e].rails[r[e].step]
            p[e].pos = func(min(t, r[e].time))

###############################################################################
# Private

_desig = {}


def _shift(pos):
    """Return a function decorator that shifts position"""
    def wrapper(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            a = f(*args, **kwargs)
            return tuple(pos[i] + a[i] for i in [0, 1])
        return wrapper
    return wrapper


def _add_desig(func):
    _desig[func.__name__] = func


@_add_desig
def straight(segment, pos, dt):
    dpos = tuple(segment[1][i] / dt for i in [0, 1])

    @_shift(pos)
    def f(time):
        return tuple(dpos[i] * time for i in [0, 1])
    pos = segment[1]
    return f, pos


@_add_desig
def pivot(segment, pos, dt):
    center, arc, time = segment[1:]
    alpha = math.atan((pos[1] - center[1]) / (pos[0] - center[0]))
    vel = arc / time

    @_shift(pos)
    def f(time):
        beta = alpha + vel * time
        return math.cos(beta), math.sin(beta)
    pos = f(time)
    return f, pos


@_add_desig
def custom(segment, pos, dt):
    param = segment[1]
    f = _shift(param, pos)
    pos = param(pos)
    return f, pos
