import logging

from gensokyo import manager

logger = logging.getLogger(__name__)


class SceneStack:

    def __init__(self):
        self.stack = []

    @property
    def top(self):
        return self.stack[-1]

    @property
    def view(self):
        return self.top.view

    @property
    def model(self):
        return self.top.model

    def push(self, scene):
        logger.debug("Push onto stack {}".format(scene))
        self.stack.append(scene)
        if hasattr(self.top, "init"):
            self.top.init()

    def pop(self):
        a = self.stack.pop()
        a.delete()


class Scene:

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def delete(self):
        self.sm.delete()
