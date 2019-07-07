class PolygonalChain:
    def __init__(self, list_of_vectors):
        self.vectors = list_of_vectors
        self.vectors_count = len(list_of_vectors)
        self.length = sum([v.length for v in self.vectors])
        self.dx = sum([v.dx for v in self.vectors])
        self.dy = sum([v.dy for v in self.vectors])
        self.dx_abs = sum([v.dx_abs for v in self.vectors])
        self.dy_abs = sum([v.dy_abs for v in self.vectors])
        try:
            self.start = list_of_vectors[0].start
            self.end = list_of_vectors[-1].end
        except IndexError:
            self.start = None
            self.end = None
