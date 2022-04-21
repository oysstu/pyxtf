from distutils import file_util
import pyxtf
import numpy as np
import os
import keyboard
import pygame
import shutil

from PIL import Image

pygame.init()

#sort_dir = "Generated PNGs"
sort_dir = "Test PNGs"

dir = sort_dir
if not os.path.isdir(dir):
    os.mkdir(dir)

Cat_A = "Category A"
if not os.path.isdir(os.path.join(sort_dir,Cat_A)):
    os.mkdir(os.path.join(sort_dir,Cat_A))

Cat_B = "Category B"
if not os.path.isdir(os.path.join(sort_dir,Cat_B)):
    os.mkdir(os.path.join(sort_dir,Cat_B))


file_list = os.listdir(sort_dir)
png_list = [value for value in file_list if value.endswith("png")]

for i in range(len(png_list)):
    png_list[i] = os.path.join(sort_dir,png_list[i])

info = pygame.display.Info()
screen_width,screen_height = info.current_w,info.current_h
img_size = (1200, 1200)
img_upper_left_h = screen_height/2-img_size[1]/2
img_upper_left_w = screen_width/2-img_size[0]/2

img_upper_left_h = (img_upper_left_h+abs(img_upper_left_h))/2
img_upper_left_w = (img_upper_left_w+abs(img_upper_left_w))/2

img_upper_left = (img_upper_left_w,img_upper_left_h)


running = True
img_number = 0
cat_A_sorted = 0
cat_B_sorted = 0

def draw_image(file):
    #if file.endswith(".png"):
    picture = pygame.image.load(file)
    picture = pygame.transform.scale(picture, img_size)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.blit(picture, img_upper_left)

def move_to_category(category, file):
    #shutil.move(file,os.path.join(sort_dir,category))
    print(file + " moved to " + category)

while running:

    if img_number == len(png_list):
        running = False

    # it's important to get all events from the 
    # event queue; otherwise it may get stuck
    for event in pygame.event.get():
        draw_image(png_list[img_number])
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_to_category(Cat_A,png_list[img_number])
                img_number+=1
                cat_A_sorted+=1
            if event.key == pygame.K_RIGHT:
                move_to_category(Cat_B,png_list[img_number])
                img_number+=1
                cat_B_sorted+=1
            if event.key == pygame.K_ESCAPE:
                running = False
        
    pygame.display.update()

print("=========================================")
print("%d images sorted. %d in category A and %d in category B." % 
    (img_number, cat_A_sorted, cat_B_sorted))

tot_A_sorted = len(os.listdir(os.path.join(sort_dir,Cat_A)))
tot_B_sorted = len(os.listdir(os.path.join(sort_dir,Cat_B)))

print("Total sorted in A: %d. Total sorted in B: %d." % (tot_A_sorted, tot_B_sorted))
print("=========================================")

