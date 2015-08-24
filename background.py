__author__ = 'Paddy'

import pygame
import random
import pygame.gfxdraw


class Rock:

    def __init__(self):

        self.surface = pygame.image.load('rock.png')
        self.surface = pygame.transform.rotate(self.surface, random.randint(0, 360))


class Background:

    def __init__(self, size):

        self.surface = pygame.Surface(size.get())

        self.y_inc = size.y / 5

        self.colours = [[199, 237, 232],
                        [160, 222, 214],
                        [126, 206, 202],
                        [69, 181, 196],
                        [22, 147, 165]]

        for y_index in range(5):

            y = (y_index * self.y_inc) + 32

            for x_index in range(size.x / 64):

                x = (x_index * 64) + 32

                pygame.gfxdraw.aacircle(self.surface, x, y, 128, self.colours[y_index])
                pygame.gfxdraw.filled_circle(self.surface, x, y, 128, self.colours[y_index])

        # Create rock bottom
        for i in range(size.x / 32):
            self.surface.blit(Rock().surface, ((i * 32) - 64, size.y - 128))
            self.surface.blit(Rock().surface, ((i * 32) - 64, size.y - 64))


class MenuBackground(Background):

    def __init__(self, size):

        Background.__init__(self, size)

        self.menu_surface = self.surface

        menu_text = open('menu_text.txt', 'r')
        menu_font = pygame.font.SysFont(None, 32)

        for i, line in enumerate(menu_text):
            l = menu_font.render(line.strip('\n'), True, (0, 0, 0))
            self.menu_surface.blit(l, (32, (i * 40) + 32))
