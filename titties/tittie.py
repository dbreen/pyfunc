import pygame
import sys


DEFAULT_COLORS = ('#ff4444', '#44ff44', '#4444ff', '#ff6699')


class Tittie(object):
    def __init__(self, dimensions, x_scale, y_scale, colors=None):
        self.dimensions = dimensions
        self.x_scale = x_scale
        self.y_scale = y_scale
        self.funcs = []

        # set the X values that we'll be using for each function
        increment = float(self.x_scale[1] - self.x_scale[0]) / self.dimensions[0]
        self.x_points = [self.x_scale[0] + x * increment
                         for x in range(0, self.dimensions[0]+1)]

        # initialize pygame and create the color objects
        pygame.init()
        pygame.display.set_caption('TITTIES!')
        self.screen = pygame.display.set_mode(dimensions)
        if not colors:
            colors = DEFAULT_COLORS
        self.colors = [pygame.Color(color) for color in colors]
        self.current_color = 0

    def translate(self, val, from_scale, to_scale):
        """
        Translate a value from the from_scale to the to_scale. For example,
        to map the value 0 from (-5, 5) to (0, 400), this function should
        return 200.
        """
        shift = 0 - from_scale[0]
        from_ = (from_scale[0] + shift, from_scale[1] + shift)
        return (to_scale[1] - to_scale[0]) / (from_[1] - from_[0]) * (val + shift)

    def translate_point(self, x, y):
        """
        Translate a point on the graph scale to the screen's pixel scale. Note
        that the y-axis must be inverted since 0 is the bottom on graphs but
        is the top on screens.
        """
        return (
            int(self.translate(x, self.x_scale, (0, self.dimensions[0]))),
            int(self.dimensions[1] -
                self.translate(y, self.y_scale, (0, self.dimensions[1])) - 1)
        )

    def add_func(self, func):
        self.funcs.append(func)

    def draw_axes(self):
        axis_color = pygame.Color('#aaaaaa')
        pygame.draw.line(self.screen, axis_color,
                         self.translate_point(self.x_scale[0], 0),
                         self.translate_point(self.x_scale[1], 0))
        pygame.draw.line(self.screen, axis_color,
                         self.translate_point(0, self.y_scale[0]),
                         self.translate_point(0, self.y_scale[1]))

    def plot(self, func):
        color = self.colors[self.current_color % len(self.colors)]
        self.current_color += 1
        points = []
        for x in self.x_points:
            y = func(x)
            points.append(self.translate_point(x, y))
        pygame.draw.lines(self.screen, color, False, points)
        pygame.display.flip()

    def plot_all(self):
        for func in self.funcs:
            self.plot(func)

    def boob(self):
        self.draw_axes()
        self.plot_all()
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

