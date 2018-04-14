from PIL import Image, ImageDraw
import math

from vectors import Vector, Point


class Graph:
    ARROW_SIZE = 0.2  # one-fifth of cell size
    ARROW_ANGLE = 30 * math.pi / 180  # 30 degrees

    def __init__(self, width, height, origin_x, origin_y, cell_size=20):
        if origin_x < 0 or origin_y < 0:
            raise Exception("origin positions can't be negative")
        self.width = width
        self.height = height
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.cell_size = cell_size
        self.image = Image.new('RGB', (self.width, self.height), "white")
        self._draw = ImageDraw.Draw(self.image)

    def draw_axes(self):
        self._draw.line(
            (self.origin_x, 0, self.origin_x, self.height),
            fill="black", width=2
        )
        self._draw.line(
            (0, self.origin_y, self.width, self.origin_y),
            fill="black", width=2
        )

    def draw_cells(self):
        # draw y lines in positive x direction
        w, h, cs = self.width, self.height, self.cell_size
        ox, oy = self.origin_x, self.origin_y
        for x in range(ox + cs, w, cs):
            self._draw.line((x, 0, x, h), fill="#999")
        # draw y lines in negative x direction
        for x in range(ox - cs, -1, -cs):
            self._draw.line((x, 0, x, h), fill="#999")
        # draw x lines in positive y direction
        for y in range(oy + cs, h, cs):
            self._draw.line((0, y, w, y), fill="#999")
        # draw x lines in negative y direction
        for y in range(oy - cs, -1, -cs):
            self._draw.line((0, y, w, y), fill="#999")

    def line(self, p1, p2, color='blue'):
        P1 = self.image_coordinate(p1)
        P2 = self.image_coordinate(p2)
        self._draw.line((P1.x, P1.y, P2.x, P2.y), fill=color, width=1)

    def arrow(self, p1, p2, color='blue'):
        # first draw line
        self.line(p1, p2, color)
        # get opposite vector from p1 to p2
        opposite = Vector(p2, p1)
        r = opposite.length
        if r <= Graph.ARROW_SIZE * 2:   # too small to draw arrow
            return
        arr_vec = opposite.unit_vector().scale(Graph.ARROW_SIZE)
        # arr_vec is unit vector with start point origin, translate it
        arr_vec = arr_vec.translate(p2)
        rotated1 = arr_vec.rotate(Graph.ARROW_ANGLE)
        rotated2 = arr_vec.rotate(-Graph.ARROW_ANGLE)
        self.line(rotated1.start, rotated1.end)
        self.line(rotated2.start, rotated2.end)

    def render(self):
        self.draw_axes()
        self.draw_cells()

    def show(self):
        # Show the image if possible
        self.image.show()

    def save(self, filepath):
        if self.image is None:
            raise Exception("Can't save, call render() first")
        self.image.save(filepath)

    def image_coordinate(self, space_coord):
        x, y = space_coord.x, space_coord.y
        # y direction is opposite
        return Point(
            self.origin_x + x * self.cell_size,
            self.origin_y - y * self.cell_size
        )

    def clear(self):
        del self._draw


if __name__ == '__main__':
    g = Graph(400, 400, 200, 200, 25)
    p1 = Point.origin()
    p2 = Point(1, 2)
    p3 = Point(4, 4)
    p4 = Point(3, 2)
    g.arrow(p1, p2)
    g.render()
    g.arrow(p1, p3, 'red')
    g.arrow(p1, p4)
    g.save('vectors.png')
