from p5 import *
from cubeDraw import *
import giiker_engine as engine

scroll = 0
rot_x = 0
rot_y = 0
rot_z = 0

cube = CubeDef()
data_polling_rate = 10

def setup():  # one time settings
    size(800, 1200)
    no_stroke()
    engine.prime("BGAPI")
    engine.link_start()
    # engine.set_inst_callback(updater)
    # print("setup does its job")
    # engine.subscribe(18)
    # updater(state3D)


def draw():  # build a frame
    global rot_z
    global cube
    #drag()

    rot_z = scroll

    background(50)
    fill(20)

    if frame_count%((1/data_polling_rate)*100)==0:
        updater()

    # square((mouse_x, mouse_y), 4)

    cube.draw(x=width/2, y=height/2, rot_x=rot_x, rot_y=rot_y, rot_z=rot_z)  # , x=width/2, y=height/2)
    # square((0, 0, 200), 100, 'CENTER')

def updater():
    data = engine.read(18)
    engine.cube.intake(data)
    s3d = engine.cube.state3D
    cube.build(s3d)
    print("up")


def key_pressed():  # control the app.
    if key == 'ESC':
        engine.unsubscribe(18)
        engine.link_stop()
        engine.unprime()
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
