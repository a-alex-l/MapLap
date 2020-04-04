import cv2
import math
import numpy
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
        block_size=101,
        level_black=10,
        rho=1,
        threshold=100,
        min_line_length=100,
        max_line_gap=10,
        min_dist_between_centers=10,
        threshold_canny=10,
        threshold_center=10,
        min_radius=0,
        max_radius=0):
    input_image = cv2.imread("/home/alex/Pictures/MapLapFile3.png")
    gray_image = make_contrast_and_gray_image(input_image, block_size, level_black)
    lines = detect_lines_without_width(gray_image, rho, threshold, min_line_length, max_line_gap)
    circles = detect_circles_without_width(gray_image, min_dist_between_centers,
                                           threshold_canny, threshold_center, min_radius, max_radius)
    print(lines.__len__())
    print("\n".join(map(str, lines)))
    print(circles.__len__())
    print("\n".join(map(str, circles)))
    show_finds(input_image, lines, circles)


def make_contrast_and_gray_image(const_image: cv2.UMat,
                                 block_size=101,
                                 level_black=10):
    gray_image = cv2.cvtColor(const_image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.adaptiveThreshold(gray_image,
                                       maxValue=255,
                                       adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       thresholdType=cv2.THRESH_BINARY_INV,
                                       blockSize=block_size,  # Parameter!
                                       C=level_black)  # Parameter!
    cv2.imshow("Show Canny", gray_image)
    return gray_image


def detect_lines_without_width(const_image: numpy.ndarray,
                               rho=1,
                               threshold=100,
                               min_line_length=100,
                               max_line_gap=10) -> list:
    coordinates: list = cv2.HoughLinesP(const_image,
                                        rho=rho,  # Parameter!
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


def detect_circles_without_width(const_image: numpy.ndarray,
                                 min_dist_between_centers=10,
                                 threshold_canny=10,
                                 threshold_center=10,
                                 min_radius=0,
                                 max_radius=0) -> list:
    centers_ans_radiuses: list = cv2.HoughCircles(const_image,
                                                  cv2.HOUGH_GRADIENT,
                                                  1,  #
                                                  min_dist_between_centers,  # minimal distance between two centers
                                                  param1=threshold_canny,  # threshold for Canny edge detector
                                                  param2=threshold_center,  # threshold for center detection
                                                  minRadius=min_radius,
                                                  maxRadius=max_radius)
    circles = []
    if centers_ans_radiuses is not None:
        for center_ans_radius in centers_ans_radiuses:
            x_center, y_center, radius = center_ans_radius[0]
            circles.append(Circle(x_center, y_center, radius, 1))
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


detector(level_black=20)