import abc
from collections import namedtuple

from pyglet.event import EventDispatcher

"""
class State to transition to
boolean Save current state

"""
Transition = namedtuple('Transition', ['to', 'save'])


class StateMachine(EventDispatcher):

    valid_states = tuple()

    def __init__(self):
        self.state = None

    def on_transition(self, transition):
        raise NotImplementedError


class State(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def enter(self):
        pass

    @abc.abstractmethod
    def exit(self):
        pass


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


class StateTree(StateMachine, TreeNode):
    pass


class StateNode(StateTree, State):
    pass
