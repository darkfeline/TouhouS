from pyglet.event import EventDispatcher


class Input(EventDispatcher):
    pass

Updater.register_event_type('on_key_press')
Updater.register_event_type('on_key_release')
