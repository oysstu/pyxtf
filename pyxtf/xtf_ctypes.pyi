import ctypes
import numpy as np
from io import IOBase, BytesIO
from typing import List, Tuple, Dict, Callable, Any



class CField:
    """
    This is a redefinition of the _ctype.CField class, which is hidden in the ctypes API.
    This class is not intended to be used at runtime, but is here to allow for static typing of the XTF-classes.
    """
    def __init__(self):
        self.offset = 0  # type: int
        self.size = 0  # type: int


class XTFBase(ctypes.LittleEndianStructure):
    """
    Base class for all XTF ctypes.Structure children.
    Exposes basic utility like printing of fields and constructing class from a buffer.
    """
    def __str__(self) -> str:
        pass

    def __new__(cls, buffer: IOBase = None):
        pass

    def __init__(self, buffer=None, *args, **kwargs):
        pass

class XTFChanInfo(XTFBase):
    TypeOfChannel = None  # type: CField
    SubChannelNumber = None  # type: CField
    CorrectionFlags = None  # type: CField
    UniPolar = None  # type: CField
    BytesPerSample = None  # type: CField
    Reserved = None  # type: CField
    ChannelName = None  # type: CField
    VoltScale = None  # type: CField
    Frequency = None  # type: CField
    HorizBeamAngle = None  # type: CField
    TiltAngle = None  # type: CField
    BeamWidth = None  # type: CField
    OffsetX = None  # type: CField
    OffsetY = None  # type: CField
    OffsetZ = None  # type: CField
    OffsetYaw = None  # type: CField
    OffsetPitch = None  # type: CField
    OffsetRoll = None  # type: CField
    BeamsPerArray = None  # type: CField
    SampleFormat = None  # type: CField
    ReservedArea2 = None  # type: CField

    def __init__(self):
        self.TypeOfChannel = None  # type: ctypes.c_ubyte
        self.SubChannelNumber = None  # type: ctypes.c_ubyte
        self.CorrectionFlags = None  # type: ctypes.c_ushort
        self.UniPolar = None  # type: ctypes.c_ushort
        self.BytesPerSample = None  # type: ctypes.c_ushort
        self.Reserved = None  # type: ctypes.c_uint
        self.ChannelName = None  # type: ctypes.Array[ctypes.c_char]
        self.VoltScale = None  # type: ctypes.c_float
        self.Frequency = None  # type: ctypes.c_float
        self.HorizBeamAngle = None  # type: ctypes.c_float
        self.TiltAngle = None  # type: ctypes.c_float
        self.BeamWidth = None  # type: ctypes.c_float
        self.OffsetX = None  # type: ctypes.c_float
        self.OffsetY = None  # type: ctypes.c_float
        self.OffsetZ = None  # type: ctypes.c_float
        self.OffsetYaw = None  # type: ctypes.c_float
        self.OffsetPitch = None  # type: ctypes.c_float
        self.OffsetRoll = None  # type: ctypes.c_float
        self.BeamsPerArray = None  # type: ctypes.c_ushort
        self.SampleFormat = None  # type: ctypes.c_ubyte
        self.ReservedArea2 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def to_bytes(self):
        pass


