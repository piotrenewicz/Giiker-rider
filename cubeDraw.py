from p5 import *
import time as t
import giiker_engine as engine

engine.cube.intake("1234567833333333123456789abc000031334143")
state3D = engine.cube.state3D


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

    def draw(self, x, y, z=0, rot_x=20, rot_y=20, rot_z=20):
        with push_matrix():
            translate(x, y, z)
            rotate_x(radians(rot_x))
            rotate_y(radians(rot_y))
            rotate_z(radians(rot_z))

            color_backup = renderer.fill_color
            self.Buff.set()
        reset_matrix()
        Zorder.order()
        Zorder.flush()
        renderer.fill_color = color_backup

    def build(self, s3D: engine.cube.state3D):
        self.Buff.cls()

        def _is_allowed(side: tuple):
            # self.sub_disable
            # self.sub_config
            #

            return True

        def _mid(mid_data: tuple):
            mid: engine.cube.Piece = mid_data[0]
            side = mid_data[1]
            if _is_allowed(side):
                self._draw_surface(mid.primary_side)


        def _edge(edge_data: tuple):
            edge: engine.cube.Edge = edge_data[0]
            side = edge_data[1]
            if _is_allowed(side):
                with push_matrix():
                    translate(self.tile_size + self.gap_size, 0, 0)
                    if edge.orientation == 0:
                        self._draw_edge(edge.primary_side, edge.secondary_side)
                    elif edge.orientation == 1:
                        self._draw_edge(edge.secondary_side, edge.primary_side)

        def _corner(corner_data: tuple):
            corner: engine.cube.Corner = corner_data[0]
            side = corner_data[1]
            if _is_allowed(side):
                with push_matrix():
                    translate(self.tile_size + self.gap_size, self.tile_size + self.gap_size)
                    if corner.orientation == 3:
                        self._draw_corner(corner.primary_side, corner.side_side, corner.top_side)  # MAIN SIDE TOP
                    elif corner.orientation == 2:
                        self._draw_corner(corner.top_side, corner.primary_side, corner.side_side)
                    elif corner.orientation == 1:
                        self._draw_corner(corner.side_side, corner.top_side, corner.primary_side)

        def _dual_edge(slice):
            with push_matrix():
                _edge(slice[2])
                rotate_z(RAD180)
                _edge(slice[0])

        def _pink_quad_edge(slice):
            with push_matrix():
                _dual_edge(slice[1, :])
                rotate_z(-RAD90)
                _dual_edge(slice[:, 1])

        def _red_quad_edge(slice):
            with push_matrix():
                _dual_edge(slice[1, ::-1])
                rotate_z(-RAD90)
                _dual_edge(slice[:, 1])

        def _blue_quad_corner(slice):
            with push_matrix():
                _corner(slice[0, 0])
                rotate_z(RAD90)
                _corner(slice[0, 2])
                rotate_z(RAD90)
                _corner(slice[2, 2])
                rotate_z(RAD90)
                _corner(slice[2, 0])

        def _green_quad_corner(slice):
            with push_matrix():
                _corner(slice[0, 2])
                rotate_z(RAD90)
                _corner(slice[0, 0])
                rotate_z(RAD90)
                _corner(slice[2, 0])
                rotate_z(RAD90)
                _corner(slice[2, 2])

        def cube():
            def frwd():
                translate(0, 0, self.tile_size + self.gap_size)

            def edgeside(slice):
                with push_matrix():
                    frwd()
                    _quad_edge(slice)

            def edgeadd(slice):
                with push_matrix():
                    frwd()
                    _dual_edge(slice)

            def cornside(slice):
                with push_matrix():
                    frwd()
                    _quad_corner(slice)

            def mid(specyfic):
                with push_matrix():
                    frwd()
                    _mid(specyfic)

            with push_matrix():
                with push_matrix():
                    frwd()
                    _mid(s3D[1, 2, 1])
                    _blue_quad_corner(s3D[:, 2, :])

                rotate_y(RAD90)
                with push_matrix():
                    frwd()
                    _mid(s3D[1, 1, 0])
                    _red_quad_edge(s3D[:, :, 0])

                rotate_y(RAD90)
                with push_matrix():
                    frwd()
                    _mid(s3D[1, 0, 1])
                    _green_quad_corner(s3D[:, 0, :])

                rotate_y(RAD90)
                with push_matrix():
                    frwd()
                    _mid(s3D[1, 1, 2])
                    _pink_quad_edge(s3D[:, :, 2])

                rotate_x(RAD90)
                mid(s3D[2, 1, 1])
                edgeadd(s3D[2, :, 1])

                rotate_x(RAD180)
                mid(s3D[0, 1, 1])
                edgeadd(s3D[0, :, 1])

        cube()

        # as a first step let's draw the whole cube, then add more features.

        #self._draw_corner("WHITE", "GREEN", "BLUE")


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

    color_region = dict()
    color_region["BLUE"] = Color(22.22142857, 99.814285, 173.4)
    color_region["YELLOW"] = Color(236.785714, 214.56428, 32.421428)
    color_region["RED"] = Color(255, 89.25, 34.242857)
    color_region["WHITE"] = Color(255, 255, 255)
    color_region["PINK"] = Color(253.5428571, 172.307142, 183.23571)
    color_region["GREEN"] = Color(106.0071428, 205.457142, 154.8214285)


    def set_color_region(self, name: str, value):
        if value is not Color:
            if value is tuple:
                value = Color(*value)

        if name in self.color_region:
            self.color_region[name] = value
        else:
            raise NameError("color_name must be one of: \n BLUE, YELLOW, RED, WHITE, PINK, GREEN")

    def get_color_region(self, name):
        if isinstance(name, int):
            name = engine.cube.const.SIDE[name]
        if name in self.color_region:
            return self.color_region[name]
        else:
            raise NameError("color_name must be one of: \n BLUE, YELLOW, RED, WHITE, PINK, GREEN")

    def _draw_surface(self, color1):
        with push_matrix():
            translate(0, 0, self.tile_size//2)
            fill(self.get_color_region(color1))
            self.Buff.add(square, ((0, 0), self.tile_size, 'CENTER'))
            # square((0, 0), self.tile_size, 'CENTER')

    def _draw_edge(self, color1, color2):
        with push_matrix():
            self._draw_surface(color1)
            rotate_y(RAD90)
            self._draw_surface(color2)

    def _draw_corner(self, color1, color2, color3):
        with push_matrix():
            self._draw_edge(color1, color2)
            rotate_x(-RAD90)
            self._draw_surface(color3)

    class Buff:
        stack = []

        @classmethod
        def add(cls, func, args):
            dest = renderer.transform_matrix
            col = renderer.fill_color
            cls.stack.append({"F": func, "A": args, "C": col, "M": dest})

        @classmethod
        def set(cls):
            for entry in cls.stack:
                func = entry["F"]
                args = entry["A"]
                col = entry["C"]
                dest = entry["M"]
                with push_matrix():
                    apply_matrix(dest)
                    Zorder.add(func, args, col)

        @classmethod
        def cls(cls):
            cls.stack = []
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
    def add(cls, func, args, color):
        dest = renderer.transform_matrix
        source = renderer.np.array([0, 0, 0, 1])
        result = dest.dot(source)
        realz = result[2]
        cls.stack.append({"F": func, "A": args, "C": color, "M": dest, "Z": realz})

    @classmethod
    def order(cls):
        temp = []

        def find_next_elem():
            lowest = 9999999999999999999
            lowest_id = 0
            for i, elem in enumerate(cls.stack):
                if lowest > elem["Z"]:
                    lowest = elem["Z"]
                    lowest_id = i
            return lowest_id

        while len(cls.stack) > 0:
            next = find_next_elem()
            temp.append(cls.stack[next])
            cls.stack.pop(next)
        cls.stack = temp

    @classmethod
    def flush(cls):
        for elem in cls.stack:
            with push_matrix():
                apply_matrix(elem["M"])
                args = elem["A"]
                func = elem["F"]
                color = elem["C"]
                renderer.fill_color = color
                func(*args)

        cls.stack = []