import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH,PLAYER_RADIUS

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y,radius=PLAYER_RADIUS)
        self.rotation = 0

    # in the Player class
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(
            self, 
            screen: pygame.Surface,
            color = "white"
            ) -> None:
        
        list_points: list = self.triangle()
        line_width = LINE_WIDTH 
        pygame.draw.polygon(screen, color, list_points, line_width)
