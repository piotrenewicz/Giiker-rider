from p5 import *
import time as t
#import giiker_engine as engine

RAD90 = 1.5707963267948966
RAD180 = 3.141592653589793

class CubeDef:
    def __init__(self, _tile_size=100, _gap_size=10):
        self.tile_size = _tile_size
        self.gap_size = _gap_size

    def build(self):
        self._draw_corner("BLUE", "GREEN", "WHITE")

    def draw(self):
        color_backup = renderer.fill_color
        zorder_order()
        zorder_flush()


    color_region = dict()
    color_region["BLUE"] = Color(0, 0, 255)
    color_region["YELLOW"] = Color(255, 255, 0)
    color_region["RED"] = Color(255, 0, 0)
    color_region["WHITE"] = Color(255, 255, 255)
    color_region["PINK"] = Color(125, 100, 15)
    color_region["GREEN"] = Color(0, 255, 0)

    def set_color_region(self, name: str, value):
        if value is not Color:
            if value is tuple:
                value = Color(*value)

        if name in self.color_region:
            self.color_region[name] = value
        else:
            raise NameError("color_name must be one of: \n BLUE, YELLOW, RED, WHITE, PINK, GREEN")

    def get_color_region(self, name: str):
        if name in self.color_region:
            return self.color_region[name]
        else:
            raise NameError("color_name must be one of: \n BLUE, YELLOW, RED, WHITE, PINK, GREEN")

    def _draw_surface(self, color="WHITE"):
        with push_matrix():
            translate(0, 0, self.tile_size//2)
            zorder_add(square, ((0, 0), self.tile_size, 'CENTER'), (0, 0, 0), self.get_color_region(color))
            # square((0, 0), self.tile_size, 'CENTER')

    def _draw_edge(self, color1, color2):
        with push_matrix():
            self._draw_surface(color1)
            rotate_x(RAD90)
            self._draw_surface(color2)

    def _draw_corner(self, color1, color2, color3):
        with push_matrix():
            self._draw_edge(color1, color2)
            rotate_y(RAD90)
            self._draw_surface(color3)


#
# BLUE
# YELLOW
# RED
# WHITE
# PINK
# GREEN

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


zorder_list = []


def zorder_add(func, args, coords: tuple, color):
    global zorder_list
    with push_matrix():
        translate(*coords)

        dest = renderer.transform_matrix
        source = renderer.np.array([0, 0, 0, 1])
        result = dest.dot(source)
        realz = result[2]
        zorder_list.append({"F": func, "A": args, "C": color, "M": dest, "Z": realz})


def zorder_order():
    global zorder_list
    print(" \n\n")
    for entry in zorder_list:
        print(entry["Z"])
    print("============================")
    temp_list = []
    def find_lowest_z():
        lowest = 9999999999999999999
        lowest_id = 0
        for i, entry in enumerate(zorder_list):
            if lowest > entry["Z"]:
                lowest = entry["Z"]
                lowest_id = i
        return lowest_id
    while len(zorder_list) > 0:
        low = find_lowest_z()
        temp_list.append(zorder_list[low])
        zorder_list.pop(low)
    zorder_list = temp_list
    for entry in zorder_list:
        print(entry["Z"])
    t.sleep(0.2)

def zorder_flush():
    global zorder_list
    for entry in zorder_list:
        with push_matrix():
            apply_matrix(entry["M"])
            args = entry["A"]
            func = entry["F"]
            color = entry["C"]
            fill(color)
            func(*args)

    zorder_list = []