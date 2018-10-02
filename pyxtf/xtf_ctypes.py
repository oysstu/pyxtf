import ctypes
from datetime import date
from io import IOBase, BytesIO
from typing import List
import numpy as np
from warnings import warn

from pyxtf.enumerations import *


# General notes from the XTF format document (rev35)
# 1. All structures should be zero-filled before use.
# 2. Unused values should remain zero.
# 3. File header is a multiple of 1024 bytes (1024 added for each multiple of 6 channels)

"""
XTF Data types - nbytes:
char    - 1 (signed)
short   - 2 (signed)
int     - * (signed) OS dependent size
long    - 4 (signed)
float   - 4
double  - 8
BYTE    - 1 (unsigned)
WORD    - 2 (unsigned)
DWORD   - 4 (unsigned)
Hex     - 0x0
"""

# Mapping from number of bytes to the unsigned numpy type
xtf_dtype = {
    1: np.uint8,
    2: np.uint16,
    4: np.uint32,
    8: np.uint64
}

"""
SampleFormat field added in X41
0 = Legacy 
1 = 4-byte IBM float 
2 = 4-byte integer 
3 = 2-byte integer 
4 = unused 
5 = 4-byte IEEE float 
6 = unused 
7 = unused 
8 = 1-byte integer
"""

# Mapping from 'sample format' to the numpy type
sample_format_dtype = {
    2: np.uint32,
    3: np.uint16,
    5: np.float32,
    8: np.uint8
}


class XTFBase(ctypes.LittleEndianStructure):
    """
    Base class for all XTF ctypes.Structure children.
    Exposes basic utility like printing of fields and constructing class from a buffer.
    """

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        """
        Initializes the XTF structure by copying from the target buffer.
        Note: not to be confused with .from_buffer and .from_buffer_copy which are the direct ctypes functions
        :param buffer: Input bytes
        :param file_header: XTFFileHeader, only necessary for XTFPingHeader
        :return:
        """
        if type(buffer) in [bytes, bytearray]:
            buffer = BytesIO(buffer)

        header_bytes = buffer.read(ctypes.sizeof(cls))
        if not header_bytes:
            raise RuntimeError('XTF file shorter than expected (end hit while reading {})'.format(cls.__name__))

        return cls.from_buffer_copy(header_bytes)

    @classmethod
    def view_from_buffer(cls, buffer: IOBase, file_header=None):
        """
        Returns a view of the XTF structure in the buffer without copying.
        :param buffer: Input bytes
        :param file_header: XTFFileHeader, only necessary for XTFPingHeader
        :return:
        """
        raise NotImplementedError("Views has not been implemented")

    def __str__(self):
        """
        Prints the fields in the class (with ctype-fields) in the order in which they appear in the structure.
        """
        fields = []
        for field_name in dir(self):
            if not field_name.startswith('_') and not field_name.endswith('_'):
                field_value = getattr(self, field_name)
                field_type = type(field_value)

                # callable(obj) will return true for the fields, using 'method' name instead
                if not field_type.__name__ == 'method':
                    if hasattr(self.__class__, field_name) and hasattr(getattr(self.__class__, field_name), 'offset'):
                        offset = getattr(self.__class__, field_name).offset
                    else:
                        offset = 2 ** 31

                    if ctypes.Array in field_type.__bases__ and field_type._type_ not in [ctypes.c_char, ctypes.c_wchar]:
                        if len(field_value) > 20:
                            val_str = field_value[:10] + ['...'] + field_value[-10:]
                        else:
                            val_str = list(field_value)
                        out_str = '{}: {}\n'.format(field_name, val_str)
                    else:
                        out_str = '{}: {}\n'.format(field_name, field_value)

                    fields.append((offset, out_str))

        # Sort by offset (non-ctypes placed last)
        fields.sort(key=lambda x: x[0])
        out = ''.join(field[1] for field in fields)

        return out


class XTFChanInfo(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('TypeOfChannel', ctypes.c_uint8),
        ('SubChannelNumber', ctypes.c_uint8),
        ('CorrectionFlags', ctypes.c_uint16),
        ('UniPolar', ctypes.c_uint16),
        ('BytesPerSample', ctypes.c_uint16),
        ('Reserved', ctypes.c_uint32),
        ('ChannelName', ctypes.c_char * 16),
        ('VoltScale', ctypes.c_float),
        ('Frequency', ctypes.c_float),
        ('HorizBeamAngle', ctypes.c_float),
        ('TiltAngle', ctypes.c_float),
        ('BeamWidth', ctypes.c_float),
        ('OffsetX', ctypes.c_float),
        ('OffsetY', ctypes.c_float),
        ('OffsetZ', ctypes.c_float),
        ('OffsetYaw', ctypes.c_float),
        ('OffsetPitch', ctypes.c_float),
        ('OffsetRoll', ctypes.c_float),
        ('BeamsPerArray', ctypes.c_uint16),
        ('SampleFormat', ctypes.c_uint8),
        ('ReservedArea2', ctypes.c_uint8 * 53)
    ]

    def __init__(self):
        super().__init__()
        self.Reserved = 1024  # For compatibility reasons with old viewers


