import math
from typing import List
import time

import cv2
import numpy as np

from geometry import Circle, Line, Point
from settings import SettingsParams


class Contrast:
    block_size: int
    level_black: int

    def __init__(self, settings: SettingsParams):
        self.block_size = int(getattr(getattr(settings, "block_size"), "value", 101))
        self.level_black = int(getattr(getattr(settings, "level_black"), "value", 20))

    def update_settings(self, settings: SettingsParams):
        self.__init__(settings)

    def get_black_white_image(self, const_image: cv2.UMat) -> np.ndarray:
        gray_image = cv2.cvtColor(const_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.adaptiveThreshold(
            gray_image,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=self.block_size,
            C=self.level_black,
        )
        return gray_image


class LineDetector:
    threshold_line: int
    min_line_length: int
    max_line_gap: int
    speed_rate: float

    def __init__(self, settings: SettingsParams):
        self.threshold_line = int(getattr(getattr(settings, "threshold_line"), "value", 100))
        self.min_line_length = int(getattr(getattr(settings, "min_line_length"), "value", 15))
        self.max_line_gap = int(getattr(getattr(settings, "max_line_gap"), "value", 10))
        self.speed_rate = float(getattr(getattr(settings, "speed_rate"), "value", 1))

    def update_settings(self, settings: SettingsParams):
        self.__init__(settings)

    def detect_lines_without_width(self, const_image: np.ndarray) -> list:
        coordinates: list = cv2.HoughLinesP(
            const_image,
            rho=1,
            theta=np.pi / 1800,
            threshold=self.threshold_line,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap,
        )
        lines = []
        if coordinates is not None:
            for coordinate in coordinates:
                x_first, y_first, x_second, y_second = coordinate[0]
                lines.append(
                    Line(Point(x_first, y_first), Point(x_second, y_second), 1)
                )
        return lines

    def lines_extension(self, lines: List[Line], gray_image: np.ndarray) -> List[Line]:
        lines.sort()
        for line in lines:
            line.sprawl_start(gray_image, self.speed_rate)
            line.swap()
            line.sprawl_start(gray_image, self.speed_rate)
        return lines

    def clarify_lines(
            self, gray_image: np.ndarray, lines: List[Line]
    ) -> List[Line]:
        lines.sort()
        ans: List[Line] = []
        used: List[bool] = [False for _ in range(0, len(lines))]
        left = 0
        for i in range(0, len(lines)):
            if not used[i]:
                while (abs(lines[left].get_cos() - lines[i].get_cos()) > 0.1 or
                       abs(lines[left].get_sin() - lines[i].get_sin()) > 0.1):
                    left = left + 1
                line = lines[i]
                for j in range(left, len(lines)):
                    if (abs(lines[j].get_cos() - line.get_cos()) > 0.1 or
                            abs(lines[j].get_sin() - line.get_sin()) > 0.1):
                        break
                    if Line(line.start, lines[j].start, 1).get_length() < \
                            Line(line.start, lines[j].end, 1).get_length():
                        lines[j].swap()
                    if Line(line.start, lines[j].start, 1).get_length() < \
                            Line(line.end, lines[j].start, 1).get_length():
                        line.swap()
                    if Line(line.start, lines[j].start, 1).get_length() < \
                            Line(line.end, lines[j].end, 1).get_length():
                        line.swap(), lines[j].swap()
                    line_s_s = Line(line.start, lines[j].start, 1)
                    line_e_e = Line(line.end, lines[j].end, 1)
                    if ((abs(line_s_s.get_length() - (line.get_length() +
                              lines[j].get_length() + line_e_e.get_length())) < 0.5 or
                         abs(line_s_s.get_length() + line_e_e.get_length() -
                             (line.get_length() + lines[j].get_length())) < 0.5) and
                            line_e_e.count_intersections(gray_image, self.speed_rate)
                            > 0.2 * line_e_e.get_length()):
                        used[j] = True
                        if (line.get_length() < line_s_s.get_length() and
                                lines[j].get_length() < line_s_s.get_length()):
                            line = Line(line.start, lines[j].start, 1)
                        else:
                            if lines[j].get_length() < line.get_length():
                                line = lines[j]

                ans.append(line)
        for line in ans:
            line.sprawl_line(gray_image, self.speed_rate)
        return ans


class CircleDetector:
    is_circle: float
    max_thickness: int
    speed_rate: float

    threshold_center: int
    min_radius: int
    max_radius: int

    def __init__(self, settings: SettingsParams):
        self.is_circle = float(getattr(getattr(settings, "is_circle"), "value", 0.75))
        self.max_thickness = int(getattr(getattr(settings, "max_thickness"), "value", 20))
        self.speed_rate = float(getattr(getattr(settings, "speed_rate"), "value", 1))
        self.threshold_center = int(getattr(getattr(settings, "threshold_center"), "value", 20))
        self.min_radius = int(getattr(getattr(settings, "min_radius"), "value", 5))
        self.max_radius = int(getattr(getattr(settings, "max_radius"), "value", 0))

    def update_settings(self, settings: SettingsParams):
        self.__init__(settings)

    def _find_right_center_and_radius(
            self,
            gray_image: np.ndarray,
            circle: Circle,
            center_gap: int = 3
    ):
        count_non_zero_now = circle.count_intersections(gray_image, self.speed_rate)
        moves = (
            (0.5, 0.5),
            (-0.5, 0.5),
            (-0.5, -0.5),
            (0.5, -0.5),
            (0.5, 0),
            (0, 0.5),
            (-0.5, 0),
            (0, -0.5)
        )
        for move in moves:
            for _ in range(0, center_gap):
                circle.center.x_coord = circle.center.x_coord + move[0]
                circle.center.y_coord = circle.center.y_coord + move[1]
                count_non_zero_move = circle.count_intersections(
                    gray_image, self.speed_rate
                )
                if count_non_zero_move > self.is_circle * 2 * np.pi * circle.radius:
                    count_non_zero_now = count_non_zero_move
                else:
                    circle.center.x_coord = circle.center.x_coord - move[0]
                    circle.center.y_coord = circle.center.y_coord - move[1]
                    break
                if (
                        count_non_zero_now > self.is_circle * 2 * np.pi * circle.radius
                        and circle.radius > self.min_radius
                ):
                    circle.radius = circle.radius - self.speed_rate / 10
                    count_non_zero_new = circle.count_intersections(
                        gray_image, self.speed_rate
                    )
                    if count_non_zero_new > self.is_circle * 2 * np.pi * circle.radius:
                        count_non_zero_now = count_non_zero_new
                    else:
                        circle.radius = circle.radius + self.speed_rate / 10

    def detect_centers_of_circles(self, gray_image: np.ndarray) -> List[Circle]:
        centers: list = cv2.HoughCircles(
            gray_image,
            cv2.HOUGH_GRADIENT,
            1.2,
            minDist=0.0001,
            param1=50,
            param2=self.threshold_center,
            minRadius=self.min_radius,
            maxRadius=self.max_radius,
        )
        if centers is not None:
            circles: list = []
            if centers is not None:
                for center in centers[0, :2000]:
                    x_center, y_center, radius = center
                    circle = Circle(Point(x_center, y_center), radius, 1.0)
                    self.speed_rate = self.speed_rate * radius / 2
                    if (circle.count_intersections(gray_image, self.speed_rate)
                            > self.is_circle * np.pi * circle.radius):
                        self._find_right_center_and_radius(gray_image, circle)
                        circles.append(circle)
                    self.speed_rate = self.speed_rate / (radius / 2)
            return circles
        return []

    def clarify_circles(
            self, gray_image: np.ndarray, centers: List[Circle]
    ) -> List[Circle]:
        circles: list = []
        used: List[bool] = [False for _ in range(0, len(centers))]
        centers.sort()
        for i in range(0, len(centers)):
            if not used[i]:
                center = centers[i]
                if (center.count_intersections(gray_image, self.speed_rate * center.radius / 2)
                        > self.is_circle * 1.5 * np.pi * center.radius):
                    self._find_right_center_and_radius(gray_image, center, self.max_thickness)
                    center.find_line_width(gray_image, self.is_circle, self.speed_rate)
                    for j in range(i + 1, len(centers)):
                        if (math.hypot(
                                center.center.x_coord - centers[j].center.x_coord,
                                center.center.y_coord - centers[j].center.y_coord)
                                <= 2 * center.line_width):
                            used[j] = True
                    for center_delete in circles:
                        if (math.hypot(
                                center.center.x_coord - center_delete.center.x_coord,
                                center.center.y_coord - center_delete.center.y_coord)
                                <= 2 * center.line_width):
                            circles.remove(center_delete)
                    circles.append(center)
        return circles

    def find_concentric(
            self, gray_image: np.ndarray, circles: List[Circle]
    ) -> List[Circle]:
        circles_ans: List[Circle] = circles.copy()
        for circle in circles:
            new_circle = \
                Circle(Point(circle.center.x_coord, circle.center.y_coord), self.min_radius, 1)
            for new_circle.radius in \
                    list(range(self.min_radius, int(circle.radius - circle.line_width / 2) - 5)) + \
                    list(range(int(circle.radius + circle.line_width / 2) + 5,
                               int(circle.center.x_coord))):
                if (new_circle.count_intersections(gray_image,
                                                   self.speed_rate * new_circle.radius / 2) >
                        self.is_circle * 2 * np.pi * new_circle.radius):
                    self._find_right_center_and_radius(gray_image, new_circle, self.max_thickness)
                    new_circle.find_line_width(gray_image, self.is_circle, self.speed_rate)
                    circles_ans.append(new_circle)
        return circles_ans


class Detector:
    contrast: Contrast
    detector_lines: LineDetector
    detector_circles: CircleDetector

    def update_settings(self, settings: SettingsParams):
        self.contrast.update_settings(settings)
        self.detector_lines.update_settings(settings)
        self.detector_circles.update_settings(settings)

    def __init__(self, settings: SettingsParams):
        self.contrast = Contrast(settings)
        self.detector_lines = LineDetector(settings)
        self.detector_circles = CircleDetector(settings)

    def _get_finds(self, lines: list, circles: list, input_image):
        image: cv2.UMat = input_image.copy()
        if circles:
            for circle in circles:
                cv2.circle(image, (int(round(circle.center.x_coord)),
                                   int(round(circle.center.y_coord))),
                           int(round(circle.radius + circle.line_width / 2)),
                           (0, 0, 0), int(round(circle.line_width)))
        if lines:
            for line in lines:
                cv2.line(image, (int(round(line.start.x_coord)), int(round(line.start.y_coord))),
                         (int(round(line.end.x_coord)), int(round(line.end.y_coord))),
                         (0, 0, 0), int(round(line.line_width)), lineType=cv2.LINE_4)
        return image

    def tmp(self, name, show_image):
        pass
        """print("Time: ", name, " ", time.perf_counter() - self.now)
        cv2.imshow(name, show_image)
        #cv2.waitKey()
        self.now = time.perf_counter()"""

    def _show_finds(self, file_path: str, lines: list, circles: list):
        input_image = cv2.imread(file_path)
        image = self._get_finds(lines, circles, 255 * np.ones(input_image.shape, input_image.dtype))
        cv2.imwrite(file_path, image)

    def normal_canny(self, gray_image: np.ndarray) -> np.ndarray:
        canny_image = gray_image.copy()
        for i in range(1, gray_image.shape[0] - 1):
            for j in range(1, gray_image.shape[1] - 1):
                if (gray_image[i][j + 1] != 0 and gray_image[i][j - 1] != 0 and
                        gray_image[i + 1][j] != 0 and gray_image[i - 1][j] != 0 and
                        gray_image[i][j] != 0):
                    canny_image[i][j] = 0
        return canny_image

    def detect(self, file_path: str) -> List[Line] and List[Circle]:
        self.now = time.perf_counter()
        input_image = cv2.imread(file_path)
        gray_image = self.contrast.get_black_white_image(input_image)
        self.tmp("0", self._get_finds([], [], input_image))
        canny_image = self.normal_canny(gray_image)
        self.tmp("1 Canny", canny_image)
        lines_preform = self.detector_lines.detect_lines_without_width(canny_image)
        self.tmp("2", self._get_finds(lines_preform, [], input_image))
        long_lines = self.detector_lines.lines_extension(lines_preform, gray_image)
        self.tmp("3", self._get_finds(long_lines, [], input_image))
        lines = self.detector_lines.clarify_lines(gray_image, long_lines)
        self.tmp("5", self._get_finds(lines, [], input_image))
        circles_centers = self.detector_circles.detect_centers_of_circles(gray_image)
        self.tmp("6", self._get_finds(lines, circles_centers, input_image))
        circles_non_concentric = self.detector_circles.clarify_circles(gray_image, circles_centers)
        self.tmp("7", self._get_finds(lines, circles_non_concentric, input_image))
        circles = self.detector_circles.find_concentric(gray_image, circles_non_concentric)
        self.tmp("8", self._get_finds(lines, circles, input_image))
        #print("Lines: ", len(lines), " Circles: ", len(circles))
        self._show_finds(file_path, lines, circles)
        return lines, circles
