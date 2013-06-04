import abc

from gensokyo.state import State


class Master(metaclass=abc.ABCMeta):

    @property
    def rootenv(self):
        try:
            return self._rootenv
        except AttributeError:
            raise NotImplementedError

    @property
    def drawer(self):
        try:
            return self._drawer
        except AttributeError:
            raise NotImplementedError


class Scene(Master, State):

    def __init__(self, rootenv, drawer):
        super().__init__(rootenv)
        self._drawer = drawer
