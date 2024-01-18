import sys
import pygame
from pygame import *
from game_objects import *
from settings import *
from network import *
from population import *
from genome import *
from level_design import levels
from input import *
import numpy as np
from time import gmtime, strftime
global cameraX, cameraY
import pandas as pd
# TODO: remove/alter all code marked with "inputs debug functionality" when inputs method is assured to work

pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Don't Fall Down!")
timer = pygame.time.Clock()

is_paused = False
bestFitness = 0
informationforscreen = None
today = "./saved/" + strftime("%Y_%m_%d__%H_%M_%S", gmtime())

menu_background = pygame.image.load('assets/background_menu.png').convert()
tutorial_background = pygame.image.load('assets/background_and_tutorial.png').convert()

debug_images = []
for i in range(0, 3, 1):
    image = pygame.image.load('assets/debugcell{0}.png'.format(i)).convert()
    image = pygame.transform.scale(image, (48, 48))
    debug_images.append(image)

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


#inputs debug functionality
def pause_menu(test_array):
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == back_to_menu \
                    or event.type == resume:
                return event.type
        largeText = pygame.font.SysFont(FONT, 115)
        TextSurf, TextRect = text_objects("Game paused", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, 50)
        screen.blit(TextSurf, TextRect)

        button("Resume", HALF_WIDTH-100, 200, 200, 50, PRIMARY, PRIMARY_HOVER, event_resume)
        button("Back to menu", HALF_WIDTH-100, 320, 200, 50, DANGER, DANGER_HOVER, event_back_to_menu)

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

        button("Begin", HALF_WIDTH-100, 200, 200, 50, PRIMARY, PRIMARY_HOVER, level_menu)
        #button("Tutorial", HALF_WIDTH - 100, 260, 200, 50, PRIMARY, PRIMARY_HOVER, tutorial)
        button("Quit", HALF_WIDTH-100, 320, 200, 50, DANGER, DANGER_HOVER, exit_game)

        largeText = pygame.font.SysFont(FONT2, 20)
        TextSurf, TextRect = text_objects("Game developed by Jaroslav Siroic [2017-12]", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, WIN_HEIGHT-30)
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("AI with evolutionary algorithm developed by Jaroslav Siroic and Jakub Mazurkiewicz [2018-06]", largeText, WHITE)
        TextRect.center = (HALF_WIDTH, WIN_HEIGHT-15)
        screen.blit(TextSurf, TextRect)

        pygame.display.update()
        timer.tick(15)


def score_board():
    if informationforscreen != None:
        largeText = pygame.font.SysFont(FONT, 20)
        TextSurf, TextRect = text_objects("Generation: {0}".format(informationforscreen['generation']), largeText, WHITE)
        TextRect.top = 15
        TextRect.left = WIN_WIDTH - 200
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("Bot NR: {0}".format(informationforscreen['botnumber']), largeText, WHITE)
        TextRect.top = 30
        TextRect.left = WIN_WIDTH - 200
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("Last fitness: {0}".format(informationforscreen['lastfitness']), largeText, WHITE)
        TextRect.top = 45
        TextRect.left = WIN_WIDTH - 200
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("Last Gen avg fitness: {0}".format(informationforscreen['lastgenerationaveragefitness']), largeText, WHITE)
        TextRect.top = 60
        TextRect.left = WIN_WIDTH - 200
        screen.blit(TextSurf, TextRect)
        TextSurf, TextRect = text_objects("Best fitness: {0}".format(informationforscreen['bestfitness']), largeText, WHITE)
        TextRect.top = 75
        TextRect.left = WIN_WIDTH - 200
        screen.blit(TextSurf, TextRect)


def level_menu(level=levels[0], index=0):

    localBestFitness = -1
    population = Population()
    population.generateRandomPopulation()
    generation = 1
    results = pd.DataFrame(columns=['generation', 'fitness'])
    lastgenerationaveragefitness = 0
    #Main Loop
    while generation <= MAX_GENERATIONS :
        botnmbr = 1

        for i in range(population.size()):

            level_output = launch_level(levels[0], population.getGenome(i))
            if level_output['event'] == player_finish:
                you_win_event = you_win_menu(index)
                if you_win_event['event'] == restart_level:
                    level_menu(level, index)
                elif you_win_event['event'] == next_level:
                    level_menu(levels[index+1], index+1)
            if level_output['event'] == player_died:
                game_over_event = game_over_menu()
                if game_over_event == restart_level:
                    level_menu(level, index)
            if level_output['event'] == restart_level:
                score = level_output['score']
                results.loc[len(results)] = [generation, score]
                population.setGenomeFitness(i,score)
                global informationforscreen
                informationforscreen = {
                    'generation' : generation,
                    'botnumber' : botnmbr,
                    'lastfitness' : score,
                    'lastgenerationaveragefitness' : lastgenerationaveragefitness,
                    'bestfitness' : localBestFitness
                }
                if score > localBestFitness:
                    global bestFitness
                    bestFitness = score
                    localBestFitness = score
                    genome = level_output['genome']
                    genome.network.save(today + "/bestfitness.json")
                botnmbr += 1


        # global fitnessovergeneration
        # fitnessovergeneration.append(population.averageFitness())

        lastgenerationaveragefitness = population.averageFitness()

        # global fittestovergeneration
        # fittestovergeneration.append(population.findFittest().fitness)
        #Evolve the population
        population.evolvePopulation()
        generation += 1
        results.to_csv(today + '/results.csv')