class XTFFileHeader(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('FileFormat', ctypes.c_uint8),
        ('SystemType', ctypes.c_uint8),
        ('RecordingProgramName', ctypes.c_char * 8),
        ('RecordingProgramVersion', ctypes.c_char * 8),
        ('SonarName', ctypes.c_char * 16),
        ('SonarType', ctypes.c_uint16),
        ('NoteString', ctypes.c_char * 64),
        ('ThisFileName', ctypes.c_char * 64),
        ('NavUnits', ctypes.c_uint16),
        ('NumberOfSonarChannels', ctypes.c_uint16),
        ('NumberOfBathymetryChannels', ctypes.c_uint16),
        ('NumberOfSnippetChannels', ctypes.c_uint8),
        ('NumberOfForwardLookArrays', ctypes.c_uint8),
        ('NumberOfEchoStrengthChannels', ctypes.c_uint16),
        ('NumberOfInterferometryChannels', ctypes.c_uint8),
        ('Reserved1', ctypes.c_uint8),
        ('Reserved2', ctypes.c_uint16),
        ('ReferencePointHeight', ctypes.c_float),
        ('ProjectionType', ctypes.c_uint8 * 12),
        ('SpheriodType', ctypes.c_uint8 * 10),
        ('NavigationLatency', ctypes.c_int32),
        ('OriginY', ctypes.c_float),
        ('OriginX', ctypes.c_float),
        ('NavOffsetY', ctypes.c_float),
        ('NavOffsetX', ctypes.c_float),
        ('NavOffsetZ', ctypes.c_float),
        ('NavOffsetYaw', ctypes.c_float),
        ('MRUOffsetY', ctypes.c_float),
        ('MRUOffsetX', ctypes.c_float),
        ('MRUOffsetZ', ctypes.c_float),
        ('MRUOffsetYaw', ctypes.c_float),
        ('MRUOffsetPitch', ctypes.c_float),
        ('MRUOffsetRoll', ctypes.c_float),
        ('ChanInfo', XTFChanInfo * 6)
    ]

    def channel_count(self, verbose: bool = False) -> int:
        """
        Returns the number of separate channels present in the XTF file.
        :param verbose: If true, the number of channels per channel type is printed.
        :return: The total number of channels.
        """
        if verbose:
            print('XTF Channels: sonar={}, bathy={}, snippet={}, forward={}, echo={}, interferometry={}'.format(
                self.NumberOfSonarChannels,
                self.NumberOfBathymetryChannels,
                self.NumberOfSnippetChannels,
                self.NumberOfForwardLookArrays,
                self.NumberOfEchoStrengthChannels,
                self.NumberOfInterferometryChannels)
            )

        n_channels = self.NumberOfSonarChannels \
                   + self.NumberOfBathymetryChannels \
                   + self.NumberOfSnippetChannels \
                   + self.NumberOfForwardLookArrays \
                   + self.NumberOfEchoStrengthChannels \
                   + self.NumberOfInterferometryChannels

        return n_channels

    def __init__(self):
        super().__init__()
        self.FileFormat = 0x7B
        self.SystemType = 1
        # Set ChanInfo[i].Reserved to 1024 for compatibility reasons (used to be NumSamples)
        for i in range(0, 6):
            self.ChanInfo[i].Reserved = 1024
            self.RecordingProgramName = b'pyxtf'
            self.RecordingProgramVersion = b'223'

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer)

        # Initialize additional fields
        obj.subbottom_info = [x for x in obj.ChanInfo if x.TypeOfChannel == XTFChannelType.subbottom]
        sonar_types = (XTFChannelType.port.value, XTFChannelType.stbd.value)
        obj.sonar_info = [x for x in obj.ChanInfo if x.TypeOfChannel in sonar_types][:obj.NumberOfSonarChannels]
        obj.bathy_info = [x for x in obj.ChanInfo if x.TypeOfChannel == XTFChannelType.bathy][:obj.NumberOfBathymetryChannels]

        return obj


