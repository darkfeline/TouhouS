from pyglet.event import EventDispatcher


class Clock(EventDispatcher):

    def tick(self, dt):
        self.dispatch_event('on_update', dt)

Clock.register_event_type('on_update')
