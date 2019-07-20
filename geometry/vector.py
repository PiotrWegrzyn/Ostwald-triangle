import math
from math import cos, sin, radians, atan2, degrees, acos

from geometry.lineinferface import LineInterface
from geometry.point import Point


class Vector(LineInterface):
    _start = None
    _end = None
    dx = 0
    dy = 0
    slope = None
    angle = 0

    def __init__(self, *args):
        if len(args) is 2:
            self.__init_from_2_points(args)
        elif len(args) is 3:
            self.__init_from_point_angle_length(args)
        elif len(args) is 4:
            self.__init_from_4_numbers(args)
        else:
            raise ValueError("Requires 2 Points or 4 Integers or Point, angle, length as arguments.")

        self.calculate_properties()

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, point):
        if not isinstance(point, Point):
            raise ValueError("Start has to be a Point.")
        self._start = point
        self.calculate_properties()

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, point):
        if not isinstance(point, Point):
            raise ValueError("Start has to be a Point.")
        self._end = point
        self.calculate_properties()

    def __init_from_2_points(self, args):
        if isinstance(args[0], Point) and isinstance(args[1], Point):
            self._start = args[0]
            self._end = args[1]
        else:
            raise ValueError("Requires 2 Points as arguments.")

    def __init_from_point_angle_length(self, args):
        if not isinstance(args[0], Point):
            raise ValueError("Requires the 1st argument to be a Point.")
        if not isinstance(args[1], (int, float)):
            raise ValueError("Requires the 2nd argument to be a number.")
        if not isinstance(args[2], (int, float)):
            raise ValueError("Requires the 3rd argument to be a number.")
        self._start = args[0]
        self.angle = args[1]
        self.rad = radians(args[1])
        length = args[2]
        self._end = Point(self.start.x + length * cos(self.rad), self.start.y + length * sin(self.rad))

    def __init_from_4_numbers(self, args):
        self._start = Point(args[0], args[1])
        self._end = Point(args[2], args[3])

    def get_split_points(self, number_of_points, proportions=None):
        if number_of_points < 2 and not proportions:
            raise ValueError("Minimum 2 points required")
        if proportions and (len(proportions) is not number_of_points):
            raise ValueError("Wrong amount of proportions")
        list_of_points = []
        for i in range(number_of_points):
            if proportions:
                change_x = self.dx * proportions[i]
                change_y = self.dy * proportions[i]
            else:
                change_x = self.dx / (number_of_points - 1) * i
                change_y = self.dy / (number_of_points - 1) * i
            list_of_points.append(
                Point(
                    self.start.x + change_x,
                    self.start.y + change_y
                )
            )
        return list_of_points

    def get_center(self):
        return Point(self.start.x + self.dx/2, self.start.y + self.dx/2)

    def split(self, number_of_lines, proportions=None):
        if number_of_lines < 1:
            raise ValueError("Minimum 1 line required")
        if proportions:
            proportions = self._convert_to_point_proportions(proportions)
        points = self.get_split_points(number_of_lines + 1, proportions)
        return [Vector(points[i], points[i + 1]) for i in range(number_of_lines)]

    def reversed(self):
        return Vector(self.end, self.start)

    @staticmethod
    def _convert_to_point_proportions(proportions):
        point_proportions = [0]
        total = sum(proportions)
        pivot = 0
        for prop in proportions:
            pivot += prop
            point_proportions.append(pivot / total)
        return point_proportions

    @staticmethod
    def dot_product(v1, v2):
        return (v1.dx * v2.dx) + (v1.dy * v2.dy)

    @staticmethod
    def angle_between(v1, v2):
        return degrees(acos(Vector.dot_product(v1, v2) / (v1.length * v2.length)))

    def calculate_properties(self):
        self.dx = self.end.x - self.start.x
        self.dy = self.end.y - self.start.y
        try:
            self.slope = self.dy/self.dx
        except ZeroDivisionError:
            self.slope = None
        self.angle = degrees(atan2(self.dy, self.dx))
        self.length = Point.distance(self.start, self.end)

    @staticmethod
    def contains_point(vector, point):
        return math.isclose(
            vector.length,
            Vector(vector.start, point).length + Vector(vector.end, point).length,
            rel_tol=1e-5
        )

    @staticmethod
    def intersection(v1, v2):
        part1 = v1.start.x * v1.end.y - v1.start.y * v1.end.x
        part2 = v2.start.x * v2.end.y - v2.start.y * v2.end.x
        divisor = v1.dx * v2.dy - v1.dy * v2.dx

        def formula(dv1, dv2):
            return (part1 * dv2 - dv1 * part2) / divisor
        try:
            x = formula(-v1.dx, -v2.dx)
            y = formula(-v1.dy, -v2.dy)
            p = Point(x, y)
            if Vector.contains_point(v1, p):
                return p
            else:
                return None
        except ZeroDivisionError:
            return None

