"""
rails provides a set "animation" movement for entities.  It is mutually
exclusive with physics.

"""

from functools import wraps
import math

from gensokyo import ces
from gensokyo import primitives
from gensokyo import locator

from hakurei.ces import Position


# TODO check this too
class Script(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class ScriptSystem(ces.System):

    req_components = (Script,)
    callable_methods = set()

    def goto(self, entity, script, step=0):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param step: index in script to jump to
        :type step: int

        """

        script.step = step - 1
    callable_methods.add(goto)

    def sleep(self, entity, script, time):

        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param time: time to sleep in seconds
        :type time: int

        """

        script.sleep = time
    callable_methods.add(sleep)

    def die(self, entity, script):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script

        """
        locator.em.delete(entity)
    callable_methods.add(die)

    def fire(self, entity, script, bullet):
        """
        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param bullet: Bullet constructor
        :type bullet: callable returning Bullet

        """
        b = bullet()
        locator.gm.add_to(b)
    callable_methods.add(fire)

    def call(self, entity, script, method_name, *args, **kwargs):

        """
        Call method with given name and pass it the given entity

        Valid methods for such calling have the type signature::

            method_name(self, entity, script, *args, **kwargs)

        `*args` and `**kwargs` are optional depending on method.

        :param entity: entity passed to call
        :type entity: Entity
        :param script: Script component passed to call
        :type script: Script
        :param method_name: name of method
        :type method_name: str

        """

        m = getattr(self, method_name)
        if m in self.callable_methods:
            return m(self, entity, script, *args, **kwargs)
        else:
            raise TypeError(method_name + " is not a callable method")

    def update(self, dt):
        for entity in self.get_with(self.req_components):
            for script in entity.get(Script):
                if script.sleep > 0:
                    script.sleep -= dt
                else:
                    if script.step < len(script.script):
                        self.call(entity, script, *script.script[script.step])
                        script.step += 1


def move_start(f, pos):
    x, y = pos
    @wraps(f)
    def wrapper(*args, **kwargs):
        a, b = f(*args, **kwargs)
        return a + x, b + y
    return wrapper


class Rails(ces.Component):

    def __init__(self, rails):
        self.rails = self.convert(rails)
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

    @staticmethod
    def convert(rails, start_pos):
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
                @move_start(pos)
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
                f = move_start(param, pos)
                pos = param(pos)
            time = segment[-1]
            r.append((f, time))
        return r


class RailSystem(ces.System):

    req_components = (Rails, Position)

    def update(self, dt):
        for entity in self.get_with(self.req_components):
            for r in entity.get(Rails):
                r.time += dt
                func = r[r.time][0]
                pos = func(r.time)
                for p in entity.get(Position):
                    p.x, p.y = pos
