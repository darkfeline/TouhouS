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

    def __richcmp__(self, int i, other):
        if i == 2:
            if (self.x == other.x and self.y == other.y and 
                    self.w == other.w and self.h == other.h):
                return True
            else:
                return False
        else:
            raise NotImplementedError

    @property
    def width(self):
        return self.w

    @width.setter
    def width(self, value):
        self.w = value

    @property
    def height(self):
        return self.h

    @height.setter
    def height(self, value):
        self.h = value

    @property
    def size(self):
        return (self.w, self.h)

    @size.setter
    def size(self, value):
        self.w, self.h = value

    @property
    def centerx(self):
        return self.w // 2 + self.x

    @centerx.setter
    def centerx(self, value):
        self.x += value - self.centerx

    @property
    def centery(self):
        return self.h // 2 + self.y

    @centery.setter
    def centery(self, value):
        self.y += value - self.centery

    @property
    def center(self):
        return (self.centerx, self.centery)

    @center.setter
    def center(self, other):
        self.centerx, self.centery = other

    @property
    def top(self):
        return self.y + self.h

    @top.setter
    def top(self, value):
        self.y += value - self.y - self.h

    @property
    def bottom(self):
        return self.y

    @bottom.setter
    def bottom(self, value):
        self.y += value - self.y

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.x += value - self.x

    @property
    def right(self):
        return self.x + self.w

    @right.setter
    def right(self, value):
        self.x += value - self.x - self.w

    def copy(self):
        return self.__class__(self.x, self.y, self.w, self.h)
