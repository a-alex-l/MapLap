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

    def get(self):
        return Point(self.x_coord, self.y_coord)

    def __mul__(self, proportion: float):
        return Point(self.x_coord * proportion, self.y_coord * proportion)

    def __add__(self, other):
        return Point(self.x_coord + other.x_coord, self.y_coord + other.y_coord)

    def __sub__(self, other):
        return self + other * -1

    def make_normal(self):
        tmp: float = self.x_coord
        self.x_coord = self.y_coord
        self.y_coord = -tmp
        return self

    def get_vector_length(self):
        return (self.x_coord * self.x_coord + self.y_coord * self.y_coord) ** 0.5


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

    def get_length(self) -> float:
        return ((self.start.x_coord - self.end.x_coord) ** 2 +
                (self.start.y_coord - self.end.y_coord) ** 2) ** 0.5

    def get_cos(self) -> float:
        return (self.start.x_coord - self.end.x_coord) / self.get_length()

    def get_sin(self) -> float:
        return (self.start.y_coord - self.end.y_coord) / self.get_length()

    def __gt__(self, other):
        return self.get_cos() < other.get_cos()

    def get(self):
        return Line(self.start.get(), self.end.get(), self.line_width)

    def rotate(self, plus):
        vector_normal: Point = self.get_normal() * plus
        vector_mid: Point = self.start * 0.5 + self.end * 0.5
        vector_start: Point = self.start - vector_mid + vector_normal
        vector_start = vector_start * (1 / vector_start.get_vector_length()) * \
                        (self.start - vector_mid).get_vector_length()
        self.start = vector_start + vector_mid
        self.end = vector_mid - vector_start

    def get_normal(self) -> Point:
        return (self.start * (1 / self.get_length()) + self.end * (1 - 1 / self.get_length())
                - self.end).make_normal()

    def count_intersections(self, gray_image: np.ndarray, speed_rate: float) -> float:
        count: float = 0
        for proportion in np.arange(0.0, 1, speed_rate / self.get_length()):
            now: Point = self.start * proportion + self.end * (1 - proportion)
            if (0 <= int(round(now.x_coord)) < gray_image.shape[1] and
                    0 <= int(round(now.y_coord)) < gray_image.shape[0] and
                    gray_image[int(round(now.y_coord))][int(round(now.x_coord))] == 255):
                count = count + speed_rate
        return count

    def swap(self):
        tmp: Point = self.start
        self.start = self.end
        self.end = tmp

    def sprawl_start(self, gray_image: np.ndarray, speed_rate: float):
        start_proportion: float = 1
        now: Point = self.start * start_proportion + self.end * (1 - start_proportion)
        while (0 <= int(round(now.x_coord)) < gray_image.shape[1] and
               0 <= int(round(now.y_coord)) < gray_image.shape[0]):
            if gray_image[int(round(now.y_coord))][int(round(now.x_coord))]:
                start_proportion += speed_rate / self.get_length()
            else:
                if speed_rate == 0.5:
                    break
                start_proportion -= speed_rate / self.get_length()
                speed_rate = 0.5
            now: Point = self.start * start_proportion + self.end * (1 - start_proportion)
        self.start = self.start * (start_proportion - speed_rate / self.get_length()) + \
                     self.end * (1 - start_proportion + speed_rate / self.get_length())

    def find_line_width(
            self, gray_image: np.ndarray, speed_rate: float
    ) -> None:
        vector_normal: Point = self.get_normal()
        line_width_along_normal: float = 1.5
        line_width_opposite_normal: float = 1.5
        line_check = Line(self.start + vector_normal, self.end + vector_normal, 1)
        while line_check.count_intersections(gray_image, speed_rate) > \
                0.95 * line_check.get_length():
            line_width_along_normal = line_width_along_normal + 1
            line_check = Line(self.start + vector_normal * line_width_along_normal,
                              self.end + vector_normal * line_width_along_normal, 1)
        line_check = Line(self.start - vector_normal, self.end - vector_normal, 1)
        while line_check.count_intersections(gray_image, speed_rate) > \
                0.95 * line_check.get_length():
            line_width_opposite_normal = line_width_opposite_normal + 1
            line_check = Line(self.start - vector_normal * line_width_opposite_normal,
                              self.end - vector_normal * line_width_opposite_normal, 1)
        self.line_width = line_width_along_normal + line_width_opposite_normal - 2.0
        self.start = self.start + vector_normal * \
                     ((line_width_along_normal - line_width_opposite_normal) / 2)
        self.end = self.end + vector_normal * \
                   ((line_width_along_normal - line_width_opposite_normal) / 2)

    def sprawl_line(self, gray_image, speed_rate):
        self.find_line_width(gray_image, speed_rate)
        new_line = self.get()
        while True:
            self = new_line
            new_line = self.get()
            new_line.rotate(0.5)
            new_line.find_line_width(gray_image, speed_rate)
            if new_line.get_length() * new_line.line_width < self.get_length() * self.line_width:
                break
        while True:
            self = new_line
            new_line = self.get()
            new_line.rotate(-0.5)
            new_line.find_line_width(gray_image, speed_rate)
            if new_line.get_length() * new_line.line_width < self.get_length() * self.line_width:
                break



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
            self.radius = self.radius + speed_rate / 10
        self.line_width = self.radius - min_radius - speed_rate / 10
        self.radius = min_radius


class Rectangle:
    """Rectangle struct"""

    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2
