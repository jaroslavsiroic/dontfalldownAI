import sys
import pygame
from pygame import *
from game_objects import *
from settings import *
import numpy as np

# TODO: create a class that would contain inputs' arguments
# TODO (?): convert the output of inputs to something digestible by the existing network classes

def inputs(x, y, cell_width, cell_height, level_width, level_height, platforms, deadly_objects, enemies):
    grid_width = level_width / cell_width
    grid_height = level_height / cell_height
    grid_x = round(x / cell_width)
    grid_y = round(y / cell_height)
    observed_l = grid_x - INPUT_VIEW_RANGE_X
    observed_r = grid_x + INPUT_VIEW_RANGE_X
    observed_u = grid_y - INPUT_VIEW_RANGE_Y
    observed_d = grid_y + INPUT_VIEW_RANGE_Y
    
    observed = np.zeros((INPUT_VIEW_RANGE_X*2+1,INPUT_VIEW_RANGE_Y*2+1))
    for p in platforms:
        p_x = round(p.rect.left / cell_width)
        p_y = round(p.rect.top / cell_width)
        if observed_l <= p_x <= observed_r and observed_u <= p_y <= observed_d:
            p_x = p_x - grid_x + INPUT_VIEW_RANGE_X
            p_y = p_y - grid_y + INPUT_VIEW_RANGE_Y
            observed[p_x,p_y] = 1
    for d in deadly_objects:
        d_x = round(d.rect.left / cell_width)
        d_y = round(d.rect.top / cell_width)
        if observed_l <= d_x <= observed_r and observed_u <= d_y <= observed_d:
            d_x = d_x - grid_x + INPUT_VIEW_RANGE_X
            d_y = d_y - grid_y + INPUT_VIEW_RANGE_Y
            observed[d_x,d_y] = 2
    for d in enemies:
        d_x = round(d.rect.left / cell_width)
        d_y = round(d.rect.top / cell_width)
        if observed_l <= d_x <= observed_r and observed_u <= d_y <= observed_d:
            d_x = d_x - grid_x + INPUT_VIEW_RANGE_X
            d_y = d_y - grid_y + INPUT_VIEW_RANGE_Y
            observed[d_x,d_y] = 2
    return observed