class XTFPacket(XTFBase):
    """
    This is base class for all packets to derive from.
    Some packets derive from the subclass XTFPacketStart instead, due to the common first fields present in many packets
    """
    _pack_ = 1
    _fields_ = []

    def get_time(self):
        # All XTF packets has the fields Year, Month, Day, Hour, Minute, Second
        # Some packets come with SourceEpoch (time since 1970-1-1) which is used if present
        # The presence of high-resolution timers vary, and will be checked for (at runtime)

        # Use epoch if available, else calculate from Year-Month-Day etc
        if hasattr(self, 'SourceEpoch') and self.SourceEpoch:
            p_time = np.datetime64(self.SourceEpoch, 's')

            # XTFAttitudeData has an additional epoch field with microseconds
            # Return immediately, as the high-precision fields added later doubles up
            if hasattr(self, 'EpochMicroseconds') and self.EpochMicroseconds:
                p_time += np.timedelta64(self.EpochMicroseconds, 'us')
                return p_time
        else:
            # Numpy does not handle leap years and varying number of days per month
            # Calculate the day from the python.datetime module
            days = (date(self.Year, self.Month, self.Day) - date(self.Year, 1, 1)).days

            # Calculate time using common fields
            p_time = np.datetime64(str(self.Year), 'Y') + \
                     np.timedelta64(days, 'D') + \
                     np.timedelta64(self.Hour, 'h') + \
                     np.timedelta64(self.Minute, 'm') + \
                     np.timedelta64(self.Second, 's')

            # Add time using high-res fields
            if hasattr(self, 'HSeconds'):
                return p_time + np.timedelta64(self.HSeconds*10, 'ms')  # HSeconds = hundredths of a second (0-99)

            if hasattr(self, 'Millisecond'):
                p_time += np.timedelta64(self.Millisecond, 'ms')

            if hasattr(self, 'Microsecond'):
                p_time += np.timedelta64(self.Microsecond, 'us')

        return p_time


class XTFPacketStart(XTFPacket):
    """
    This is a structure representing the first few bytes in (most) of the XTF packets.
    It can be used to inspect the packet type before reading the whole header.
    """
    _pack_ = 1
    _fields_ = [
        ('MagicNumber', ctypes.c_uint16),
        ('HeaderType', ctypes.c_uint8),
        ('SubChannelNumber', ctypes.c_uint8),  # Note: For RawSerialHeader, this is SerialPort (same size)
        ('NumChansToFollow', ctypes.c_uint16),
        ('Reserved1', ctypes.c_uint16 * 2),
        ('NumBytesThisRecord', ctypes.c_uint32)
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header: XTFFileHeader=None):
        obj = super().create_from_buffer(buffer)

        if obj.MagicNumber != 0xFACE:
            raise RuntimeError('XTF packet does not start with the correct identifier (0xFACE).')

        return obj

    def __init__(self):
        super().__init__()

        self.MagicNumber = 0xFACE
        self.HeaderType = XTFHeaderType.user_defined


class XTFUnknownPacket(XTFPacketStart):
    """
    Class for packets without a known implementation. Any data after the header is returned as bytes
    Note: If you have documentation for any of these structures, please let me know
    """
    def __init__(self):
        super().__init__()
        self.data = b''

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header: XTFFileHeader=None):
        obj = super().create_from_buffer(buffer)

        n_bytes = obj.NumBytesThisRecord - ctypes.sizeof(cls)
        obj.data = buffer.read(n_bytes)

        return obj



class XTFAttitudeData(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Reserved2', ctypes.c_uint32 * 2),
        ('EpochMicroseconds', ctypes.c_uint32),
        ('SourceEpoch', ctypes.c_uint32),
        ('Pitch', ctypes.c_float),  # Positive value is nose up
        ('Roll', ctypes.c_float),   # Positive value is roll to starboard
        ('Heave', ctypes.c_float),  # Positive value is sensor up
        ('Yaw', ctypes.c_float),  # Positive value is turn right
        ('TimeTag', ctypes.c_uint32),
        ('Heading', ctypes.c_float),
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Millisecond', ctypes.c_uint16),
        ('Reserved3', ctypes.c_uint8)
        ]

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.attitude


class XTFNotesHeader(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('ReservedBytes', ctypes.c_uint8 * 35),
        ('NotesText', ctypes.c_char * 200)
    ]

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.notes.value


class XTFRawSerialHeader(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('HSeconds', ctypes.c_uint8),  # Hundredths of seconds (0-99)
        ('JulianDay', ctypes.c_uint16),
        ('TimeTag', ctypes.c_uint32),  # Millisecond timer value
        ('StringSize', ctypes.c_uint16)  # After this, the number of ascii bytes follow
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header: XTFFileHeader=None):
        obj = super().create_from_buffer(buffer)
        # TODO: Make getters/setters that updates StringSize when changed
        obj.RawAsciiData = buffer.read(ctypes.sizeof(ctypes.c_char) * obj.StringSize.value)

        return obj

    def __init__(self):
        super().__init__()

        self.RawAsciiData = b''
        self.HeaderType = XTFHeaderType.raw_serial.value

    # Serialport and subchannelnumber is the same variable
    # The documentation uses serialport, so this redirection is added to match the docs
    @property
    def SerialPort(self):
        return self.SubChannelNumber

    @SerialPort.setter
    def SerialPort(self, value):
        self.SubChannelNumber = value

    # Just declaration of variables to more easily generate entries in the .pyi file
    _typing_static_ = []
    _typing_instance_ = [
        ('SerialPort', 'ctypes.c_uint8'),
        ('RawAsciiData', 'bytes')
    ]


