class Line:
    x_first: int = 0
    y_first: int = 0
    x_second: int = 0
    y_second: int = 0
    line_width: float = 0

    def __init__(self, x_first: int, y_first: int, x_second: 
                 int, y_second: int, line_width: int = 1):
        self.x_first = x_first
        self.y_first = y_first
        self.x_second = x_second
        self.y_second = y_second
        self.line_width = line_width

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.x_first.__str__() + " " + self.y_first.__str__() + " " \
               + self.x_second.__str__() + " " + self.y_second.__str__() + " " + self.line_width.__str__()


class Circle:
    x_center: float = 0
    y_center: float = 0
    radius: float = 0
    line_width: float = 0

    def __init__(self, x_center: int, y_center: int, radius: int, line_width: int = 1):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.line_width = line_width

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.x_center.__str__() + " " + self.y_center.__str__() + " " \
               + self.radius.__str__() + " " + self.line_width.__str__()

# from detector branch
