class Rect:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return 'Rect({}, {}, {}, {})'.format(self.x, self.y, self.width,
                self.height)

    def __eq__(self, other):
        if (self.x == other.x and self.y == other.y and 
                self.width == other.width and self.height == other.height):
            return True
        else:
            return False

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, value):
        self.width, self.height = value

    @property
    def centerx(self):
        return self.width // 2 + self.x

    @centerx.setter
    def centerx(self, value):
        self.x += value - self.centerx

    @property
    def centery(self):
        return self.height // 2 + self.y

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
        return self.y + self.height

    @top.setter
    def top(self, value):
        self.y += value - self.y - self.height

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
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.x += value - self.x - self.width

    def copy(self):
        return self.__class__(self.x, self.y, self.width, self.height)
