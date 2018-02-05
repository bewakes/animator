from animator.elements.drawable import Drawable

from PIL import Image
import subprocess

DEFAULT_COLOR = (127, 255, 212, 255)
DEFAULT_POSITION = (100, 50)
DEFAULT_BACKGROUND = (0, 0, 0, 0)
DEFAULT_ALPHA = 1


class TEXConfig:
    """Attributes for tex"""
    def __init__(self,
            formula="",
            position=DEFAULT_POSITION,
            color=DEFAULT_COLOR,
            background=DEFAULT_BACKGROUND,
            alpha=DEFAULT_ALPHA
            ):
        self.formula = formula
        self.position = position
        self.color = color
        self.background = background
        self.alpha = alpha


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
        self._alpha =  config.alpha
        self._image = image

    def get_config(self):
        conf = TEXConfig()
        conf.color = self._color
        conf.formula = self._formula
        conf.position = self._position
        conf.alpha = self._alpha
        conf.background = self._background
        return conf

    def fade_in(self, frames=2, start_opacity=0, final_opacity=1):
        """
        fade in from start_opacity to final_opacity
        """
        assert start_opacity < final_opacity
        increment = (final_opacity - start_opacity) / float(frames)
        alphas = [start_opacity + f*increment for f in range(frames)]
        conf = self.get_config()
        texobjs = []
        for alpha in alphas:
            conf.alpha = alpha
            texobjs.append(TEX(conf, self._image))
        return texobjs

    def fade_out(self, frames=2, start_opacity=1, final_opacity=0):
        """
        fade out from start_opacity to final_opacity
        """
        assert start_opacity > final_opacity
        increment = (final_opacity - start_opacity) / float(frames)
        alphas = [start_opacity + f*increment for f in range(frames)]
        conf = self.get_config()
        texobjs = []
        for alpha in alphas:
            conf.alpha = alpha
            texobjs.append(TEX(conf, self._image))
        return texobjs

    def render_to(self, image):
        if self._image:
            image.paste(self._image, self._position, self._image)
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
        size = img.size
        # create a new rgba image to blend the latex with the alpha
        image = Image.new('RGBA', size)
        newim = Image.blend(image, img, self._alpha)
        subprocess.run(["rm", "out.png"])
        return newim
