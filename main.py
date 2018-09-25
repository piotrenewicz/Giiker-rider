from p5 import *
from cubeDraw import *

scroll = 0
rot_x = 0
rot_y = 0
rot_z = 0

cube = CubeDef()

def setup():  # one time settings
    size(800, 1200)
    no_stroke()


def draw():  # build a frame
    global rot_z
    global cube
    #drag()
    rot_z = scroll

    background(50)
    fill(20)
    square((mouse_x, mouse_y), 4)
    rotate_x(radians(rot_x))
    rotate_y(radians(rot_y))
    rotate_z(radians(rot_z))
    cube.build()

    reset_matrix()
    translate(width/2, height/2)
    cube.draw()
    #square((0, 0, 200), 100, 'CENTER')


def key_pressed():  # control the app.
    if key == 'ESC':
        exit()


# cleanup time


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
