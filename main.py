import sys
import pygame
from pygame import *
from game_objects import *
from settings import *
from level_design import levels
global cameraX, cameraY

pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Don't Fall Down!")
timer = pygame.time.Clock()

is_paused = False

menu_background = pygame.image.load('assets/background_menu.png').convert()
tutorial_background = pygame.image.load('assets/background_and_tutorial.png').convert()

bg = pygame.image.load('assets/S.png').convert()
bg = pygame.transform.scale(bg, (48, 48))

platform_images = []

for i in range(1, 6, 1):
    image = pygame.image.load('assets/C{0}.png'.format(i)).convert()
    image = pygame.transform.scale(image, (48, 48))
    platform_images.append(image)

spike = pygame.image.load('assets/spike.png').convert_alpha()
spike = pygame.transform.scale(spike, (48, 48))


def exit_game():
    sys.exit(0)


def event_resume():
    pygame.event.post(pygame.event.Event(resume))


def event_restart_level():
    pygame.event.post(pygame.event.Event(restart_level))


def event_back_to_menu():
    pygame.event.post(pygame.event.Event(back_to_menu))


def event_pause():
    pygame.event.post(pygame.event.Event(pause))


def event_next_level():
    pygame.event.post(pygame.event.Event(next_level))


def text_objects(text, font, color=(0, 0, 0)):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse_pos[0] > x and y+h > mouse_pos[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    smallText = pygame.font.SysFont(FONT2, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)


def tutorial():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == back_to_menu:
                return

        screen.fill(WHITE)
        screen.blit(tutorial_background, (0, 0))

        button("Go back", 10, 10, 200, 50, PRIMARY, PRIMARY_HOVER, event_back_to_menu)

        pygame.display.update()
        timer.tick(15)


def pause_menu():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == restart_level \
                    or event.type == back_to_menu \
                    or event.type == resume:
                return event.type
            if event.type == KEYDOWN and event.key == K_SPACE:
                return restart_level
        largeText = pygame.font.SysFont(FONT, 115)
        TextSurf, TextRect = text_objects("Game paused", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, 50)
        screen.blit(TextSurf, TextRect)

        button("Resume", HALF_WIDTH-100, 200, 200, 50, PRIMARY, PRIMARY_HOVER, event_resume)
        button("Restart level", HALF_WIDTH - 100, 260, 200, 50, PRIMARY, PRIMARY_HOVER, event_restart_level)
        button("Back to menu", HALF_WIDTH-100, 320, 200, 50, DANGER, DANGER_HOVER, event_back_to_menu)

        largeText = pygame.font.SysFont(FONT2, 40)
        TextSurf, TextRect = text_objects("Hit 'space' to restart", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, WIN_HEIGHT - 40)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        timer.tick(15)


def you_win_menu(index):
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == restart_level \
                    or event.type == back_to_menu \
                    or event.type == next_level:
                return event.type
            if event.type == KEYDOWN and event.key == K_SPACE:
                return next_level

        text = "You win!"

        if len(levels)-1 == index:
            text = "You beat the game!"
        else:
            button("Next level", HALF_WIDTH-100, 200, 200, 50, PRIMARY, PRIMARY_HOVER, event_next_level)
            largeText = pygame.font.SysFont(FONT2, 40)
            TextSurf, TextRect = text_objects("Hit 'space' for Next level", largeText, WHITE)
            TextRect.center = (HALF_WIDTH, WIN_HEIGHT - 40)
            screen.blit(TextSurf, TextRect)

        largeText = pygame.font.SysFont(FONT, 115)
        TextSurf, TextRect = text_objects(text, largeText, WHITE)
        TextRect.center = (HALF_WIDTH, 50)
        screen.blit(TextSurf, TextRect)

        button("Restart level", HALF_WIDTH - 100, 260, 200, 50, PRIMARY, PRIMARY_HOVER, event_restart_level)
        button("Back to menu", HALF_WIDTH-100, 320, 200, 50, DANGER, DANGER_HOVER, event_back_to_menu)

        pygame.display.update()
        timer.tick(15)


def game_over_menu():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == restart_level or event.type == back_to_menu:
                return event.type
            if event.type == KEYDOWN and event.key == K_SPACE:
                return restart_level
        text = "You loose!"
        largeText = pygame.font.SysFont(FONT, 115)
        TextSurf, TextRect = text_objects(text, largeText, DANGER)
        TextRect.center = (HALF_WIDTH, 50)
        screen.blit(TextSurf, TextRect)

        button("Restart level", HALF_WIDTH - 100, 260, 200, 50, PRIMARY, PRIMARY_HOVER, event_restart_level)
        button("Back to menu", HALF_WIDTH - 100, 320, 200, 50, DANGER, DANGER_HOVER, event_back_to_menu)

        largeText = pygame.font.SysFont(FONT2, 40)
        TextSurf, TextRect = text_objects("Hit 'space' to restart", largeText, DANGER)
        TextRect.center = (HALF_WIDTH, WIN_HEIGHT - 40)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        timer.tick(15)


def main_menu():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        screen.blit(menu_background, (0, 0))
        largeText = pygame.font.SysFont(FONT, 115)
        TextSurf, TextRect = text_objects("Don't Fall Down!", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, 50)
        screen.blit(TextSurf, TextRect)

        button("Play!", HALF_WIDTH-100, 200, 200, 50, PRIMARY, PRIMARY_HOVER, level_menu)
        button("Tutorial", HALF_WIDTH - 100, 260, 200, 50, PRIMARY, PRIMARY_HOVER, tutorial)
        button("Quit", HALF_WIDTH-100, 320, 200, 50, DANGER, DANGER_HOVER, exit_game)

        largeText = pygame.font.SysFont(FONT2, 20)
        TextSurf, TextRect = text_objects("Developed by Jaroslav Siroic [2017-12]", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, WIN_HEIGHT-15)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        timer.tick(15)


def level_menu(level=levels[0], index=0):

    level_event = launch_level(level)

    if level_event == player_finish:
        you_win_event = you_win_menu(index)
        if you_win_event == restart_level:
            level_menu(level, index)
        elif you_win_event == next_level:
            level_menu(levels[index+1], index+1)
    if level_event == player_died:
        game_over_event = game_over_menu()
        if game_over_event == restart_level:
            level_menu(level, index)
    if level_event == restart_level:
        level_menu(level, index)


def launch_level(level=levels[0]):

    up = down = left = right = False
    entities = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    deadly_objects = pygame.sprite.Group()
    player = None
    x = y = 0
    # build the level

    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y, timer, platform_images)
                platforms.add(p)
                entities.add(p)
            if col.isdigit():
                digit = int(col)
                if digit < len(platform_images):
                    p = Platform(x, y, timer, platform_images, digit)
                else:
                    p = Platform(x, y, timer, platform_images, len(platform_images)-1)
                platforms.add(p)
                entities.add(p)
            if col == "F":
                e = FinishBlock(x, y)
                platforms.add(e)
                entities.add(e)
            if col == "W":
                e = Water(x, y)
                deadly_objects.add(e)
                entities.add(e)
            if col == "R":
                e = Rock(x, y)
                platforms.add(e)
                entities.add(e)
            if col == "^":
                e = Spike(x, y, spike)
                deadly_objects.add(e)
                entities.add(e)
            if col == "<":
                e = Spike(x, y, pygame.transform.rotate(spike, 90))
                deadly_objects.add(e)
                entities.add(e)
            if col == "V":
                e = Spike(x, y, pygame.transform.rotate(spike, 180))
                deadly_objects.add(e)
                entities.add(e)
            if col == ">":
                e = Spike(x, y, pygame.transform.rotate(spike, -90))
                deadly_objects.add(e)
                entities.add(e)
            if col == "U":
                player = Player(x, y, platforms, deadly_objects)
                entities.add(player)
            if col == "E":
                e = Enemy(x, y, platforms, timer, deadly_objects)
                entities.add(e)
                enemies.add(e)
            x += 48
        y += 48
        x = 0

    if player is None:
        player = Player(48, 48, platforms, deadly_objects)

    total_level_width = len(level[0])*48
    total_level_height = len(level)*48
    camera = Camera(complex_camera, total_level_width, total_level_height)

    in_game = True

    while in_game:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                exit_game()
            if e.type == player_finish:
                return player_finish
            if e.type == player_died:
                return player_died
            if e.type == pause:
                pause_event = pause_menu()
                if pause_event == restart_level or pause_event == back_to_menu:
                    return pause_event
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit("ESCAPE")
            if e.type == KEYDOWN and e.key == K_SPACE:
                event_pause()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        for y in range(48):
            for x in range(48):
                screen.blit(bg, (x * 48, y * 48))

        camera.update(player)
        # update player, draw everything else
        player.update(up, down, left, right, enemies)
        platforms.update()
        enemies.update()

        for e in entities:
            screen.blit(e.image, camera.apply(e))
        button("PAUSE", 10, 10, 100, 50, PRIMARY, PRIMARY_HOVER, event_pause)

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()
