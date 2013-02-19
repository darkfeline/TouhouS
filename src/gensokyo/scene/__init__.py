import abc

from gensokyo import state


class Scene(state.StateNode, metaclass=abc.ABCMeta):
    pass
