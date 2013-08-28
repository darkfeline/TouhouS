import abc
import weakref
import logging

__all__ = []
logger = logging.getLogger(__name__)


def _public(f):
    __all__.append(f.__name__)
    return f


@_public
class StateMachine:

    """
    Simple state machine.

    StateMachine self-binds to master, so you do not need to keep a separate
    reference.

    StateMachine also implements special event hooks.  Events beginning
    with ``hook_`` are redirected to the method with the same name.

    """

    def __init__(self, graph):
        self._graph = graph
        self._state = None

    def init(self, state, *args, **kwargs):
        if self._state is not None:
            raise OpenStateError('Cannot init an open StateMachine.')
        self._state = state(self, *args, **kwargs)
        self._state.enter()

    @property
    def graph(self):
        return self._graph

    @property
    def state(self):
        return self._state

    def event(self, event, *args, **kwargs):
        if event.startswith('hook_'):
            getattr(self, event)(*args, **kwargs)
        else:
            self._state_change(event, *args, **kwargs)

    def _state_change(self, event, *args, **kwargs):
        assert isinstance(event, str)
        old_state = self._state
        if old_state is None:
            raise ClosedStateError('StateMachine already closed.')
        try:
            new = self._graph[old_state.__class__][event]
        except KeyError as e:
            raise NotEventError('{} is not a valid event for state {}'.format(
                event, old_state)) from e
        old_state.exit()
        if new is None:
            self._state = None
        else:
            new = new(self, *args, **kwargs)
            new.enter()
            self._state = new


@_public
class State(metaclass=abc.ABCMeta):

    """
    Defines two methods for entering and exiting the State, as well as
    an attribute which maps events (strings) to resultant States.  State is
    transitive in the MRO (takes a single argument and passes along the rest).

    Attributes:
        transitions: class attribute, dict mapping events to states

    Methods:
        enter: abstract method
        exit: abstract method

    """

    def __init__(self, master, *args, **kwargs):
        self._master = weakref.ref(master)
        super().__init__(*args, **kwargs)

    @property
    def master(self):
        return self._master()

    @abc.abstractmethod
    def enter(self):
        """This method is called when entering a state"""
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self):
        """This method is called when exiting a state"""
        raise NotImplementedError


def _make_getter(name):
    def getter(self):
        try:
            return getattr(self, name)
        except AttributeError:
            raise NotImplementedError
    return getter


@_public
class NotEventError(Exception):
    pass


@_public
class ClosedStateError(Exception):
    pass


@_public
class OpenStateError(Exception):
    pass
