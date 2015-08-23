import random

__author__ = 'Paddy'

'''
Ludum Dare 33 - August 21st-24th | #LDJAM | U+2603 | Theme: You are the Monster
'''

import pygame
import pygame.surface as surface
import settings_parse
import time
import math


class Position:

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y

    def get(self):

        return self.x, self.y

    def move(self, x, y):

        self.x += x
        self.y += y

    def get_diff(self, point):

        return self.x - point.x, self.y - point.y

    def __add__(self, other):

        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):

        return Position(self.x - other.x, self.y - other.y)

    def __str__(self):

        return 'x = ' + str(self.x) + ' y = ' + str(self.y)


class Line:

    def __init__(self):

        self.start = Position()
        self.end = Position()
        self.focal = Position()
        self.gradient = 0

    def find_gradient(self):

        delta = self.start - self.focal
        self.gradient = delta.x / delta.y

    def find_end(self, limits):

        delta_x = self.start.x - self.focal.x
        delta_y = self.start.y - self.focal.y

        try:
            gradient = delta_x / delta_y
        except ZeroDivisionError:
            print 'zero error'
            gradient = 0

        if gradient > 0:
            overreach_x = limits.x - self.start.x
            y_coord = limits.x

        else:
            overreach_x = self.start.x
            y_coord = 0

        x_coord = overreach_x * gradient

        self.end = Position(x_coord, y_coord)
        return self.end


class Taniwha:

    def __init__(self, limits):

        self.position = Position(100, 100)
        self.focal_point = Position()
        self.vector_point = Position()
        self.acc = 500
        self.speed = self.get_speed()
        self.direction = self.get_direction()

        self.eyes = [Position(52, 15), Position(12, 15)]
        self.lasers = [Line(), Line()]
        self.lasers_on = False

        for i in range(2):
            self.lasers[i].start = self.eyes[i]

        self.joystick = None
        self.limits = limits

        self.surface = surface.Surface((64, 64))
        self.surface.fill((128, 128, 0))
        for eye in self.eyes:
            pygame.draw.circle(self.surface, (0, 128, 0), eye.get(), 5)

    def get_speed(self):

        x, y = self.vector_point.get_diff(Position())

        return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

    def get_direction(self):

        x, y = self.vector_point.get_diff(Position())

        if x >= 0:
            try:
                angle = math.atan(y / x)

            except ZeroDivisionError:
                angle = math.atan(y)

        else:
            try:
                angle = math.pi - math.atan(y / x)

            except ZeroDivisionError:
                angle = math.pi - math.atan(y)

        return abs(angle)

    def update_focal(self, time_elapsed):

        if self.joystick:

            if not (-0.2 < self.joystick.get_axis(4) < 0.2):
                self.focal_point.x += self.joystick.get_axis(4) * self.acc * time_elapsed

            if not (-0.2 < self.joystick.get_axis(3) < 0.2):
                self.focal_point.y += self.joystick.get_axis(3) * self.acc * time_elapsed

        else:
            mouse_pos = pygame.mouse.get_pos()
            self.focal_point.x = mouse_pos[0]
            self.focal_point.y = mouse_pos[1]

        for laser, eye in zip(self.lasers, self.eyes):
            laser.start = eye + self.position
            laser.focal = self.focal_point
            laser.find_end(self.limits)

    def update(self, time_elapsed, keys):

        if keys[pygame.K_a]:
            self.vector_point.x -= self.acc * time_elapsed

        if keys[pygame.K_d]:
            self.vector_point.x += self.acc * time_elapsed

        if keys[pygame.K_w]:
            self.vector_point.y -= self.acc * time_elapsed

        if keys[pygame.K_s]:
            self.vector_point.y += self.acc * time_elapsed

        if keys[pygame.K_SPACE]:
            self.lasers_on = True

        else:
            self.lasers_on = False

        if self.joystick:

            if not (-0.2 < self.joystick.get_axis(0) < 0.2):
                self.vector_point.x += self.joystick.get_axis(0) * self.acc * time_elapsed

            if not (-0.2 < self.joystick.get_axis(1) < 0.2):
                self.vector_point.y += self.joystick.get_axis(1) * self.acc * time_elapsed

            if self.joystick.get_axis(2) < -0.5:
                self.lasers_on = True

            else:
                self.lasers_on = False

        self.speed = self.get_speed()
        self.direction = self.get_direction()

        x_move = self.vector_point.x * time_elapsed
        y_move = self.vector_point.y * time_elapsed

        self.vector_point.x -= x_move
        self.vector_point.y -= y_move

        self.position.x += x_move
        self.position.y += y_move


