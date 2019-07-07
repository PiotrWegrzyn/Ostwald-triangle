import unittest
from math import atan, degrees

from geometry.vector import Vector
from geometry.point import Point


class TestVectorClass(unittest.TestCase):

    def test_equality_correct_data(self):
        a = Point(0, 0)
        b = Point(3, 4)
        vector1 = Vector(a, b)
        vector2 = Vector(a, b)
        self.assertEqual(vector1, vector2)

    def test_equality_incorrect_data(self):
        a = Point(0, 0)
        b = Point(3, 4)
        vector1 = Vector(a, b)
        c = Point(1, 1)
        vector2 = Vector(a, c)
        self.assertNotEqual(vector1, vector2)

    def test_init_with_points(self):
        a = Point(0, 0)
        b = Point(3, 4)
        vector = Vector(a, b)
        self.assertEqual(vector.start.x, 0)
        self.assertEqual(vector.start.y, 0)
        self.assertEqual(vector.end.x, 3)
        self.assertEqual(vector.end.y, 4)

    def test_init_with_integers(self):
        vector = Vector(0, 0, 3, 4)
        self.assertEqual(vector.start.x, 0)
        self.assertEqual(vector.start.y, 0)
        self.assertEqual(vector.end.x, 3)
        self.assertEqual(vector.end.y, 4)

    def test_init_with_angle(self):
        vector = Vector(Point(0, 0), degrees(atan(4 / 3)), 5)
        self.assertEqual(0, vector.start.x)
        self.assertEqual(0, vector.start.y)
        self.assertEqual(3.0000000000000004, vector.end.x)
        self.assertEqual(3.9999999999999996, vector.end.y)

    def test_length_calculation(self):
        a = Point(0, 0)
        b = Point(3, 4)
        vector = Vector(a, b)
        self.assertEqual(vector.length, 5)

    def test_equally_split_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        points = vector.get_split_points(3)

        self.assertEqual(points, [a, Point(0, 5), b])

    def test_proportions_split_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        points = vector.get_split_points(3, [0, 0.4, 1])
        self.assertEqual(points, [a, Point(0, 4), b])

    def test_equally_split_points_with_less_than_2_points(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        with self.assertRaises(ValueError):
            vector.get_split_points(0)

    def test_equally_split_points_with_division_by_0(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        with self.assertRaises(ValueError):
            vector.get_split_points(1)

    def test_get_middle(self):
        a = Point(0, 0)
        b = Point(10, 10)
        vector = Vector(a, b)
        middle = vector.get_middle()
        self.assertEqual(Point(5, 5), middle)

    def test_split_correct_amount_of_vectors(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        desired_amount_of_vectors = 4
        split_vectors = vector.split(desired_amount_of_vectors)
        self.assertEqual(desired_amount_of_vectors, len(split_vectors))

    def test_split_correct_point_coords(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        desired_amount_of_vectors = 4
        split_vectors = vector.split(desired_amount_of_vectors)
        self.assertEqual(Vector(Point(0, 2.5), Point(0, 5)), split_vectors[1])

    def test_split_proportions(self):
        a = Point(0, 0)
        b = Point(0, 10)
        vector = Vector(a, b)
        desired_amount_of_vectors = 4
        split_vectors = vector.split(desired_amount_of_vectors, [6,2,1,1])
        self.assertEqual(Vector(Point(0, 8), Point(0, 9)), split_vectors[2])

    def test_split_less_than_1(self):
        a = Point(0, 0)
        b = Point(10, 10)
        vector = Vector(a, b)
        with self.assertRaises(ValueError):
            vector.split(0)

    def test_reverse(self):
        a = Point(0, 0)
        b = Point(10, 10)
        vector = Vector(a, b)
        vector_reversed = Vector(b, a)
        self.assertEqual(vector_reversed, vector.reversed())

    def test_connect(self):
        a = Point(0, 0)
        b = Point(10, 10)
        c = Point(20, 0)
        vector1 = Vector(a, b)
        vector2 = Vector(b, c)
        self.assertEqual(vector_reversed, vector.reversed())


if __name__ == '__main__':
    unittest.main()
