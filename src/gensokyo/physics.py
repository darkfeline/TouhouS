#!/usr/bin/env python3

"""
Physics components use some consistent terminology to keeps things
understandable:

`vel`, `acc`
    velocity, acceleration vectors

`speed`, `accel`
    speed, acceleration, i.e. magnitude of vel, acc

If these do not apply, the fact will be explicitly stated.

"""

import abc

from pyglet.event import EventDispatcher

from gensokyo.primitives import Vector

class AbstractPhysicsComponent(EventDispatcher):

    __meta__ = abc.ABCMeta

AbstractPhysicsComponent.register_event_type('on_dx')
AbstractPhysicsComponent.register_event_type('on_dy')


class DiffBasePhysicsComp(AbstractPhysicsComponent):

    """
    Differentials Base Physics Component

    Provides simple single velocity movement, with differetial vectors to an
    arbitrary degree (v, dv, ddv, ...)

    On update, sends `on_dx` and `on_dy` according to v and `dt`.  Then it
    changes v according to dv and `dt`.  And so on.

    Get/set methods take an index `i` which refers to the 'degree' of the
    vector.  0 is v, 1 is dv, 2 is ddv, and so on.

    """

    def __init__(self, n=1):
        self.vectors = [Vector(0, 0) for i in range(n)]

    def get_vector(self, i):
        try:
            return self.vectors[i]
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)

    def set_vector(self, i, vector):
        try:
            self.vectors[i] = vector
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)

    def get_mag(self, i):
        try:
            return self.vectors[i].length
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)

    def set_mag(self, i, value):
        try:
            self.vectors[i].length = value
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)

    def get_dir(self, i):
        try:
            return self.vectors[i].get_unit_vector()
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)

    def set_dir(self, i, value):
        speed = self.get_mag(i)
        try:
            self.set_vector(i, value)
        except IndexError:
            raise IndexError(self + " doesn't have vector with degree " + i)
        self.set_mag(speed)

    def update(self, dt):
        v = self.get_vector(0)
        self.dispatch_event('on_dx', v.x * dt)
        self.dispatch_event('on_dy', v.y * dt)
        if len(self.vectors) > 1:
            for i in range(1, len(self.vectors) - 1):
                v = self.get_vector(i)
                dv = self.get_vector(i + 1)
                v.x = v.x + dv.x * dt
                v.y = v.y + dv.y * dt
                self.set_vector(i, v)


class LinearPhysicsComp(DiffBasePhysicsComp):

    """
    Linear Physics Component

    Provides simple single velocity movement and adds convenience properties.

    """

    def __init__(self):
        super().__init__(1)

    @property
    def vel(self):
        return self.get_vector(0)

    @vel.setter
    def vel(self, value):
        self.set_vector(1, value)

    @property
    def speed(self):
        return self.vel.length

    @speed.setter
    def speed(self, value):
        self.vel = self.vdir * value

    @property
    def vdir(self):
        return self.vel.get_unit_vector()

    @vdir.setter
    def vdir(self, value):
        """Set velocity direction as the same as vector"""
        speed = self.speed
        self.vel = vector
        self.speed = speed


class LinearAccelPhysicsComp(LinearPhysicsComp):

    """
    Physics Component

    .. attribute:: accel

        acceleration amount per second

    .. attribute:: max_speed

        Caps speed after acceleration.  -1 for uncapped.

    """

    def __init__(self):
        super().__init__()
        self.accel = 0
        self.max_speed = -1

    def update(self, dt):
        super().update(dt)
        if self.speed < self.max_speed:
            self.speed += self.accel * dt
            if self.speed > self.max_speed:
                self.speed = self.max_speed


class LinearDestComp(LinearPhysicsComp):

    """
    Moves at a constant speed to the destination.
    """

    def __init__(self, x, y):
        super().__init__()
        self.pos = Vector(x, y)
        self.dest = Vector(0, 0)

    @property
    def dpos(self):
        return self.dest - self.pos

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        self._dest = value
        speed = self.speed
        self.vel = value - self.pos
        self.speed = speed

    def on_dx(self, dx):
        self.pos += Vector(dx, 0)

    def on_dy(self, dy):
        self.pos += Vector(0, dy)

    def update(self, dt):
        if not self.dpos.length = 0:
            super().update(dt)


class SmoothDestComp(LinearDestComp):

    """
    Moves with smooth acceleration and deceleration toward dest.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.accel = 0
        self.max_speed = -1

    @property
    def accel_dist(self):
        return self.max_speed - self.speed

    @property
    def decel_dist(self):
        return self.speed

    def update(self, dt):
        super().update(dt)
        if not self.dpos.length = 0:
            if self.dpos.length <= self.decel_dist:
                self.speed -= self.accel * dt
            elif self.speed < self.max_speed:
                self.speed += self.accel * dt
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