class XTFPingChanHeader(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('ChannelNumber', ctypes.c_uint16),
        ('DownsampleMethod', ctypes.c_uint16),
        ('SlantRange', ctypes.c_float),             # Slant range [m]
        ('GroundRange', ctypes.c_float),            # Ground range [m, optional]
        ('TimeDelay', ctypes.c_float),              # Delay from transmit to recording started [s]
        ('TimeDuration', ctypes.c_float),           # Duration of recording [s]
        ('SecondsPerPing', ctypes.c_float),         # Time between pings [s]
        ('ProcessingFlags', ctypes.c_uint16),       # See enumeration
        ('Frequency', ctypes.c_uint16),             # Center transmit frequency
        ('InitialGainCode', ctypes.c_uint16),
        ('GainCode', ctypes.c_uint16),
        ('BandWidth', ctypes.c_uint16),
        ('ContactNumber', ctypes.c_uint32),
        ('ContactClassification', ctypes.c_uint16),
        ('ContactSubNumber', ctypes.c_uint8),
        ('ContactType', ctypes.c_uint8),
        ('NumSamples', ctypes.c_uint32),            # Number of samples following header
        ('MillivoltScale', ctypes.c_uint16),
        ('ContactTimeOffTrack', ctypes.c_float),
        ('ContactCloseNumber', ctypes.c_uint8),
        ('Reserved2', ctypes.c_uint8),
        ('FixedVSOP', ctypes.c_float),
        ('Weight', ctypes.c_int16),                 # Weight factor
        ('ReservedSpace', ctypes.c_uint8 * 4)
    ]


class XTFPingHeader(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('HSeconds', ctypes.c_uint8),
        ('JulianDay', ctypes.c_uint16),
        ('EventNumber', ctypes.c_uint32),
        ('PingNumber', ctypes.c_uint32),
        ('SoundVelocity', ctypes.c_float),
        ('OceanTide', ctypes.c_float),
        ('Reserved2', ctypes.c_uint32),
        ('ConductivityFreq', ctypes.c_float),
        ('TemperatureFreq', ctypes.c_float),
        ('PressureFreq', ctypes.c_float),
        ('PressureTemp', ctypes.c_float),
        ('Conductivity', ctypes.c_float),
        ('WaterTemperature', ctypes.c_float),
        ('Pressure', ctypes.c_float),
        ('ComputedSoundVelocity', ctypes.c_float),
        ('MagX', ctypes.c_float),
        ('MagY', ctypes.c_float),
        ('MagZ', ctypes.c_float),
        ('AuxVal1', ctypes.c_float),
        ('AuxVal2', ctypes.c_float),
        ('AuxVal3', ctypes.c_float),
        ('AuxVal4', ctypes.c_float),
        ('AuxVal5', ctypes.c_float),
        ('AuxVal6', ctypes.c_float),
        ('SpeedLog', ctypes.c_float),
        ('Turbidity', ctypes.c_float),
        ('ShipSpeed', ctypes.c_float),
        ('ShipGyro', ctypes.c_float),
        ('ShipYcoordinate', ctypes.c_double),
        ('ShipXcoordinate', ctypes.c_double),
        ('ShipAltitude', ctypes.c_uint16),  # Decimeters
        ('ShipDepth', ctypes.c_uint16),  # Decimeters
        ('FixTimeHour', ctypes.c_uint8),
        ('FixTimeMinute', ctypes.c_uint8),
        ('FixTimeSecond', ctypes.c_uint8),
        ('FixTimeHsecond', ctypes.c_uint8),
        ('SensorSpeed', ctypes.c_float),
        ('KP', ctypes.c_float),
        ('SensorYcoordinate', ctypes.c_double),
        ('SensorXcoordinate', ctypes.c_double),
        ('SonarStatus', ctypes.c_uint16),
        ('RangeToFish', ctypes.c_uint16),
        ('BearingToFish', ctypes.c_uint16),
        ('CableOut', ctypes.c_uint16),
        ('Layback', ctypes.c_float),
        ('CableTension', ctypes.c_float),
        ('SensorDepth', ctypes.c_float),
        ('SensorPrimaryAltitude', ctypes.c_float),
        ('SensorAuxAltitude', ctypes.c_float),
        ('SensorPitch', ctypes.c_float),
        ('SensorRoll', ctypes.c_float),
        ('SensorHeading', ctypes.c_float),
        ('Heave', ctypes.c_float),
        ('Yaw', ctypes.c_float),
        ('AttitudeTimeTag', ctypes.c_uint32),
        ('DOT', ctypes.c_float),
        ('NavFixMilliseconds', ctypes.c_uint32),
        ('ComputerClockHour', ctypes.c_uint8),
        ('ComputerClockMinute', ctypes.c_uint8),
        ('ComputerClockSecond', ctypes.c_uint8),
        ('ComputerClockHsec', ctypes.c_uint8),
        ('FishPositionDeltaX', ctypes.c_int16),
        ('FishPositionDeltaY', ctypes.c_int16),
        ('FishPositionErrorCode', ctypes.c_uint8),
        ('OptionalOffset', ctypes.c_uint32),
        ('CableOutHundredths', ctypes.c_uint8),
        ('ReservedSpace2', ctypes.c_uint8 * 6)
    ]

    # Just declaration of variables to more easily generate entries in the .pyi file
    # TODO: Generate it automatically by inspecing __init__
    _typing_static_ = []
    _typing_instance_ = [
        ('ping_chan_headers', 'List[XTFPingChanHeader]'),
        ('data', 'List[np.ndarray]')
    ]

    _bathy_header_types = [
            XTFHeaderType.bathy_xyza.value,
            XTFHeaderType.bathy.value,
            XTFHeaderType.multibeam_raw_beam_angle
        ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header: XTFFileHeader=None):
        if not file_header:
            raise RuntimeError('Initialization of XTFPingHeader from buffer requires file_header to be passed.')

        obj = super().create_from_buffer(buffer=buffer)

        obj.ping_chan_headers = []  # type: List[XTFPingChanHeader]
        obj.data = None

        # Sonar and bathy has a different data structure following the header
        if obj.HeaderType == XTFHeaderType.sonar:
            obj.data = []  # type: List[np.ndarray]

            bytes_remaining = obj.NumBytesThisRecord - ctypes.sizeof(XTFPingHeader)

            for i in range(0, obj.NumChansToFollow):
                # Retrieve XTFPingChanHeader for this channel
                p_chan = XTFPingChanHeader.create_from_buffer(buffer=buffer)
                obj.ping_chan_headers.append(p_chan)
                bytes_remaining -= ctypes.sizeof(XTFPingChanHeader)

                # Backwards-compatibility: retrive from NumSamples if possible, else use old field
                n_samples = p_chan.NumSamples if p_chan.NumSamples > 0 else file_header.sonar_info[i].Reserved

                # Calculate number of bytes to read
                n_bytes = n_samples * file_header.sonar_info[i].BytesPerSample
                if n_bytes > bytes_remaining:
                    raise RuntimeError('Number of bytes to read exceeds the number of bytes remaining in packet.')

                # Read the data and output as a numpy array of the specified bytes-per-sample
                samples = buffer.read(n_bytes)
                if not samples:
                    raise RuntimeError('File ended while reading data packets (file corrupt?)')

                bytes_remaining -= len(samples)

                # Favor getting the sample format from the dedicated field added in X41.
                # If the field is not populated deduce the type from the bytes per sample field.
                if file_header.sonar_info[i].SampleFormat in sample_format_dtype:
                    sample_format = sample_format_dtype[file_header.sonar_info[i].SampleFormat]
                else:
                    sample_format = xtf_dtype[file_header.sonar_info[i].BytesPerSample]

                samples = np.frombuffer(samples, dtype=sample_format)
                obj.data.append(samples)

        elif obj.HeaderType == XTFHeaderType.bathy_xyza:
            # Bathymetry uses the same header as sonar, but without the XTFPingChanHeaders

            # TODO: Should the sub-channel number be used to index chan_info (?)
            # sub_chan = obj.SubChannelNumber

            # Read the data that follows
            n_bytes = obj.NumBytesThisRecord - ctypes.sizeof(XTFPingHeader)
            samples = buffer.read(n_bytes)
            if not samples:
                warn('XTFBathyHeader without any data encountered.')

            # Processed bathy data consists of repeated XTFBeamXYZA structures
            # Note: Using a ctypes array is a _lot_ faster than constructing a list of BeamXYZA
            num_xyza = n_bytes // ctypes.sizeof(XTFBeamXYZA)
            xyza_array_type = XTFBeamXYZA * num_xyza
            xyza_array_type._pack_ = 1
            obj.data = xyza_array_type.from_buffer_copy(samples)

        elif obj.HeaderType == XTFHeaderType.reson_7018_watercolumn:
            # 7018 water column consists of XTFPingHeader followed by (one?) XTFPingChanHeader, then vendor data

            # Retrieve XTFPingChanHeader
            p_chan = XTFPingChanHeader.create_from_buffer(buffer=buffer)
            obj.ping_chan_headers.append(p_chan)

            # Read the data that follows
            n_bytes = obj.NumBytesThisRecord - ctypes.sizeof(XTFPingHeader) - ctypes.sizeof(XTFPingChanHeader)
            samples = buffer.read(n_bytes)
            if not samples:
                warn('XTFPingHeader (Reson7018) without any data encountered.')

            obj.data = samples

        else:
            # Generic XTFPingHeader construction
            n_bytes = obj.NumBytesThisRecord - ctypes.sizeof(XTFPingHeader)
            samples = buffer.read(n_bytes)
            if not samples and n_bytes > 0:
                warn('XTFPingHeader without any data encountered.')

            # The data is the raw bytes following the header
            obj.data = samples

        return obj

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.sonar.value


class XTFPosRawNavigation(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Microsecond', ctypes.c_uint16),
        ('RawYcoordinate', ctypes.c_double),
        ('RawXcoordinate', ctypes.c_double),
        ('RawAltitude', ctypes.c_double),
        ('Pitch', ctypes.c_float),
        ('Roll', ctypes.c_float),
        ('Heave', ctypes.c_float),
        ('Heading', ctypes.c_float),
        ('Reserved2', ctypes.c_uint8)
    ]

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.pos_raw_navigation.value


class XTFQPSSingleBeam(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('TimeTag', ctypes.c_uint32),
        ('Id', ctypes.c_int32),
        ('SoundVelocity', ctypes.c_float),
        ('Intensity', ctypes.c_float),
        ('Quality', ctypes.c_int32),
        ('TwoWayTravelTime', ctypes.c_float),
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Millisecond', ctypes.c_uint16),
        ('Reserved2', ctypes.c_uint8 * 7)
    ]

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.q_singlebeam.value


class XTFQPSMultiTXEntry(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('Id', ctypes.c_int),
        ('Intensity', ctypes.c_float),
        ('Quality', ctypes.c_int),
        ('TwoWayTravelTime', ctypes.c_float),
        ('DeltaTime', ctypes.c_float),
        ('OffsetX', ctypes.c_float),  # Number of bytes without padding (header+data)
        ('OffsetY', ctypes.c_float),
        ('OffsetZ', ctypes.c_float),
        ('Reserved', ctypes.c_float * 4)
    ]


class XTFQPSMBEEntry(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('Id', ctypes.c_int),
        ('Intensity', ctypes.c_double),
        ('Quality', ctypes.c_int),
        ('TwoWayTravelTime', ctypes.c_double),
        ('DeltaTime', ctypes.c_double),
        ('OffsetX', ctypes.c_double),  # Number of bytes without padding (header+data)
        ('OffsetY', ctypes.c_double),
        ('OffsetZ', ctypes.c_double),
        ('Reserved', ctypes.c_float * 4)
    ]


class XTFRawCustomHeader(XTFPacket):
    _pack_ = 1
    _fields_ = [
        ('MagicNumber', ctypes.c_uint16),
        ('HeaderType', ctypes.c_uint8),
        ('ManufacturerID', ctypes.c_uint8),
        ('SonarID', ctypes.c_uint16),
        ('PacketID', ctypes.c_uint16 * 2),
        ('Reserved1', ctypes.c_uint32),
        ('NumBytesThisRecord', ctypes.c_uint32),
        ('Id', ctypes.c_int32),
        ('SoundVelocity', ctypes.c_float),
        ('Intensity', ctypes.c_float),
        ('Quality', ctypes.c_int32),
        ('TwoWayTravelTime', ctypes.c_float),
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Millisecond', ctypes.c_uint16),
        ('Reserved2', ctypes.c_uint8 * 7)
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer=buffer)
        if obj.MagicNumber != 0xFACE:
            raise RuntimeError('XTF packet does not start with the correct identifier (0xFACE).')

        return obj

    def __init__(self):
        super().__init__()
        self.MagicNumber = 0xFACE
        self.HeaderType = XTFHeaderType.custom_vendor_data.value


class XTFHeaderNavigation(XTFPacket):
    _pack_ = 1
    _fields_ = [
        ('MagicNumber', ctypes.c_uint16),
        ('HeaderType', ctypes.c_uint8),
        ('Reserved', ctypes.c_uint8 * 7),
        ('NumBytesThisRecord', ctypes.c_uint32),
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Microsecond', ctypes.c_uint32),
        ('SourceEpoch', ctypes.c_uint32),
        ('TimeTag', ctypes.c_uint32),
        ('RawYcoordinate', ctypes.c_double),
        ('RawXcoordinate', ctypes.c_double),
        ('RawAltitude', ctypes.c_double),
        ('TimeFlag', ctypes.c_uint8),
        ('Reserved2', ctypes.c_uint8 * 6)
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer=buffer)
        if obj.MagicNumber != 0xFACE:
            raise RuntimeError('XTF packet does not start with the correct identifier (0xFACE).')

        return obj

    def __init__(self):
        super().__init__()
        self.MagicNumber = 0xFACE
        self.HeaderType = XTFHeaderType.navigation.value


