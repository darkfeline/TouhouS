import abc

from gensokyo.state import State


class Master(metaclass=abc.ABCMeta):
    pass

for x in ('rootenv', 'statem', 'drawer', 'clock'):
    y = '_' + x
    def getter(self):
        return getattr(self, y, None)
    setattr(Master, x, property(getter))


class Scene(Master, State):

    def __init__(self, master):
        super().__init__(master)
