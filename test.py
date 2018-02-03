from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle, CircleConfig
from animator.elements import Text, TextConfig

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


    # add text
    font = "arial.ttf"
    text_conf = TextConfig(text="bibek",size=40,position=(200, 200), font=font)
    text = Text(text_conf)
    animator.add_frames_objects(0, text.fade_in(animator.total_frames))

    text_conf.position=(300, 300)
    text_conf.color = (50, 200, 0, 255)
    text_conf.text = "pandey"
    newtxt = Text(text_conf)
    animator.add_frames_objects(0, newtxt.fade_out(animator.total_frames))

    text_conf.position = (0, 50)
    text_conf.size = 30
    text_conf.text = "Trying to make a video maker of my own"
    rollertext = Text(text_conf)
    animator.add_frames_objects(0, rollertext.roll(animator.total_frames))

    animator.compile_frames()
    images = animator.get_compiled_frames()
    for i, img in enumerate(images):
        img.save('/tmp/temp{}.png'.format(i), subsampling=0, quality=50)

if __name__ == '__main__':
    test_animator()
