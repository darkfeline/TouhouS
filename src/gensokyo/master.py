import abc

from gensokyo.state import State


class Master(metaclass=abc.ABCMeta):
    pass

for x in ('rootenv', 'drawer'):
    y = '_' + x
    def getter(self):
        return getattr(self, y, None)
    setattr(Master, x, property(getter))


class Scene(Master, State):

    def __init__(self, rootenv, drawer):
        super().__init__(rootenv)
        self._drawer = drawer
