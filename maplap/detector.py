import math
from typing import List
import cv2
import numpy as np


class Point:
    first: int
    second: int

    def __init__(self, first: int, second: int):
        self.first = first
        self.second = second

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.first} {self.second}"

    def __gt__(self, other):
        return self.first < other.first or (
                self.first == other.first and self.second < other.second)


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

    def __gt__(self, other):
        return self.center < other.center

    def count_intersections(self, gray_image: np.ndarray, speed_rate: int) -> int:
        count: int = 0
        if self.center.first - self.radius < 0 \
                or self.center.first + self.radius >= gray_image.shape[1] \
                or self.center.second - self.radius < 0 \
                or self.center.second + self.radius >= gray_image.shape[0]:
            return 0
        for phi in np.arange(0.0, 2 * np.pi, speed_rate / self.radius):
            if gray_image[round(self.center.second + self.radius * math.sin(phi))]\
                    [round(self.center.first + self.radius * math.cos(phi))] != 0:
                count = count + speed_rate
        return count

    def find_line_width(self, gray_image: np.ndarray, is_circle: float, speed_rate: int) -> None:
        min_radius = self.radius
        while self.count_intersections(gray_image, speed_rate) \
                > is_circle * 2 * np.pi * self.radius:
            self.radius = self.radius + 1
        self.line_width = self.radius - min_radius - 1
        self.radius = min_radius

    def find_right_center_and_radius(self,
                                     gray_image: np.ndarray,
                                     is_circle: float = 0.6,
                                     max_thickness: int = 20,
                                     min_radius: int = 5,
                                     speed_rate: int = 5):
        count_non_zero_now = self.count_intersections(gray_image, speed_rate)
        moves = ((1, 1), (-1, 1), (-1, -1), (1, -1),
                 (1, 0), (0, 1), (-1, 0), (0, -1),
                 (1, 0), (0, 1), (-1, 0), (0, -1))
        for move in moves:
            for _ in range(0, max_thickness):
                self.center.first = self.center.first + move[0]
                self.center.second = self.center.second + move[1]
                count_non_zero_move = self.count_intersections(gray_image, speed_rate)
                if count_non_zero_move > is_circle * 2 * np.pi * self.radius:
                    count_non_zero_now = count_non_zero_move
                else:
                    self.center.first = self.center.first - move[0]
                    self.center.second = self.center.second - move[1]
                    break
                if count_non_zero_now > is_circle * 2 * np.pi * self.radius and \
                        self.radius > min_radius:
                    self.radius = self.radius - 1
                    count_non_zero_new = self.count_intersections(gray_image, speed_rate)
                    if count_non_zero_new > is_circle * 2 * np.pi * self.radius:
                        count_non_zero_now = count_non_zero_new
                    else:
                        self.radius = self.radius + 1


class Detector:
    block_size: int
    level_black: int

    threshold_line: int
    min_line_length: int
    max_line_gap: int

    is_circle: float
    max_thickness: int
    speed_rate: int

    threshold_center: int
    min_radius: int
    max_radius: int

    def __init__(self, file_sittings: str):
        self.block_size = 101
        self.level_black = 20

        self.threshold_line = 100
        self.min_line_length = 15
        self.max_line_gap = 10

        self.is_circle = 0.75
        self.max_thickness = 20
        self.speed_rate = 1

        self.threshold_center = 20
        self.min_radius = 5
        self.max_radius = 0

    def detect(self, file_path: str) -> List[Line] and List[Circle]:
        input_image = cv2.imread(file_path)
        gray_image = self.get_black_white_image(input_image)
        canny_image = cv2.Canny(gray_image, 100, 50)
        lines = self.detect_lines_without_width(canny_image)
        circles_centers = self.detect_centers_of_circles(gray_image)
        circles = self.clarify_circles(gray_image, circles_centers)
        return lines, circles

    def get_black_white_image(self, const_image: cv2.UMat) -> np.ndarray:
        gray_image = cv2.cvtColor(const_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.adaptiveThreshold(gray_image,
                                           maxValue=255,
                                           adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           thresholdType=cv2.THRESH_BINARY_INV,
                                           blockSize=self.block_size,  # Parameter!
                                           C=self.level_black)  # Parameter!
        return gray_image

    def detect_lines_without_width(self, const_image: np.ndarray) -> list:
        coordinates: list = cv2.HoughLinesP(const_image,
                                            rho=1,
                                            theta=math.pi / 180,
                                            threshold=self.threshold_line,
                                            minLineLength=self.min_line_length,
                                            maxLineGap=self.max_line_gap)
        lines = []
        if coordinates is not None:
            for coordinate in coordinates:
                x_first, y_first, x_second, y_second = coordinate[0]
                lines.append(Line(Point(x_first, y_first), Point(x_second, y_second), 1))
        return lines

    def detect_centers_of_circles(self, gray_image: np.ndarray) -> List[Circle]:
        centers: list = cv2.HoughCircles(gray_image,
                                         cv2.HOUGH_GRADIENT,
                                         1,
                                         minDist=0.0001,
                                         param1=50,
                                         param2=self.threshold_center,
                                         minRadius=self.min_radius,
                                         maxRadius=self.max_radius)
        if centers is not None:
            circles: list = []
            if centers is not None:
                for center in centers[0, :]:
                    x_center, y_center, radius = map(int, center)
                    circles.append(Circle(Point(x_center, y_center), radius, 1))
            return circles
        return []

    def clarify_circles(self,
                        gray_image: np.ndarray,
                        centers: List[Circle]) -> List[Circle]:
        circles: list = []
        centers.sort()
        for center in centers:
            if center.count_intersections(gray_image, self.speed_rate) \
                    > self.is_circle * 2 * np.pi * center.radius:
                center.find_right_center_and_radius(gray_image, self.is_circle, self.max_thickness,
                                                    self.min_radius, self.speed_rate)
                center.find_line_width(gray_image, self.is_circle, self.speed_rate)
                for center_delete in centers:
                    if math.hypot(center.center.first - center_delete.center.first,
                                  center.center.second - center_delete.center.second) <= \
                            2 * center.line_width:
                        centers.remove(center_delete)
                for center_delete in circles:
                    if math.hypot(center.center.first - center_delete.center.first,
                                  center.center.second - center_delete.center.second) <= \
                            2 * center.line_width:
                        circles.remove(center_delete)
                circles.append(center)
        return circles
