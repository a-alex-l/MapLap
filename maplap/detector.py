import math
import cv2
import numpy as np


class Line:
    x_first: int = 0
    y_first: int = 0
    x_second: int = 0
    y_second: int = 0
    line_width: int = 1

    def __init__(self,
                 x_first: int,
                 y_first: int,
                 x_second: int,
                 y_second: int):
        self.x_first = x_first
        self.y_first = y_first
        self.x_second = x_second
        self.y_second = y_second

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.x_first} {self.y_first} {self.x_second} {self.y_second} {self.line_width}"


class Circle:
    x_center: int = 0
    y_center: int = 0
    radius: int = 0
    line_width: int = 0

    def __init__(self, x_center: int, y_center: int, radius: int, line_width: int = 1):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.line_width = line_width

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.x_center} {self.y_center} {self.radius} {self.line_width}"


def detector(file_path,
             block_size: int = 101,
             level_black: int = 20,

             threshold_line: int = 100,
             min_line_length: int = 5,
             max_line_gap: int = 5,

             is_circle: float = 0.6,
             max_thickness: int = 20,

             find_rate: int = 1,
             threshold_center: int = 35,
             min_radius: int = 5,
             max_radius: int = 0) -> list:
    input_image = cv2.imread(file_path)
    gray_image = get_black_white_image(input_image, block_size, level_black)
    canny_image = cv2.Canny(gray_image, 100, 50)
    lines = detect_lines_without_width(canny_image, threshold_line, min_line_length, max_line_gap)
    circles_centers = detect_centers_of_circles(gray_image,
                                                find_rate,
                                                threshold_center,
                                                min_radius,
                                                max_radius)
    circles = clarify_circles(gray_image, circles_centers, is_circle, max_thickness, min_radius)
    return lines + circles


def get_black_white_image(const_image: cv2.UMat,
                          block_size: int = 101,
                          level_black: int = 20) -> np.ndarray:
    gray_image = cv2.cvtColor(const_image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.adaptiveThreshold(gray_image,
                                       maxValue=255,
                                       adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       thresholdType=cv2.THRESH_BINARY_INV,
                                       blockSize=block_size,  # Parameter!
                                       C=level_black)  # Parameter!
    return gray_image


def detect_lines_without_width(const_image: np.ndarray,
                               threshold_line: int = 100,
                               min_line_length: int = 15,
                               max_line_gap: int = 10) -> list:
    coordinates: list = cv2.HoughLinesP(const_image,
                                        rho=1,
                                        theta=math.pi / 180,
                                        threshold=threshold_line,  # threshold for line detection
                                        minLineLength=min_line_length,  # minimal line length
                                        maxLineGap=max_line_gap)  # max gap between two lines
    lines = []
    if coordinates is not None:
        for coordinate in coordinates:
            x_first, y_first, x_second, y_second = coordinate[0]
            lines.append(Line(x_first, y_first, x_second, y_second))
    return lines


def count_intersections(gray_image: np.ndarray,
                        x_center: int,
                        y_center: int,
                        radius: int) -> int:
    count: int = 0
    if x_center - radius < 0 or x_center + radius >= gray_image.shape[1]\
            or y_center - radius < 0 or y_center + radius >= gray_image.shape[0]:
        return 0
    for phi in np.arange(0.0, 2 * np.pi, 5 / radius):
        if gray_image[round(y_center + radius * math.sin(phi))]\
           [round(x_center + radius * math.cos(phi))] != 0:
            count = count + 5
    return count


def detect_centers_of_circles(gray_image: np.ndarray,
                              find_rate: int = 1,
                              threshold_center: int = 20,
                              min_radius: int = 0,
                              max_radius: int = 0) -> list:
    centers: list = cv2.HoughCircles(gray_image,
                                     cv2.HOUGH_GRADIENT,
                                     find_rate,
                                     minDist=0.0001,
                                     param1=50,  # threshold for Canny edge detector
                                     param2=threshold_center,  # threshold for center detection
                                     minRadius=min_radius,
                                     maxRadius=max_radius)
    if centers is not None:
        circles: list = []
        if centers is not None:
            for center in centers[0, :]:
                x_center, y_center, radius = map(int, center)
                circles.append(Circle(x_center, y_center, radius, 1))
        return circles
    return list()


def find_radius_and_line_width(gray_image: np.ndarray, circle: Circle, is_circle: float) -> Circle:
    circle.line_width = 1
    while count_intersections(gray_image,
                              circle.x_center,
                              circle.y_center,
                              circle.radius + circle.line_width) \
            > is_circle * 2 * np.pi * (circle.radius + circle.line_width):
        circle.line_width = circle.line_width + 1
    circle.line_width = circle.line_width - 1
    return circle


def find_right_center_and_radius(gray_image: np.ndarray,
                                 circle: Circle,
                                 is_circle: float = 0.6,
                                 max_thickness: int = 20,
                                 min_radius: int = 5) -> Circle:
    count_non_zero_now = \
        count_intersections(gray_image, circle.x_center, circle.y_center, circle.radius)
    moves = ((1, 0), (0, 1), (-1, 0), (0, -1),
             (1, 0), (0, 1), (-1, 0), (0, -1),
             (1, 0), (0, 1), (-1, 0), (0, -1))
    for move in moves:
        for _ in range(1, max_thickness):
            count_non_zero_move = count_intersections(gray_image,
                                                      circle.x_center + move[0],
                                                      circle.y_center + move[1],
                                                      circle.radius)
            if count_non_zero_move > is_circle * 2 * np.pi * circle.radius:
                circle.x_center = circle.x_center + move[0]
                circle.y_center = circle.y_center + move[1]
                count_non_zero_now = count_non_zero_move
            else:
                break
            if count_non_zero_now > is_circle * 2 * np.pi * circle.radius and\
               circle.radius > min_radius:
                count_non_zero_new = count_intersections(gray_image,
                                                         circle.x_center,
                                                         circle.y_center,
                                                         circle.radius - 1)
                if count_non_zero_new > is_circle * 2 * np.pi * (circle.radius - 1):
                    circle.radius = circle.radius - 1
                    count_non_zero_now = count_non_zero_new
    return circle


def clarify_center(gray_image: np.ndarray,
                   circle: Circle,
                   is_circle: float = 0.6,
                   max_thickness: int = 20,
                   min_radius: int = 5) -> Circle:
    circle = find_right_center_and_radius(gray_image, circle, is_circle, max_thickness, min_radius)
    circle = find_radius_and_line_width(gray_image, circle, is_circle)
    return circle


def clarify_circles(gray_image: np.ndarray,
                    centers: list,
                    is_circle: float = 0.6,
                    max_thickness: int = 20,
                    min_radius: int = 5) -> list:
    circles: list = []
    for center in centers:
        if count_intersections(gray_image, center.x_center, center.y_center, center.radius) \
                > is_circle * 2 * np.pi * center.radius:
            center = clarify_center(gray_image, center, is_circle, max_thickness, min_radius)
            for center_delete in centers:
                if math.hypot(center.x_center - center_delete.x_center,
                              center.y_center - center_delete.y_center) <= \
                        2 * center.line_width:
                    centers.remove(center_delete)
            for center_delete in circles:
                if math.hypot(center.x_center - center_delete.x_center,
                              center.y_center - center_delete.y_center) <= \
                        2 * center.line_width:
                    circles.remove(center_delete)
            circles.append(center)
    return circles
