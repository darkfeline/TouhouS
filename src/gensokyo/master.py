import abc

__all__ = ['Master']


class Master(metaclass=abc.ABCMeta):
    pass

for x in ('rootenv', 'statem', 'drawer', 'clock'):
    y = '_' + x
    def getter(self):
        return getattr(self, y, None)
    setattr(Master, x, property(getter))
del x, y, getter
