from geometry.lineinferface import LineInterface
from geometry.point import Point
from math import cos, sin, radians


class Vector(LineInterface):
    start = None
    end = None

    def __init__(self, *args):
        if len(args) is 2:
            self.__init_from_2_points(args)
        elif len(args) is 3:
            self.__init_from_point_angle_length(args)
        elif len(args) is 4:
            self.__init_from_4_numbers(args)
        else:
            raise ValueError("Requires 2 Points or 4 Integers or Point, angle, length as arguments.")

        self.dx = self.end.x - self.start.x
        self.dy = self.end.y - self.start.y
        self.length = Point.distance(self.start, self.end)

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end

    def __init_from_2_points(self, args):
        if isinstance(args[0], Point) and isinstance(args[1], Point):
            self.start = args[0]
            self.end = args[1]
        else:
            raise ValueError("Requires 2 Points as arguments.")

    def __init_from_point_angle_length(self, args):
        if not isinstance(args[0], Point):
            raise ValueError("Requires the 1st argument to be a Point.")
        if not isinstance(args[1], (int, float)):
            raise ValueError("Requires the 2nd argument to be a number.")
        if not isinstance(args[2], (int, float)):
            raise ValueError("Requires the 3rd argument to be a number.")
        self.start = args[0]
        self.angle = args[1]
        self.rad = radians(args[1])
        length = args[2]
        self.end = Point(self.start.x + length * cos(self.rad), self.start.y + length * sin(self.rad))

    def __init_from_4_numbers(self, args):
        self.start = Point(args[0], args[1])
        self.end = Point(args[2], args[3])

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

    def get_geometric_center(self):
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

    def _convert_to_point_proportions(self, proportions):
        point_proportions = [0]
        total = sum(proportions)
        pivot = 0
        for prop in proportions:
            pivot += prop
            point_proportions.append(pivot / total)
        return point_proportions

