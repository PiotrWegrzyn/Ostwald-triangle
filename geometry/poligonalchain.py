from geometry import Point
from geometry.lineinferface import LineInterface


class PolygonalChain(LineInterface):
    def __init__(self, list_of_vectors):
        self.vectors = list_of_vectors
        self.vectors_count = len(list_of_vectors)
        self.length = sum([v.length for v in self.vectors])
        self.dx = sum([v.dx for v in self.vectors])
        self.dy = sum([v.dy for v in self.vectors])
        try:
            self.start = list_of_vectors[0].start
            self.end = list_of_vectors[-1].end
        except IndexError:
            self.start = None
            self.end = None

    def get_split_points(self, number_of_points, proportions=None):
        if number_of_points < 2 and not proportions:
            raise ValueError("Minimum 2 points required")
        if proportions and (len(proportions) is not number_of_points):
            raise ValueError("Wrong amount of proportions")
        if proportions and sum([1 for p in proportions if p > 1]):
            raise ValueError("Proportion cannot be bigger than 1")
        list_of_points = []
        distance_between_points = self.length/(number_of_points-1) # at least 2
        current_line_index = 0
        for i in range(number_of_points):
            if proportions:
                current_distance = self.length * proportions[i]
            else:
                current_distance = distance_between_points * i
            while current_distance > self.len_before_vector(current_line_index+1):
                current_line_index += 1
            prop = (current_distance - self.len_before_vector(current_line_index))/self.vectors[current_line_index].length
            list_of_points.append(self.vectors[current_line_index].get_split_points(1, proportions=[prop])[0])
        return list_of_points

    def len_before_vector(self, vector_index):
        return sum(self.vectors[v].length for v in range(vector_index))

    def get_center(self):
        return Point(self.start.x + self.dx/2, self.start.y + self.dx/2)
