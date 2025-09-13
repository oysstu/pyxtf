"""
Example of how to convert an XTF file to an image (.png).
Toggle resize_half_width if your image width needs to be resized to half width.
Toggle concatenate_channel weighted argument to fit your data requirements.
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from pyxtf import xtf_read, concatenate_channel, XTFHeaderType

# Read file header and packets
test_path = 'test.xtf'
(fh, p) = xtf_read(test_path)

resize_half_width = True # Resize image, half width
weighted = True # Toggle concatenate_channel weighted argument to fit your data input requirements

# Get sonar packets if present
if XTFHeaderType.sonar in p:
    upper_limit = 2 ** 16

    # Concatenate all sonar packet data in channel 0
    np_chan = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=0, weighted=weighted)
    
    # Clip to range (max cannot be used due to outliers)
    # More robust methods are possible (through histograms / statistical outlier removal)
    np_chan.clip(0, upper_limit - 1, out=np_chan)

    # The sonar data is logarithmic (dB), add small value to avoid log10(0)
    np_chan = np.log10(np_chan + 1, dtype=np.float32)

    # Need to find minimum and maximum value for scaling
    vmin = np_chan.min()
    vmax = np_chan.max()

    # Scaling values to fit datatype uint16
    np_chan_16bit = ((np_chan - vmin) / (vmax - vmin)) * 65535
    np_chan_16bit = np.clip(np_chan_16bit, 0, 65535)

    # Storing image as uint16
    img = Image.fromarray(np_chan_16bit.astype(np.uint16))
    if resize_half_width: # Resizing to half width
        img = img.resize((int(img.size[0]/2), img.size[1]))
    img.save('test_16bit.png')

    # Scaling values to fit datatype uint8
    np_chan_8bit = ((np_chan - vmin) / (vmax - vmin)) * 255
    np_chan_8bit = np.clip(np_chan_8bit, 0, 255)

    # Storing image as uint8
    img = Image.fromarray(np_chan_8bit.astype(np.uint8))
    if resize_half_width: # Resizing to half width
        img = img.resize((int(img.size[0]/2), img.size[1]))
    img.save('test_8bit.png')