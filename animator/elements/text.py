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

    def copy(self):
        return TextConfig(self.text, self.color, self.size, self.position, self.font)


class Text(Drawable):
    """
    Text Drawable class

    Attributes
    ----------
    _color : color of the text
    _text : the text to be rendered
    _size : the size of the text
    _wrapped_texts : wrapped texts objects of the given long text
    """
    def __init__(self, config=TextConfig(), wrapped_texts=None):
        if '\n' in config.text or '\r' in config.text:
            raise Exception("Please don't use newlines in text, instead use multiple texts")
        self._text = config.text
        self._color = config.color
        self._size = config.size
        self._position = config.position
        self._font = config.font
        self._wrapped_texts = wrapped_texts

    @classmethod
    def new(cls, config, width):
        """
        Returns wrapped Text object based on config and window width
        """
        org_conf = config.copy()
        OFFSET = 15  # line height offset
        xpos = config.position[0]
        font = ImageFont.truetype(config.font, config.size)
        size = font.getsize(config.text)
        lineheight = size[1]
        if xpos + size[0] > width:  # needs to be wrapped
            wrapped = []
            curr_pos = 0
            while True:
                pos = _get_next_wrap_index(config.text[curr_pos:], config, width, font)
                if pos is None:
                    wrapped.append(config.text[curr_pos:])
                    break
                wrapped.append(config.text[curr_pos:curr_pos+pos+1])
                curr_pos += pos + 1
            assert len(config.text) == len(''.join(wrapped))
            child_texts = []
            for i, x in enumerate(wrapped):
                ypos = config.position[1] + lineheight + OFFSET
                config.position = (xpos, ypos)
                config.text = x
                child_texts.append(Text(config))
            return Text(org_conf, wrapped_texts=child_texts)
        else:
            return Text(org_conf)

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
        # TODO: implement this
        return self.copy()

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
            if self._wrapped_texts:
                wrapped = []
                for x in self._wrapped_texts:
                    conf = x.get_config()
                    conf.color = color
                    wrapped.append(Text(conf))
                texts.append(wrapped)
            else:
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
            if self._wrapped_texts:
                wrapped = []
                for x in self._wrapped_texts:
                    conf = x.get_config()
                    conf.color = color
                    wrapped.append(Text(conf))
                texts.append(wrapped)
            else:
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
            if not self._wrapped_texts:
                conf = self.get_config()
                conf.text = self._text[:newlen]
                text_objs.append(Text(conf))
            else:
                wrapped_texts = []
                curr = newlen
                for i, x in enumerate(self._wrapped_texts):
                    xconf = x.get_config()
                    if curr <= len(xconf.text):
                        xconf.text =  xconf.text[:curr+1]
                        wrapped_texts = self._wrapped_texts[:i]
                        wrapped_texts.append(Text(xconf))
                        break
                    else:
                        curr = curr - len(xconf.text)
                text_objs.append(wrapped_texts)
        return text_objs

    def render_to(self, image):
        """
        Return Image object corresponding to the attributes.
        """
        # draw = ImageDraw.Draw(image)
        if not self._wrapped_texts:
            txt = Image.new('RGBA', image.size, (255,255,255,0))
            draw = ImageDraw.Draw(txt)
            if self._font:
                font = ImageFont.truetype(self._font, self._size)
                draw.text(self._position, self._text, fill=self._color, font=font)
            else:
                draw.text(self._position, self._text, self._color)
            img = Image.alpha_composite(image, txt)
            return img
        else:
            for x in self._wrapped_texts:
                img = x.render_to(image)
                image = Image.alpha_composite(image, img)
            return image


def _get_next_wrap_index(text, config, width, font):
    xpos = config.position[0]
    if not _exceeds_width(text, xpos, width, font):
        return None
    size = font.getsize(text)
    # find ratio of text width to width of image - starting position
    ratio = (width - xpos) / float(size[0])
    # approximate index of where to wrap
    approx_ind = int(ratio * len(text))
    # if approx_ind+1 < len(text) and text[approx_ind+1] == ' ':
    #     return approx_ind + 1
    # find a space before the index from where we might wrap text
    while True:
        space_pos = _previous_space_pos(approx_ind, text)
        if not _exceeds_width(text[:space_pos-1], xpos, width, font):
            return space_pos
        approx_ind = space_pos - 1


def _exceeds_width(text, xpos, width, font):
    size = font.getsize(text)
    return xpos + size[0] > width


def _previous_space_pos(curr_index, text):
    """
    Returns the next space ahead of current_index
    """
    if text[curr_index] == ' ':
        return curr_index
    for x in range(curr_index-1, -1, -1):
        if text[x] == ' ':
            return x
    # no space, return the same index
    return curr_index
