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
        return self.__str__()

    def __str__(self):
        return self.x_first.__str__() + " " + self.y_first.__str__() + " " \
               + self.x_second.__str__() + " " + self.y_second.__str__() + " " + self.line_width.__str__()


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
        return self.__str__()

    def __str__(self):
        return self.x_center.__str__() + " " + self.y_center.__str__() + " " \
               + self.radius.__str__() + " " + self.line_width.__str__()


def detector(  # input_image
        block_size: int = 101,
        level_black: int = 20,

        threshold: int = 100,
        min_line_length: int = 15,
        max_line_gap: int = 10,

        threshold_canny: int = 100,
        threshold_center: int = 100,
        min_radius: float = 0,
        max_radius: float = 0) -> list:
    input_image = cv2.imread("/home/alex/Pictures/MapLapFile8.png")
    gray_image = get_gray_image(input_image, block_size, level_black)
    circles_centers = detect_centers_of_circles(gray_image, threshold_canny, threshold_center, min_radius, max_radius)
    circles = find_radiuses_and_line_width(gray_image, circles_centers)
    canny_image = get_canny_edge_image(gray_image, threshold_canny)
    lines = detect_lines_without_width(canny_image, threshold, min_line_length, max_line_gap)
    print(lines.__len__())
    print("\n".join(map(str, lines)))
    print(circles.__len__())
    print("\n".join(map(str, circles)))
    show_finds(input_image, lines, circles)
    return lines + circles


def get_gray_image(const_image: cv2.UMat,
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


def get_canny_edge_image(const_image: np.ndarray, threshold_canny: int = 200) -> np.ndarray:
    canny_image = cv2.Canny(const_image,
                            threshold1=threshold_canny,  # 100% edge
                            threshold2=threshold_canny / 2)  # if connected to edge its edge too.
    cv2.imshow("Show Canny", canny_image)
    return canny_image


def detect_lines_without_width(const_image: np.ndarray,
                               threshold: int = 100,
                               min_line_length: int = 15,
                               max_line_gap: int = 10) -> list:
    coordinates: list = cv2.HoughLinesP(const_image,
                                        rho=1,
                                        theta=math.pi / 180,
                                        threshold=threshold,  # threshold for line detection
                                        minLineLength=min_line_length,  # minimal line length
                                        maxLineGap=max_line_gap)  # max gap between two lines
    lines = []
    if coordinates is not None:
        for coordinate in coordinates:
            x_first, y_first, x_second, y_second = coordinate[0]
            lines.append(Line(x_first, y_first, x_second, y_second, 1))
    return lines


def detect_centers_of_circles(const_image: np.ndarray,
                              threshold_canny: int = 200,
                              threshold_center: int = 100,
                              min_radius: float = 0,
                              max_radius: float = 0) -> list:
    centers: list = cv2.HoughCircles(const_image,
                                     cv2.HOUGH_GRADIENT,
                                     1,
                                     minDist=10,
                                     param1=threshold_canny,  # threshold for Canny edge detector
                                     param2=threshold_center,  # threshold for center detection
                                     minRadius=min_radius,
                                     maxRadius=max_radius)
    if centers is not None:
        return centers[0, :]
    else:
        return list()


def find_radiuses_and_line_width(canny_image: np.ndarray, centers) -> list:
    circles = []
    if centers is not None:
        for center in centers:
            x_center, y_center, radius = center
            circles.append(Circle(x_center, y_center, radius, 0))
    return circles


def show_finds(const_image: cv2.UMat, lines: list, circles: list):
    image = cv2.UMat(const_image).get()
    if lines:
        for line in lines:
            cv2.line(image, (line.x_first, line.y_first), (line.x_second, line.y_second),
                     (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    if circles:
        for circle in circles:
            cv2.circle(image, (circle.x_center, circle.y_center), circle.radius,
                       (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), circle.line_width)
    cv2.imshow("Show", image)
    cv2.waitKey()


detector()
