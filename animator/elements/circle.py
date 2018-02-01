from animator.elements.drawable import Drawable
from PIL import ImageDraw

DEFAULT_COLOR = (255, 0, 0, 255)
DEFAULT_RADIUS = 20
DEFAULT_CENTER = (0, 0)


class CircleConfig:
    def __init__(
            self,
            center=DEFAULT_CENTER,
            radius=DEFAULT_RADIUS,
            color=DEFAULT_COLOR
            ):
        self.color = color
        self.radius = radius
        self.center = center
        self.filled = True


class Circle(Drawable):
    """
    Circle Drawable class

    Attributes
    ----------
    _center : tuple (x, y) giving the center of the circle
    _radius : radius of the circle
    _filled : if it is filled
    _color : color of the circle
    _opacity: opacity of the circle
    """
    def __init__(self, config):
        self._center = config.center
        self._radius = config.radius
        self._filled = config.filled
        self._color = config.color
        self._stroke = 1
        self._opacity = 1

    def get_bounding_box(self):
        return (
            self._center[0]-self._radius, self._center[1]-self._radius,
            self._center[0]+self._radius, self._center[1]+self._radius
        )

    def render_to(self, image):
        """
        Return image object corresponding to the attributes
        Parameters
        ----------
        image : a pillow Image object to which the circle is rendered
        """
        draw = ImageDraw.Draw(image)
        draw.ellipse(self.get_bounding_box(), fill=self._color)
        return image

    def copy(self):
        c = Circle(CircleConfig())
        c._center = self._center
        c._radius = self._radius
        c._filled = self._filled
        c._color = self._color
        return c

    def translate(self, vector, frames=1):
        """
        Return translated object/s
        Parameters
        ----------
        @vector : (x, y) is the vector which will translate the object
        @frames : if provided returns objects by interpolating positions in the frames
        """
        if frames <= 1:
            new = self.copy()
            new._center = (
                self._center[0]+vector[0],
                self._center[1]+vector[1]
            )
            return new
        else:
            inc_x = vector[0]/float(frames)
            inc_y = vector[1]/float(frames)
            circles = []
            curr_circle = self.copy()
            for x in range(frames):
                circles.append(curr_circle)
                curr_circle = curr_circle.translate((inc_x, inc_y))
            return circles
