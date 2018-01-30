#############
# PSEUDOCODE
#############

configuration = {
    'height': 123,
    'width': 123,
    'fps': 30,
    'background': 'black',
    'time': 30 # seconds
}
animator = Animator(configuration)
#
# Animator has one of the attributes: 
#       _frames_slot = [[drawables ...], ...]
# The drawables will be drawn and merged/pasted into the specific frame they belong to
#  after calling animator.compile_frames()
#
print(animator.total_frames) # calculated by time and fps
circle = elements.Circle(config) # config = {'r': 12, 'x': 12 ...}

# Frame is a private class inside Animator module, basically wraps Image with some other parameters like frame number
first_frame = animator.new_frame() # initialize with empty blank image, can't change width/height attributes
first_frame.set_image(circle.translate(10, 10)) # doesn't render yet, only after compiling

animator.add_frame_object(1, first_frame)

# translate, starting from from_pos to to_pos, with trail_settings
trail_settings = {
    'skip_frames': 0, # num of trail frames to skip, default 0
    'opacity': 0.5,
    'color': 'blue', # trail color
}
# num frames: number of frames to interpolate the translation
num_frames = animator.total_frames - 1 # all frames except the first frame

frames_array = circle.translate_trailing(from_pos, to_pos, num_frames, trail_settings)
animator.add_frames(2, frames_array) # begin frames from frame number 2
# equivalent to : for ind, frame in enumerate(frames_array): animator.add_frame(ind+2, frame)

rect = elements.Rectangle(config) # config = {"width": 100, "height": 234}
rect_frames_array = rect.rotate_cycle(direction, animator.total_frames)
animator.add_frames(1, rect_frames_array)

animator.compile_frames() # merge rectangle and circle frames

animator.add_audio(audiofile) # future, enhancement
animator.save('abc.gif') # save as gif
animator.save('abc.mp4') # save as abc.mp4
