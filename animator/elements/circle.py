from animator.elements.drawable import Drawable

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
        self._opacity = extras.get('opacity', 1)

    def render(self):
        """
        Return image object corresponding to the attributes
        """
        pass

