import numpy as np
import pygame as pg
from random import randint, gauss

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_SIZE = (800, 600)


def rand_color():
    """
    Generates a random RGB color tuple.

    Returns:
        tuple: Random RGB color tuple.
    """
    return (randint(0, 255), randint(0, 255), randint(0, 255))


class GameObject:
    def move(self):
        """
        Moves the game object.
        """
        pass

    def draw(self, screen):
        """
        Draws the game object on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the object on.
        """
        pass


class Shell(GameObject):
    def __init__(self, coord, vel, rad=20, color=None):
        """
        Initializes a Shell object.

        Args:
            coord (list): The initial coordinates of the shell [x, y].
            vel (list): The initial velocity of the shell [vx, vy].
            rad (int): The radius of the shell (default: 20).
            color (tuple): The color of the shell (default: None).
        """
        self.coord = coord
        self.vel = vel
        if color is None:
            color = rand_color()
        self.color = color
        self.rad = rad
        self.is_alive = True

    def check_corners(self, refl_ort=0.8, refl_par=0.9):
        """
        Checks if the shell has hit the corners of the screen and reflects its velocity accordingly.

        Args:
            refl_ort (float): The coefficient of restitution for the orthogonal direction (default: 0.8).
            refl_par (float): The coefficient of restitution for the parallel direction (default: 0.9).
        """
        for i in range(2):
            if self.coord[i] < self.rad:
                self.coord[i] = self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)
            elif self.coord[i] > SCREEN_SIZE[i] - self.rad:
                self.coord[i] = SCREEN_SIZE[i] - self.rad
                self.vel[i] = -int(self.vel[i] * refl_ort)
                self.vel[1 - i] = int(self.vel[1 - i] * refl_par)

    def move(self, time=1, grav=0):
        """
        Moves the shell based on its velocity and gravitational acceleration.

        Args:
            time (int): The time step for the movement (default: 1).
            grav (int): The gravitational acceleration affecting the shell (default: 0).
        """
        self.vel[1] += grav
        for i in range(2):
            self.coord[i] += time * self.vel[i]
        self.check_corners()
        if self.vel[0] ** 2 + self.vel[1] ** 2 < 2 ** 2 and self.coord[1] > SCREEN_SIZE[1] - 2 * self.rad:
            self.is_alive = False

    def draw(self, screen):
        """
        Draws the shell on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the shell on.
        """
        pg.draw.circle(screen, self.color, self.coord, self.rad)


