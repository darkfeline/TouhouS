.. module:: gensokyo.state

state - State Framework
=======================

:mod:`gensokyo` provides a simple event-based state machine framework.
The current state of execution is defined by the event handlers bound to
event dispatchers.  Thus, the :mod:`gensokyo.state` module provides
suitable :class:`StateMachine` and :class:`State` classes for managing
event handlers on state transitions.

Example
-------

Example usage::

   from gensokyo.master import Master
   from gensokyo.clock import Clock

   class StateA(State):

      def __init__(self, master, *args, **kwargs):
         self.i = 0

      def on_update(self, dt):
         """Do stuff."""
         self.i += dt
         if self.i > 50:
         self.master.event('next')

      def enter(self):
         self.master.clock.push_handlers(self)

      def exit(self):
         self.master.clock.remove_handlers(self)

   class StateB(State):

      def __init__(self, master, *args, **kwargs):
         self.i = 0

      def on_update(self, dt):
         """Do stuff."""
         self.i += dt
         if self.i > 40:
         self.master.event('exit')

      def enter(self):
         self.master.clock.push_handlers(self)

      def exit(self):
         self.master.clock.remove_handlers(self)

   class CustomMachine(Master, StateMachine): pass

   statem = CustomMachine({
      StateA: {
         'next': StateB,
      },
      StateB: {
         'exit': None,
      },
   })
   statem._clock = Clock()
   statem.init(StateA)
   while True:
      statem.clock.tick()

StateMachine objects
--------------------

.. class:: StateMachine(graph)

   StateMachine instances manage a level of the state graph.  Most
   likely, you will need to subclass StateMachine and attach event
   dispatcher objects to it during construction.  That way, States,
   which will be given a reference to the StateMachine, will be able to
   access these event dispatchers and be able to set and remove event
   handlers.

   `graph` is a dictionary::

      {
         (state, {
            event: transition_state,
         })
      }

   :mod:`gensokyo.master` provides a class that defines a standard set
   of event dispatchers.  Most likely, you will subclass both
   :class:`gensokyo.master.Master` and StateMachine, in which case
   Master can go anywhere in the MRO.

   Make sure you properly close the StateMachine when exiting by
   transitioning to a :const:`None` state.

   StateMachine must be last in the MRO.

    .. method:: init(state, *args, **kwargs)

      Set the initial state.  `state` is a :class:`State` class or
      subclass.  `args` and `kwargs` are passed to the state's
      constructor.  Reopens the StateMachine if closed.

    .. method:: event(event, *args, **kwargs)

      Declare that `event` happened.  This results in a state
      transition.  `args` and `kwargs` are passed to the new state's
      constructor.

   Read only properties:

      .. attribute:: state

         The current state.  If the StateMachine is closed, the state is
         :const:`None`.

Setting Up States
-----------------

.. class:: State(master, *args, **kwargs)

   You should never need to create State instances manually, as
   everything is handled through StateManager instances.  

   In order to set up a state graph, you need to make at least one
   subclass of State, implement necessary :meth:`__init__`,
   :meth:`enter`, and :meth:`exit` methods, then set up a graph
   dictionary mapping States and events to resultant States.

   States are transitive in the MRO.  State.__init__ takes its argument
   and passes the rest along the MRO.

   .. method::
      enter()
      exit()

      Abstract methods which are called on state transitions.  These
      should set and unset event handlers that define the state.

   Read only properties:

   .. attribute:: master

      The State instance's owning StateMachine instance.
