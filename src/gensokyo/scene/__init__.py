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
        try:
            self.top.init()
        except AttributeError:
            pass

    def pop(self):
        a = self.stack.pop()
        a.delete()

    def update(self, dt):
        """Calls update on top of stack"""
        self.top.update(dt)


class Scene:

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def update(self, dt):
        self.sm.update(dt)

    def delete(self):
        self.sm.delete()
