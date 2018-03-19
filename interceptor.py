

class Interceptor:

    def __init__(self, line):
        self.line = line
        self.counter = 0
        self.centroid = None
        self.last_centroid = None

    def exec(self, centroid):
        self.centroid = centroid
        if self.centroid is not None and self.last_centroid is not None:
            self.evaluate(self.centroid, self.last_centroid)
        self.last_centroid = self.centroid

    def evaluate(self, centroid, last_centroid):
        line_param = self.calcParams(self.line['init'], self.line['end'])
        centroid_param = self.calcParams(centroid, last_centroid)

        return self.areLinesIntersecting(line_param, centroid_param, centroid, last_centroid)

    def calcParams(self, point1, point2):  # line's equation Params computation
        if point2[1] - point1[1] == 0:
            a = 0
            b = -1.0
        elif point2[0] - point1[0] == 0:
            a = -1.0
            b = 0
        else:
            a = (point2[1] - point1[1]) / (point2[0] - point1[0])
            b = -1.0

        c = (-a * point1[0]) - b * point1[1]
        return (a, b, c)

    def areLinesIntersecting(self, params1, params2, point1, point2):
        det = params1[0] * params2[1] - params2[0] * params1[1]
        if det == 0:
            return False  # lines are parallel
        else:
            x = (params2[1] * -params1[2] - params1[1] * -params2[2]) / det
            y = (params1[0] * -params2[2] - params2[0] * -params1[2]) / det
            if(x <= max(point1[0], point2[0]) and
                    x >= min(point1[0], point2[0]) and
                    y <= max(point1[1], point2[1]) and
                    y >= min(point1[1], point2[1])):
                print("intersecting in:", x, y)
                self.counter += 1
                return True  # lines are intersecting inside the line segment
            else:
                return False  # lines are intersecting but outside of the line segment