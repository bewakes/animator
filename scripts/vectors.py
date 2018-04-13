from PIL import Image, ImageDraw
import math


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

    def line(self, x1, y1, x2, y2, color='blue'):
        X1, Y1 = self.image_coordinate((x1, y1))
        X2, Y2 = self.image_coordinate((x2, y2))
        self._draw.line((X1, Y1, X2, Y2), fill=color, width=2)

    def arrow(self, x1, y1, x2, y2, color='blue'):
        # first draw line
        self.line(x1, y1, x2, y2, color)
        # get polar
        r, theta = get_polar_vec(x2, y2, x1, y1)
        if r <= Graph.ARROW_SIZE * 2:   # too small to draw arrow
            return
        left_arr_angle = theta - Graph.ARROW_ANGLE
        right_arr_angle = theta + Graph.ARROW_ANGLE
        left_arr = get_cartesian_vec(Graph.ARROW_SIZE, left_arr_angle)
        right_arr = get_cartesian_vec(Graph.ARROW_SIZE, right_arr_angle)
        left_dest = add_vecs(x2, y2, *left_arr)
        right_dest = add_vecs(x2, y2, *right_arr)
        self.line(x2, y2, *left_dest, color)
        self.line(x2, y2, *right_dest, color)

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

    def image_coordinate(self, graph_coord):
        x, y = graph_coord
        # y direction is opposite
        return self.origin_x + x * self.cell_size,\
            self.origin_y - y * self.cell_size

    def clear(self):
        del self._draw


# HELPER FUNCTIONS
def vec_length(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


def get_unit_vector(x1, y1, x2, y2):
    length = vec_length(x1, y1, x2, y2)
    return (x2-x1)/length, (y2-y1)/length


def get_polar_vec(x1, y1, x2, y2):
    r = vec_length(x1, y1, x2, y2)
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        if dy > 0:
            return r, math.pi / 2.0
        else:
            return r, 3*math.pi/2.0
    angle = math.atan(abs(float(dy))/abs(dx))
    if dx < 0 and dy <= 0:
        return r, math.pi + angle
    elif dx < 0 and dy > 0:
        return r, math.pi - angle
    elif dx > 0 and dy > 0:
        return r, angle
    elif dx > 0 and dy <= 0:
        return r, 2*math.pi - angle
    return 0, 0  # perhaps it won't reach here


def get_cartesian_vec(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def add_vecs(x1, y1, x2, y2):
    return x1+x2, y1+y2


def scale_vec(x, y, f):
    return x*f, y*f


if __name__ == '__main__':
    g = Graph(400, 400, 200, 200, 25)
    g.render()
    g.arrow(0, 0, 1, 2)
    g.arrow(0, 0, 4, 4, 'red')
    g.arrow(0, 0, 3, 2)
    g.save('test.png')
