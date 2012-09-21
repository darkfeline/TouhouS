#!/usr/bin/env python3

from pyglet.event import EventDispatcher

from gensokyo.primitives import Vector

class FreePhysicsComp(EventDispatcher):

    """
    Free Physics Component

    Provides simple single velocity movement, with physics vectors to an
    arbitrary degree (v, dv, ddv, ...)

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
            self.set_vector(i) = value
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

FreePhysicsComp.register_event_type('on_dx')
FreePhysicsComp.register_event_type('on_dy')

class LinearPhysicsComp(EventDispatcher):

    """
    Linear Physics Component

    Provides simple single velocity movement

    """

    def __init__(self):
        self.vel = Vector(0, 0)

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

    def update(self, dt):
        self.dispatch_event('on_dx', self.vel.x * dt)
        self.dispatch_event('on_dy', self.vel.y * dt)

LinearPhysicsComp.register_event_type('on_dx')
LinearPhysicsComp.register_event_type('on_dy')


class AccelPhysicsComp(VelPhysicsComp):

    """
    Physics Component

    Provides freeform velocity and acceleration, with capped velocity

    .. attribute:: max_speed

        Caps speed after acceleration.  -1 for uncapped.

    """

    def __init__(self):
        super().__init__()
        self.acc = Vector(0, 0)
        self.max_speed = -1

    @property
    def accel(self):
        return self.acc.length

    @accel.setter
    def accel(self, value):
        self.acc = self.adir * value

    @property
    def adir(self):
        return self.acc.get_unit_vector()

    @adir.setter
    def adir(self, value):
        """Set acceleration direction as the same as vector"""
        speed = self.speed
        self.acc = vector
        self.speed = speed

    def update(self, dt):
        super().update(dt)
        self.vel += self.acc * dt
        if self.max_speed >= 0 and self.speed > self.max_speed:
            self.speed = self.max_speed


class LinearAccelPhysicsComp(VelPhysicsComp):

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
        self.speed += self.accel * dt
        if self.max_speed >= 0 and self.speed > self.max_speed:
            self.speed = self.max_speed
