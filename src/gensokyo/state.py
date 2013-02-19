"""
state.py
========

Provides a simple state machine framework.  Everything is event-driven; thus
there is no main loop.  A clock somewhere controls "tick" events, and that
controls the execution.  What defines a state is which event handlers are
attached.

"""

import abc
import logging

__all__ = ['StateMachine', 'State', 'NotEventError']
logger = logging.getLogger(__name__)


class StateMachine:

    """
    Simple state machine.  Plug n Play.
    """

    def __init__(self, rootenv, state):
        self.rootenv = rootenv
        state.enter(rootenv)
        self.state = state

    def event(self, event, *args, **kwargs):
        assert isinstance(event, str)
        new = self.state.event(event, *args, **kwargs)
        self.state.exit(self.rootenv)
        new.enter(self.rootenv)
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
    event
        dispatch event

    Attributes:

    transitions
        class attribute, dict mapping events to states
    """

    transitions = {}

    def event(self, event, *args, **kwargs):
        assert isinstance(event, str)
        try:
            s = self.transitions[event]
        except KeyError:
            raise NotEventError
        return s(*args, **kwargs)

    @abc.abstractmethod
    def enter(self, rootenv):
        """This method is called when entering a state"""
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self, rootenv):
        """This method is called when exiting a state"""
        raise NotImplementedError


class NotEventError(Exception):
    pass