class XTFFileHeader(XTFBase):
    FileFormat = None  # type: CField
    SystemType = None  # type: CField
    RecordingProgramName = None  # type: CField
    RecordingProgramVersion = None  # type: CField
    SonarName = None  # type: CField
    SonarType = None  # type: CField
    NoteString = None  # type: CField
    ThisFileName = None  # type: CField
    NavUnits = None  # type: CField
    NumberOfSonarChannels = None  # type: CField
    NumberOfBathymetryChannels = None  # type: CField
    NumberOfSnippetChannels = None  # type: CField
    NumberOfForwardLookArrays = None  # type: CField
    NumberOfEchoStrengthChannels = None  # type: CField
    NumberOfInterferometryChannels = None  # type: CField
    Reserved1 = None  # type: CField
    Reserved2 = None  # type: CField
    ReferencePointHeight = None  # type: CField
    ProjectionType = None  # type: CField
    SpheriodType = None  # type: CField
    NavigationLatency = None  # type: CField
    OriginY = None  # type: CField
    OriginX = None  # type: CField
    NavOffsetY = None  # type: CField
    NavOffsetX = None  # type: CField
    NavOffsetZ = None  # type: CField
    NavOffsetYaw = None  # type: CField
    MRUOffsetY = None  # type: CField
    MRUOffsetX = None  # type: CField
    MRUOffsetZ = None  # type: CField
    MRUOffsetYaw = None  # type: CField
    MRUOffsetPitch = None  # type: CField
    MRUOffsetRoll = None  # type: CField
    ChanInfo = None  # type: CField

    def __init__(self):
        self.FileFormat = None  # type: ctypes.c_ubyte
        self.SystemType = None  # type: ctypes.c_ubyte
        self.RecordingProgramName = None  # type: ctypes.Array[ctypes.c_char]
        self.RecordingProgramVersion = None  # type: ctypes.Array[ctypes.c_char]
        self.SonarName = None  # type: ctypes.Array[ctypes.c_char]
        self.SonarType = None  # type: ctypes.c_ushort
        self.NoteString = None  # type: ctypes.Array[ctypes.c_char]
        self.ThisFileName = None  # type: ctypes.Array[ctypes.c_char]
        self.NavUnits = None  # type: ctypes.c_ushort
        self.NumberOfSonarChannels = None  # type: ctypes.c_ushort
        self.NumberOfBathymetryChannels = None  # type: ctypes.c_ushort
        self.NumberOfSnippetChannels = None  # type: ctypes.c_ubyte
        self.NumberOfForwardLookArrays = None  # type: ctypes.c_ubyte
        self.NumberOfEchoStrengthChannels = None  # type: ctypes.c_ushort
        self.NumberOfInterferometryChannels = None  # type: ctypes.c_ubyte
        self.Reserved1 = None  # type: ctypes.c_ubyte
        self.Reserved2 = None  # type: ctypes.c_ushort
        self.ReferencePointHeight = None  # type: ctypes.c_float
        self.ProjectionType = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.SpheriodType = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.NavigationLatency = None  # type: ctypes.c_int
        self.OriginY = None  # type: ctypes.c_float
        self.OriginX = None  # type: ctypes.c_float
        self.NavOffsetY = None  # type: ctypes.c_float
        self.NavOffsetX = None  # type: ctypes.c_float
        self.NavOffsetZ = None  # type: ctypes.c_float
        self.NavOffsetYaw = None  # type: ctypes.c_float
        self.MRUOffsetY = None  # type: ctypes.c_float
        self.MRUOffsetX = None  # type: ctypes.c_float
        self.MRUOffsetZ = None  # type: ctypes.c_float
        self.MRUOffsetYaw = None  # type: ctypes.c_float
        self.MRUOffsetPitch = None  # type: ctypes.c_float
        self.MRUOffsetRoll = None  # type: ctypes.c_float
        self.ChanInfo = None  # type: ctypes.Array[XTFChanInfo]
    def channel_count(self, verbose: bool = False) -> int:
        pass
    def to_bytes(self):
        pass


