import pygame


class MovingBall:
    def __init__(self, x, y, radius, step, screen_width, screen_height, color=(220, 45, 45)):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        min_x = self.radius
        max_x = self.screen_width - self.radius
        min_y = self.radius
        max_y = self.screen_height - self.radius

        if min_x <= new_x <= max_x:
            self.x = new_x
        if min_y <= new_y <= max_y:
            self.y = new_y

    def handle_key(self, key):
        if key == pygame.K_UP:
            self.move(0, -self.step)
        elif key == pygame.K_DOWN:
            self.move(0, self.step)
        elif key == pygame.K_LEFT:
            self.move(-self.step, 0)
        elif key == pygame.K_RIGHT:
            self.move(self.step, 0)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)