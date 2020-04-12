import random
from source.Detector import *


def generator_images(random_seed=0, circles=5, lines=5, thickness="thin", width=100, height=100) -> list:
    # ->ListOfLinesAndCircles
    random.seed(random_seed)
    figures = []
    line_width = 1
    if thickness == "thick":
        line_width = 5

    for i in range(circles):
        x_center = random.randint(1, width - 1)
        y_center = random.randint(1, height - 1)
        radius = random.randint(1, min(x_center, width - x_center, y_center, height - y_center))
        figures.append(Circle(x_center, y_center, radius, line_width))

    for i in range(lines):
        x_first = random.randint(1, width)
        y_first = random.randint(1, height)
        x_second = random.randint(1, width)
        y_second = random.randint(1, height)
        figures.append(Line(x_first, y_first, x_second, y_second, line_width))
    return figures


generator_images()