class Cannon(GameObject):
        def __init__(self, coord=[30, SCREEN_SIZE[1] // 2], angle=0, max_pow=50, min_pow=10, color=RED):
            """
            Initializes a Cannon object.

            Args:
                coord (list): The initial coordinates of the cannon [x, y] (default: [30, SCREEN_SIZE[1] // 2]).
                angle (float): The initial angle of the cannon in radians (default: 0).
                max_pow (int): The maximum power of the cannon (default: 50).
                min_pow (int): The minimum power of the cannon (default: 10).
                color (tuple): The color of the cannon (default: RED).
            """
            self.coord = coord
            self.angle = angle
            self.max_pow = max_pow
            self.min_pow = min_pow
            self.color = color
            self.active = False
            self.pow = min_pow
            self.current_projectile_type = Shell
            self.size = 20  # Added the size attribute and assigned a value

        def set_projectile_type(self, projectile_type):
            """
            Sets the type of projectile to be used by the cannon.

            Args:
                projectile_type (class): The class representing the projectile type.
            """
            self.current_projectile_type = projectile_type

        def strike(self):
            """
            Strikes the cannon and launches a projectile.

            Returns:
                GameObject: The projectile object launched.
            """
            vel = self.pow
            angle = self.angle
            projectile = self.current_projectile_type(
                list(self.coord), [int(vel * np.cos(angle)), int(vel * np.sin(angle))]
            )
            self.pow = self.min_pow
            self.active = False
            return projectile

        def move_left(self):
            """
            Moves the cannon to the left.
            """
            self.coord[0] -= 5

        def move_right(self):
            """
            Moves the cannon to the right.
            """
            self.coord[0] += 5

        def shoot(self):
            """
            Creates a bullet object and returns it.

            Returns:
                Bullet: The bullet object created.
            """
            bullet = Bullet(coord=[self.coord[0], self.coord[1] - self.size], size=5, color=(255, 255, 0), speed=5)
            return bullet

        def draw(self, screen):
            """
            Draws the cannon on the screen.

            Args:
                screen (pygame.Surface): The surface to draw the cannon on.
            """
            pg.draw.rect(screen, self.color, (self.coord[0] - self.size, self.coord[1] - self.size, self.size * 2, self.size * 2))
            pg.draw.circle(screen, self.color, self.coord, self.size)
            pg.draw.line(
                screen,
                self.color,
                self.coord,
                (
                    int(self.coord[0] + self.size * np.cos(self.angle)),
                    int(self.coord[1] + self.size * np.sin(self.angle))
                ),
                5
            )
class Target(GameObject):
    def __init__(self, coord=None, color=None, size=None):
        """
        Initializes a Target object.

        Args:
            coord (list): The initial coordinates of the target [x, y] (default: None).
            color (tuple): The color of the target (default: None).
            size (int): The size of the target (default: None).
        """
        if coord is None:
            coord = [randint(600, 700), randint(100, 500)]
        self.coord = coord
        if color is None:
            color = rand_color()
        self.color = color
        if size is None:
            size = randint(10, 50)
        self.size = size

    def move(self):
        """
        Moves the target horizontally by decrementing its x-coordinate.
        """
        self.coord[0] -= 1

    def draw(self, screen):
        """
        Draws the target on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the target on.
        """
        pg.draw.circle(screen, self.color, self.coord, self.size)
class Bullet(GameObject):
    def __init__(self, coord, size, color, speed):
        """
        Initializes a Bullet object.

        Args:
            coord (list): The initial coordinates of the bullet [x, y].
            size (int): The size of the bullet.
            color (tuple): The color of the bullet.
            speed (int): The speed of the bullet.
        """
        self.coord = coord
        self.size = size
        self.color = color
        self.speed = speed
        self.is_alive = True

    def move(self):
        """
        Moves the bullet horizontally by incrementing its x-coordinate.
        """
        self.coord[0] += self.speed

    def draw(self, screen):
        """
        Draws the bullet on the screen.

        Args:
            screen (pygame.Surface): The surface to draw the bullet on.
        """
        pg.draw.circle(screen, self.color, self.coord, self.size)
def main():
    """
    The main game loop.
    """
    screen = pg.display.set_mode(SCREEN_SIZE)
    clock = pg.time.Clock()
    finished = False
    shells = []
    targets = [Target() for _ in range(2)]
    cannon = Cannon()
    bullets = []
    score = 0
    font = pg.font.SysFont('Arial', 36)

    while not finished:
        clock.tick(50)
        screen.fill(BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    cannon.active = True
                elif event.key == pg.K_UP:
                    cannon.pow += 1
                elif event.key == pg.K_DOWN:
                    cannon.pow -= 1
                elif event.key == pg.K_LEFT:
                    cannon.move_left()
                elif event.key == pg.K_RIGHT:
                    cannon.move_right()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    shells.append(cannon.strike())

        for shell in shells:
            shell.move()
            shell.draw(screen)
            if not shell.is_alive:
                shells.remove(shell)

        for target in targets:
            target.move()
            target.draw(screen)

        for bullet in bullets:
            bullet.move()
            bullet.draw(screen)
            if bullet.coord[0] > SCREEN_SIZE[0]:
                bullets.remove(bullet)

        if cannon.active:
            cannon.draw(screen)

        text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(text, (10, 10))

        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()

