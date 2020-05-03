from pylatex import Document, UnsafeCommand, TikZ, TikZCoordinate, TikZDraw, TikZOptions
from pylatex.base_classes import CommandBase, Arguments, Command
from pylatex.package import Package

from geometry import Circle, Line


# delete useless \usepackage


class GeneratorLatexCode:

    def __init__(self, list_of_lines_and_circles):
        geometry_options = {
            "margin": "0in",
            # "textwidth" : "1pt"
            # "paperheight": str(height) + "pt",
            # "paperwidth": str(width) + "pt",
        }
        self.doc = Document(page_numbers=False, geometry_options=geometry_options)
        circle_comm = UnsafeCommand('newcommand', r'\Circle', options=5,
                                    extra_arguments=r'\draw[line width = #1, radius = #2, scale = #3] (#4, #5) circle')
        self.doc.append(circle_comm)

        # some scaling problems
        self.pic = self.generator_pic(list_of_lines_and_circles)
        self.doc.append(self.pic)

    class CircleCommand(CommandBase):
        # extra_arguments=r'\draw[line width = #1, radius = #2, scale = #3] (#4, #5) circle')
        """
        A class representing a custom LaTeX command.

        This class represents a custom LaTeX command named
        ``exampleCommand``.
        """

        _latex_name = 'Circle'
        packages = [Package('tikz')]

        def dumps(self):
            """Represent the command as a string in LaTeX syntax.
            Returns
            -------
            str
                The LaTeX formatted command
            """

            options = self.options.dumps()
            arguments = self.arguments.dumps()

            if self.extra_arguments is None:
                return r'\{command}{options}{arguments};' \
                    .format(command=self.latex_name, options=options,
                            arguments=arguments)

            extra_arguments = self.extra_arguments.dumps()

            return r'\{command}{arguments}{options}{extra_arguments};' \
                .format(command=self.latex_name, arguments=arguments,
                        options=options, extra_arguments=extra_arguments)

    def get_scale(self) -> float:
        return 0.015

    def add_circle(self, picture, circle):
        picture.append(self.CircleCommand(arguments=Arguments(circle.line_width, circle.radius, self.get_scale(),
                                                               circle.center.x_coord, circle.center.y_coord)))
        # node_kwargs = {
        #     "line width": str(circle.line_width),
        #     "radius": str(circle.radius),
        #     "scale": str(get_scale()),
        # }
        # center = TikZCoordinate(circle.center.x_coord, circle.center.y_coord)
        # pic.append(
        #     TikZDraw([center, "circle"], options=TikZOptions(**node_kwargs))
        # )

    def add_line(self, picture, line):
        node_kwargs = {"line width": str(line.line_width), "scale": str(self.get_scale())}
        first = TikZCoordinate(line.start.x_coord, line.start.y_coord)
        second = TikZCoordinate(line.end.x_coord, line.end.y_coord)
        picture.append(TikZDraw([first, "--", second], options=TikZOptions(**node_kwargs)))

    def generator_pic(self, list_of_lines_and_circles) -> TikZ:
        picture = TikZ()
        for i in list_of_lines_and_circles:
            if isinstance(i, Circle):
                self.add_circle(picture, i)
            elif isinstance(i, Line):
                self.add_line(picture, i)
        return picture

    # def generator_latex_code(list_of_lines_and_circles) -> Document:
    #     geometry_options = {
    #         "margin": "0in",
    #         # "textwidth" : "1pt"
    #         # "paperheight": str(height) + "pt",
    #         # "paperwidth": str(width) + "pt",
    #     }
    #     doc = Document(page_numbers=False, geometry_options=geometry_options)
    #
    #     circle_comm = UnsafeCommand('newcommand', '\Circle', options=5,
    #                                 extra_arguments=r'\draw[line width = #1, radius = #2, scale = #3] (#4, #5) circle')
    #     doc.append(circle_comm)
    #
    #     # some scaling problems
    #
    #     doc.append(generator_pic(list_of_lines_and_circles))
    #
    #     return doc

    def generator_latex_str(self) -> str:
        return self.doc.dumps()

    def generator_one_picture_packages_str(self) -> str:
        # no ideas how it works

        return self.pic.dumps_packages()

    def generator_one_picture_str(self) -> str:
        return self.pic.dumps()

    def generator_latex_tex(self, filename):
        self.doc.generate_tex(filename)

    def generator_latex_pdf(self, filename):
        # some problems with saving existed file

        self.doc.generate_pdf(filename)
