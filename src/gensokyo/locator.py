import sys


class ServiceLocator:

    """
    Service locator

    .. attribute:: key_state
    .. attribute:: state_tree
    .. attribute:: window
    .. attribute:: graphics
    .. attribute:: clock

    """

    def __init__(self):
        self.key_state = None
        self.state_tree = None
        self.window = None
        self.graphics = None
        self.clock = None

sys.modules[__name__] = ServiceLocator()
