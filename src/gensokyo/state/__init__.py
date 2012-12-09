import abc
import functools
from collections import namedtuple

from pyglet.event import EventDispatcher, EVENT_HANDLED


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


class StateNode(StateTree, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self, root):
        raise NotImplementedError

    @abc.abstractmethod
    def exit(self, root):
        raise NotImplementedError
