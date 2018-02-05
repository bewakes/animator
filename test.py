from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle, CircleConfig
from animator.elements import Text, TextConfig
from animator.elements import TEX, TEXConfig

import math

def test_animator():
    conf = AnimatorConfig(duration=5, fps=30)
    animator = Animator(conf)

    # another circle(yellow)
    yellow_conf = CircleConfig(radius=10, color=(255,255,0,255), center=(100,20))
    yellow_circle = Circle(yellow_conf)
    yellow_translated = yellow_circle.translate((0, 200), frames=int(animator.total_frames/2))

    NUM_BOUNCES = 25
    bounce = 250
    ref_circle = yellow_circle
    for x in range(NUM_BOUNCES):
        yellow_translated = ref_circle.translate((bounce, 0), frames=int(animator.total_frames/NUM_BOUNCES))
        # bounce_back = yellow_translated[-1].translate((0, -200), frames=int(animator.total_frames/NUM_BOUNCES))
        animator.add_frames_objects(math.ceil(x*animator.total_frames/NUM_BOUNCES), yellow_translated)
        ref_circle = yellow_translated[-1]
        bounce *= -1

    # add text
    font = "arial.ttf"
    text_conf = TextConfig(text="bibek", size=40, position=(200, 200), font=font)

    text_conf.position = (50, 50)
    text_conf.color = (135, 206, 250, 255)
    text_conf.size = 30
    text_conf.text = "Hey, Wassup?? This video has been made by a tool created by me."
    rollertext = Text.new(text_conf, animator._width)
    # rollertext = Text(text_conf)
    # animator.add_frame_object(0, rollertext)
    animator.add_frames_objects(0, rollertext.roll(animator.total_frames))

    texconf = TEXConfig()
    texconf.formula = r"\frac{\lambda}{3.4}"
    tex = TEX(texconf)
    animator.add_frame_object(0, tex)

    animator.compile_frames()
    images = animator.get_compiled_frames()
    for i, img in enumerate(images[:1]):
        img.save('/tmp/temp{}.png'.format(i), subsampling=0, quality=50)

if __name__ == '__main__':
    test_animator()
