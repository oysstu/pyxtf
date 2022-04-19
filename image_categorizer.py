from distutils import file_util
import pyxtf
import numpy as np
import os
import keyboard
import pygame
import shutil

from PIL import Image

pygame.init()


sort_dir = "Generated PNGs"

dir = sort_dir
if not os.path.isdir(dir):
    os.mkdir(dir)

Cat1 = "Category 1"
if not os.path.isdir(os.path.join(sort_dir,Cat1)):
    os.mkdir(os.path.join(sort_dir,Cat1))

Cat2 = "Category 2"
if not os.path.isdir(os.path.join(sort_dir,Cat2)):
    os.mkdir(os.path.join(sort_dir,Cat2))


file_list = os.listdir(sort_dir)
png_list = [value for value in file_list if value.endswith("png")]

for i in range(len(png_list)):
    png_list[i] = os.path.join(sort_dir,png_list[i])

info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h


running = True
img_number = 0

def draw_image(file):
    img_size = (1200, 1200)
    img_upper_left = (screen_width/2-img_size[0]/2,screen_height/2-img_size[1]/2)

    #if file.endswith(".png"):
    picture = pygame.image.load(file)
    picture = pygame.transform.scale(picture, img_size)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.blit(picture, img_upper_left)

def move_to_category(category, file):
    shutil.move(file,os.path.join(sort_dir,category))
    print(file + " moved to " + category)

while running:

    # it's important to get all events from the 
    # event queue; otherwise it may get stuck
    for event in pygame.event.get():
        draw_image(png_list[img_number])
        if event.type == pygame.QUIT:
            running = False
        if img_number == len(png_list):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_to_category(Cat1,png_list[img_number])
                img_number+=1
            if event.key == pygame.K_RIGHT:
                move_to_category(Cat2,png_list[img_number])
                img_number+=1
            if event.key == pygame.K_ESCAPE:
                running = False

        
    pygame.display.update()


