.. module:: gensokyo.sprite

sprite - Sprites and Drawing
============================

The sprite module provides a helper interface to Pyglet's Sprites and
Batches.

Sprites
-------

.. class:: BaseSprite(constructor, drawer, group, *args, **kwargs)

   BaseSprite is the simple base wrapper for Pyglet batchable VertexList
   classes, such as Sprite and Label.  `constructor` is the Pyglet class
   to wrap, `drawer` is a :class:`SpriteDrawer` instance, `group` is the
   batch drawing group (a string), and `args` and `kwargs` are passed to
   the Pyglet class constructor.

   The resultant object is automatically added to `drawer` with group
   `group`.  Thus, the BaseSprite instance serves simply as a reference
   to the Pyglet object after creation.

   BaseSprite implements a destructor :meth:`__del__`, which deletes the
   batched Pyglet sprite/vertex list.

   .. attribute:: sprite

      Pyglet sprite object

.. class::
   Sprite(drawer, group, *args, **kwargs)
   Label(drawer, group, *args, **kwargs)

   BaseSprite-wrapped versions of Pyglet's Sprite and Label.

Drawing
-------

.. class:: BaseDrawer

   Abstract base drawer class

   .. method:: draw()

      Abstract method for a drawer.

   Event handlers:

   .. method:: on_draw()

      Call :meth:`draw`.

.. class:: SpriteDrawer(layers)

   Subclasses :class:`BaseDrawer`.  `layers` is an ordered tuple of
   drawing level groups or layers.  This determines the order in which
   added sprites are drawn.  Layers are drawn in order, meaning layers
   further back in the tuple will appear on top of earlier ones.

   .. note::

      Due to an implementation detail, Labels are drawn after all
      Sprites are drawn.

   .. method::
      draw()
      on_draw()

      Inherited from :class:`BaseDrawer`.  :meth:`draw` is implemented.

   .. method:: add_sprite(sprite, group)

      Add a sprite with given group.  This doesn't need to be called as
      the BaseSprite constructor automatically calls this.

.. class:: DrawerStack(layers=tuple())

   Subclasses :class:`SpriteDrawer`.  :class:`DrawerStack` is a stack of
   :class:`SpriteDrawer` instances, and is also a :class:`SpriteDrawer`
   itself.

   .. method::
      on_draw()
      add_sprite(sprite, group)

      Inherited from :class:`SpriteDrawer`.

   .. method:: draw()

      Draw sprites.  The stack's own sprites are drawn first, and then
      sprites are drawn in order from drawers down the stack.

   .. method:: add(drawer)

      Add a drawer to the bottom of the stack

   .. method:: remove(drawer)

      Remove the first instance of `drawer` from the stack, starting
      from the top.
