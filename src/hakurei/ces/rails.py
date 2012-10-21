"""
rails provides a set "animation" movement for entities.  It is mutually
exclusive with physics.

"""

from gensokyo import ces

from hakurei.ces import Position


class Rails(ces.Component):

    def __init__(self, rails):
        """
        Format for rails::

            [(action, *args, until), ...]

        """
        self.rails = rails
        self.time = 0

    @property
    def current(self):
        cur = 0
        while self.rails[cur][-1] < self.time:
            cur += 1
        return self.rails[cur][:-1]


class RailSystem(ces.System):

    req_components = (Rails, Position)
    callable_methods = set()

    def call(self, pos, method_name, *args, **kwargs):
        """
        :param pos: position
        :type pos: tuple
        :param method_name: name of method
        :type method_name: str

        """
        m = getattr(self, method_name)
        if m in self.callable_methods:
            return m(self, pos, *args, **kwargs)
        else:
            raise TypeError(method_name + " is not a callable method")

    def update(self, dt):
        for entity in self.get_with(self.req_components):
            for r in entity.get(Rails):
                for p in entity.get(Position):
                    p.x, p.y = self.call((p.x, p.y), *r.current)
                r.time += dt
