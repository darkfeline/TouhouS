from pyglet.event import EventDispatcher


class Updater(EventDispatcher):
    pass

Updater.register_event_type('on_update')
