from Detector import *
from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions)
from gen_im import *


def generator_latex_code(list_of_lines_and_circles, filename='result.tex') -> Document:
    doc = Document()

    with doc.create(TikZ()) as pic:
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                node_kwargs = {'line width': str(i.line_width) + 'pt',
                               "radius": str(i.radius)}
                pic.append(TikZDraw([TikZCoordinate(i.x_center, i.y_center), 'circle'],
                                    options=TikZOptions(**node_kwargs)))
            elif isinstance(i, Line):
                node_kwargs = {'line width': str(i.line_width) + 'pt'}
                first = TikZCoordinate(i.x_first, i.y_first)
                second = TikZCoordinate(i.x_second, i.y_second)
                pic.append(TikZDraw([first, '--', second],
                                    options=TikZOptions(**node_kwargs)))

    return doc


def generator_latex_str(list_of_lines_and_circles) -> str:
    return generator_latex_code(list_of_lines_and_circles).dumps()


def generator_latex_tex(list_of_lines_and_circles, filename):
    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_tex(filename)


def generator_latex_pdf(list_of_lines_and_circles, filename):
    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_pdf(filename)
