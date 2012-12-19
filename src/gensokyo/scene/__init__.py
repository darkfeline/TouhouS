from gensokyo import state
from gensokyo import ces


class Scene(state.StateNode, ces.Environment):

    def __init__(self):
        super().__init__()
        self.graphics = None
        self.input = None
