from pyglet.event import EventDispatcher


class Clock(EventDispatcher):

    def tick(self, dt):
        self.dispatch_event('on_update', dt)

    def add_clock(self, clock):
        self.push_handlers(on_update=clock.tick)

    def remove_clock(self, clock):
        self.remove_handlers(on_update=clock.tick)

Clock.register_event_type('on_update')
