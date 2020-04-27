import math

import numpy as np


class Point:
    x_coord: float
    y_coord: float

    def __init__(self, first: float, second: float):
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
    radius: float
    line_width: float

    def __init__(self, center: Point, radius: float, line_width: float = 1):
        self.center = center
        self.radius = radius
        self.line_width = line_width

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.center} {self.radius} {self.line_width}"

    def __gt__(self, other):
        return self.center < other.center

    def count_intersections(self, gray_image: np.ndarray, speed_rate: float) -> float:
        count: float = 0
        if (
            round(self.center.x_coord - self.radius) < 0
            or round(self.center.x_coord + self.radius) >= gray_image.shape[1]
            or round(self.center.y_coord - self.radius) < 0
            or round(self.center.y_coord + self.radius) >= gray_image.shape[0]
        ):
            return 0
        for phi in np.arange(0.0, 2 * np.pi, speed_rate / self.radius):
            x_coord: int = int(round(self.center.y_coord + self.radius * math.sin(phi)))
            y_coord: int = int(round(self.center.x_coord + self.radius * math.cos(phi)))
            if gray_image[x_coord][y_coord] != 0:
                count = count + speed_rate
        return count

    def find_line_width(
        self, gray_image: np.ndarray, is_circle: float, speed_rate: float
    ) -> None:
        min_radius: float = self.radius
        while (
            self.count_intersections(gray_image, speed_rate)
            > is_circle * 2 * np.pi * self.radius
        ):
            self.radius = self.radius + speed_rate/10
        self.line_width = self.radius - min_radius - speed_rate/10
        self.radius = min_radius


class Rectangle:
    """Rectangle struct"""

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2