class XTFPacket(XTFBase):
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFPacketStart(XTFPacket):
    MagicNumber = None  # type: CField
    HeaderType = None  # type: CField
    SubChannelNumber = None  # type: CField
    NumChansToFollow = None  # type: CField
    Reserved1 = None  # type: CField
    NumBytesThisRecord = None  # type: CField

    def __init__(self):
        self.MagicNumber = None  # type: ctypes.c_ushort
        self.HeaderType = None  # type: ctypes.c_ubyte
        self.SubChannelNumber = None  # type: ctypes.c_ubyte
        self.NumChansToFollow = None  # type: ctypes.c_ushort
        self.Reserved1 = None  # type: ctypes.Array[ctypes.c_ushort]
        self.NumBytesThisRecord = None  # type: ctypes.c_uint
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFUnknownPacket(XTFPacketStart):
    MagicNumber = None  # type: CField
    HeaderType = None  # type: CField
    SubChannelNumber = None  # type: CField
    NumChansToFollow = None  # type: CField
    Reserved1 = None  # type: CField
    NumBytesThisRecord = None  # type: CField

    def __init__(self):
        self.MagicNumber = None  # type: ctypes.c_ushort
        self.HeaderType = None  # type: ctypes.c_ubyte
        self.SubChannelNumber = None  # type: ctypes.c_ubyte
        self.NumChansToFollow = None  # type: ctypes.c_ushort
        self.Reserved1 = None  # type: ctypes.Array[ctypes.c_ushort]
        self.NumBytesThisRecord = None  # type: ctypes.c_uint
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFAttitudeData(XTFPacketStart):
    Reserved2 = None  # type: CField
    EpochMicroseconds = None  # type: CField
    SourceEpoch = None  # type: CField
    Pitch = None  # type: CField
    Roll = None  # type: CField
    Heave = None  # type: CField
    Yaw = None  # type: CField
    TimeTag = None  # type: CField
    Heading = None  # type: CField
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    Millisecond = None  # type: CField
    Reserved3 = None  # type: CField

    def __init__(self):
        self.Reserved2 = None  # type: ctypes.Array[ctypes.c_uint]
        self.EpochMicroseconds = None  # type: ctypes.c_uint
        self.SourceEpoch = None  # type: ctypes.c_uint
        self.Pitch = None  # type: ctypes.c_float
        self.Roll = None  # type: ctypes.c_float
        self.Heave = None  # type: ctypes.c_float
        self.Yaw = None  # type: ctypes.c_float
        self.TimeTag = None  # type: ctypes.c_uint
        self.Heading = None  # type: ctypes.c_float
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.Millisecond = None  # type: ctypes.c_ushort
        self.Reserved3 = None  # type: ctypes.c_ubyte
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFNotesHeader(XTFPacketStart):
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    ReservedBytes = None  # type: CField
    NotesText = None  # type: CField

    def __init__(self):
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.ReservedBytes = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.NotesText = None  # type: ctypes.Array[ctypes.c_char]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFRawSerialHeader(XTFPacketStart):
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    HSeconds = None  # type: CField
    JulianDay = None  # type: CField
    TimeTag = None  # type: CField
    StringSize = None  # type: CField

    def __init__(self):
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.HSeconds = None  # type: ctypes.c_ubyte
        self.JulianDay = None  # type: ctypes.c_ushort
        self.TimeTag = None  # type: ctypes.c_uint
        self.StringSize = None  # type: ctypes.c_ushort
        self.SerialPort = None  # type: ctypes.c_uint8
        self.RawAsciiData = None  # type: bytes
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFPingChanHeader(XTFBase):
    ChannelNumber = None  # type: CField
    DownsampleMethod = None  # type: CField
    SlantRange = None  # type: CField
    GroundRange = None  # type: CField
    TimeDelay = None  # type: CField
    TimeDuration = None  # type: CField
    SecondsPerPing = None  # type: CField
    ProcessingFlags = None  # type: CField
    Frequency = None  # type: CField
    InitialGainCode = None  # type: CField
    GainCode = None  # type: CField
    BandWidth = None  # type: CField
    ContactNumber = None  # type: CField
    ContactClassification = None  # type: CField
    ContactSubNumber = None  # type: CField
    ContactType = None  # type: CField
    NumSamples = None  # type: CField
    MillivoltScale = None  # type: CField
    ContactTimeOffTrack = None  # type: CField
    ContactCloseNumber = None  # type: CField
    Reserved2 = None  # type: CField
    FixedVSOP = None  # type: CField
    Weight = None  # type: CField
    ReservedSpace = None  # type: CField

    def __init__(self):
        self.ChannelNumber = None  # type: ctypes.c_ushort
        self.DownsampleMethod = None  # type: ctypes.c_ushort
        self.SlantRange = None  # type: ctypes.c_float
        self.GroundRange = None  # type: ctypes.c_float
        self.TimeDelay = None  # type: ctypes.c_float
        self.TimeDuration = None  # type: ctypes.c_float
        self.SecondsPerPing = None  # type: ctypes.c_float
        self.ProcessingFlags = None  # type: ctypes.c_ushort
        self.Frequency = None  # type: ctypes.c_ushort
        self.InitialGainCode = None  # type: ctypes.c_ushort
        self.GainCode = None  # type: ctypes.c_ushort
        self.BandWidth = None  # type: ctypes.c_ushort
        self.ContactNumber = None  # type: ctypes.c_uint
        self.ContactClassification = None  # type: ctypes.c_ushort
        self.ContactSubNumber = None  # type: ctypes.c_ubyte
        self.ContactType = None  # type: ctypes.c_ubyte
        self.NumSamples = None  # type: ctypes.c_uint
        self.MillivoltScale = None  # type: ctypes.c_ushort
        self.ContactTimeOffTrack = None  # type: ctypes.c_float
        self.ContactCloseNumber = None  # type: ctypes.c_ubyte
        self.Reserved2 = None  # type: ctypes.c_ubyte
        self.FixedVSOP = None  # type: ctypes.c_float
        self.Weight = None  # type: ctypes.c_short
        self.ReservedSpace = None  # type: ctypes.Array[ctypes.c_ubyte]
    def to_bytes(self):
        pass


