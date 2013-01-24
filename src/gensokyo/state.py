"""
Everything is event-driven.  Thus there is no main loop.  The state machine is
in charge of adding and removing event handlers.  States have their own data,
and expose two methods for activation and deactivation, managing its event
handlers.

"""

import abc
from collections import namedtuple
import logging

from pyglet.event import EventDispatcher

__all__ = ['Transition', 'StateMachine', 'StateNode']
logger = logging.getLogger(__name__)

Transition = namedtuple('Transition', ['to', 'save'])
"""
`to` is the resultant state and should be a :class:`State`.  `save` is a
Boolean and indicates whether or not to save the current state

"""


class StateMachine(EventDispatcher):

    """
    A state machine that works with a tree of states.

    States are tree nodes.

    The current state of the state machine is determined by the handlers of its
    states which are attached to global event dispatchers, the root
    environment.  Thus, the state machine itself doesn't do anything, merely
    coordinating event handlers.  The tree serves as data-keeping to keep track
    of this state.  Transitions are made by dispatching the 'on_transition'
    event to the root.  The event should be sent with a :class:`Transition`
    named tuple.

    Transition tuples have two fields: a string `to` state to transition to,
    and a boolean `save` indicating whether the current state should be left
    or "saved" on the tree.  The transition will traverse upward from the
    current leaf until a node is found that can have the indicated state.  Each
    traversed state will be left, and removed if `save` is ``False``, and
    kept in the tree if `save` is ``True``.  If an instance of the state is
    still in the tree ("saved"), then it will be restored.  Otherwise, a new
    instance of the class will be made, added to the tree, and activated.

    :class:`StateMachine` subclasses pyglet's
    :class:`pyglet.event.EventDispatcher`.  Of note is its
    :meth:`dispatch_event` method.

    .. automethod:: init

    .. method:: dispatch_event(event_type, *args)

        Dispatches event `event_type` to attached event handlers.
        :class:`StateMachine` handles the 'on_transition' event.

    """

    def __init__(self):
        super().__init__()

    def init(self, state, rootenv):
        """Initialize state machine"""
        self.tree = state
        self.state = state
        self.rootenv = rootenv
        state.enter(rootenv)

    def on_transition(self, transition):
        assert isinstance(transition, Transition)
        while transition.to not in self.state.valid_states:
            if not transition.save:
                self.state.parent[type(self.state)] = None
            self.state.exit(self.rootenv)
            self.state = self.state.parent
            if self.state is None:
                return
        a = self.state[transition.to]
        if a is None:
            a = transition.to()
            self.state[transition.to] = a
        self.state = a
        a.enter()

StateMachine.register_event_type('on_transition')


class StateNode(metaclass=abc.ABCMeta):

    """
    A meta class for States.  Has two abstract methods, :meth:`enter` and
    :meth:`exit`

    .. autoattribute:: valid_states
    .. automethod:: enter
    .. automethod:: exit

    """

    valid_states = {}
    """Maps strings to states"""

    def __init__(self, parent):
        self.states = dict(
            (self.valid_states[key], None) for key in self.valid_states)
        self.parent = parent

    @abc.abstractmethod
    def enter(self, rootenv):
        """This method is called when entering a state"""
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self, rootenv):
        """This method is called when exiting a state"""
        raise NotImplementedError
