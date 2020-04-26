import math

import numpy as np


class Point:
    x_coord: int
    y_coord: int

    def __init__(self, first: int, second: int):
        self.x_coord = first
        self.y_coord = second

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.x_coord} {self.y_coord}"

    def __gt__(self, other):
        return (
            self.x_coord < other.x_coord
            or self.x_coord == other.x_coord
            and self.y_coord < other.y_coord
        )


class Line:
    start: Point
    end: Point
    line_width: int

    def __init__(self, start: Point, end: Point, line_width: int):
        self.start = start
        self.end = end
        self.line_width = line_width

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.start} {self.end} {self.line_width}"


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

    def __gt__(self, other):
        return self.center < other.center

    def count_intersections(self, gray_image: np.ndarray, speed_rate: float) -> int:
        count: int = 0
        if (
            self.center.x_coord - self.radius < 0
            or self.center.x_coord + self.radius >= gray_image.shape[1]
            or self.center.y_coord - self.radius < 0
            or self.center.y_coord + self.radius >= gray_image.shape[0]
        ):
            return 0
        for phi in np.arange(0.0, 2 * np.pi, speed_rate / self.radius):
            x_coord = round(self.center.y_coord + self.radius * math.sin(phi))
            y_coord = round(self.center.x_coord + self.radius * math.cos(phi))
            if gray_image[x_coord][y_coord] != 0:
                count = count + speed_rate
        return count

    def find_line_width(
        self, gray_image: np.ndarray, is_circle: float, speed_rate: int
    ) -> None:
        min_radius = self.radius
        while (
            self.count_intersections(gray_image, speed_rate)
            > is_circle * 2 * np.pi * self.radius
        ):
            self.radius = self.radius + 1
        self.line_width = self.radius - min_radius - 1
        self.radius = min_radius


class Rectangle:
    """Rectangle struct"""

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2
