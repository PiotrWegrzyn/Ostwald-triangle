from math import cos, radians, sin


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index):
        return tuple(self)[index]

    @staticmethod
    def distance(p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return (dx ** 2 + dy ** 2) ** 0.5

    @staticmethod
    def rotate(point, angle):
        rotated_x = cos(radians(angle)) * point[0] - sin(radians(angle)) * point[1]
        rotated_y = sin(radians(angle)) * point[0] + cos(radians(angle)) * point[1]
        return Point(rotated_x, rotated_y)
