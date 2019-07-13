class LineInterface:
    length = 0
    start = None
    end = None

    def get_split_points(self, number_of_points, proportions=None):
        raise NotImplemented

    def split(self, number_of_lines, proportions=None):
        raise NotImplemented

    def get_center(self):
        raise NotImplemented

