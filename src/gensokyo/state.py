"""
state.py
========

Provides a simple state machine framework.  Everything is event-driven; thus
there is no main loop.  A clock somewhere controls "tick" events, and that
controls the execution.  What defines a state is which event handlers are
attached.

master in this module refers generally to any object with event dispatcher
attributes that would then be used in State's enter() and exit(); instances of
Master from master.py are one possibility.
"""

import abc
import weakref
import logging

from gensokyo.master import Master

__all__ = ['StateMachine', 'State', 'NotEventError']
logger = logging.getLogger(__name__)


class StateMachine:

    """
    Simple state machine.

    StateMachine also implements special event hooks.  Events beginning
    with 'hook_' are redirected to the method with the same name.
    """

    def __init__(self, master):
        self._master = weakref.ref(master)

    def init(self, state, *args, **kwargs):
        self.state = state(self.master, *args, **kwargs)
        self.state.enter()

    @property
    def master(self):
        return self._master()

    def event(self, event, *args, **kwargs):
        if event.startswith('hook_'):
            getattr(self, event)(*args, **kwargs)
        else:
            self._state_change(event, *args, **kwargs)

    def _state_change(self, event, *args, **kwargs):
        assert isinstance(event, str)
        try:
            new = self.state.transitions[event]
        except KeyError:
            raise NotEventError('{} is not a valid event'.format(event))
        self.state.exit()
        if new is None:
            self.state = None
            return
        new = new(self.master, *args, **kwargs)
        new.enter()
        self.state = new


class State(metaclass=abc.ABCMeta):

    """
    Defines two methods for entering and exiting the State, as well as an
    attribute which maps events (strings) to resultant States.

    Methods:

    enter
        abstract method
    exit
        abstract method

    Attributes:

    transitions
        class attribute, dict mapping events to states
    """

    transitions = {}

    def __init__(self, master):
        self._master = weakref.ref(master)

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


class Scene(Master, State):
    pass


class NotEventError(Exception):
    pass
