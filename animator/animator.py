from PIL import Image
import subprocess
import os

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
    _audio_path : path of audio
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
        self._video_config = {
            # for ffmpeg to take shortest  of images and audio into video
            'shortest': True
        }
        self._audio_path = None

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
                if type(drawable) != list:
                    image.paste(drawable.render_to(image))
                else:
                    for x in drawable:
                        image.paste(x.render_to(image))
            self._compiled_frames[ind] = image

    def get_compiled_frame(self, index):
        return self._compiled_frames[index]

    def get_compiled_frames(self):
        return self._compiled_frames

    def add_audio(self, audiopath):
        self._audio_path = audiopath

    def convert_to_video(self, video_path=None):
        """
        This should be in .mp4 format
        """
        if not self._compiled_frames:
            raise Exception("You have not compiled frames. Please call compile_frames() first")

        if not video_path:
            raise Exception("Please provide video path with name, only mp4 videos will be generated")
        path_splitted = video_path.split('/')
        if len(path_splitted) == 1:  # its just the name
            path = path_splitted[0].split('.')[0]  # just take name w/o extension
        else:
            if not path_splitted[-1]:  # check if name is provided
                raise Exception("Please provide video path with name, only mp4 videos will be generated")
            path = '/'.join(path_splitted[:-1]) + '/' + path_splitted[-1].split('.')[0]
        path = path + '.mp4'
        # ffmpeg to the rescue
        for i, frame in enumerate(self.get_compiled_frames()):
            frame.save('/tmp/frame{}.png'.format(i), subsampling=0, quality=50)
        ffmpeg_command = "ffmpeg -r {fps} -s {width}x{height} -i /tmp/frame%d.png {audio_input} -shortest -crf 20 -b 4M -c:v h264 {video_path}"
        if self._audio_path:
            audio_input = "-i " + self._audio_path.replace(' ', '@#@#')
        else:
            audio_input = ''
        command = ffmpeg_command.format(
            fps=self._fps,
            width=self._width,
            height=self._height,
            audio_input=audio_input,
            video_path=path
        )
        try:
            command = command.split()
            command = list(map(lambda x: x.replace('@#@#', ' '), command))
            print(command)
            subprocess.run(command)
        except Exception as e:
            print("Something went wrong." + e)
        else:
            # delete files
            files = os.listdir('/tmp/')
            for f in files:
                if f.endswith(".png"):
                    os.remove(os.path.join('/tmp', f))
            # subprocess.run(["rm", "/tmp/frame*.png"], shell=True)
        print("Converted video")