class XTFPingHeader(XTFPacketStart):
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    HSeconds = None  # type: CField
    JulianDay = None  # type: CField
    EventNumber = None  # type: CField
    PingNumber = None  # type: CField
    SoundVelocity = None  # type: CField
    OceanTide = None  # type: CField
    Reserved2 = None  # type: CField
    ConductivityFreq = None  # type: CField
    TemperatureFreq = None  # type: CField
    PressureFreq = None  # type: CField
    PressureTemp = None  # type: CField
    Conductivity = None  # type: CField
    WaterTemperature = None  # type: CField
    Pressure = None  # type: CField
    ComputedSoundVelocity = None  # type: CField
    MagX = None  # type: CField
    MagY = None  # type: CField
    MagZ = None  # type: CField
    AuxVal1 = None  # type: CField
    AuxVal2 = None  # type: CField
    AuxVal3 = None  # type: CField
    AuxVal4 = None  # type: CField
    AuxVal5 = None  # type: CField
    AuxVal6 = None  # type: CField
    SpeedLog = None  # type: CField
    Turbidity = None  # type: CField
    ShipSpeed = None  # type: CField
    ShipGyro = None  # type: CField
    ShipYcoordinate = None  # type: CField
    ShipXcoordinate = None  # type: CField
    ShipAltitude = None  # type: CField
    ShipDepth = None  # type: CField
    FixTimeHour = None  # type: CField
    FixTimeMinute = None  # type: CField
    FixTimeSecond = None  # type: CField
    FixTimeHsecond = None  # type: CField
    SensorSpeed = None  # type: CField
    KP = None  # type: CField
    SensorYcoordinate = None  # type: CField
    SensorXcoordinate = None  # type: CField
    SonarStatus = None  # type: CField
    RangeToFish = None  # type: CField
    BearingToFish = None  # type: CField
    CableOut = None  # type: CField
    Layback = None  # type: CField
    CableTension = None  # type: CField
    SensorDepth = None  # type: CField
    SensorPrimaryAltitude = None  # type: CField
    SensorAuxAltitude = None  # type: CField
    SensorPitch = None  # type: CField
    SensorRoll = None  # type: CField
    SensorHeading = None  # type: CField
    Heave = None  # type: CField
    Yaw = None  # type: CField
    AttitudeTimeTag = None  # type: CField
    DOT = None  # type: CField
    NavFixMilliseconds = None  # type: CField
    ComputerClockHour = None  # type: CField
    ComputerClockMinute = None  # type: CField
    ComputerClockSecond = None  # type: CField
    ComputerClockHsec = None  # type: CField
    FishPositionDeltaX = None  # type: CField
    FishPositionDeltaY = None  # type: CField
    FishPositionErrorCode = None  # type: CField
    OptionalOffset = None  # type: CField
    CableOutHundredths = None  # type: CField
    ReservedSpace2 = None  # type: CField

    def __init__(self):
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.HSeconds = None  # type: ctypes.c_ubyte
        self.JulianDay = None  # type: ctypes.c_ushort
        self.EventNumber = None  # type: ctypes.c_uint
        self.PingNumber = None  # type: ctypes.c_uint
        self.SoundVelocity = None  # type: ctypes.c_float
        self.OceanTide = None  # type: ctypes.c_float
        self.Reserved2 = None  # type: ctypes.c_uint
        self.ConductivityFreq = None  # type: ctypes.c_float
        self.TemperatureFreq = None  # type: ctypes.c_float
        self.PressureFreq = None  # type: ctypes.c_float
        self.PressureTemp = None  # type: ctypes.c_float
        self.Conductivity = None  # type: ctypes.c_float
        self.WaterTemperature = None  # type: ctypes.c_float
        self.Pressure = None  # type: ctypes.c_float
        self.ComputedSoundVelocity = None  # type: ctypes.c_float
        self.MagX = None  # type: ctypes.c_float
        self.MagY = None  # type: ctypes.c_float
        self.MagZ = None  # type: ctypes.c_float
        self.AuxVal1 = None  # type: ctypes.c_float
        self.AuxVal2 = None  # type: ctypes.c_float
        self.AuxVal3 = None  # type: ctypes.c_float
        self.AuxVal4 = None  # type: ctypes.c_float
        self.AuxVal5 = None  # type: ctypes.c_float
        self.AuxVal6 = None  # type: ctypes.c_float
        self.SpeedLog = None  # type: ctypes.c_float
        self.Turbidity = None  # type: ctypes.c_float
        self.ShipSpeed = None  # type: ctypes.c_float
        self.ShipGyro = None  # type: ctypes.c_float
        self.ShipYcoordinate = None  # type: ctypes.c_double
        self.ShipXcoordinate = None  # type: ctypes.c_double
        self.ShipAltitude = None  # type: ctypes.c_ushort
        self.ShipDepth = None  # type: ctypes.c_ushort
        self.FixTimeHour = None  # type: ctypes.c_ubyte
        self.FixTimeMinute = None  # type: ctypes.c_ubyte
        self.FixTimeSecond = None  # type: ctypes.c_ubyte
        self.FixTimeHsecond = None  # type: ctypes.c_ubyte
        self.SensorSpeed = None  # type: ctypes.c_float
        self.KP = None  # type: ctypes.c_float
        self.SensorYcoordinate = None  # type: ctypes.c_double
        self.SensorXcoordinate = None  # type: ctypes.c_double
        self.SonarStatus = None  # type: ctypes.c_ushort
        self.RangeToFish = None  # type: ctypes.c_ushort
        self.BearingToFish = None  # type: ctypes.c_ushort
        self.CableOut = None  # type: ctypes.c_ushort
        self.Layback = None  # type: ctypes.c_float
        self.CableTension = None  # type: ctypes.c_float
        self.SensorDepth = None  # type: ctypes.c_float
        self.SensorPrimaryAltitude = None  # type: ctypes.c_float
        self.SensorAuxAltitude = None  # type: ctypes.c_float
        self.SensorPitch = None  # type: ctypes.c_float
        self.SensorRoll = None  # type: ctypes.c_float
        self.SensorHeading = None  # type: ctypes.c_float
        self.Heave = None  # type: ctypes.c_float
        self.Yaw = None  # type: ctypes.c_float
        self.AttitudeTimeTag = None  # type: ctypes.c_uint
        self.DOT = None  # type: ctypes.c_float
        self.NavFixMilliseconds = None  # type: ctypes.c_uint
        self.ComputerClockHour = None  # type: ctypes.c_ubyte
        self.ComputerClockMinute = None  # type: ctypes.c_ubyte
        self.ComputerClockSecond = None  # type: ctypes.c_ubyte
        self.ComputerClockHsec = None  # type: ctypes.c_ubyte
        self.FishPositionDeltaX = None  # type: ctypes.c_short
        self.FishPositionDeltaY = None  # type: ctypes.c_short
        self.FishPositionErrorCode = None  # type: ctypes.c_ubyte
        self.OptionalOffset = None  # type: ctypes.c_uint
        self.CableOutHundredths = None  # type: ctypes.c_ubyte
        self.ReservedSpace2 = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.ping_chan_headers = None  # type: List[XTFPingChanHeader]
        self.data = None  # type: List[np.ndarray]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFPosRawNavigation(XTFPacketStart):
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    Microsecond = None  # type: CField
    RawYcoordinate = None  # type: CField
    RawXcoordinate = None  # type: CField
    RawAltitude = None  # type: CField
    Pitch = None  # type: CField
    Roll = None  # type: CField
    Heave = None  # type: CField
    Heading = None  # type: CField
    Reserved2 = None  # type: CField

    def __init__(self):
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.Microsecond = None  # type: ctypes.c_ushort
        self.RawYcoordinate = None  # type: ctypes.c_double
        self.RawXcoordinate = None  # type: ctypes.c_double
        self.RawAltitude = None  # type: ctypes.c_double
        self.Pitch = None  # type: ctypes.c_float
        self.Roll = None  # type: ctypes.c_float
        self.Heave = None  # type: ctypes.c_float
        self.Heading = None  # type: ctypes.c_float
        self.Reserved2 = None  # type: ctypes.c_ubyte
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFQPSSingleBeam(XTFPacketStart):
    TimeTag = None  # type: CField
    Id = None  # type: CField
    SoundVelocity = None  # type: CField
    Intensity = None  # type: CField
    Quality = None  # type: CField
    TwoWayTravelTime = None  # type: CField
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    Millisecond = None  # type: CField
    Reserved2 = None  # type: CField

    def __init__(self):
        self.TimeTag = None  # type: ctypes.c_uint
        self.Id = None  # type: ctypes.c_int
        self.SoundVelocity = None  # type: ctypes.c_float
        self.Intensity = None  # type: ctypes.c_float
        self.Quality = None  # type: ctypes.c_int
        self.TwoWayTravelTime = None  # type: ctypes.c_float
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.Millisecond = None  # type: ctypes.c_ushort
        self.Reserved2 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFQPSMultiTXEntry(XTFBase):
    Id = None  # type: CField
    Intensity = None  # type: CField
    Quality = None  # type: CField
    TwoWayTravelTime = None  # type: CField
    DeltaTime = None  # type: CField
    OffsetX = None  # type: CField
    OffsetY = None  # type: CField
    OffsetZ = None  # type: CField
    Reserved = None  # type: CField

    def __init__(self):
        self.Id = None  # type: ctypes.c_int
        self.Intensity = None  # type: ctypes.c_float
        self.Quality = None  # type: ctypes.c_int
        self.TwoWayTravelTime = None  # type: ctypes.c_float
        self.DeltaTime = None  # type: ctypes.c_float
        self.OffsetX = None  # type: ctypes.c_float
        self.OffsetY = None  # type: ctypes.c_float
        self.OffsetZ = None  # type: ctypes.c_float
        self.Reserved = None  # type: ctypes.Array[ctypes.c_float]
    def to_bytes(self):
        pass


