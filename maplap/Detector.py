import cv2
import math
import numpy as np
import random


class Line:
    x_first: int = 0
    y_first: int = 0
    x_second: int = 0
    y_second: int = 0
    line_width: int = 0

    def __init__(self, x_first: int, y_first: int, x_second: int, y_second: int, line_width: int = 1):
        self.x_first = x_first
        self.y_first = y_first
        self.x_second = x_second
        self.y_second = y_second
        self.line_width = line_width

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


def detector(input_image: cv2.UMat,
             block_size: int = 101,
             level_black: int = 20,

             threshold_line: int = 100,
             min_line_length: int = 15,
             max_line_gap: int = 10,

             find_rate: int = 1,
             threshold_center: int = 12,
             min_radius: int = 0,
             max_radius: int = 0) -> list:
    gray_image = get_black_white_image(input_image, block_size, level_black)
    canny_image = cv2.Canny(gray_image, 100, 50)
    cv2.imshow("Show Canny", canny_image)

    circles_centers = detect_centers_of_circles(gray_image, find_rate, threshold_center, min_radius, max_radius)
    lines = detect_lines_without_width(canny_image, threshold_line, min_line_length, max_line_gap)

    circles = find_radius_and_line_width(gray_image, circles_centers)
    show_finds(input_image, lines, circles)
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


def detect_centers_of_circles(const_image: np.ndarray,
                              find_rate: int = 2,
                              threshold_center: int = 100,
                              min_radius: int = 0,
                              max_radius: int = 0) -> list:
    centers: list = cv2.HoughCircles(const_image,
                                     cv2.HOUGH_GRADIENT,
                                     find_rate,
                                     minDist=0.0001,
                                     param1=50,  # threshold for Canny edge detector
                                     param2=threshold_center,  # threshold for center detection
                                     minRadius=min_radius,
                                     maxRadius=max_radius)
    if centers is not None:
        return centers[0, :]
    else:
        return list()


def is_here_circle(gray_image: np.ndarray,
                   x_center: int,
                   y_center: int,
                   radius: int,
                   is_circle: float = 0.7) -> bool:
    circle_image = np.zeros(gray_image.shape, gray_image.dtype)
    cv2.circle(circle_image, (x_center, y_center), radius, (255, 255, 255))
    and_image = cv2.bitwise_and(gray_image, circle_image, mask=None)
    cv2.imshow("Circle", circle_image)
    cv2.imshow("And", and_image)
    #cv2.waitKey()
    return cv2.countNonZero(and_image) > is_circle * cv2.countNonZero(circle_image)


def find_radius_and_line_width(gray_image: np.ndarray, centers) -> list:
    circles = []
    if centers is not None:
        for center in centers:
            x_center, y_center, radius = map(int, center)
            if is_here_circle(gray_image, x_center, y_center, radius):
                line_width = 1
                while is_here_circle(gray_image, x_center, y_center, radius + line_width):
                    line_width = line_width + 1
                line_width = line_width - 1
                if line_width != 0:
                    circles.append(Circle(x_center, y_center, radius, line_width))
    return circles


def show_finds(const_image: cv2.UMat, lines: list, circles: list):
    image = cv2.UMat(const_image).get()
    print("Lines ", len(lines))
    print("Circles ", len(circles))
    if lines:
        for line in lines:
            cv2.line(image, (line.x_first, line.y_first), (line.x_second, line.y_second),
                     (random.randint(0, 255), random.randint(0, 255), 255), line.line_width)
    if circles:
        for circle in circles:
            cv2.circle(image, (circle.x_center, circle.y_center), circle.radius,
                       (255, random.randint(0, 255), random.randint(0, 255)), circle.line_width)
    cv2.imshow("Show", image)
    cv2.waitKey()


input_image = cv2.imread("/home/alex/Pictures/MapLapFile10.png")
detector(input_image)
