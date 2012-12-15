import abc
import functools
from collections import namedtuple
import logging

from pyglet.event import EventDispatcher, EVENT_HANDLED

logger = logging.getLogger(__name__)


class TreeNode:

    """
    Be careful using this externally; ``root`` property is memoized

    """

    def __init__(self):
        super().__init__()
        self.parent = None
        self.children = set()

    def add(self, child):
        self.children.add(child)
        child.parent = self

    def remove(self, child):
        self.children.remove(child)
        child.parent = None

    @property
    @functools.lru_cache()
    def root(self):
        if self.parent:
            return self.parent.root
        else:
            return self

"""
class State to transition to
boolean Save current state

"""
Transition = namedtuple('Transition', ['to', 'save'])


class StateTree(TreeNode, EventDispatcher):

    """
    A state machine crossed with a tree.

    StateTree is the root node.  All children nodes are instances of StateNode,
    which is a subclass of StateTree that are also states.  The root node
    StateTree itself is not a state, but it can have a state (it is a state
    machine).  Its children are states, but can also have children states.
    Thus, a tree.

    The current state of the state machine is determined by the handlers of its
    states which are attached to e.g. global event dispatchers.  Thus, the
    state machine itself doesn't do anything, merely coordinating which
    listeners are subscribed and unsubscribed to which global events.  The tree
    serves as data-keeping to keep track of this state.  Transitions are made
    by dispatching the 'on_transition' event to the root.  The event should be
    sent with a ``Transition`` named tuple.

    Transition tuples have two fields: a string ``to`` state to transition to,
    and a boolean ``save`` indicating whether the current state should be left
    or "saved" on the tree.  The transition will traverse upward from the
    current leaf until a node is found that can have the indicated state.  Each
    traversed state will be left, and removed if ``save`` is ``False``, and
    kept in the tree if ``save`` is ``True``.  If an instance of the state is
    still in the tree ("saved"), then it will be restored.  Otherwise, a new
    instance of the class will be made, added to the tree, and activated.

    Nodes start off with their state set to ``None``.  You can navigate to a
    sub-state by adding it to the valid_states tuple and transitioning to it.
    You can exit sub-states by transitioning back to the node itself.

    .. attribute: valid_states
        A dict that maps string state names to StateNode class objects

    """

    valid_states = {}

    def __init__(self):
        super().__init__()
        self.state = None

    def _leave(self):
        self.state.exit()
        self.remove_handlers(self.state)
        self.state = None

    def _transition(self, state):
        state.enter()
        self.root.push_handlers(state)
        self.state = state

    def on_transition(self, transition):
        if self.state is not None:
            if not transition.save:
                logging.debug("Removing state %s", self.state)
                self.remove(self.state)
            logging.debug("Leaving state %s", self.state)
            self._leave()
        if transition.to in self.valid_states:
            logging.debug("Handling transition %s", transition)
            state = self.valid_states[transition.to]
            for child in list(self.children):
                if isinstance(child, state):
                    a = child
                    break
            try:
                self._transition(a)
            except NameError:
                a = state()
                self.add(a)
                self._transition(a)
            return EVENT_HANDLED

StateTree.register_event_type('on_transition')


class State(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self):
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self):
        raise NotImplementedError


class StateNode(StateTree, State):
    pass
