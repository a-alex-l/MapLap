import math
from typing import List

import cv2
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
        return self.x_coord < other.x_coord or \
               self.x_coord == other.x_coord and \
               self.y_coord < other.y_coord


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

    def count_intersections(self, gray_image: np.ndarray, speed_rate: int) -> int:
        count: int = 0
        if self.center.x_coord - self.radius < 0 \
                or self.center.x_coord + self.radius >= gray_image.shape[1] \
                or self.center.y_coord - self.radius < 0 \
                or self.center.y_coord + self.radius >= gray_image.shape[0]:
            return 0
        for phi in np.arange(0.0, 2 * np.pi, speed_rate / self.radius):
            x_coord = round(self.center.y_coord + self.radius * math.sin(phi))
            y_coord = round(self.center.x_coord + self.radius * math.cos(phi))
            if gray_image[x_coord][y_coord] != 0:
                count = count + speed_rate
        return count

    def find_line_width(self, gray_image: np.ndarray, is_circle: float, speed_rate: int) -> None:
        min_radius = self.radius
        while self.count_intersections(gray_image, speed_rate) \
                > is_circle * 2 * np.pi * self.radius:
            self.radius = self.radius + 1
        self.line_width = self.radius - min_radius - 1
        self.radius = min_radius


class Contrast:
    block_size: int
    level_black: int

    def __init__(self, block_size: int = 101, level_black: int = 20):
        self.block_size = block_size
        self.level_black = level_black

    def get_black_white_image(self, const_image: cv2.UMat) -> np.ndarray:
        gray_image = cv2.cvtColor(const_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.adaptiveThreshold(gray_image,
                                           maxValue=255,
                                           adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           thresholdType=cv2.THRESH_BINARY_INV,
                                           blockSize=self.block_size,  # Parameter!
                                           C=self.level_black)  # Parameter!
        return gray_image


class LineDetector:
    threshold_line: int
    min_line_length: int
    max_line_gap: int
    speed_rate: int

    def __init__(self, threshold_line: int = 100, min_line_length: int = 15,
                 max_line_gap: int = 10, speed_rate: int = 1):
        self.threshold_line = threshold_line
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap
        self.speed_rate = speed_rate

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


class CircleDetector:
    is_circle: float
    max_thickness: int
    speed_rate: int

    threshold_center: int
    min_radius: int
    max_radius: int

    def __init__(self):
        self.is_circle = 0.75
        self.max_thickness = 20
        self.speed_rate = 1

        self.threshold_center = 20
        self.min_radius = 5
        self.max_radius = 0

    def _find_right_center_and_radius(self, gray_image: np.ndarray, circle: Circle):
        count_non_zero_now = circle.count_intersections(gray_image, self.speed_rate)
        moves = ((1, 1), (-1, 1), (-1, -1), (1, -1),
                 (1, 0), (0, 1), (-1, 0), (0, -1),
                 (1, 0), (0, 1), (-1, 0), (0, -1))
        for move in moves:
            for _ in range(0, self.max_thickness):
                circle.center.x_coord = circle.center.x_coord + move[0]
                circle.center.y_coord = circle.center.y_coord + move[1]
                count_non_zero_move = circle.count_intersections(gray_image, self.speed_rate)
                if count_non_zero_move > self.is_circle * 2 * np.pi * circle.radius:
                    count_non_zero_now = count_non_zero_move
                else:
                    circle.center.x_coord = circle.center.x_coord - move[0]
                    circle.center.y_coord = circle.center.y_coord - move[1]
                    break
                if count_non_zero_now > self.is_circle * 2 * np.pi * circle.radius and \
                        circle.radius > self.min_radius:
                    circle.radius = circle.radius - 1
                    count_non_zero_new = circle.count_intersections(gray_image, self.speed_rate)
                    if count_non_zero_new > self.is_circle * 2 * np.pi * circle.radius:
                        count_non_zero_now = count_non_zero_new
                    else:
                        circle.radius = circle.radius + 1

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
                self._find_right_center_and_radius(gray_image, center)
                center.find_line_width(gray_image, self.is_circle, self.speed_rate)
                for center_delete in centers:
                    if math.hypot(center.center.x_coord - center_delete.center.x_coord,
                                  center.center.y_coord - center_delete.center.y_coord) <= \
                            2 * center.line_width:
                        centers.remove(center_delete)
                for center_delete in circles:
                    if math.hypot(center.center.x_coord - center_delete.center.x_coord,
                                  center.center.y_coord - center_delete.center.y_coord) <= \
                            2 * center.line_width:
                        circles.remove(center_delete)
                circles.append(center)
        return circles


class Detector:
    contrast: Contrast
    detector_lines: LineDetector
    detector_circles: CircleDetector

    def __init__(self):
        self.contrast = Contrast()
        self.detector_lines = LineDetector()
        self.detector_circles = CircleDetector()

    def detect(self, file_path: str) -> List[Line] and List[Circle]:
        input_image = cv2.imread(file_path)
        gray_image = self.contrast.get_black_white_image(input_image)
        canny_image = cv2.Canny(gray_image, 100, 50)
        lines = self.detector_lines.detect_lines_without_width(canny_image)
        circles_centers = self.detector_circles.detect_centers_of_circles(gray_image)
        circles = self.detector_circles.clarify_circles(gray_image, circles_centers)
        return lines, circles
