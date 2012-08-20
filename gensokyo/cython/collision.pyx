# cython: profile=True

cimport libc.stdlib

cdef class AABB:

    cdef int c[2]
    cdef int w[2]
    
    def __cinit__(self, int x, int y, int w, int h):
        self.w[0] = w // 2
        self.w[1] = h // 2
        self.c[0] = self.w[0] + x
        self.c[1] = self.w[1] + y

    cpdef int collide(self, AABB other) except? -1:
        if (abs(self.c[0] - other.c[0]) > (self.w[0] + other.w[0])):
            return 0
        if (abs(self.c[1] - other.c[1]) > (self.w[1] + other.w[1])):
            return 0
        return 1


cdef struct llist:
    int value
    llist *next


cdef class AABBGrid:

    cdef int grid[100][2][2]
    cdef llist *first
    cdef llist *last

    def __cinit__(self):
        cdef int i
        cdef llist *cur
        cdef llist *next
        cur = self.first
        cur.value = 0
        for i in range(1, 99):
            cur.next.value = i
            cur = cur.next
        self.last = cur

    cpdef int add(self, int x, int y, int w, int h) except? -1:
        cdef int i
        i = self.first.value
        self.first = self.first.next
        self.grid[i][0][0] = x
        self.grid[i][0][1] = y
        self.grid[i][1][0] = w
        self.grid[i][1][1] = h
        return i
