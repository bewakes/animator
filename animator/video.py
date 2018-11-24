import skvideo
import skvideo.io
import numpy
from PIL import Image


class Video:
    """
    Video class to manipulate video
    """
    def __init__(self, video):
        """
        @video: skvideo.io.FFmpegReader() object
        """
        self.video = video
        self.num_frames, self.height, self.width, self.num_channels = \
            video.getShape()
        self.frames = [
            numpy.array(Image.fromarray(frame).convert('RGBA'))
            for frame in video.nextFrame()
        ]
        self.fps = video.inputfps

    @classmethod
    def from_file(cls, filepath):
        return cls(skvideo.io.FFmpegReader(filepath))

    def get_frame(self, frame_index):
        return self.frames[frame_index]

    def add_text(self, text=None, start_frame=0, num_frames=10):
        frames = self.frames[start_frame:start_frame+num_frames]
        newframes = []
        for frame in frames:
            img = Image.fromarray(frame, 'RGBA')
            newimg = text.render_to(img)
            newframes.append(numpy.array(newimg))
        self.frames = self.frames[:start_frame] +\
            newframes + self.frames[start_frame+num_frames:]

    def write_output_video(self, path):
        vid_out = skvideo.io.FFmpegWriter(
            path,
            inputdict={
                '-r': str(self.fps),
            },
            outputdict={
                '-vcodec': 'libx264',
                '-pix_fmt': 'yuv420p',
                '-r': str(self.fps),
            }
        )
        for frame in self.frames:
            vid_out.writeFrame(frame)
        vid_out.close()


if __name__ == '__main__':
    v = Video.from_file('/home/bibek/corrupted_video.mp4')
    # print(dir(v.video))