def launch_level(level=levels[0], genome=None):

    genome.network.fromgenes(genome.genes)

    up = down = left = right = False
    entities = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    deadly_objects = pygame.sprite.Group()
    bots = pygame.sprite.Group()
    #inputs debug functionality
    if INPUT_OUTPUT_DEBUG == 1:
        specific_bot = None
        input_randomization_frame_max = 3
        input_randomization_frame_countdown = input_randomization_frame_max
    #inputs debug functionality
    player = None
    x = y = 0
    STARTX = 0
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
            if col == "B":
                STARTX = x
                for i in range(1):
                    bot = Bot(x, y, platforms, deadly_objects, enemies)
                    bots.add(bot)
                    entities.add(bot)
                    #inputs debug functionality
                    # if INPUT_OUTPUT_DEBUG == 1:
                    specific_bot = bot
            if col == "E":
                e = Enemy(x, y, platforms, timer, deadly_objects)
                entities.add(e)
                enemies.add(e)
            x += CELL_WIDTH
        y += CELL_HEIGHT
        x = 0

    total_level_width = len(level[0])*CELL_WIDTH
    total_level_height = len(level)*CELL_HEIGHT
    camera = Camera(complex_camera, total_level_width, total_level_height)

    level_width = len(level[0])
    level_height = len(level)
    level_array = np.zeros((level_width,level_height))
    in_game = True
    return_object = {
        'event': None,
        'genome': None,
        'score': None
    }

    while in_game:
        timer.tick(4000)

        for e in pygame.event.get():
            if e.type == QUIT:
                exit_game()
            if e.type == player_finish:
                return_object['event'] = restart_level
                return_object['genome'] = genome
                return_object['score'] = specific_bot.rect.left - STARTX + 1000
                return return_object
            if e.type == player_died:
                return_object['event'] = player_died
                return return_object
            if e.type == restart_level:
                return_object['event'] = restart_level
                return_object['genome'] = genome
                return_object['score'] = specific_bot.rect.left - STARTX
                return return_object
            if e.type == pause:
                #inputs debug functionality
                if INPUT_OUTPUT_DEBUG == 1:
                    if specific_bot != None:
                        test_array = inputs(level_array,specific_bot.rect.left,specific_bot.rect.top)
                    else:
                        test_array = inputs(level_array,0,0)
                else:
                    test_array = None
                pause_event = pause_menu(test_array)
                #inputs debug functionality
                if pause_event == restart_level or pause_event == back_to_menu:
                    return_object['event'] = pause_event
                    return return_object
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

        if player == None and len(bots.sprites()) > 0:
            camera.update(sorted(bots.sprites(), reverse=True, key=lambda b: b.rect.left)[0])
        elif player != None:
            camera.update(player)
            player.update(up, down, left, right, enemies)
        elif len(bots.sprites()) == 0:
            event_restart_level()
        # update player, draw everything else

        level_array.fill(0)
        sprites_to_level_array(level_array,platforms,1)
        sprites_to_level_array(level_array,deadly_objects,-1)
        sprites_to_level_array(level_array,enemies,-1)

        debug_array = inputs(level_array,specific_bot.rect.left,specific_bot.rect.top)
        NNinput = debug_array.flatten()
        NNinput = np.reshape(NNinput, (NNinput.shape[0],-1))
        specific_bot.input_table = genome.network.feedforward(NNinput)

        platforms.update()
        enemies.update()
        bots.update()

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        #inputs debug functionality
        if INPUT_OUTPUT_DEBUG == 1:
            for x in range(0,INPUT_VIEW_RANGE_X*2+1):
                for y in range(0,INPUT_VIEW_RANGE_Y*2+1):
                    p = int(debug_array[x,y])
                    if -1 <= p <= 1:
                        screen.blit(debug_images[p+1],(x*48,y*48))
                    else:
                        screen.blit(debug_images[1],(x*48,y*48))
                        largeText = pygame.font.SysFont(FONT, 40)
                        TextSurf, TextRect = text_objects(str(p), largeText, WHITE)
                        TextRect.center = (x*48+24, y*48+24)
                        screen.blit(TextSurf, TextRect)

            largeText = pygame.font.SysFont(FONT, 40)
            TextSurf, TextRect = text_objects("LEFT", largeText, DANGER if specific_bot.left else WHITE)
            TextRect.top = WIN_HEIGHT-50
            TextRect.left = 200
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects("JUMP", largeText, DANGER if specific_bot.up else WHITE)
            TextRect.top = WIN_HEIGHT-50
            TextRect.left = 300
            screen.blit(TextSurf, TextRect)
            TextSurf, TextRect = text_objects("RIGHT", largeText, DANGER if specific_bot.right else WHITE)
            TextRect.top = WIN_HEIGHT-50
            TextRect.left = 400
            screen.blit(TextSurf, TextRect)
        #inputs debug functionality

        button("PAUSE", 10, WIN_HEIGHT-60, 100, 50, PRIMARY, PRIMARY_HOVER, event_pause)
        score_board()
        pygame.display.flip()


if __name__ == "__main__":
    if len(sys.argv) != 1:
        #Evaluate a single genome
        if str(sys.argv[1])=="-evaluate":
            print(str(sys.argv[2]))
            net = load(str(sys.argv[2]))
            genome = Genome(net)
            global savestat
            savestat = False
            fitness = []
            for i in range(100):
                level_output = launch_level(levels[0], genome)
                if level_output['event'] == restart_level:
                    score = level_output['score']
                    fitness.append(score)
                    print("fitness : %s " % score)

            average = sum(fitness) / float(len(fitness))
            printc("Average fitness : %s" % average,"red")
            pygame.quit()
            sys.exit()
        #Show the stat of an experiment
        if str(sys.argv[1])=="-stats":
            pass
            # showStat(str(sys.argv[2]))
    else:
        main_menu()
