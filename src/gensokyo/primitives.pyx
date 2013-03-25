# cython: profile=True
# cython: language_level=3
# cython: embedsignature=True

import math

try:
    Numbers = (int, float, complex)
except NameError:
    Numbers = (int, float)

cdef int _collide_circle_rect(Circle circle, Rect rect) except? -1:
    if rect.left < circle.x < rect.right: return True
    if rect.bottom < circle.y > rect.top: return True
    if circle.y - circle.r < rect.bottom < circle.y + circle.r: return True
    if circle.y - circle.r < rect.top < circle.y + circle.r: return True
    if circle.x - circle.r < rect.left < circle.x + circle.r: return True
    if circle.x - circle.r < rect.right < circle.x + circle.r: return True
    return False

cdef class Rect:

    cdef public int x
    cdef public int y
    cdef public int w
    cdef public int h

    def __cinit__(self, int x, int y, int w, int h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return 'Rect({}, {}, {}, {})'.format(self.x, self.y, self.w,
                self.h)

    def __richcmp__(x, y, int op):
        if not isinstance(x, Rect) or not isinstance(y, Rect):
            return NotImplemented
        if op == 2:
            return x.x == y.x and x.y == y.y and x.w == y.w and x.h == y.h
        elif op == 3:
            return x.x != y.x or x.y != y.y or x.w != y.w or x.h != y.h
        else:
            return NotImplemented

    def __mul__(x, y):
        if isinstance(x, Rect):
            self, other = x, y
        else:
            self, other = y, x
        if isinstance(other, Numbers):
            return Rect(self.x, self.y, self.w * other, self.h * other)
        else:
            return NotImplemented

    property width:
        def __get__(self):
            return self.w
        def __set__(self, value):
            self.w = value

    property height:
        def __get__(self):
            return self.h
        def __set__(self, value):
            self.h = value

    property size:
        def __get__(self):
            return (self.w, self.h)
        def __set__(self, value):
            self.w, self.h = value

    property centerx:
        def __get__(self):
            return self.w // 2 + self.x
        def __set__(self, value):
            self.x += value - self.centerx

    property centery:
        def __get__(self):
            return self.h // 2 + self.y
        def __set__(self, value):
            self.y += value - self.centery

    property center:
        def __get__(self):
            return (self.centerx, self.centery)
        def __set__(self, other):
            self.centerx, self.centery = other

    property top:
        def __get__(self):
            return self.y + self.h
        def __set__(self, value):
            self.y += value - self.y - self.h

    property bottom:
        def __get__(self):
            return self.y
        def __set__(self, value):
            self.y += value - self.y

    property left:
        def __get__(self):
            return self.x
        def __set__(self, value):
            self.x += value - self.x

    property right:
        def __get__(self):
            return self.x + self.w
        def __set__(self, value):
            self.x += value - self.x - self.w

    property topleft:
        def __get__(self):
            return (self.x, self.y + self.h)
        def __set__(self, value):
            a = self.topleft
            self.x += value[0] - a[0]
            self.y += value[1] - a[1]

    property topright:
        def __get__(self):
            return (self.x + self.w, self.y + self.h)
        def __set__(self, value):
            a = self.topright
            self.x += value[0] - a[0]
            self.y += value[1] - a[1]

    property bottomleft:
        def __get__(self):
            return (self.x, self.y)
        def __set__(self, value):
            a = self.bottomleft
            self.x += value[0] - a[0]
            self.y += value[1] - a[1]

    property bottomright:
        def __get__(self):
            return (self.x + self.w, self.y)
        def __set__(self, value):
            a = self.bottomright
            self.x += value[0] - a[0]
            self.y += value[1] - a[1]

    def copy(self):
        return self.__class__(self.x, self.y, self.w, self.h)

    def collide(self, other):
        if isinstance(other, Rect):
            if other.right < self.left: return False
            if other.left > self.right: return False
            if other.top < self.bottom: return False
            if other.bottom > self.top: return False
            return True
        if isinstance(other, Circle):
            return _collide_circle_rect(other, self)
        else:
            raise NotImplementedError

cdef class Circle:

    cdef public int x
    cdef public int y
    cdef public double r

    def __cinit__(self, int x, int y, double r):
        self.x = x
        self.y = y
        self.r = r

    def __richcmp__(self, other, int i):
        if i == 2:
            if isinstance(other, Circle):
                if (self.x, self.y, self.r) == (other.x, other.y, other.r):
                    return True
                else:
                    return False
            else:
                return NotImplemented
        elif i == 3:
            return not (self == other)
        else:
            return NotImplemented

    def __mul__(x, y):
        if isinstance(x, Circle):
            self, other = x, y
        else:
            self, other = y, x
        if isinstance(other, Numbers):
            return Circle(self.x, self.y, self.r * other)
        else:
            return NotImplemented

    def copy(self):
        return self.__class__(self.x, self.y, self.r)

    def collide(self, other):
        if isinstance(other, Circle):
            dist = Vector(other.x - self.x, other.y - self.y)
            if dist.length <= self.r + other.r:
                return True
            else:
                return False
        if isinstance(other, Rect):
            return _collide_circle_rect(self, other)
        else:
            raise NotImplementedError


cdef class Vector:

    cdef public double x
    cdef public double y

    def __cinit__(self, double x, double y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError

    def __add__(x, y):
        if not isinstance(x, Vector) or not isinstance(y, Vector):
            return NotImplemented
        return Vector(x.x + y.x, x.y + y.y)

    def __sub__(x, y):
        if not isinstance(x, Vector) or not isinstance(y, Vector):
            return NotImplemented
        return Vector(x.x - y.x, x.y - y.y)

    def __richcmp__(x, y, int op):
        if not isinstance(x, Vector) or not isinstance(y, Vector):
            return NotImplemented
        if op == 2:
            return x.x == y.x and x.y == y.y
        elif op == 3:
            return x.x != y.x or x.y != y.y
        else:
            return NotImplemented

    def __mul__(x, y):
        if isinstance(x, Vector):
            self, other = x, y
        else:
            self, other = y, x
        if isinstance(other, Numbers):
            return Vector(self.x * other, self.y * other)
        else:
            return NotImplemented

    def __str__(self):
        return "Vector({}, {})".format(self.x, self.y)

    property length:
        def __get__(self):
            return math.sqrt(self.x ** 2 + self.y ** 2)
        def __set__(self, value):
            angle = self.angle
            self.x = value * math.cos(angle)
            self.y = value * math.sin(angle)

    property angle:
        def __get__(self):
            if self.x == 0:
                if self.y > 0:
                    return math.pi / 2
                elif self.y < 0:
                    return math.pi * 3 / 2
                else:
                    raise NoAngleError
            else:
                return math.fmod(math.atan2(self.y, self.x) + 2 * math.pi,
                        2 * math.pi)
        def __set__(self, value):
            l = self.length
            self.x = l * math.cos(value)
            self.y = l * math.sin(value)

    def get_unit_vector(self):
        try:
            t = self.angle
        except NoAngleError:
            return Vector(0, 0)
        return Vector(math.cos(t), math.sin(t))

    def copy(self):
        return self.__class__(self.x, self.y)


class NoAngleError(Exception): pass
