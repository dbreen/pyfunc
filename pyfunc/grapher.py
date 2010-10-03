import os
import pygame
import sys


ROOT_DIR = os.path.dirname(__file__)
RESOURCE_DIR = os.path.join(ROOT_DIR, "resources")
DEFAULT_COLORS = ('#ff4444', '#44ff44', '#4444ff', '#ff6699')
DEFAULT_FONT = os.path.join(RESOURCE_DIR, "fonts", "inconsolata.otf")
FONT_SIZE = 14


class Grapher(object):
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
        pygame.display.set_caption('pyfunc')
        self.screen = pygame.display.set_mode(dimensions)
        if not colors:
            colors = DEFAULT_COLORS
        self.colors = [pygame.Color(color) for color in colors]
        self.current_color = 0

        pygame.font.init()
        self.font = pygame.font.Font(DEFAULT_FONT, FONT_SIZE)

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
        # axis labels
        x_pos = self.dimensions[1] - self.translate(0, self.y_scale, (0, self.dimensions[1]))
        y_pos = self.translate(0, self.x_scale, (0, self.dimensions[0])) + 3
        axis_labels = (
            (self.x_scale[0], False, True, 0, x_pos),
            (self.x_scale[1], True, True, self.dimensions[0], x_pos),
            (self.y_scale[1], False, False, y_pos, 0),
            (self.y_scale[0], False, True, y_pos, self.dimensions[1])
        )
        for label in axis_labels:
            self.render_text(*label, color=axis_color)

    def render_text(self, text, offset_x, offset_y, x, y, color):
        surf = self.font.render(str(text), True, color)
        if offset_x:
            x -= surf.get_width()
        if offset_y:
            y -= surf.get_height()
        self.screen.blit(surf, (x, y))

    def plot(self, func, position):
        color = self.colors[self.current_color % len(self.colors)]
        self.current_color += 1

        # draw the function definition in the curve's color, as a legend
        funcname = self.font.render(func.as_str, True, color)
        self.screen.blit(funcname, (5, (FONT_SIZE+2) * position + 5))

        points = []
        for x in self.x_points:
            try:
                y = func(x)
            except Exception, e:
                print "Plotting %s failed: %s" % (x, e)
            else:
                points.append(self.translate_point(x, y))
        pygame.draw.lines(self.screen, color, False, points)
        pygame.display.flip()

    def plot_all(self):
        for i, func in enumerate(self.funcs):
            self.plot(func, i)

    def run(self):
        self.draw_axes()
        self.plot_all()
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
