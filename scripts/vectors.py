import math


class Point:
    __slots__ = ['__x', '__y', '__r', '__theta']

    def __init__(self, x=None, y=None):
        self.__x = x
        self.__y = y
        self.__r = None
        self.__theta = None

    @classmethod
    def new(cls, x, y):
        return cls(x, y)

    @classmethod
    def from_polar(cls, r, theta):
        point = cls()
        point.__x = r * math.cos(theta)
        point.__y = r * math.sin(theta)
        point.__r = r
        point.__theta = theta
        return point

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def r(self):
        if self.__r is None:
            self.__r = self.origin_distance()
        return self.__r

    @property
    def theta(self):
        if self.__theta is None:
            self.__theta = self.angle()
        return self.__theta

    def __sub__(self, point):
        return self.new(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return self.new(self.x + point.x, self.y + point.y)

    def scale(self, f):
        return self.new(self.x * f, self.y * f)

    def rotate(self, angle):
        newangle = self.theta + angle
        return self.new(self.r*math.cos(newangle), self.r*math.sin(newangle))

    def origin_distance(self):
        return round(
            (self.x**2 + self.y**2)**0.5,
            5
        )

    def angle(self):
        dx = self.x
        dy = self.y
        if dx == 0:
            if dy > 0:
                return math.pi / 2.0
            else:
                return 3*math.pi/2.0
        angle = math.atan(abs(float(dy))/abs(dx))
        if dx < 0 and dy <= 0:
            return math.pi + angle
        elif dx < 0 and dy > 0:
            return math.pi - angle
        elif dx > 0 and dy > 0:
            return angle
        elif dx > 0 and dy <= 0:
            return 2*math.pi - angle

    @classmethod
    def origin(cls):
        return cls(0, 0)

    def __str__(self):
        return "Point({}, {})".format(self.x, self.y)


class Vector:
    __slots__ = ['__start', '__end', '__length', '__angle', '__direction']

    def __init__(self, start, end):
        self.__start = start
        self.__end = end
        self.__length = None
        self.__direction = self.end - self.start
        self.__angle = None

    @classmethod
    def new(cls, start, end):
        return cls(start, end)

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def direction(self):
        return self.__direction

    @property
    def length(self):
        if self.__length is None:
            self.__length = self.__direction.origin_distance()
        return self.__length

    @property
    def angle(self):
        if self.__angle is None:
            self.__angle = self.__direction.angle()
        return self.__angle

    def scale(self, f):
        scaled_dir = self.direction.scale(f)
        newend = self.start + scaled_dir
        return self.new(self.start, newend)

    def rotate(self, angle):
        rotated_dir = self.direction.rotate(angle)
        newend = self.start + rotated_dir
        return self.new(self.start, newend)

    def translate(self, point):
        newstart = self.start + point
        newend = self.end + point
        return self.new(newstart, newend)

    def unit_vector(self):
        start = Point.origin()
        end = self.__direction.scale(1./self.length)
        return self.new(start, end)

    def __add__(self, vec):
        # FIXME: messed up, what to return? fix this
        end = self.end + vec.direction
        return self.new(self.start, end)

    def __str__(self):
        return "{} -> {}".format(self.start, self.end)


if __name__ == '__main__':
    p = Point.origin()
    start = Point(4, 5)
    print(start.scale(3))
    end = Point(5, -4)
    print(start.r, start.theta)
    vec = Vector(start, end)
    print(vec)
