import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH,ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            "white",
            self.position,
            self.radius,
            LINE_WIDTH
        )

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self):
        self.kill() #heradadod de pygame
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angulo = random.uniform(20,50)
        direccion_1 =self.velocity.rotate(angulo)
        direccion_2 =self.velocity.rotate(-angulo)

        new_radio = self.radius - ASTEROID_MIN_RADIUS

        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radio)

        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radio)

        asteroid_1.velocity = direccion_1 * 1.2
        asteroid_2.velocity = direccion_2 * 1.2
        