from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle, CircleConfig

def test_animator():
    conf = AnimatorConfig()
    conf.duration = 1
    conf.fps = 30
    animator = Animator(conf)
    circle =  Circle(CircleConfig())
    #animator.add_frame_object(0, circle)  # set first frame
    #animator.add_frame_object(0, circle.translate((30, 400)))  # add another circle
    translated_objects = circle.translate((100, 300), frames=animator.total_frames)
    animator.add_frames_objects(0, translated_objects)
    animator.compile_frames()
    images = animator.get_compiled_frames()
    for i, img in enumerate(images):
        img.save('/tmp/temp{}.jpg'.format(i))

if __name__ == '__main__':
    test_animator()
