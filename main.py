from p5 import *

scroll = 0
rot_x = 66
rot_y = 20
rot_z = 21
RAD90 = 1.5707963267948966
RAD180 = 3.141592653589793


def setup():  # one time settings
    size(800, 1200)


def draw():  # build a frame
    global rot_z
    #drag()
    rot_z = scroll

    background(50)
    fill(20)
    square((mouse_x, mouse_y), 4)
    translate(width/2, height/2)
    rotate_x(radians(rot_x))
    rotate_y(radians(rot_y))
    rotate_z(radians(rot_z))
    box()  # custom box


def box(size=100):
    def _box_side():
        with push_matrix():
            translate(0, 0, size//2)
            square((0, 0), size, 'CENTER')
        with push_matrix():
            translate(0, 0, -size//2)
            square((0, 0), size, 'CENTER')

    with push_matrix():
        _box_side()
        rotate_x(RAD90)
        _box_side()
        rotate_y(RAD90)
        _box_side()


def key_pressed():  # control the app.
    if key == 'ESC':
        exit()


def mouse_wheel(event):
    global scroll
    scroll += event.count


_pmouse_x = 0
_pmouse_y = 0


def mouse_moved(event):
    if mouse_is_pressed:
        global rot_x
        global rot_y
        global _pmouse_x
        global _pmouse_y
        rot_x += event.x - _pmouse_x
        rot_y += event.y - _pmouse_y
        _pmouse_x = event.x
        _pmouse_y = event.y


run()  # spawn the window
