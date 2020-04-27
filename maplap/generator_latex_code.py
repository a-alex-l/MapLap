from pylatex import Document, TikZ, TikZCoordinate, TikZDraw, TikZOptions

from geometry import Circle, Line


def generator_latex_code(list_of_lines_and_circles) -> Document:
    geometry_options = {
        "margin": "0in",
        # "paperheight": str(height) + "pt",
        # "paperwidth": str(width) + "pt",
    }

    # some scaling problems

    doc = Document(page_numbers=False, geometry_options=geometry_options)
    with doc.create(TikZ()) as pic:
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                node_kwargs = {
                    "line width": str(i.line_width) + "pt",
                    "radius": str(i.radius),
                    "scale": "0.15",
                }
                center = TikZCoordinate(i.center.x_coordinate, i.center.y_coordinate)
                pic.append(
                    TikZDraw([center, "circle"], options=TikZOptions(**node_kwargs))
                )
            elif isinstance(i, Line):
                node_kwargs = {"line width": str(i.line_width) + "pt", "scale": "0.15"}
                first = TikZCoordinate(
                    i.point_first.x_coordinate, i.point_first.y_coordinate
                )
                second = TikZCoordinate(
                    i.point_second.x_coordinate, i.point_second.y_coordinate
                )
                pic.append(
                    TikZDraw([first, "--", second], options=TikZOptions(**node_kwargs))
                )

    return doc


def generator_latex_str(list_of_lines_and_circles) -> str:
    return generator_latex_code(list_of_lines_and_circles).dumps()


def generator_latex_tex(list_of_lines_and_circles, filename):
    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_tex(filename)


def generator_latex_pdf(list_of_lines_and_circles, filename):
    # some problems with saving existed file

    doc = generator_latex_code(list_of_lines_and_circles)
    doc.generate_pdf(filename)
