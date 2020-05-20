from pylatex import Document, TikZ, TikZOptions, NoEscape

import tkinter as tk

from geometry import Circle, Line, Point


class GeneratorLatexCode:

    def __init__(self, list_of_lines_and_circles):
        geometry_options = {
            "margin": "0in",
            # "paperheight": str(height) + "pt",
            # "paperwidth": str(width) + "pt",
        }
        self.list_of_lines_and_circles = self.reverse_y(list_of_lines_and_circles)
        self.doc = Document(page_numbers=False, geometry_options=geometry_options)
        self.pic = self.generator_pic()
        self.doc.append(self.pic)

    @staticmethod
    def reverse_y(list_of_lines_and_circles):
        max_y_coord = 0
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                max_y_coord = max(max_y_coord, i.center.y_coord)
            elif isinstance(i, Line):
                max_y_coord = max(max_y_coord, i.start.y_coord, i.end.y_coord)
        new_list = []
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                new_list.append(Circle(Point(i.center.x_coord, max_y_coord - i.center.y_coord), i.radius, i.line_width))
            elif isinstance(i, Line):
                new_list.append(Line(Point(i.start.x_coord, max_y_coord - i.start.y_coord),
                                     Point(i.end.x_coord, max_y_coord - i.end.y_coord), i.line_width))
        return new_list

    @staticmethod
    def __get_scale() -> float:
        root = tk.Tk()
        width_px = root.winfo_screenwidth()
        width_mm = root.winfo_screenmmwidth()
        width_cm = width_mm / 10
        width_cmpd = width_cm / width_px
        return width_cmpd

    @staticmethod
    def __circle_command_string(width, x, y, radius):
        return f'\\draw[line width = {width:.2f}] ({x:.2f}, {y:.2f}) circle ({radius:.2f});'

    def __add_circle(self, picture, circle):
        picture.append(NoEscape(self.__circle_command_string(circle.line_width,
                                                             circle.center.x_coord, circle.center.y_coord,
                                                             circle.radius)))

    @staticmethod
    def __line_command_string(width, x1, y1, x2, y2):
        return f'\\draw[line width = {width:.2f}] ({x1:.2f}, {y1:.2f}) -- ({x2:.2f}, {y2:.2f});'

    def __add_line(self, picture, line):
        picture.append(NoEscape(self.__line_command_string(line.line_width,
                                                           line.start.x_coord, line.start.y_coord,
                                                           line.end.x_coord, line.end.y_coord)))

    def generator_pic(self) -> TikZ:
        options = {"scale": f'{self.__get_scale():.4f}'}
        picture = TikZ(options=TikZOptions(**options))
        for i in self.list_of_lines_and_circles:
            if isinstance(i, Circle):
                self.__add_circle(picture, i)
            elif isinstance(i, Line):
                self.__add_line(picture, i)
        return picture

    def generator_latex_str(self) -> str:
        return self.doc.dumps()

    def generator_one_picture_packages_str(self) -> str:
        return self.pic.dumps_packages()

    def generator_one_picture_str(self) -> str:
        return self.pic.dumps()

    def generator_latex_tex(self, filename):
        self.doc.generate_tex(filename)

    def generator_latex_pdf(self, filename):
        self.doc.generate_pdf(filename)
