from pyglet.event import EventDispatcher


class Input(EventDispatcher):
    pass

Input.register_event_type('on_key_press')
Input.register_event_type('on_key_release')
