class LineInfo:
    def __init__(self, line, series=None, points=None, labels=None):
        self.line = line
        self.series = series
        if series and not points:
            self.points = len(series.get_point_wages())
        else:
            self.points = points
        self.labels = labels
