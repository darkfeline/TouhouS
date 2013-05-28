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

from gensokyo import ecs

__all__ = ['Position', 'SlavePosition']


class Position(ecs.Component):

    """
    Position is a final class.

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
        self._slaves = []
        self.pos = pos

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


class SlavePosition(ecs.Component, metaclass=abc.ABCMeta):

    """
    Virtual class for components that need to update with Position

    SlavePosition is a transition class, i.e., its __init__ passes on its
    parameters, minus its own, to the next class in the MRO.  (Next is
    technically Component, but it is an empty virtual class).  It can also
    serve as a final class, provided no extra parameters are given, in which
    case the MRO ends with ['SlavePosition', 'Component']
    """

    def __init__(self, master, *args, **kwargs):
        master.add_slave(self)
        super().__init__(*args, **kwargs)
        self.setpos(master.pos)

    @abc.abstractmethod
    def setpos(self, pos):
        raise NotImplementedError
