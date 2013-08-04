.. module:: gensokyo.master

master - General serivce provider
=================================

.. class:: Master

   .. attribute::
      rootenv
      drawer
      clock

      These properties return a reference to the named service.  They
      are simple getters for their underscore-preceded cousins.
      :attr:`_rootenv` is set by the engine, so :attr:`rootenv` is
      accessible to all instances, subclassed or otherwise.
