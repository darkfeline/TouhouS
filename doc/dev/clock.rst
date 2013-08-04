.. module:: gensokyo.clock

clock - Clocking, Tick/Update
=============================

Since :mod:`gensokyo` doesn't use a main loop, an EventDispatcher is
used to push :const:`'on_update'` events.  Anything that would
normally run on a main loop needs to register an appropriate handler
with a Clock object.  The :mod:`gensokyo.clock` module exists solely
for this class.

Although :mod:`gensokyo` strives to be purely event-driven,
fundamentally there still needs to be a main loop.  You will need to
schedule a "master" Clock with Pyglet's clock, which will then tick
accordingly::

   master_clock = Clock()
   pyglet.clock.get_default().schedule(master_clock)

.. class:: Clock

   .. method:: tick

      Dispatches an :const:`'on_update'` event.

   .. method::
      add_clock(clock)
      remove_clock(clock)

      These methods allow adding and removing other Clocks, so that they
      will tick along with the current clock.  This simplifies
      management of the "main loop" to adding and removing
      pre-configured Clocks.  For example, you can implement a Clock
      subclass which only ticks once every two ticks and instantly get
      time dilation by putting game entities on the slow Clock.  (You're
      welcome.)

Events
------

.. data:: 'on_update'

   Update event.  Tick event.
