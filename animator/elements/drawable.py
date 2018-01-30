class NotImplementedError(Exception):
    pass


class Drawable:
    """
    Drawable object that can be rendered in animation frame
    """
    def __init__(self):
        pass

    def render(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError
