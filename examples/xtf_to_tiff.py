import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pyxtf import xtf_read, concatenate_channel, XTFHeaderType

# Read file header and packets
test_path = 'test.xtf'
(fh, p) = xtf_read(test_path)

# Get sonar if present
if XTFHeaderType.sonar in p:
    upper_limit = 2 ** 16
    np_chan = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=0, weighted=True)
    
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
    img.save('uint16_image.tiff')

    # Scaling values to fit datatype uint8
    np_chan_8bit = ((np_chan - vmin) / (vmax - vmin)) * 255
    np_chan_8bit = np.clip(np_chan_8bit, 0, 255)

    # Resizing width only and storing image as uint8
    img = Image.fromarray(np_chan_8bit.astype(np.uint8))
    img = img.resize((int(img.size[0]/2), img.size[1]), Image.Resampling.LANCZOS)
    img.save('uint8_image.tiff')