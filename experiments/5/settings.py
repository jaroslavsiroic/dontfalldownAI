import pygame

WIN_WIDTH = 1200
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

CELL_WIDTH = 48
CELL_HEIGHT = 48

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

player_finish = pygame.USEREVENT + 1
player_died = pygame.USEREVENT + 2
restart_level = pygame.USEREVENT + 3
back_to_menu = pygame.USEREVENT + 4
resume = pygame.USEREVENT + 5
pause = pygame.USEREVENT + 6
next_level = pygame.USEREVENT + 7

#colors
WHITE = (200, 200, 200)
BLACK = (20, 20, 20)

FONT = "timesnewromance"
FONT2 = "comicsansms"
PRIMARY = (0, 200, 0)
PRIMARY_HOVER = (0, 250, 0)

DANGER = (200, 0, 0)
DANGER_HOVER = (250, 0, 0)

SEED = 123
INPUT_VIEW_RANGE_X = 3
INPUT_VIEW_RANGE_Y = 3

INPUT_OUTPUT_DEBUG = 1
OUTPUT_SIZE  = 3

MAX_GENERATIONS = 50