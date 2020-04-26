class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.x} {self.y}"


class Line:
    point_first: Point
    point_second: Point
    line_width: int

    def __init__(self, point_first: Point, point_second: Point, line_width: int):
        self.point_first = point_first
        self.point_second = point_second
        self.line_width = line_width

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.point_first} {self.point_second} {self.line_width}"


class Circle:
    center: Point
    radius: int
    line_width: int

    def __init__(self, center: Point, radius: int, line_width: int = 1):
        self.center = center
        self.radius = radius
        self.line_width = line_width

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.center} {self.radius} {self.line_width}"