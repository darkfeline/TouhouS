.. module:: gensokyo.clock

clock - Clocking, Tick/Update
=============================

Since :mod:`gensokyo` doesn't use a main loop, an EventDispatcher is
used to push :const:`'on_update'` events.  Anything that would
normally run on a main loop needs to register an appropriate handler
with a Clock object.  The :mod:`gensokyo.clock` module exists solely
for this class.

.. class:: Clock

   .. method:: tick

      Dispatches an :const:`'on_update'` event.

   .. method::
      add_clock(clock)
      remove_clock(clock)

      These methods allow adding and removing other Clocks, so that they
      will tick along with the current clock.  This simplifies
      management of the "main loop" to adding and removing
      pre-configured Clocks.

Events
------

.. data:: 'on_update'

   Update event.  Tick event.
