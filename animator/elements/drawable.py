from copy import copy

class NotImplementedError(Exception):
    pass


class Drawable:
    """
    Drawable object that can be rendered in animation frame
    """
    def __init__(self):
        pass

    def render_to(self, image):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def copy(self):
        raise NotImplementedError

    def translate(self, vector, frames=1):
        """vector is a tuple (x, y)"""
        raise NotImplementedError

    def get_config(self):
        """Get the config"""
        raise NotImplementedError

