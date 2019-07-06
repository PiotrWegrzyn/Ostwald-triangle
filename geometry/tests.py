import unittest
from math import atan, degrees

from geometry.line import Line
from geometry.point import Point


class TestLineClass(unittest.TestCase):

    def test_init_with_points(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line = Line(a, b)
        self.assertEqual(line.start.x, 0)
        self.assertEqual(line.start.y, 0)
        self.assertEqual(line.end.x, 3)
        self.assertEqual(line.end.y, 4)

    def test_init_with_integers(self):
        line = Line(0, 0, 3, 4)
        self.assertEqual(line.start.x, 0)
        self.assertEqual(line.start.y, 0)
        self.assertEqual(line.end.x, 3)
        self.assertEqual(line.end.y, 4)

    def test_init_with_angle(self):
        line = Line(Point(0, 0), degrees(atan(4/3)), 5)
        self.assertEqual(0, line.start.x)
        self.assertEqual(0, line.start.y)
        self.assertEqual(3.0000000000000004, line.end.x)
        self.assertEqual(3.9999999999999996, line.end.y)

    def test_length_calculation(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line = Line(a, b)
        self.assertEqual(line.length, 5)

    def test_equally_split_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = Line(a, b)
        points = line.get_equally_split_points(3)
        points_x = [p.x for p in points]
        points_y = [p.y for p in points]
        self.assertEqual(points_x, [a.x, Point(0, 5).x, b.x])
        self.assertEqual(points_y, [a.y, Point(0, 5).y, b.y])

    def test_equally_split_points_with_less_than_2_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = Line(a, b)
        with self.assertRaises(ValueError):
            line.get_equally_split_points(0)

    def test_equally_split_points_with_division_by_0(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = Line(a, b)
        with self.assertRaises(ValueError):
            line.get_equally_split_points(1)


if __name__ == '__main__':
    unittest.main()
