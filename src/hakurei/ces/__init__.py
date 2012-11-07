import abc

from gensokyo import ces


class Wrapper(ces.Entity):

    def __init__(self, component):
        self.add(component)


class Position(ces.Component):

    """
    Abstract Interface for components who have a position, i.e. x, y
    coordinates that need to be updated by physics

    """

    # TODO change this to tuple

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def x(self):
        raise NotImplementedError

    @abc.abstractproperty
    def y(self):
        raise NotImplementedError
