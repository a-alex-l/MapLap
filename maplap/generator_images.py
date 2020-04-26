import random
from detector import Circle, Line, Point


def generator_images(
        random_seed=0, circles=5, lines=5, max_thickness=1, size=100
) -> list:
    # ->ListOfLinesAndCircles
    random.seed(random_seed)
    figures = []

    for _ in range(circles):
        x_center = random.randint(1, size)
        y_center = random.randint(1, size)
        radius = random.randint(
            1, min(x_center, size - x_center, y_center, size - y_center)
        )
        line_width = random.randint(1, max_thickness)
        figures.append(Circle(Point(x_center, y_center), radius, line_width))

    for _ in range(lines):
        x_first = random.randint(1, size)
        y_first = random.randint(1, size)
        x_second = random.randint(1, size)
        y_second = random.randint(1, size)
        line_width = random.randint(1, max_thickness)
        figures.append(
            Line(Point(x_first, y_first), Point(x_second, y_second), line_width)
        )

    return figures
