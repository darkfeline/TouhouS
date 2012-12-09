import abc
import functools
from collections import namedtuple

from pyglet.event import EventDispatcher, EVENT_HANDLED

from gensokyo import manager


class TreeNode:

    def __init__(self):
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

    The state machine runs by dispatching events from the root.  The current
    state is determined by the event handlers currently attached to the root.
    The tree serves as data-keeping to keep track of this state.  Transitions
    are made by dispatching the 'on_transition' event to the root.  The event
    should be send with a ``Transition`` named tuple.

    Transition tuples have two fields: a class object ``to`` of the state to
    transition to, and a boolean ``save`` indicating whether the current state
    should be left or "saved" on the tree.  The transition will traverse upward
    from the current leaf until a node is found that can have the indicated
    state.  If an instance of the state is still in the tree ("saved"), then it
    will be restored.  Otherwise, a new instance of the class will be made,
    added to the tree, and activated.

    Nodes start off with their state set to ``None``.  Nodes which will not
    have their own states should leave it ``None`` and leave ``valid_states``
    empty.  Others should set both.  You cannot return to ``None`` state; if
    you need that functionality, use a dummy state instead.

    """

    valid_states = tuple()

    def __init__(self):
        super().__init__()
        self.state = None

    def _leave(self):
        self.state.exit(self.root)
        self.remove_handlers(self.state)
        self.state = None

    def _transition(self, state):
        state.enter(self.root)
        self.root.push_handlers(state)
        self.state = state

    def on_transition(self, transition):
        if self.state is not None:
            if not transition.save:
                self.remove(self.state)
            self._leave()
        if transition.to in self.valid_states:
            for child in list(self.children):
                if isinstance(child, transition.to):
                    a = child
                    break
            try:
                self._transition(a)
            except NameError:
                a = transition.to()
                self.add(a)
                self._transition(a)
            return EVENT_HANDLED

StateTree.register_event_type('on_transition')


class State(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self, root):
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self, root):
        raise NotImplementedError


class StateNode(StateTree, State):
    pass


###############################################################################
# Implementations
###############################################################################
class Scene(StateNode):

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def delete(self):
        self.em.delete()
        self.sm.delete()


class NullState(StateNode):

    def enter(self, root):
        pass

    def exit(self, root):
        pass