class XTFQPSMBEEntry(XTFBase):
    Id = None  # type: CField
    Intensity = None  # type: CField
    Quality = None  # type: CField
    TwoWayTravelTime = None  # type: CField
    DeltaTime = None  # type: CField
    OffsetX = None  # type: CField
    OffsetY = None  # type: CField
    OffsetZ = None  # type: CField
    Reserved = None  # type: CField

    def __init__(self):
        self.Id = None  # type: ctypes.c_int
        self.Intensity = None  # type: ctypes.c_double
        self.Quality = None  # type: ctypes.c_int
        self.TwoWayTravelTime = None  # type: ctypes.c_double
        self.DeltaTime = None  # type: ctypes.c_double
        self.OffsetX = None  # type: ctypes.c_double
        self.OffsetY = None  # type: ctypes.c_double
        self.OffsetZ = None  # type: ctypes.c_double
        self.Reserved = None  # type: ctypes.Array[ctypes.c_float]
    def to_bytes(self):
        pass


class XTFRawCustomHeader(XTFPacket):
    MagicNumber = None  # type: CField
    HeaderType = None  # type: CField
    ManufacturerID = None  # type: CField
    SonarID = None  # type: CField
    PacketID = None  # type: CField
    Reserved1 = None  # type: CField
    NumBytesThisRecord = None  # type: CField
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    HSecond = None  # type: CField
    JulianDay = None  # type: CField
    Reserved2 = None  # type: CField
    PingNumber = None  # type: CField
    TimeTag = None  # type: CField
    NumCustomerBytes = None  # type: CField
    Reserved3 = None  # type: CField

    def __init__(self):
        self.MagicNumber = None  # type: ctypes.c_ushort
        self.HeaderType = None  # type: ctypes.c_ubyte
        self.ManufacturerID = None  # type: ctypes.c_ubyte
        self.SonarID = None  # type: ctypes.c_ushort
        self.PacketID = None  # type: ctypes.c_ushort
        self.Reserved1 = None  # type: ctypes.Array[ctypes.c_ushort]
        self.NumBytesThisRecord = None  # type: ctypes.c_uint
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.HSecond = None  # type: ctypes.c_ubyte
        self.JulianDay = None  # type: ctypes.c_ushort
        self.Reserved2 = None  # type: ctypes.Array[ctypes.c_ushort]
        self.PingNumber = None  # type: ctypes.c_uint
        self.TimeTag = None  # type: ctypes.c_uint
        self.NumCustomerBytes = None  # type: ctypes.c_uint
        self.Reserved3 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFHeaderNavigation(XTFPacket):
    MagicNumber = None  # type: CField
    HeaderType = None  # type: CField
    Reserved = None  # type: CField
    NumBytesThisRecord = None  # type: CField
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    Microsecond = None  # type: CField
    SourceEpoch = None  # type: CField
    TimeTag = None  # type: CField
    RawYcoordinate = None  # type: CField
    RawXcoordinate = None  # type: CField
    RawAltitude = None  # type: CField
    TimeFlag = None  # type: CField
    Reserved2 = None  # type: CField

    def __init__(self):
        self.MagicNumber = None  # type: ctypes.c_ushort
        self.HeaderType = None  # type: ctypes.c_ubyte
        self.Reserved = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.NumBytesThisRecord = None  # type: ctypes.c_uint
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.Microsecond = None  # type: ctypes.c_uint
        self.SourceEpoch = None  # type: ctypes.c_uint
        self.TimeTag = None  # type: ctypes.c_uint
        self.RawYcoordinate = None  # type: ctypes.c_double
        self.RawXcoordinate = None  # type: ctypes.c_double
        self.RawAltitude = None  # type: ctypes.c_double
        self.TimeFlag = None  # type: ctypes.c_ubyte
        self.Reserved2 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFHeaderGyro(XTFPacket):
    MagicNumber = None  # type: CField
    HeaderType = None  # type: CField
    Reserved = None  # type: CField
    NumBytesThisRecord = None  # type: CField
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    Microsecond = None  # type: CField
    SourceEpoch = None  # type: CField
    TimeTag = None  # type: CField
    Gyro = None  # type: CField
    TimeFlag = None  # type: CField
    Reserved1 = None  # type: CField

    def __init__(self):
        self.MagicNumber = None  # type: ctypes.c_ushort
        self.HeaderType = None  # type: ctypes.c_ubyte
        self.Reserved = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.NumBytesThisRecord = None  # type: ctypes.c_uint
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.Microsecond = None  # type: ctypes.c_uint
        self.SourceEpoch = None  # type: ctypes.c_uint
        self.TimeTag = None  # type: ctypes.c_uint
        self.Gyro = None  # type: ctypes.c_float
        self.TimeFlag = None  # type: ctypes.c_ubyte
        self.Reserved1 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFHighSpeedSensor(XTFPacketStart):
    Year = None  # type: CField
    Month = None  # type: CField
    Day = None  # type: CField
    Hour = None  # type: CField
    Minute = None  # type: CField
    Second = None  # type: CField
    HSeconds = None  # type: CField
    NumSensorBytes = None  # type: CField
    RelativeBathyPingNum = None  # type: CField
    Reserved3 = None  # type: CField

    def __init__(self):
        self.Year = None  # type: ctypes.c_ushort
        self.Month = None  # type: ctypes.c_ubyte
        self.Day = None  # type: ctypes.c_ubyte
        self.Hour = None  # type: ctypes.c_ubyte
        self.Minute = None  # type: ctypes.c_ubyte
        self.Second = None  # type: ctypes.c_ubyte
        self.HSeconds = None  # type: ctypes.c_ubyte
        self.NumSensorBytes = None  # type: ctypes.c_uint
        self.RelativeBathyPingNum = None  # type: ctypes.c_uint
        self.Reserved3 = None  # type: ctypes.Array[ctypes.c_ubyte]
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class XTFBeamXYZA(XTFBase):
    dPosOffsetTrX = None  # type: CField
    dPosOffsetTrY = None  # type: CField
    fDepth = None  # type: CField
    dTime = None  # type: CField
    usAmpl = None  # type: CField
    ucQuality = None  # type: CField

    def __init__(self):
        self.dPosOffsetTrX = None  # type: ctypes.c_double
        self.dPosOffsetTrY = None  # type: ctypes.c_double
        self.fDepth = None  # type: ctypes.c_float
        self.dTime = None  # type: ctypes.c_double
        self.usAmpl = None  # type: ctypes.c_short
        self.ucQuality = None  # type: ctypes.c_ubyte
    def to_bytes(self):
        pass


