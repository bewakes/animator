from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle, CircleConfig

def test_animator():
    conf = AnimatorConfig()
    conf.duration = 1
    conf.fps = 30
    animator = Animator(conf)
    circ_conf = CircleConfig()
    circle = Circle(circ_conf)
    # animator.add_frame_object(0, circle)  # set first frame
    # animator.add_frame_object(0, circle.translate((30, 400)))  # add another circle
    translated_objects = circle.translate((100, 300), frames=animator.total_frames)
    animator.add_frames_objects(0, translated_objects)

    # another circle
    circ_conf.color = (0,0,255,255)
    circ_conf.center = (100, 20)
    blue = Circle(circ_conf)
    blue_translated = blue.translate((400, 400), frames=animator.total_frames)
    animator.add_frames_objects(0, blue_translated)

    animator.compile_frames()
    images = animator.get_compiled_frames()
    for i, img in enumerate(images):
        img.save('/tmp/temp{}.jpg'.format(i), subsampling=0, quality=100)

if __name__ == '__main__':
    test_animator()
