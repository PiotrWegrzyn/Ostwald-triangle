from geometry.point import Point
from math import cos, sin, radians


class Line:
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
        self.calculate_length()

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
        rad = radians(args[1])
        length = args[2]
        self.end = Point(self.start.x + length * cos(rad), self.start.y + length * sin(rad))

    def __init_from_4_numbers(self, args):
        self.start = Point(args[0], args[1])
        self.end = Point(args[2], args[3])

    def calculate_length(self):
        self.dx = self.end.x - self.start.x
        self.dy = self.end.y - self.start.y
        self.length = (self.dx ** 2 + self.dy ** 2) ** 0.5

    def get_equally_split_points(self, number_of_points):
        if number_of_points < 2:
            raise ValueError("Minimum 2 points required")
        list_of_points = []
        for i in range(number_of_points):
            list_of_points.append(
                Point(
                    self.start.x + (self.dx / (number_of_points-1)) * i,
                    self.start.y + (self.dy / (number_of_points-1)) * i
                )
            )
        return list_of_points

