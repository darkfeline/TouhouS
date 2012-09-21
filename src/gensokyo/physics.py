#!/usr/bin/env python3

from pyglet.event import EventDispatcher

from gensokyo.primitives import Vector

class LinearPhysicsComp(EventDispatcher):

    """
    Linear Physics Component

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
