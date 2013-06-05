import abc
import logging

logger = logging.getLogger(__name__)


class Stage(metaclass=abc.ABCMeta):

    def __init__(self, world, master):
        self.world = world
        self.master = master

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError


class ScriptedStage(Stage):

    def __init__(self, world, master):
        super().__init__(world, master)
        self.scripts = []

    def add(self, script):
        assert isinstance(script, Script)
        self.scripts.append(script)

    def remove(self, script):
        assert isinstance(script, Script)
        self.scripts.remove(script)

    def on_update(self, dt):
        for x in self.scripts:
            x.run(self, dt)


class Script(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def run(self, stage, dt):
        raise NotImplementedError
