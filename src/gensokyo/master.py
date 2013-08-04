import logging

__all__ = []
logger = logging.getLogger(__name__)


def _public(f):
    __all__.append(f.__name__)
    return f


def _make_getter(name):
    def getter(self):
        try:
            return getattr(self, name)
        except AttributeError:
            raise NotImplementedError
    return getter


@_public
class Master:
    """
    Implements a set of properties like a service dispatcher.  It can be placed
    anywhere in the MRO.

    """

for x in ('rootenv', 'drawer', 'clock'):
    getter = _make_getter('_' + x)
    setattr(Master, x, property(getter))