class XTFHeaderGyro(XTFPacket):
    _pack_ = 1
    _fields_ = [
        ('MagicNumber', ctypes.c_uint16),
        ('HeaderType', ctypes.c_uint8),
        ('Reserved', ctypes.c_uint8 * 7),
        ('NumBytesThisRecord', ctypes.c_uint32),
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('Microsecond', ctypes.c_uint32),
        ('SourceEpoch', ctypes.c_uint32),
        ('TimeTag', ctypes.c_uint32),
        ('Gyro', ctypes.c_float),
        ('TimeFlag', ctypes.c_uint8),
        ('Reserved1', ctypes.c_uint8 * 26)
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer=buffer)
        if obj.MagicNumber != 0xFACE:
            raise RuntimeError('XTF packet does not start with the correct identifier (0xFACE).')

        return obj

    def __init__(self):
        super().__init__()
        self.MagicNumber = 0xFACE
        self.HeaderType = XTFHeaderType.gyro.value


class XTFHighSpeedSensor(XTFPacketStart):
    _pack_ = 1
    _fields_ = [
        ('Year', ctypes.c_uint16),
        ('Month', ctypes.c_uint8),
        ('Day', ctypes.c_uint8),
        ('Hour', ctypes.c_uint8),
        ('Minute', ctypes.c_uint8),
        ('Second', ctypes.c_uint8),
        ('HSeconds', ctypes.c_uint8),
        ('NumSensorBytes', ctypes.c_uint32),
        ('RelativeBathyPingNum', ctypes.c_uint32),
        ('Reserved3', ctypes.c_uint8 * 34)
    ]

    def __init__(self):
        super().__init__()
        self.HeaderType = XTFHeaderType.highspeed_sensor2.value


class XTFBeamXYZA(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('dPosOffsetTrX', ctypes.c_double),
        ('dPosOffsetTrY', ctypes.c_double),
        ('fDepth', ctypes.c_float),
        ('dTime', ctypes.c_double),
        ('usAmpl', ctypes.c_int16),
        ('ucQuality', ctypes.c_uint8)
    ]


class SNP0(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('ID', ctypes.c_uint32),                # Identifier code. SNP0= 0x534E5030
        ('HeaderSize', ctypes.c_uint16),        # Header size, bytes
        ('DataSize', ctypes.c_uint16),          # Data size following header, bytes
        ('PingNumber', ctypes.c_uint32),        # Sequential ping number
        ('Seconds', ctypes.c_uint32),           # Time since 00:00:00 1-Jan-1970
        ('Millisec', ctypes.c_uint32),
        ('Latency', ctypes.c_uint16),           # Time from ping to output (ms)
        ('SonarID', ctypes.c_uint16 * 2),       # Least significant four bytes of ethernet address
        ('SonarModel', ctypes.c_uint16),        # Coded model number of sonar
        ('Frequency', ctypes.c_uint16),         # Sonar frequency (kHz)
        ('SSpeed', ctypes.c_uint16),            # Programmed sound velocity (m/sec)
        ('SampleRate', ctypes.c_uint16),        # A/D sample rate (samples/sec)
        ('PingRate', ctypes.c_uint16),          # Pings per second (0.001 Hz steps)
        ('Range', ctypes.c_uint16),             # Range setting (meters)
        ('Power', ctypes.c_uint16),             # Power
        ('Gain', ctypes.c_uint16),              # (b15 = auto, b14 = TVG, b6..0 = gain)
        ('PulseWidth', ctypes.c_uint16),        # Transmit pulse width (microseconds)
        ('Spread', ctypes.c_uint16),            # TVG spreading, n*log(R), 0.25dB steps
        ('Absorb', ctypes.c_uint16),            # TVG absorption, dB/km, 1dB steps
        ('Proj', ctypes.c_uint16),              # b7 = steering, b4..0 = projector type
        ('ProjWidth', ctypes.c_uint16),         # Transmit beam width along track, 0.1 deg
        ('SpacingNum', ctypes.c_uint16),        # Receiver beam spacing, numerator, degrees
        ('SpacingDen', ctypes.c_uint16),        # Receiver beam spacing, denominator
        ('ProjAngle', ctypes.c_int16),          # Projector steering, degrees*PKT_STEER_RES
        ('MinRange', ctypes.c_uint16),          # Range filter settings
        ('MaxRange', ctypes.c_uint16),          # Range filter settings
        ('MinDepth', ctypes.c_uint16),          # Depth filter settings
        ('MaxDepth', ctypes.c_uint16),          # Depth filter settings
        ('Filters', ctypes.c_uint16),           # Enabled filters, b1 = depth, b0 = range
        ('bFlags', ctypes.c_uint8 * 2),         # b0..11 spare, b12-14 snipMode, b15 RollStab, b16 RollStab enabled
        ('HeadTemp', ctypes.c_int16),           # Head temperature, 0.1C steps
        ('BeamCnt', ctypes.c_uint16)            # Number of beams
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer=buffer)
        if obj.ID != 0x534E5030:
            raise RuntimeError('XTF packet does not start with the correct identifier (0x534E5030).')

        return obj

    def __init__(self):
        super().__init__()
        self.ID = 0x534E5030


