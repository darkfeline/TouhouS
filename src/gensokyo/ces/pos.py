import abc

from gensokyo import ces


class Position(ces.Component):

    def __init__(self, pos):
        self.pos = pos


class SlavePosition(ces.Component, metaclass=abc.ABCMeta):

    """Virtual class for components that need to update with Position"""

    @abc.abstractmethod
    def setpos(self, pos):
        raise NotImplementedError
