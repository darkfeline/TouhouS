import abc

from gensokyo import ces

__all__ = ['Position', 'SlavePosition']


class Position(ces.Component):

    def __init__(self, pos):
        self.pos = pos
        self._slaves = []

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        for slave in self._slaves:
            slave.setpos(value)

    def add_slave(self, slave):
        self._slaves.append(slave)

    def remove_slave(self, slave):
        self._slaves.remove(slave)


class SlavePosition(ces.Component, metaclass=abc.ABCMeta):

    """Virtual class for components that need to update with Position"""

    def __init__(self, master):
        master.add_slave(self)
        self.setpos(master.pos)

    @abc.abstractmethod
    def setpos(self, pos):
        raise NotImplementedError
