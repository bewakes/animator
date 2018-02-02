from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle, CircleConfig

def test_animator():
    conf = AnimatorConfig(duration=2, fps=30)
    animator = Animator(conf)

    circ_conf = CircleConfig()
    circle = Circle(circ_conf)
    translated_objects = circle.translate((100, 300), frames=animator.total_frames)
    animator.add_frames_objects(0, translated_objects)

    # another circle(blue)
    blue_conf = CircleConfig(color=(0,0,255,255), center=(100,20))
    blue_circle = Circle(blue_conf)
    blue_translated = blue_circle.translate((400, 400), frames=animator.total_frames)
    animator.add_frames_objects(0, blue_translated)

    animator.compile_frames()
    images = animator.get_compiled_frames()
    for i, img in enumerate(images):
        img.save('/tmp/temp{}.jpg'.format(i), subsampling=0, quality=100)

if __name__ == '__main__':
    test_animator()
