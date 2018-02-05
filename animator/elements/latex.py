from animator.elements.drawable import Drawable

from PIL import Image
import subprocess

DEFAULT_COLOR = (127, 255, 212, 255)
DEFAULT_POSITION = (100, 50)
DEFAULT_BACKGROUND = (0, 0, 0, 0)


class TEXConfig:
    """Attributes for tex"""
    def __init__(self,
            formula="",
            position=DEFAULT_POSITION,
            color=DEFAULT_COLOR,
            background=DEFAULT_BACKGROUND
            ):
        self.formula = formula
        self.position = position
        self.color = color
        self.background = background


class TEX(Drawable):
    """
    LaTex drawable class

    Attributes
    ----------
    _color: color of formula text
    _formula: the formula
    _position: position of the formula
    _background: background color
    """
    def __init__(self, config=TEXConfig(), image=None):
        self._color = config.color
        self._formula = config.formula
        self._position = config.position
        self._background = config.background
        self._image = image

    def get_config(self):
        conf = TEXConfig()
        conf.color = self._color
        conf.formula = self._formula
        conf.position = self._position
        conf.background = self._background
        return conf

    def render_to(self, image):
        if self._image:
            im = image.paste(self._image, self._position, self._image)
        else:
            img = self._create_image()
            self._image = img
            image.paste(img, self._position, img)
        return image

    def _create_image(self):
        """
        Create image using shell commands and tools
        """
        if self._image:
            return self._image
        try:
            command = "tex2im -b transparent -t cyan"
            subprocess.run([*command.split(), self._formula])
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return None
        # tex2im converts to out.png by default
        img = Image.open('out.png').convert('RGBA')
        subprocess.run(["rm", "out.png"])
        return img
