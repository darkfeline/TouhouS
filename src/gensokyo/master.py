import abc

__all__ = ['Master']


def _make_getter(name):
    def getter(self):
        return getattr(self, name, None)
    return getter


class Master(metaclass=abc.ABCMeta):
    pass

for x in ('rootenv', 'statem', 'drawer', 'clock'):
    getter = _make_getter('_' + x)
    setattr(Master, x, property(getter))
