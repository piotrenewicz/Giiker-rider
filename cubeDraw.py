from p5 import *
import time as t
# import giiker_engine as engine

RAD90 = 1.5707963267948966
RAD180 = 3.141592653589793


class CubeDef:
    def __init__(self, _tile_size=100, _gap_size=10, _sub_disable=True):
        # sub_disable True-Can disable a face on it's own, False-Can enable a face on it's own
        self.tile_size = _tile_size
        self.gap_size = _gap_size
        self.sub_disable = _sub_disable
        self.sub_config = [True, True, True, True, True, True]

        # A boolean for each face.
        # faces are through 1-6
        # 1 - BLUE
        # 2 - YELLOW
        # 3 - RED
        # 4 - WHITE
        # 5 - PINK
        # 6 - GREEN

    # animation support will require being able to turn faces of the cube on and of
    # the best way to do this is to define a variable keeping what faces are active
    # and then toggle pieces properly.

    # also there needs to be a check if this system is to be used for disabling or enabling pieces of cube.

    def build(self):
        # as a first step let's draw the whole cube, then add more features.

        self._draw_corner("WHITE", "GREEN", "BLUE")


        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        # self._draw_corner("WHITE", "WHITE", "WHITE")
        #
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        # self._draw_edge("WHITE", "WHITE")
        #
        # self._draw_surface("WHITE")
        # self._draw_surface("WHITE")
        # self._draw_surface("WHITE")
        # self._draw_surface("WHITE")
        # self._draw_surface("WHITE")


        #




    def draw(self):
        color_backup = renderer.fill_color
        Zorder.order()
        Zorder.flush()

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

    def _draw_surface(self, color1="WHITE"):
        with push_matrix():
            translate(0, 0, self.tile_size//2)
            Zorder.add(square, ((0, 0), self.tile_size, 'CENTER'), (0, 0, 0), self.get_color_region(color1))
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

# def box(size=100):
#     def _box_side():
#         with push_matrix():
#             translate(0, 0, size//2)
#             square((0, 0), size, 'CENTER')
#         with push_matrix():
#             translate(0, 0, -size//2)
#             square((0, 0), size, 'CENTER')
#
#     with push_matrix():
#         _box_side()
#         rotate_x(RAD90)
#         _box_side()
#         rotate_y(RAD90)
#         _box_side()


class Zorder:
    stack = []

    @classmethod
    def add(cls, func, args, coords: tuple, color):
        with push_matrix():
            translate(*coords)

            dest = renderer.transform_matrix
            source = renderer.np.array([0, 0, 0, 1])
            result = dest.dot(source)
            realz = result[2]
            Zorder.stack.append({"F": func, "A": args, "C": color, "M": dest, "Z": realz})

    @classmethod
    def order(cls):
        temp = []

        def find_next_elem():
            lowest = 9999999999999999999
            lowest_id = 0
            for i, elem in enumerate(Zorder.stack):
                if lowest > elem["Z"]:
                    lowest = elem["Z"]
                    lowest_id = i
            return lowest_id

        while len(Zorder.stack) > 0:
            next = find_next_elem()
            temp.append(Zorder.stack[next])
            Zorder.stack.pop(next)
        Zorder.stack = temp

    @classmethod
    def flush(cls):
        for elem in Zorder.stack:
            with push_matrix():
                apply_matrix(elem["M"])
                args = elem["A"]
                func = elem["F"]
                color = elem["C"]
                fill(color)
                func(*args)

        Zorder.stack = []