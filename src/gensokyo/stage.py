import abc
import weakref
import logging

logger = logging.getLogger(__name__)


class Stage(metaclass=abc.ABCMeta):

    def __init__(self, world, master):
        self._world = weakref.ref(world)
        self._master = weakref.ref(master)

    @property
    def world(self):
        return self._world()

    @property
    def master(self):
        return self._master()

    @abc.abstractmethod
    def on_update(self, dt):
        raise NotImplementedError


class ScriptedStage(Stage):

    def __init__(self, world, master):
        super().__init__(world, master)
        self._scripts = []

    @property
    def scripts(self):
        return self._scripts

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
