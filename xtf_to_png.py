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
    # Height of devided image seqtions
    h = w1+w2
    # To store pixels
    t = (h, w1+w2, 3)
    # RGB colours of the printout
    #colour = (1, 0.8, 0.5)
    colour = (1, 1, 1)
    # Scale pixel intensity
    scale = 1

    """
    # Creation of Array
    A=np.zeros(t,dtype=np.uint8)   # Creates all Zeros Datatype Unsigned Integer
    for j in range(h):
        for k in range(w1):
            pix = scale*sonar_packets[j].data[0][k]%256
            A[j,k]=[pix*colour[0],pix*colour[1],pix*colour[2]]    # Assigning Colors to Each Pixel 
        for k in range(w1,w2+w1):
            pix = scale*sonar_packets[j].data[1][k-w1]%256
            A[j,k]=[pix*colour[0],pix*colour[1],pix*colour[2]]    # Assigning Colors to Each Pixel
    """

    dir = "Generated PNGs"
    if not os.path.isdir(dir):
        os.mkdir(dir)

    for i in range(0, h_total, h):
        # Creates all Zeros Datatype Unsigned Integer
        Array = np.zeros(t, dtype=np.uint8)

        for j in range(h):
            if i+j > h_total-1:
                break
            for k in range(w1):
                pix = scale*sonar_packets[i+j].data[0][k] % 256
                # Assigning Colors to Each Pixel
                Array[j, k] = [pix*colour[0], pix*colour[1], pix*colour[2]]
            for k in range(w1, w2+w1):
                pix = scale*sonar_packets[i+j].data[1][k-w1] % 256
                # Assigning Colors to Each Pixel
                Array[j, k] = [pix*colour[0], pix*colour[1], pix*colour[2]]
        img = Image.fromarray(Array, "RGB")
        img.save(dir + "/" + input_file + "_" + str(i//h) + ".png")

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
