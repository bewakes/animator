from vector import Vector, Point


class Point3d(Point):
    __slots__ = ['__x', '__y', '__z', '__r', '__alpha', '__beta', '__gamma']

    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.__x = x
        self.__y = y
        self.__z = z

    @classmethod
    def new(cls, x, y, z):
        return cls(x, y, z)

    @classmethod
    def from_polar(cls, r, alpha, beta, gamma):
        # TODO:
        pass

    @property
    def z(self):
        return self.__z

    def __sub__(self, point):
        return self.new(self.x + point.x, self.y - point.y, self.z - point.z)

    def __add__(self, point):
        return self.new(self.x + point.x, self.y + point.y, self.z + point.z)

    def scale(self, f):
        return self.new(self.x * f, self.y * f, self.z * f)

    def rotate(self, alpha=0, beta=0, gamma=0):
        # TODO: implement this
        pass

    def origin_distance(self):
        return round(
            (self.x**2 + self.y**2 + self.z**2)**0.5,
            5
        )

    @classmethod
    def origin(cls):
        return cls(0, 0, 0)

    def __str__(self):
        return "Point3d({}, {}, {})".format(self.x, self.y, self.z)


class Vector3d(Vector):
    __slots__ = [
        '__start', '__end', '__length', '__alpha',
        '__beta', '__gamma', '__direction'
    ]

    def __init__(self, start, end):
        super().__init__(start, end)
        self.__start = start
        self.__end = end
        self.__direction = self.end - self.start
        self.__length = None
        self.__alpha = None
        self.__beta = None
        self.__gamma = None

    # seems like many methods need not be overridden

    def rotate(self, angle):
        # TODO: implement
        pass


if __name__ == '__main__':
    p = Point3d.origin()
    p2 = Point3d(4, 6, 1)
    print(p + p2)
    print(p+p2+p2)
    print(p2.scale(3))
    vec = Vector3d(p2, p2.scale(3))
    print(vec.unit_vector())
