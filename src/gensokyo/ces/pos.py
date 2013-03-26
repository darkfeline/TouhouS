"""
pos.py
======

Contains position stuff.

Entities often need to have a Position, but certain components need to be
updated with regard to that Position.  SlavePositions are registered with an
Entity's Position, and is updated by the Position's setter.  Components are
supposed to contain only data, with logic encapsulated by Systems, but I
implemented this inter-component observer/event relationship for simplicity's
sake.

"""

import abc

from gensokyo import ces

__all__ = ['Position', 'SlavePosition']


class Position(ces.Component):

    """
    Attributes:

    pos
        Self-explanatory

    Methods:

    add_slave
        Add slave position
    remove_slave
        Remove slave position

    These methods are documented, but usually don't need to be called.
    """

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
