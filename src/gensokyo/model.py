from gensokyo import manager


class Model:

    def __init__(self):
        self.em = manager.EntityManager()
        self.sm = manager.SystemManager()
        self.gm = manager.GroupManager()
        self.tm = manager.TagManager()

    def init(self):
        pass

    def update(self, dt):
        self.sm.update(dt)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
