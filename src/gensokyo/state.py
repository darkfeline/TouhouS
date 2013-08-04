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

    def init(self, state, *args, **kwargs):
        self._state = state(self, *args, **kwargs)
        self._state.enter()

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
        try:
            new = self._state.transitions[event]
        except KeyError as e:
            raise NotEventError('{} is not a valid event'.format(event)) from e
        try:
            s = self._state
        except AttributeError as e:
            raise ClosedStateError('StateMachine already closed') from e
        else:
            s.exit()
        if new is None:
            self._state = None
            return
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
        enter: method
        exit: abstract method

    """

    transitions = {}

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
class BaseMaster:
    """
    Implements a set of properties like a service dispatcher.  It can be placed
    anywhere in the MRO.

    """

for x in ('rootenv', 'drawer', 'clock'):
    getter = _make_getter('_' + x)
    setattr(BaseMaster, x, property(getter))


@_public
class Master(BaseMaster, StateMachine):
    pass


@_public
class NotEventError(Exception):
    pass


@_public
class ClosedStateError(Exception):
    pass
