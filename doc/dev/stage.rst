.. module:: gensokyo.stage

stage - Stage Data and Scripting
================================

.. class:: Stage(world, master)

   Stage is the base class for holding stage data.

   .. attribute:: world

      The ecs world.

   .. attribute:: master

      The master StateMachine.

   Event handlers:

   .. method:: on_update(dt)

      Abstract method.  This defines what the stage does on each tick.
      Generally, you would keep an internal timer (`dt` is the time
      since the last tick in seconds), and do stuff at certain points in
      time.  You can make other event handlers to do stuff triggered not
      by time, but by other events.  But generally you will want at
      least this to script stuff.

.. class:: ScriptedStage(world, master)

   Subclasses :class:`Stage`.  ScriptedStage additionally allows adding
   and removing :class:`Scripts`, which allows you to split Stage
   scripting into easy to manage chunks.

   .. method::
      add(script)
      remove(script)

      Appends and removes scripts.  Order is appending to end and
      removing the first from front.

   Read only properties:

   .. attribute::
      world
      master

      Inherited from :class:`Stage`.

   .. attribute:: scripts

      The list of scripts.

   Event handlers:

   .. method:: on_update(dt)

.. class:: Script

   Scripts to use with :class:`ScriptedStage`.  Script is abstract, so
   you will need to subclass or register.

   .. method:: run(stage, dt)

      Abstract method.  This is run during the
      :meth:`ScriptedStage.on_update` loop.
