from turtle import right
import pyxtf
import numpy as np
import os

from PIL import Image


def generate_pngs(input_file):
    print("Generating PNGs from " + input_file)
    (file_header, packets) = pyxtf.xtf_read(input_file)

    # Retrieve a list of all sonar packets
    sonar_packets = packets[pyxtf.XTFHeaderType.sonar]
    # The Width and Height of a sidescan image
    w1 = np.size(sonar_packets[0].data[0])
    w2 = np.size(sonar_packets[0].data[1])
    h_total = len(sonar_packets)
    #h_total = 1250

    # Height of devided image sections
    img_height = w1
    # To store pixels
    t_left = (h_total, w1, 3)
    t_right = (h_total, w2, 3)
    # RGB colours of the printout
    #colour = (1, 0.8, 0.5)
    colour = (1, 1, 1)
    # Scale pixel intensity
    scale = 1

    input_file = input_file.split(os.path.sep)[-1]



    png_dir = "Generated PNGs"
    if not os.path.isdir(png_dir):
        os.mkdir(png_dir)


    # Creates all Zeros Datatype Unsigned Integer
    Left = np.zeros(t_left, dtype=np.uint8)
    Right = np.zeros(t_right, dtype=np.uint8)

    for i in range(h_total):
        for j in range(w1):
            pix = scale*sonar_packets[i].data[0][j] % 256
            # Assigning Colors to Each Pixel
            Left[i, j] = [pix*colour[0], pix*colour[1], pix*colour[2]]
        for j in range(w2):
            pix = scale*sonar_packets[i].data[1][j] % 256
            # Assigning Colors to Each Pixel
            Right[i, j] = [pix*colour[0], pix*colour[1], pix*colour[2]]

    # See if last image will be too wide compared to its height
    if h_total % w1 > w1*0.5:
        # Height is more than half of width
        for k in range(0,h_total,w1):
            img_left = Image.fromarray(Left[k:k+w1], "RGB")
            filename_left = input_file + "_" + str(k//img_height).zfill(4) + "_left.png"
            img_left.save(os.path.join(png_dir,filename_left))
            img_right = Image.fromarray(Right[k:k+w1], "RGB")
            filename_right = input_file + "_" + str(k//img_height).zfill(4) + "_right.png"
            img_right.save(os.path.join(png_dir,filename_right))
    else:
        # Height is less than half of width. Merge last image with second to last
        # Save all but last image.
        for k in range(0,h_total-w1,w1):
            img_left = Image.fromarray(Left[k:k+w1], "RGB")
            filename_left = input_file + "_" + str(k//img_height).zfill(4) + "_left.png"
            img_left.save(os.path.join(png_dir,filename_left))
            img_right = Image.fromarray(Right[k:k+w1], "RGB")
            filename_right = input_file + "_" + str(k//img_height).zfill(4) + "_right.png"
            img_right.save(os.path.join(png_dir,filename_right))
        # Save last image.
        img_left = Image.fromarray(Left[k:k+2*w1], "RGB")
        filename_left = input_file + "_" + str(k//img_height).zfill(4) + "_left.png"
        img_left.save(os.path.join(png_dir,filename_left))
        img_right = Image.fromarray(Right[k:k+2*w1], "RGB")
        filename_right = input_file + "_" + str(k//img_height).zfill(4) + "_right.png"
        img_right.save(os.path.join(png_dir,filename_right))



        # img.show()
    return

xtf_dir = "XTF files"
if not os.path.isdir(xtf_dir):
    os.mkdir(xtf_dir)

# Go through all files in directory xtf_dir.
for file in os.listdir(xtf_dir):
    # If file is xtf, generate png's from it.
    if file.endswith(".xtf"):
        generate_pngs(os.path.join(xtf_dir,file))




#generate_pngs("testfil.xtf")