class SNP1(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('ID', ctypes.c_uint32),            # Identifier code. SNP1= 0x534E5031
        ('HeaderSize', ctypes.c_uint16),    # Header size, bytes
        ('DataSize', ctypes.c_uint16),      # Data size following header, bytes
        ('PingNumber', ctypes.c_uint32),    # Sequential ping number
        ('Beam', ctypes.c_uint16),          # Beam number 0 .. N-1
        ('SnipSamples', ctypes.c_uint16),   # Snippet size, samples
        ('GainStart', ctypes.c_uint16),     # Gain at start of snippet, 0.01 dB steps (0=ignore)
        ('GainEnd', ctypes.c_uint16),       # Gain at end of snippet, 0.01 dB steps (0=ignore)
        ('FragOffset', ctypes.c_uint16),    # Fragment offset, samples from ping
        ('FragSamples', ctypes.c_uint16)    # Fragment size, samples
    ]

    @classmethod
    def create_from_buffer(cls, buffer: IOBase, file_header=None):
        obj = super().create_from_buffer(buffer=buffer)
        if obj.ID != 0x534E5031:
            raise RuntimeError('XTF packet does not start with the correct identifier (0x534E5031).')

        return obj

    def __init__(self):
        super().__init__()
        self.ID = 0x534E5031


# Mapping from enumerated header type to the class implementation
# TODO: XTF bathy snippets (SNP0/SNP1 etc) requires a custom implementation in xtf_read
XTFPacketClasses = {
    XTFHeaderType.sonar: XTFPingHeader,
    XTFHeaderType.bathy: XTFPingHeader,
    XTFHeaderType.bathy_xyza: XTFPingHeader,
    XTFHeaderType.multibeam_raw_beam_angle: XTFPingHeader, # Raw vendor data is returned as raw bytes
    XTFHeaderType.reson_7125_snippet: XTFPingHeader,  # The custom vendor data is returned as raw bytes
    XTFHeaderType.reson_7125: XTFPingHeader,  # The custom vendor data is returned as raw bytes
    XTFHeaderType.reson_7018_watercolumn: XTFPingHeader,  # The custom vendor data is returned as raw bytes
    XTFHeaderType.attitude: XTFAttitudeData,
    XTFHeaderType.notes: XTFNotesHeader,
    XTFHeaderType.raw_serial: XTFRawSerialHeader,
    XTFHeaderType.pos_raw_navigation: XTFPosRawNavigation,
    XTFHeaderType.q_singlebeam: XTFQPSSingleBeam,
    XTFHeaderType.custom_vendor_data: XTFRawCustomHeader,
    XTFHeaderType.navigation: XTFHeaderNavigation,
    XTFHeaderType.gyro: XTFHeaderGyro,
    XTFHeaderType.sourcetime_gyro: XTFHeaderGyro,
    XTFHeaderType.highspeed_sensor2: XTFHighSpeedSensor,
    XTFHeaderType.unknown: XTFUnknownPacket
}


if __name__ == '__main__':
    # TODO: Move these assertions to a test routine
    header_sizes = [
        (XTFFileHeader, 1024),
        (XTFChanInfo, 128),
        (XTFAttitudeData, 64),
        (XTFNotesHeader, 256),
        (XTFRawSerialHeader, 30),
        (XTFPingHeader, 256),
        (XTFPingChanHeader, 64),
        (XTFHighSpeedSensor, 64),
        (XTFBeamXYZA, 31),
        (XTFHeaderGyro, 64),
        (SNP0, 74),
        (SNP1, 24)
    ]
    for (xtf_header, n_bytes) in header_sizes:
        assert ctypes.sizeof(xtf_header) == n_bytes, \
            "{} expected size is {} bytes, was {} bytes".format(xtf_header.__name__, n_bytes, ctypes.sizeof(xtf_header))


