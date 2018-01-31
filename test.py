from animator.animator import Animator, AnimatorConfig
from animator.elements import Circle

def test_animator():
    conf = AnimatorConfig()
    conf.duration = 1
    conf.fps = 1
    animator = Animator(conf)
    circle =  Circle((0,0), 10)
    circle2 =  Circle((50,50), 10)
    animator.add_frame_object(0, circle)  # set first frame
    animator.add_frame_object(0, circle2)  # add another circle
    animator.compile_frames()
    image = animator.get_compiled_frame(0)
    print(image)
    image.save('/tmp/temp.jpg')

if __name__ == '__main__':
    test_animator()
