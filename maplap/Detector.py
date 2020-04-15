import cv2
import math
import numpy as np
import random


class Line:
    x_first: int = 0
    y_first: int = 0
    x_second: int = 0
    y_second: int = 0
    line_width: float = 0

    def __init__(self, x_first: int, y_first: int, x_second: int, y_second: int, line_width: int = 1):
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


def detector(input_image: cv2.UMat,
             block_size: int = 101,
             level_black: int = 20,

             threshold_line: int = 100,
             min_line_length: int = 15,
             max_line_gap: int = 10,

             find_rate: float = 1,
             threshold_center: int = 50,
             min_radius: float = 0,
             max_radius: float = 0) -> list:
    gray_image = get_black_white_image(input_image, block_size, level_black)
    canny_image = cv2.Canny(gray_image, 100, 50)
    lines = detect_lines_without_width(canny_image, threshold_line, min_line_length, max_line_gap)
    return lines


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
    cv2.imshow("Show Gaussian", gray_image)
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
            lines.append(Line(x_first, y_first, x_second, y_second, 1))
    return lines


input_image = cv2.imread("/home/alex/Pictures/MapLapFile6.png")
detector(input_image)
