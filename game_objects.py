import pygame
from pygame import *
import random
from settings import *
import numpy as np


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y, platforms, deadly_objects):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.deadly_objects = deadly_objects
        self.platforms = platforms

        self.image = pygame.image.load('assets/cube_face1.png').convert()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = Rect(x, y, 48, 48)

    def update(self, up, down, left, right, enemies):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 8
        if down:
            pass
        if left:
            self.xvel = -8
        if right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel)

        collided_enemies = pygame.sprite.spritecollide(self, enemies, False)
        collided_deadly_objects = pygame.sprite.spritecollide(self, self.deadly_objects, False)
        if collided_enemies or collided_deadly_objects:
            pygame.event.post(pygame.event.Event(player_died))

    def collide(self, xvel, yvel):
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)

        for p in collided_platforms:
            if isinstance(p, FinishBlock):
                pygame.event.post(pygame.event.Event(player_finish))
            if isinstance(p, Water) or isinstance(p, Spike):
                pygame.event.post(pygame.event.Event(player_died))
            if isinstance(p, Platform):
                p.collided = True
            if xvel > 0:
                self.rect.right = p.rect.left
                # collide right
            if xvel < 0:
                self.rect.left = p.rect.right
                # collide left
            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.yvel = 0
            if yvel < 0:
                self.rect.top = p.rect.bottom
                # collide up


class Bot(Player):
    current_cooldown = 0

    def __init__(self, x, y, platforms, deadly_objects, enemies):
        Player.__init__(self, x, y, platforms, deadly_objects)

        self.image = pygame.image.load('assets/cube_face1_green.png').convert()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.enemies = enemies

        self.rnd = random.Random()
        self.input_table = np.zeros((OUTPUT_SIZE,1))

        self.xvel = 0
        self.yvel = 0
        self.left = self.right = self.up = self.onGround = False

        self.rect = Rect(x, y, 48, 48)

    def go_jump(self):
        self.up = True

    def go_right(self):
        self.left = False
        self.right = True

    def go_left(self):
        self.left = True
        self.right = False

    def ai(self):
        self.up = False
        self.right = False
        self.left = False
        if self.input_table[0] > 0.5 and self.input_table[1] > 0.5:
            if self.input_table[0] > self.input_table[1]:
                self.input_table[1] = 0
            else:
                self.input_table[0] = 0
        if self.input_table[0] > 0.5:
            self.go_left()
        if self.input_table[1] > 0.5:
            self.go_right()
        if self.input_table[2] > 0.5:
            self.go_jump()

    def update(self):
        self.ai()
        if self.up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 8
        if self.left:
            self.xvel = -8
        if self.right:
            self.xvel = 8
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            self.up = False
            if self.yvel > 100: self.yvel = 100
        if not(self.left or self.right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel)

        collided_deadly_objects = pygame.sprite.spritecollide(self, self.deadly_objects, False)
        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)
        if collided_deadly_objects or collided_enemies:
            self.kill()

    def collide(self, xvel, yvel):
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        for p in collided_platforms:
            if isinstance(p, FinishBlock):
                self.kill()
                print("BOT WIN!")
            if isinstance(p, Platform):
                p.collided = True
            if isinstance(p, Water) or isinstance(p, Spike):
                self.kill()
            if xvel > 0:
                self.rect.right = p.rect.left
            if xvel < 0:
                self.rect.left = p.rect.right
            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.yvel = 0
            if yvel < 0:
                self.rect.top = p.rect.bottom


class Enemy(Player):
    current_cooldown = 0

    def __init__(self, x, y, platforms, clock, deadly_objects):
        Player.__init__(self, x, y, platforms, deadly_objects)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.rnd = random.Random(SEED)

        self.cooldown = self.rnd.randint(3, 7) * 1000
        self.clock = clock

        self.image = pygame.image.load('assets/cube_enemy1.png').convert()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.left = self.right = self.up = False

        self.rect = Rect(x, y, 48, 48)

    def ai(self):
        if self.current_cooldown <= 0:
            self.current_cooldown = self.cooldown
            if self.rnd.randint(0, 1):
                self.left = True
                self.right = False
            else:
                self.left = False
                self.right = True

            self.jump()
        else:
            self.current_cooldown -= self.clock.get_time()

    def jump(self):
        if self.rnd.randint(0, 1):
            self.up = True

    def changeDirection(self):
        self.left = not self.left
        self.right = not self.right

    def update(self):
        self.ai()
        if self.up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 5
        if self.left:
            self.xvel = -2
        if self.right:
            self.xvel = 2
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            self.up = False
            if self.yvel > 100: self.yvel = 100
        if not(self.left or self.right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel)

        collided_deadly_objects = pygame.sprite.spritecollide(self, self.deadly_objects, False)
        if collided_deadly_objects:
            self.kill()

    def collide(self, xvel, yvel):
        collided_platforms = pygame.sprite.spritecollide(self, self.platforms, False)
        rand = self.rnd.randint(0, 1)
        for p in collided_platforms:
            if isinstance(p, Water) or isinstance(p, Spike):
                self.kill()
            if xvel > 0:
                self.rect.right = p.rect.left
                if rand:
                    self.jump()
                else:
                    self.changeDirection()
            if xvel < 0:
                self.rect.left = p.rect.right
                if rand:
                    self.jump()
                else:
                    self.changeDirection()
            if yvel > 0:
                self.rect.bottom = p.rect.top
                self.onGround = True
                self.yvel = 0
            if yvel < 0:
                self.rect.top = p.rect.bottom


class Platform(Entity):
    collided = False
    cooldown = 1000
    current_cooldown = 1000

    def __init__(self, x, y, clock, platform_images, counter=None):
        Entity.__init__(self)
        if counter is None:
            counter = random.randint(0, 4)
        self.platform_images = platform_images
        self.counter = counter
        self.clock = clock
        self.image = platform_images[self.counter]
        self.rect = Rect(x, y, 48, 48)

    def update(self):
        if self.collided:
            if self.current_cooldown <= 0:
                if self.counter == 0:
                    self.kill()
                    return
                self.current_cooldown = self.cooldown
                self.counter -= 1
                self.image = self.platform_images[self.counter]
            else:
                self.current_cooldown -= self.clock.get_time()


class Water(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load('assets/W.png').convert()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = Rect(x, y, 48, 48)


class Spike(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        self.image = image
        self.rect = Rect(x, y, 48, 48)


class Rock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load('assets/R.png').convert()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = Rect(x, y, 48, 48)


class FinishBlock(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load('assets/finish.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = Rect(x, y, 48, 48)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        if target is not None:
            self.state = self.camera_func(self.state, target.rect)


def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)


def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)
