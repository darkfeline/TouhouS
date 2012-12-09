from gensokyo import manager
from gensokyo import state


class Scene(state.StateNode):

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()
        self.graphics = None
        self.updater = None
        self.input = None

    def delete(self):
        self.em.delete()
        self.sm.delete()
