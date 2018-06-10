import sys
import pygame
from pygame import *
from game_objects import *
from settings import *
import numpy as np

# TODO: create a class that would contain inputs' arguments
# TODO (?): convert the output of inputs to something digestible by the existing network classes

def sprites_to_level_array(target,sprite_group,value):
    level_width = target.shape[0]
    level_height = target.shape[1]
    for p in sprite_group:
        x = round(p.rect.left / CELL_WIDTH)
        y = round(p.rect.top / CELL_HEIGHT)
        if 0 <= x < level_width and 0 <= y < level_height:
            target[int(x),int(y)] = value

def inputs(level_array,x,y):
    level_width = level_array.shape[0]
    level_height = level_array.shape[1]
    observed_width = INPUT_VIEW_RANGE_X*2+1
    observed_height = INPUT_VIEW_RANGE_Y*2+1
    observed = np.zeros((observed_width,observed_height))
    
    center_x = round(x / CELL_WIDTH)
    center_y = round(y / CELL_HEIGHT)
    
    observed_level_left = max(0,min(level_width,center_x - INPUT_VIEW_RANGE_X))
    observed_level_top = max(0,min(level_height,center_y - INPUT_VIEW_RANGE_Y))
    observed_level_right = max(0,min(level_width,center_x + INPUT_VIEW_RANGE_X + 1))
    observed_level_bottom = max(0,min(level_height,center_y + INPUT_VIEW_RANGE_Y + 1))
    
    if observed_level_left == observed_level_right or observed_level_top == observed_level_bottom:
        return observed
    
    level_observed_left = max(0,min(observed_width,-(center_x - INPUT_VIEW_RANGE_X)))
    level_observed_top = max(0,min(observed_height,-(center_y - INPUT_VIEW_RANGE_Y)))
    level_observed_right = max(0,min(observed_width,observed_width-(center_x + INPUT_VIEW_RANGE_X + 1 - level_width)))
    level_observed_bottom = max(0,min(observed_height,observed_height-(center_y + INPUT_VIEW_RANGE_Y + 1 - level_height)))
    
    observed[level_observed_left:level_observed_right,level_observed_top:level_observed_bottom] = level_array[observed_level_left:observed_level_right,observed_level_top:observed_level_bottom]
    return observed