class Fish:

    def __init__(self, limits, bubble_handler):

        random_y = random.randint(0, limits.y - 100)

        self.direction = random.choice([-1, 1])

        self.surface = pygame.image.load('Fish.png')

        if self.direction > 0:
            self.position = Position(0, random_y)
            self.surface = pygame.transform.flip(self.surface, True, False)

        else:
            self.position = Position(limits.x, random_y)

        self.speed = 100

        self.health_points = 1

        self.last_bubble = time.time()
        self.bubble_handler = bubble_handler
        self.bubble_time = random.uniform(0.9, 2.5)



    def point_collide(self, point):

        if self.position.x < point.x < (self.position.x + 64):
            if self.position.y < point.y < (self.position.y + 64):
                return True

        return False

    def update(self, time_elapsed, taniwha):

        self.position.x += self.speed * self.direction * time_elapsed
        self.position.y += math.sin(self.position.x / 40) / 10

        if taniwha.lasers_on:
            if self.point_collide(taniwha.focal_point):
                self.health_points -= time_elapsed

        if time.time() > (self.last_bubble + self.bubble_time):
            self.last_bubble = time.time()
            bubble_start = Position(self.position.x, self.position.y)
            self.bubble_handler(bubble_start)


class Diver(Fish):

    def __init__(self, limits, bubble_handler):

        Fish.__init__(self, limits, bubble_handler)

        self.surface = pygame.image.load('Diver.png')

        self.health_points = 2

        self.bubble_period = random.uniform(0.3, 0.5)
        self.last_bubble_lot = time.time()
        self.bubble_time = random.uniform(0.05, 0.1)

        self.photo_distance = 100
        self.photo = False

    def update(self, time_elapsed, taniwha):

        distance = self.speed * time_elapsed

        if not self.photo:

            if (taniwha.position.x - self.photo_distance) < self.position.x < (taniwha.position.x + self.photo_distance):

                if (taniwha.position.y - self.photo_distance) < self.position.y < (taniwha.position.y + self.photo_distance):
                    self.photo = True

            if (taniwha.position.x + self.photo_distance) < self.position.x:
                self.position.x -= distance

            elif (taniwha.position.x - self.photo_distance) > self.position.x:
                self.position.x += distance

            if (taniwha.position.y + self.photo_distance) < self.position.y:
                self.position.y -= distance

            elif (taniwha.position.y - self.photo_distance) > self.position.y:
                self.position.y += distance

        else:
            self.position.y -= distance

        if taniwha.lasers_on:
            if self.point_collide(taniwha.focal_point):
                self.health_points -= time_elapsed

        current_time = time.time()

        # Check for burst of bubbles
        if current_time < (self.last_bubble_lot + self.bubble_period):

            if current_time > (self.last_bubble + self.bubble_time):
                self.last_bubble = time.time()
                bubble_start = Position(self.position.x, self.position.y)
                self.bubble_handler(bubble_start)

            else:
                self.last_bubble_lot = current_time



class Bubble:

    def __init__(self, pos=Position()):

        self.position = pos
        self.speed = 500

        self.surface = pygame.image.load('Bubble.png')

    def update(self, time_elapsed):

        self.position.y -= self.speed * time_elapsed
        self.position.x += self.speed * time_elapsed * random.uniform(-1.3, 1.3)


def point_outside(point, limits):

    if 0 < point.x < limits.x:
        if 0 < point.y < limits.y:
            return False

    return True


