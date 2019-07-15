from math import ceil


class Series:

    def __init__(self, start, end, scale=1):
        if scale == 0:
            raise ValueError("Scale cannot be 0")

        self.start = start
        self.end = end
        self.scale = scale

        self.standardized_range = self.calculate_standardized_range()
        self.points = self.calculate_points()
        self.full_scale_points = self.calculate_full_scale_points()

    def calculate_points(self):
        return ceil(self.standardized_range) + 1

    def calculate_full_scale_points(self):
        return int(self.standardized_range) + 1

    def calculate_standardized_range(self):
        return (self.end - self.start) / self.scale

    def get_point_wages(self):
        if self.start == self.end:
            return []
        wages = [w/self.standardized_range for w in range(self.full_scale_points)]
        if self.points-self.full_scale_points:
            wages += [1]
        return wages

    def get_values(self):
        return [wage * (self.end-self.start) + self.start for wage in self.get_point_wages()]

    def change_range(self, start=None, end=None):
        if start:
            self.start = start
        if end:
            self.end = end
        self.standardized_range = self.calculate_standardized_range()
        self.points = self.calculate_points()
        self.full_scale_points = self.calculate_full_scale_points()
