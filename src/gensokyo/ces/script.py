"""
Scripting module

Provides stuff for versatile scripting.

Units
*****

The basic data structure is a *scripting unit*.  Scripting units are tuples
containing *condition units*.  Condition units are also tuples like so::

    (if, then, then, ...)

``if`` is a function that returns Boolean.  It is followed by any number of
functions (``then`` in the above example) which are called if the ``if`` is
``True``.  If ``then`` returns a scripting unit, it will be added to the
Script's list of active units.  Otherwise, ``then`` should return ``None``.  If
it returns a list of scripting units, all of them will be added.  Newly added
units will not be run until the next loop.

If ``then`` is the constant ``EXPIRE``, the scripting unit will be expired.
This is immediate, so make sure it is the last item in its condition unit.

``if`` and ``then`` are passed their entity as their first argument.

``if`` and ``then`` are example names; please do not use them (``if`` is a
Python keyword).

Scripting is functional; it evaluates only.  Thus, build the state checking
into the functions (i.e., "currying").  If you need to store data, store it in
the Script component.

Scripts and ScriptSystem
************************

Script instances have a list of currently active scripting units.

Entities can have multiple Scripts, but there is generally no need, except to
split responsibilities, possibly.

ScriptSystem instances iterate over Script objects and iterate over their
active scripting units every update loop.  Scripting units function like
datafied if/elses::

    (
        (if, then_do_this, and_this),
        (else_if, do_this)
    )

The conditions in each scripting unit are exclusive, evaluated in order.

.. data:: EXPIRE

"""

from gensokyo import ces
from gensokyo import locator

EXPIRE = 'expire'


class Script(ces.Component):

    """
    .. attribute:: units

    """

    def __init__(self, units):
        self.units = units


class ScriptSystem(ces.System):

    req_components = (Script,)

    def update(self, dt):
        for entity in locator.em.get_with(self.req_components):
            for script in entity.get(self.req_components[0]):
                for unit in list(script.units):
                    for cond in unit:
                        test, run = cond[0], cond[1:]
                        if test(entity):
                            for f in run:
                                if f == EXPIRE:
                                    script.units.remove(unit)
                                else:
                                    r = f(entity)
                                    if r:
                                        try:
                                            script.units.extend(r)
                                        except TypeError:
                                            assert isinstance(r, tuple)
                                            script.units.append(r)
