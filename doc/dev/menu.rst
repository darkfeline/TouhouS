.. module:: gensokyo.menu

menu - Menu Framework
=====================

This module is more or less just the :mod:`gensokyo.state` module state
framework with some frills.  The main :class:`Menu` is just a
:class:`gensokyo.state.StateMachine` and
:class:`gensokyo.master.Master`.  Its states are the individual levels
or sections of the menu, :class:`MenuPane` instances.

Like states, to set up a menu, you need to define :class:`MenuPane`
subclasses and a menu graph (a state graph).

.. class:: Menu(graph, x, y)

   Subclasses :class:`gensokyo.state.StateMachine` and
   :class:`gensokyo.master.Master`.

   Inherited from StateMachine:

   .. method::
      init(state, *args, **kwargs)
      event(event, *args, **kwargs)

   .. attribute::
      graph
      state

   Inherited from Master:

   .. attribute::
      rootenv
      drawer
      clock

   Menu creates and keeps its own MenuDrawer, which can be accessed via
   the property :attr:`clock`.

.. class:: MenuPane(master, x, y)

   Subclasses :class:`gensokyo.state.State` and
   :class:`gensokyo.master.Master`.  Like State, you do not need to
   instantiate these normally.

   .. method::
      enter
      exit

      Standard State methods.

   Event Handlers:

   .. method:: on_key_press(symbol, modifiers)

      This is attached to the Pyglet root window, which dispatches key
      press events.
   

.. class:: MenuDrawer

   Simple :class:`gensokyo.sprite.DrawerStack` subclass with only a
   :const:`MENU_GROUP` layer.  You do not need to instantiate this;
   :class:`Menu` does that.

Abstract classes
----------------

.. class:: BaseMenuPane(master, x, y, *args, **kwargs)

   Subclasses :class:`gensokyo.state.State`.  Abstract base class for
   :class:`MenuPane`.  Mainly defines the constructor signature for menu
   panes.  May go away in the future.

Constants
---------

.. data:: MENU_GROUP

   Drawing group for menus.
