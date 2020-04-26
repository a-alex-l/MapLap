from pylatex import Document, TikZ, TikZCoordinate, TikZDraw, TikZOptions

from detector import Circle, Line


# TikZNode, TikZUserPath
def generator_latex_code(list_of_lines_and_circles) -> Document:
    doc = Document()

    with doc.create(TikZ()) as pic:
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                node_kwargs = {"line width": str(i.line_width) + "pt", "radius": str(i.radius)}
                center = TikZCoordinate(i.center.x_coordinate, i.center.y_coordinate)
                pic.append(TikZDraw([center, "circle"], options=TikZOptions(**node_kwargs)))
            elif isinstance(i, Line):
                node_kwargs = {"line width": str(i.line_width) + "pt"}
                first = TikZCoordinate(i.point_first.x_coordinate, i.point_first.y_coordinate)
                second = TikZCoordinate(i.point_second.x_coordinate, i.point_second.y_coordinate)
                pic.append(TikZDraw([first, "--", second], options=TikZOptions(**node_kwargs)))

    return doc


def generator_latex_str(list_of_lines_and_circles) -> str:
    return generator_latex_code(list_of_lines_and_circles).dumps()


def generator_latex_tex(list_of_lines_and_circles, filename):
    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_tex(filename)


def generator_latex_pdf(list_of_lines_and_circles, filename):
    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_pdf(filename)
