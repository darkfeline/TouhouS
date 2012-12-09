from pyglet.evet import EventDispatcher


class Graphics(EventDispatcher):

    def __init__(self):
        self.levels = []

    def push(self, level):
        self.levels.append(level)
        self.push_handlers(level)

    def pop(self):
        level = self.levels.pop()
        self.remove_handlers(level)

Graphics.register_event_type('on_add_sprite')
Graphics.register_event_type('on_draw')
