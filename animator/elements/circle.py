from animator.elements.drawable import Drawable
from PIL import Image, ImageDraw

DEFAULT_COLOR = (255, 0, 0, 255)
DEFAULT_RADIUS = 20
DEFAULT_CENTER = (0, 0)

class CircleConfig:
    def __init__(self):
        self.color = DEFAULT_COLOR
        self.radius = DEFAULT_RADIUS
        self.center = DEFAULT_CENTER
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
    def __init__(self, center, radius, extras={}):
        self._center = center
        self._radius = radius
        self._filled = extras.get('filled', False)
        self._color = extras.get('color', 'skyblue')
        self._stroke = extras.get('color', 'black')
        self._opacity = extras.get('opacity', 1)

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
        draw.ellipse(self.get_bounding_box(), fill=(200,200,0,255))
        return image

