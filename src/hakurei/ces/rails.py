"""
rails provides a set "animation" movement for entities.  It is mutually
exclusive with physics.

"""

from gensokyo import ces
from gensokyo import primitives

from hakurei.ces import Position


class Rails(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0
        self.track = None


class RailSystem(ces.System):

    req_components = (Rails,)
    callable_methods = set()

    def track(self, entity, rails, *args):
        entity.track = args
    callable_methods.add(track)

    def goto(self, entity, rails, step=0):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param rails: Rails component passed to call
        :type rails: Rails
        :param step: index in script to jump to
        :type step: int

        """

        rails.step = step - 1
    callable_methods.add(goto)

    def sleep(self, entity, rails, time):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param rails: Rails component passed to call
        :type rails: Rails
        :param time: time to sleep in seconds
        :type time: int

        """

        rails.sleep = time
    callable_methods.add(sleep)

    def call(self, entity, rails, method_name, *args, **kwargs):

        """
        Call method with given name and pass it the given entity

        Valid methods for such calling have the type signature::

            method_name(self, entity, rails, *args, **kwargs)

        `*args` and `**kwargs` are optional depending on method.

        :param entity: entity passed to call
        :type entity: Entity
        :param rails: Rails component passed to call
        :type rails: Rails
        :param method_name: name of method
        :type method_name: str

        """

        m = getattr(self, method_name)
        if m in self.callable_methods:
            return m(self, entity, rails, *args, **kwargs)
        else:
            raise TypeError(method_name + " is not a callable method")

    def update(self, dt):
        for entity in self.get_with(self.req_components):
            for rails in entity.get(Rails):
                if rails.sleep > 0:
                    rails.sleep -= dt
                else:
                    if rails.step < len(rails.script):
                        self.call(entity, rails, *rails.script[rails.step])
                        rails.step += 1


class TrackSystem(ces.System):

    req_components = (Rails, Position)
    callable_methods = set()

    def linear(self, pos, dt, speed, vector):
        pos = primitives.Vector(*pos)
        move = vector.get_unit_vector()  # make a copy
        move.length = move.length * dt * speed
        pos += move
        return (pos.x, pos.y)
    callable_methods.add(linear)

    def circle(self, pos, dt, center, angular_vel):
        pos = primitives.Vector(*pos)
        a = (pos - center)
        a.angle += angular_vel * dt
        pos = center + a
        return (pos.x, pos.y)
    callable_methods.add(circle)

    def curve(self, pos, dt, speed, center):
        pass

    def call(self, pos, dt, method_name, *args, **kwargs):
        """
        :param pos: position
        :type pos: tuple
        :param dt: delta time
        :type dt: float
        :param method_name: name of method
        :type method_name: str

        """
        m = getattr(self, method_name)
        if m in self.callable_methods:
            return m(self, pos, dt, *args, **kwargs)
        else:
            raise TypeError(method_name + " is not a callable method")

    def update(self, dt):
        for entity in self.get_with(self.req_components):
            for r in entity.get(Rails):
                for p in entity.get(Position):
                    p.x, p.y = self.call((p.x, p.y), dt, *r.track)
