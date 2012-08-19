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

    def __richcmp__(self, other, int i):
        if i == 2:
            if (self.x == other.x and self.y == other.y and 
                    self.w == other.w and self.h == other.h):
                return True
            else:
                return False
        else:
            raise NotImplementedError

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

    def copy(self):
        return self.__class__(self.x, self.y, self.w, self.h)
