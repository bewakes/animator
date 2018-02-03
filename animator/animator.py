from PIL import Image


DEFAULT_FPS = 30
DEFAULT_HEIGHT = 480
DEFAULT_WIDTH = 640
DEFAULT_DURATION = 10  # seconds
DEFAULT_BACKGROUND = (0, 0, 0, 255)


class AnimatorConfig:
    def __init__(
            self,
            width=DEFAULT_WIDTH,
            height=DEFAULT_HEIGHT,
            fps=DEFAULT_FPS,
            duration=DEFAULT_DURATION,
            background=DEFAULT_BACKGROUND
            ):
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.background = background


class Animator:
    """
    Main class for animation

    Attributes
    ----------
    _fps : frames per second
    _duration : duration of whole animation in seconds
    _raw_frames : list(slots) for frames containing list of drawables
    _compiled_frames : list(slots) for frames containing rendered/merged drawables
    _total_frames : total number of frames
    _height : height of each frame
    _width : width of each frame
    _background : background color
    """
    def __init__(self, config=AnimatorConfig()):
        self._config = config
        self._fps = config.fps
        self._height = config.height
        self._width = config.width
        self._duration = config.duration
        self._total_frames = self._duration * self._fps
        self._raw_frames = [[] for _ in range(self._total_frames)]
        self._compiled_frames = [None for _ in range(self._total_frames)]
        self._background = config.background

    @property
    def total_frames(self):
        return self._total_frames


    def add_frame_object(self, frame_index, drawable):
        """Add a drawable object to frame slot given by frame_index"""
        assert frame_index >= 0, "No negative indexing"
        assert frame_index < self._total_frames, "frames slot length exceeded"
        self._raw_frames[frame_index].append(drawable)

    def add_frames_objects(self, start_index, drawables):
        """Add drawable objects to multiple frames starting from start_index"""
        for i, drawable in enumerate(drawables):
            self.add_frame_object(start_index+i, drawable)

    def compile_frames(self):
        for ind, frame in enumerate(self._raw_frames):
            image = Image.new('RGBA', (self._width, self._height), self._background)
            for drawable in frame:
                image.paste(drawable.render_to(image))
            self._compiled_frames[ind] = image

    def get_compiled_frame(self, index):
        return self._compiled_frames[index]

    def get_compiled_frames(self):
        return self._compiled_frames
