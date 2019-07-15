from math import ceil


class Series:

    def __init__(self, start, end, scale=1):
        if scale == 0:
            raise ValueError("Scale cannot be 0")

        self._start = start
        self._end = end
        self._scale = scale

        self.standardized_range = (self._end - self._start) / self._scale
        self.points = self.calculate_points()
        self.full_scale_points = self.calculate_full_scale_points()

    def calculate_points(self):
        return ceil(self.standardized_range) + 1

    def calculate_full_scale_points(self):
        return int(self.standardized_range) + 1

    def get_point_wages(self):
        if self._start == self._end:
            return []
        wages = [w/self.standardized_range for w in range(self.full_scale_points)]
        if self.points-self.full_scale_points:
            wages += [1]
        return wages

    def change_range(self, start=None, end=None):
        if start:
            self._start = start
        if end:
            self._end = end
        self.points = self.calculate_points()
        self.full_scale_points = self.calculate_full_scale_points()

