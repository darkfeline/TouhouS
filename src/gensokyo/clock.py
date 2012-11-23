from pyglet import event
from pyglet import clock

from gensokyo.globals import FPS


class Clock(event.EventDispatcher):

    def __init__(self):
        def update(dt):
            self.dispatch_event('on_update', dt)
        self._update_func = update
        clock.schedule_interval(update, 1 / FPS)

    def delete(self):
        super().delete()
        clock.unschedule(self._update_func)

Clock.register_event_type('on_update')
