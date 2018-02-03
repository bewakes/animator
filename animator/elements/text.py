from animator.elements.drawable import Drawable
from PIL import ImageDraw, ImageFont, Image
import math

DEFAULT_COLOR = (0, 0, 255, 255)
DEFAULT_POSITION = (50, 0)
DEFAULT_SIZE = 20

class TextConfig:
    """Attributes for text"""
    def __init__(
            self,
            text="",
            color=DEFAULT_COLOR,
            size=DEFAULT_SIZE,
            position=DEFAULT_POSITION,
            font=None
            ):
        self.text = text
        self.color = color
        self.size = size
        self.position = position
        self.font = font


class Text(Drawable):
    """
    Text Drawable class

    Attributes
    ----------
    _color : color of the text
    _text : the text to be rendered
    _size : the size of the text
    """
    def __init__(self, config=TextConfig()):
        self._text = config.text
        self._color = config.color
        self._size = config.size
        self._position = config.position
        self._font = config.font

    def get_config(self):
        conf = TextConfig()
        conf.text = self._text
        conf.color = self._color
        conf.size = self._size
        conf.position = self._position
        conf.font = self._font
        return conf

    def copy(self):
        conf = self.get_config()
        return Text(conf)

    def translate(self, vector, frames=1):
        """
        @vector : (x, y) is translation vector
        @frames : if provided returns objects by interpolating
        """
        pass

    def fade_in(self, frames=2, start_opacity=0, final_opacity=1):
        """
        fade in from start_opacity to final_opacity
        """
        assert start_opacity < final_opacity
        increment = (final_opacity - start_opacity) / float(frames)
        rgb = self._color[:-1]
        colors = [(*rgb, int(255*(start_opacity + f*increment))) for f in range(frames)]
        texts = []
        for color in colors:
            conf = self.get_config()
            conf.color = color
            texts.append(Text(conf))
        return texts

    def fade_out(self, frames=2, start_opacity=1, final_opacity=0):
        """
        fade in from start_opacity to final_opacity
        """
        assert start_opacity > final_opacity
        increment = (start_opacity - final_opacity) / float(frames)
        rgb = self._color[:-1]
        colors = [(*rgb, int(255*(start_opacity - f*increment))) for f in range(frames)]
        texts = []
        for color in colors:
            conf = self.get_config()
            conf.color = color
            texts.append(Text(conf))
        return texts

    def roll(self, frames=2):
        """
        display text one char at a time
        """
        textlen = len(self._text)
        if not textlen:
            # do nothing, just return frames
            return [self]*frames
        chars_per_frame = textlen/float(frames)

        if chars_per_frame > 1:
            roundfunc = math.floor
        elif chars_per_frame < 1:
            roundfunc = math.ceil
        else:
            roundfunc = lambda x: x

        text_objs = []
        curr_size = 0
        for x in range(frames):
            curr_size += chars_per_frame
            newlen = roundfunc(curr_size)
            conf = self.get_config()
            conf.text = self._text[:newlen]
            text_objs.append(Text(conf))
        return text_objs

    def render_to(self, image):
        """
        Return Image object corresponding to the attributes.
        """
        # draw = ImageDraw.Draw(image)
        txt = Image.new('RGBA', image.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt)
        if self._font:
            font = ImageFont.truetype(self._font, self._size)
            draw.text(self._position, self._text, fill=self._color, font=font)
        else:
            draw.text(self._position, self._text, self._color)
        txt.convert("RGB")
        img = Image.alpha_composite(image, txt)
        return img
