"""
Example of how to write an XTF file from other source.
All fields that are marked as required in the XTF spec are filled with a value.
"""

import pyxtf
import datetime
import numpy as np
import ctypes

#
# Setup dummy data
#

# Note: Enum to ctype conversion
#       must either append .value or cast to int (even though it derives from IntEnum)

# Initialize file header
fh = pyxtf.XTFFileHeader()
fh.SonarName = b'TestWriter'
fh.SonarType = pyxtf.XTFSonarType.unknown1
fh.NavUnits = pyxtf.XTFNavUnits.latlon.value
fh.NumberOfSonarChannels = 2

# Port chaninfo
fh.ChanInfo[0].TypeOfChannel = pyxtf.XTFChannelType.port.value
fh.ChanInfo[0].SubChannelNumber = 0
fh.ChanInfo[0].BytesPerSample = 1
fh.ChanInfo[0].SampleFormat = pyxtf.XTFSampleFormat.byte.value

# Stbd chaninfo
fh.ChanInfo[1].TypeOfChannel = pyxtf.XTFChannelType.stbd.value
fh.ChanInfo[1].SubChannelNumber = 1
fh.ChanInfo[1].BytesPerSample = 1
fh.ChanInfo[1].SampleFormat = pyxtf.XTFSampleFormat.byte.value

# Create fake pings
pings = []
for i in range(10):
    t = datetime.datetime.now()

    p = pyxtf.XTFPingHeader()
    p.HeaderType = pyxtf.XTFHeaderType.sonar.value
    p.NumChansToFollow = 2
    p.Year = t.year
    p.Month = t.month
    p.Day = t.day
    p.Hour = t.hour
    p.Minute = t.minute
    p.Second = t.second
    p.HSeconds = int(t.microsecond / 1e4)
    p.PingNumber = i
    p.SoundVelocity = 1500
    p.WaterTemperature = 8
    p.FixTimeHour = t.hour
    p.FixTimeMinute = t.minute
    p.FixTimeSecond = t.second
    p.FixTimeHsecond = int(t.microsecond / 1e4)
    p.SensorSpeed = 1.5
    p.SensorXcoordinate = 45.0
    p.SensorYcoordinate = 45.0
    p.SensorDepth = 100
    p.SensorPrimaryAltitude = 10
    p.SensorPitch = 15
    p.SensorRoll = 0
    p.SensorHeading = 45

    # Setup ping chan headers
    n_samp = 20
    c = (pyxtf.XTFPingChanHeader(), pyxtf.XTFPingChanHeader())
    c[0].ChannelNumber = 0
    c[0].SlandRange = 30
    c[0].Frequency = 340
    c[0].NumSamples = n_samp
    c[1].ChannelNumber = 1
    c[1].SlandRange = 30
    c[1].Frequency = 340
    c[1].NumSamples = n_samp

    p.ping_chan_headers = c

    # Data
    d0 = np.arange(0, n_samp, 1, dtype=np.uint8)*(i+1)
    d1 = np.arange(n_samp, 0, -1, dtype=np.uint8)*(i+1)
    p.data = [d0, d1]

    # Set packet size
    sz = ctypes.sizeof(pyxtf.XTFPingHeader)
    sz += ctypes.sizeof(pyxtf.XTFPingChanHeader) * 2
    sz += len(d0) + len(d1)
    p.NumBytesThisRecord = sz

#
# Write to file
#

with open('test.xtf', 'wb') as f:
    # Write file header
    f.write(bytes(fh))

    for p in pings:
        f.write(bytes(p))

        # Write ping channel headers and data
        # TODO: Make __bytes__ do this automatically for XTFPingHeader
        for c, d in zip(p.ping_chan_headers, p.data):
            f.write(bytes(c))
            f.write(bytes(d))






