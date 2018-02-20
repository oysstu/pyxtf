import numpy as np
import matplotlib.pyplot as plt
from pyxtf import xtf_read, concatenate_channel, XTFHeaderType


# Read file header and packets
# The following file and others can be downloaded from
# www.tritonimaginginc.com/site/content/public/downloads/DemoFiles/DemoFiles.zip
test_path = r'Reson7125.XTF'
(fh, p) = xtf_read(test_path)

print('The following (supported) packets are present (XTFHeaderType:count): \n\t' +
      str([key.name + ':{}'.format(len(v)) for key, v in p.items()]))

# Get multibeam (xyza) if present
if XTFHeaderType.bathy_xyza in p:
    np_mb = [[y.fDepth for y in x.data] for x in p[XTFHeaderType.bathy_xyza]]
    np_mb = np.vstack(np_mb)
    # Transpose if the longest axis is vertical
    is_horizontal = np_mb.shape[0] < np_mb.shape[1]
    np_mb = np_mb if is_horizontal else np_mb.T
    plt.figure()
    plt.imshow(np_mb, cmap='hot')
    plt.colorbar(orientation='horizontal')

# Get sonar if present
if XTFHeaderType.sonar in p:
    upper_limit = 2 ** 16
    np_chan1 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=0, weighted=True)
    np_chan2 = concatenate_channel(p[XTFHeaderType.sonar], file_header=fh, channel=1, weighted=True)

    # Clip to range (max cannot be used due to outliers)
    # More robust methods are possible (through histograms / statistical outlier removal)
    np_chan1.clip(0, upper_limit - 1, out=np_chan1)
    np_chan2.clip(0, upper_limit - 1, out=np_chan2)

    # The sonar data is logarithmic (dB), add small value to avoid log10(0)
    np_chan1 = np.log10(np_chan1 + 1, dtype=np.float32)
    np_chan2 = np.log10(np_chan2 + 1, dtype=np.float32)

    # Transpose so that the largest axis is horizontal
    np_chan1 = np_chan1 if np_chan1.shape[0] < np_chan1.shape[1] else np_chan1.T
    np_chan2 = np_chan2 if np_chan2.shape[0] < np_chan2.shape[1] else np_chan2.T

    # The following plots the waterfall-view in separate subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.imshow(np_chan1, cmap='gray', vmin=0, vmax=np.log10(upper_limit))
    ax2.imshow(np_chan2, cmap='gray', vmin=0, vmax=np.log10(upper_limit))
    fig.tight_layout()

    # The following plots a waterfall-view of the 100th ping (in the file)
    # fig, (ax1, ax2) = plt.subplots(2,1)
    # ax1.plot(np.arange(0, np_chan1.shape[1]), np_chan1[196, :])
    # ax2.plot(np.arange(0, np_chan2.shape[1]), np_chan2[196, :])

if XTFHeaderType.attitude in p:
    pings = p[XTFHeaderType.attitude]  # type: List[XTFAttitudeData]
    heave = [ping.Heave for ping in pings]
    pitch = [ping.Pitch for ping in pings]
    roll = [ping.Roll for ping in pings]
    heading = [ping.Heading for ping in pings]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(range(0, len(heave)), heave, label='heave')
    ax1.plot(range(0, len(pitch)), pitch, label='pitch')
    ax1.plot(range(0, len(roll)), roll, label='roll')
    ax1.legend()
    ax2.plot(range(0, len(heading)), heading, label='heading')
    ax2.legend()
    fig.tight_layout()

if XTFHeaderType.navigation in p:
    pings = p[XTFHeaderType.navigation]  # type: List[XTFHeaderNavigation]
    alt = [ping.RawAltitude for ping in pings]
    x = [ping.RawXcoordinate for ping in pings]
    y = [ping.RawYcoordinate for ping in pings]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.plot(range(0, len(alt)), alt, label='altitude')
    ax1.set_title('altitude')
    ax2.plot(range(0, len(x)), x, label='x')
    ax2.set_title('x')
    ax3.plot(range(0, len(y)), y, label='y')
    ax3.set_title('y')
    fig.tight_layout()

plt.show()