def main():

    """
    The main game function. Welcome to the beginning of the end.
    :return:
    """

    # First we must initialize the pygame module and game clock before most things happen
    pygame.init()
    game_clock = pygame.time.Clock()

    # Grab the settings from the settings file. They are placed in a dictionary.
    settings = settings_parse.parse_settings('settings.cfg')

    window_name = 'Taniwha'
    window_resolution = settings['x_resolution'], settings['y_resolution']

    # Check to see if the game should run in full screen
    flags = 0
    if settings['full_screen']:
        flags = pygame.FULLSCREEN

    # Build the main game window according to the settings provided
    pygame.display.set_caption(window_name)
    window = pygame.display.set_mode(window_resolution, flags, 32)

    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    except pygame.error:
        joystick = None

    world_limits = Position(settings['x_resolution'], settings['y_resolution'])

    # Init world objects
    taniwha = Taniwha(world_limits)
    number_fish = 5
    number_divers = 2

    bubbles = []

    def create_bubble(pos):

        bubbles.append(Bubble(pos))

    fish = [Fish(world_limits, create_bubble) for i in range(number_fish)]
    divers = [Diver(world_limits, create_bubble) for i in range(number_divers)]

    # Bubble particle check
    bubble_check = time.time()

    # Initialize the variable game loop time step
    last_time = time.time()

    while True:

        # The heart of the variable game loop. Keeps track of how long a frame takes to complete
        current_time = time.time()
        time_elapsed = current_time - last_time
        last_time = current_time

        window.fill((0, 0, 128))

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.JOYAXISMOTION:

                taniwha.joystick = joystick

            if event.type == pygame.MOUSEMOTION:

                taniwha.joystick = None

        # Update game objects
        taniwha.update(time_elapsed, keys)
        taniwha.update_focal(time_elapsed)

        fish_copy = fish

        for f in fish:
            f.update(time_elapsed, taniwha)

        for f in fish_copy:
            if f.health_points < 0:
                fish.remove(f)

            if point_outside(f.position, world_limits):
                fish.remove(f)

        if len(fish) < number_fish:
            fish.append(Fish(world_limits, create_bubble))

        divers_copy = divers

        for diver in divers:
            diver.update(time_elapsed, taniwha)

        for diver in divers_copy:
            if diver.health_points < 0:
                divers.remove(diver)

            if point_outside(diver.position, world_limits):
                divers.remove(diver)

        if len(divers) < number_divers:
            divers.append(Diver(world_limits, create_bubble))

        # Update Bubbles
        bubbles_copy = bubbles

        for bubble in bubbles:
            bubble.update(time_elapsed)

        for bubble in bubbles_copy:
            if bubble.position.y < 0:
                bubbles.remove(bubble)

        # Render all game objects
        window.blit(taniwha.surface, taniwha.position.get())
        vector_position = (int(taniwha.position.x + taniwha.vector_point.x),
                           int(taniwha.position.y + taniwha.vector_point.y))
        focal_point = (int(taniwha.focal_point.x), int(taniwha.focal_point.y))
        pygame.draw.circle(window, (255, 0, 0), vector_position, 5)
        pygame.draw.circle(window, (255, 64, 0), focal_point, 5)
        for f in fish:
            window.blit(f.surface, f.position.get())

        for diver in divers:
            window.blit(diver.surface, diver.position.get())

        if taniwha.lasers_on:
            for laser in taniwha.lasers:
                pygame.draw.line(window, (245, 50, 77), laser.start.get(), laser.focal.get(), 8)
                pygame.draw.line(window, (215, 114, 94), laser.start.get(), laser.focal.get(), 3)

                if current_time > (bubble_check + random.uniform(0.02, 0.05)):
                    bubble_check = current_time

                    b_pos = Position(taniwha.focal_point.x, taniwha.focal_point.y)
                    create_bubble(b_pos)

        for bubble in bubbles:
            window.blit(bubble.surface, bubble.position.get())

        pygame.display.update()


if __name__ == '__main__':

    main()
