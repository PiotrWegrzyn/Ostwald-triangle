from geometry import Point


class Vector:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.dx = self.end.x - self.start.x
        self.dy = self.end.y - self.start.y
        self.length = Point.distance(start, end)
