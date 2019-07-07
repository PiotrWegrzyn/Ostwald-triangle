import unittest
from math import atan, degrees

from geometry.linesegment import LineSegment
from geometry.point import Point


class TestLineClass(unittest.TestCase):

    def test_equality_correct_data(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line1 = LineSegment(a, b)
        line2 = LineSegment(a, b)
        self.assertEqual(line1, line2)

    def test_equality_incorrect_data(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line1 = LineSegment(a, b)
        c = Point(1, 1)
        line2 = LineSegment(a, c)
        self.assertNotEqual(line1, line2)

    def test_init_with_points(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line = LineSegment(a, b)
        self.assertEqual(line.start.x, 0)
        self.assertEqual(line.start.y, 0)
        self.assertEqual(line.end.x, 3)
        self.assertEqual(line.end.y, 4)

    def test_init_with_integers(self):
        line = LineSegment(0, 0, 3, 4)
        self.assertEqual(line.start.x, 0)
        self.assertEqual(line.start.y, 0)
        self.assertEqual(line.end.x, 3)
        self.assertEqual(line.end.y, 4)

    def test_init_with_angle(self):
        line = LineSegment(Point(0, 0), degrees(atan(4 / 3)), 5)
        self.assertEqual(0, line.start.x)
        self.assertEqual(0, line.start.y)
        self.assertEqual(3.0000000000000004, line.end.x)
        self.assertEqual(3.9999999999999996, line.end.y)

    def test_length_calculation(self):
        a = Point(0, 0)
        b = Point(3, 4)
        line = LineSegment(a, b)
        self.assertEqual(line.length, 5)

    def test_equally_split_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        points = line.get_split_points(3)

        self.assertEqual(points, [a, Point(0, 5), b])

    def test_proportions_split_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        points = line.get_split_points(3, [0, 0.4, 1])
        self.assertEqual(points, [a, Point(0, 4), b])

    def test_equally_split_points_with_less_than_2_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        with self.assertRaises(ValueError):
            line.get_split_points(0)

    def test_equally_split_points_with_division_by_0(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        with self.assertRaises(ValueError):
            line.get_split_points(1)

    def test_get_middle(self):
        a = Point(0, 0)
        b = Point(10, 10)
        line = LineSegment(a, b)
        middle = line.get_middle()
        self.assertEqual(Point(5, 5), middle)

    def test_split_correct_amount_of_lines(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        desired_amount_of_lines = 4
        split_lines = line.split(desired_amount_of_lines)
        self.assertEqual(desired_amount_of_lines, len(split_lines))

    def test_split_correct_point_coords(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        desired_amount_of_lines = 4
        split_lines = line.split(desired_amount_of_lines)
        self.assertEqual(LineSegment(Point(0, 2.5), Point(0, 5)), split_lines[1])

    def test_split_proportions(self):
        a = Point(0, 0)
        b = Point(0, 10)
        line = LineSegment(a, b)
        desired_amount_of_lines = 4
        split_lines = line.split(desired_amount_of_lines, [6,2,1,1])
        self.assertEqual(LineSegment(Point(0, 8), Point(0, 9)), split_lines[2])

    def test_split_less_than_1(self):
        a = Point(0, 0)
        b = Point(10, 10)
        line = LineSegment(a, b)
        with self.assertRaises(ValueError):
            line.split(0)

    def test_reverse(self):
        a = Point(0, 0)
        b = Point(10, 10)
        line = LineSegment(a, b)
        line_reversed = LineSegment(b, a)
        self.assertEqual(line_reversed, line.reversed())


if __name__ == '__main__':
    unittest.main()
