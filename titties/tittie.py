import pygame
import sys


COLORS = ('#ff0000', '#00ff00', '#0000ff')


class Tittie(object):
    def __init__(self, dimensions, x_scale, y_scale):
        self.dimensions = dimensions
        self.x_scale = x_scale
        self.y_scale = y_scale
        pygame.init()
        pygame.display.set_caption('TITTIES!')
        self.screen = pygame.display.set_mode(dimensions)
        self.colors = [pygame.Color(color) for color in COLORS]
        self.current_color = 0
        increment = float(x_scale[1] - x_scale[0]) / dimensions[0]
        self.x_points = [x_scale[0] + x * increment
                         for x in range(0, dimensions[0]+1)]
        axis_color = pygame.Color('#aaaaaa')
        pygame.draw.line(self.screen, axis_color,
                         self.translate_point(x_scale[0], 0),
                         self.translate_point(x_scale[1], 0))
        pygame.draw.line(self.screen, axis_color,
                         self.translate_point(0, y_scale[0]),
                         self.translate_point(0, y_scale[1]))

    def translate(self, val, from_scale, to_scale):
        return val / (from_scale[1] - from_scale[0]) * \
                      (to_scale[1] - to_scale[0])

    def translate_point(self, x, y):
        return (
            int(self.translate(x, self.x_scale, (0, self.dimensions[0])) +
                self.dimensions[0] / 2),
            int(-self.translate(y, self.y_scale, (0, self.dimensions[1])) +
                self.dimensions[1] / 2)
        )

    def plot(self, func):
        color = self.colors[self.current_color % len(self.colors)]
        self.current_color += 1
        points = []
        for x in self.x_points:
            y = func(x)
            points.append(self.translate_point(x, y))
        pygame.draw.lines(self.screen, color, False, points)
        pygame.display.flip()

    def boob(self):
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