class SNP0(XTFBase):
    ID = None  # type: CField
    HeaderSize = None  # type: CField
    DataSize = None  # type: CField
    PingNumber = None  # type: CField
    Seconds = None  # type: CField
    Millisec = None  # type: CField
    Latency = None  # type: CField
    SonarID = None  # type: CField
    SonarModel = None  # type: CField
    Frequency = None  # type: CField
    SSpeed = None  # type: CField
    SampleRate = None  # type: CField
    PingRate = None  # type: CField
    Range = None  # type: CField
    Power = None  # type: CField
    Gain = None  # type: CField
    PulseWidth = None  # type: CField
    Spread = None  # type: CField
    Absorb = None  # type: CField
    Proj = None  # type: CField
    ProjWidth = None  # type: CField
    SpacingNum = None  # type: CField
    SpacingDen = None  # type: CField
    ProjAngle = None  # type: CField
    MinRange = None  # type: CField
    MaxRange = None  # type: CField
    MinDepth = None  # type: CField
    MaxDepth = None  # type: CField
    Filters = None  # type: CField
    bFlags = None  # type: CField
    HeadTemp = None  # type: CField
    BeamCnt = None  # type: CField

    def __init__(self):
        self.ID = None  # type: ctypes.c_uint
        self.HeaderSize = None  # type: ctypes.c_ushort
        self.DataSize = None  # type: ctypes.c_ushort
        self.PingNumber = None  # type: ctypes.c_uint
        self.Seconds = None  # type: ctypes.c_uint
        self.Millisec = None  # type: ctypes.c_uint
        self.Latency = None  # type: ctypes.c_ushort
        self.SonarID = None  # type: ctypes.Array[ctypes.c_ushort]
        self.SonarModel = None  # type: ctypes.c_ushort
        self.Frequency = None  # type: ctypes.c_ushort
        self.SSpeed = None  # type: ctypes.c_ushort
        self.SampleRate = None  # type: ctypes.c_ushort
        self.PingRate = None  # type: ctypes.c_ushort
        self.Range = None  # type: ctypes.c_ushort
        self.Power = None  # type: ctypes.c_ushort
        self.Gain = None  # type: ctypes.c_ushort
        self.PulseWidth = None  # type: ctypes.c_ushort
        self.Spread = None  # type: ctypes.c_ushort
        self.Absorb = None  # type: ctypes.c_ushort
        self.Proj = None  # type: ctypes.c_ushort
        self.ProjWidth = None  # type: ctypes.c_ushort
        self.SpacingNum = None  # type: ctypes.c_ushort
        self.SpacingDen = None  # type: ctypes.c_ushort
        self.ProjAngle = None  # type: ctypes.c_short
        self.MinRange = None  # type: ctypes.c_ushort
        self.MaxRange = None  # type: ctypes.c_ushort
        self.MinDepth = None  # type: ctypes.c_ushort
        self.MaxDepth = None  # type: ctypes.c_ushort
        self.Filters = None  # type: ctypes.c_ushort
        self.bFlags = None  # type: ctypes.Array[ctypes.c_ubyte]
        self.HeadTemp = None  # type: ctypes.c_short
        self.BeamCnt = None  # type: ctypes.c_ushort
    def to_bytes(self):
        pass


class SNP1(XTFBase):
    ID = None  # type: CField
    HeaderSize = None  # type: CField
    DataSize = None  # type: CField
    PingNumber = None  # type: CField
    Beam = None  # type: CField
    SnipSamples = None  # type: CField
    GainStart = None  # type: CField
    GainEnd = None  # type: CField
    FragOffset = None  # type: CField
    FragSamples = None  # type: CField

    def __init__(self):
        self.ID = None  # type: ctypes.c_uint
        self.HeaderSize = None  # type: ctypes.c_ushort
        self.DataSize = None  # type: ctypes.c_ushort
        self.PingNumber = None  # type: ctypes.c_uint
        self.Beam = None  # type: ctypes.c_ushort
        self.SnipSamples = None  # type: ctypes.c_ushort
        self.GainStart = None  # type: ctypes.c_ushort
        self.GainEnd = None  # type: ctypes.c_ushort
        self.FragOffset = None  # type: ctypes.c_ushort
        self.FragSamples = None  # type: ctypes.c_ushort
    def to_bytes(self):
        pass


