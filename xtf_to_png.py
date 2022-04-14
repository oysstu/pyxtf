from turtle import right
import pyxtf
import numpy as np
import os

from PIL import Image


def generate_pngs(input_file):
    (file_header, packets) = pyxtf.xtf_read(input_file)

    # Retrieve a list of all sonar packets
    sonar_packets = packets[pyxtf.XTFHeaderType.sonar]
    # The Width and Height of a sidescan image
    w1 = np.size(sonar_packets[0].data[0])
    w2 = np.size(sonar_packets[0].data[1])
    h_total = len(sonar_packets)
    #h_total = 1500

    # Height of devided image sections
    h = w1
    # To store pixels
    t_left = (h_total, w1, 3)
    t_right = (h_total, w2, 3)
    # RGB colours of the printout
    #colour = (1, 0.8, 0.5)
    colour = (1, 1, 1)
    # Scale pixel intensity
    scale = 1



    dir = "Generated PNGs"
    if not os.path.isdir(dir):
        os.mkdir(dir)


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

    for k in range(0,h_total,w1):
        img_left = Image.fromarray(Left[k:k+w1], "RGB")
        img_left.save(dir + "/" + input_file + "_" + str(k//h) + "_left.png")
        img_right = Image.fromarray(Right[k:k+w1], "RGB")
        img_right.save(dir + "/" + input_file + "_" + str(k//h) + "_right.png")


        # img.show()


    return

"""
# Go through all files in current directory.
for file in os.listdir():
    # I files is xtf, generate png's from it.
    if file.endswith(".xtf"):
        generate_pngs(file)
"""
generate_pngs("testfil.xtf")
