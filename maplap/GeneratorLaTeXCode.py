from maplap.Detector import *
from pylatex import (Document, TikZ, TikZNode,
                     TikZDraw, TikZCoordinate,
                     TikZUserPath, TikZOptions)


def generator_latex_code(list_of_lines_and_circles, filename='result.tex'):
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

    doc.generate_tex(filename)
