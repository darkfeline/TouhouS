.. module:: gensokyo.ui

ui - Simple UI drawing
======================

.. class:: FPSDisplay(drawer, x, y, clock)

   `clock` is a Pyglet clock, not a :class:`gensokyo.clock.Clock`.  It's
   used to calculate the FPS.

   .. attribute:: clock

      The referenced Pyglet clock isntance.

   Event handlers:

   .. method:: on_update(dt)

      This must be attached to an event dispatcher, probably a clock.
      Note that this is only responsible for updating; the actual fps
      comes from the Pyglet clock: the base FPS or "master" FPS, if you
      have a single master clock scheduled.  Usually the update tick and
      the FPS tick will be the same though, unless you're implementing
      UI slowdown special effects.

.. class:: TextCounter(drawer, x, y, title, value=0, width=190)

   Create a TextCounter instance which is drawn like this::

      <title>          <value>

   For example::

      Score              56000

   `x` and `y` give the coordinates of the upper left corner. `width`
   gives the width.

   Properties:

   .. attribute::
      title
      value

      Inherited from :class:`Counter`.  Getter and setter are
      implemented.

.. class:: IconCounter(drawer, x, y, title, value=0, width=190)

   Create an IconCounter instance which is drawn like this::

      <title>          <#value_of_icons>

   For example::

      Lives                    * * * * *

   `x` and `y` give the coordinates of the upper left corner. `width`
   gives the width.

   Properties:

   .. attribute::
      title
      value

      Inherited from :class:`Counter`.  Getter and setter are
      implemented.

   Class attributes:

   .. attribute:: icon_img

      Image to use.  Default is :const:`gensokyo.resources.star`.

   .. attribute:: display_max

      Maximum value.  Default is 8.

Abstract classes, Base classes, Constants
-----------------------------------------

.. data:: UI_GROUP

   Drawing group of all UI sprites.

.. class:: UILabel(drawer, *args, **kwargs)

   Simple subclass of :class:`gensokyo.sprite.Sprite`. The drawing
   group of instances are set to :const:`UI_GROUP`.

.. class:: Counter

   Abstract interface class.
 
   Describes the following abstract properties:

   .. attribute:: title

      The title, name, or label of the counter.

   .. attribute:: value

      The value of the counter.  Can be displayed in text, icons, or
      hidden by implementations.
