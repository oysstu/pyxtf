#from sympy import N, false
import numpy as np
import os

import pygame

pygame.init()


info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
screen_width,screen_height = info.current_w,info.current_h

img_size = (1200, 1200)

print(screen_height, screen_width)