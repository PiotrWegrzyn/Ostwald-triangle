class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def distance(p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return (dx ** 2 + dy ** 2) ** 0.5

