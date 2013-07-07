"""
master.py
=========

Provides an abstract base class Master for classes that implement a defined set
of event dispatchers/other "global" level objects.
"""

import abc

__all__ = ['Master']


def _make_getter(name):
    def getter(self):
        try:
            return getattr(self, name)
        except AttributeError:
            raise NotImplementedError
    return getter


class Master(metaclass=abc.ABCMeta):
    """
    Master implements a set of properties like a service dispatcher.  It can be
    placed anywhere in the MRO.
    """

for x in ('rootenv', 'statem', 'drawer', 'clock'):
    getter = _make_getter('_' + x)
    setattr(Master, x, property(getter))
