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

class KMOutputDatagramHeader(KMBase):
    NumberOfBytes = None  # type: CField
    StartID = None  # type: CField
    DatagramType = None  # type: CField
    EMModelNumber = None  # type: CField
    Date = None  # type: CField
    Time = None  # type: CField

    def __init__(self):
        self.NumberOfBytes = None  # type: ctypes.c_uint
        self.StartID = None  # type: ctypes.c_ubyte
        self.DatagramType = None  # type: ctypes.c_ubyte
        self.EMModelNumber = None  # type: ctypes.c_ushort
        self.Date = None  # type: ctypes.c_uint
        self.Time = None  # type: ctypes.c_uint
    def get_time(self):
        pass
    def to_bytes(self):
        pass


class KMRawRangeAngle78_TX(XTFBase):
    TiltAngle = None  # type: CField
    FocusRange = None  # type: CField
    SignalLength = None  # type: CField
    TransmitDelay = None  # type: CField
    CentreFrequency = None  # type: CField
    MeanAbsorptionCoeff = None  # type: CField
    SignalWaveformId = None  # type: CField
    SectorNumber = None  # type: CField
    SignalBandwidth = None  # type: CField

    def __init__(self):
        self.TiltAngle = None  # type: ctypes.c_short
        self.FocusRange = None  # type: ctypes.c_ushort
        self.SignalLength = None  # type: ctypes.c_float
        self.TransmitDelay = None  # type: ctypes.c_float
        self.CentreFrequency = None  # type: ctypes.c_float
        self.MeanAbsorptionCoeff = None  # type: ctypes.c_ushort
        self.SignalWaveformId = None  # type: ctypes.c_ubyte
        self.SectorNumber = None  # type: ctypes.c_ubyte
        self.SignalBandwidth = None  # type: ctypes.c_float
    def to_bytes(self):
        pass


class KMRawRangeAngle78_RX(XTFBase):
    BeamAngle = None  # type: CField
    SectorNumber = None  # type: CField
    DetectionInfo = None  # type: CField
    DetectionWindowLength = None  # type: CField
    QualityFactor = None  # type: CField
    DCorr = None  # type: CField
    TravelTime = None  # type: CField
    Reflectivity = None  # type: CField
    CleaningInfo = None  # type: CField
    Spare = None  # type: CField

    def __init__(self):
        self.BeamAngle = None  # type: ctypes.c_short
        self.SectorNumber = None  # type: ctypes.c_ubyte
        self.DetectionInfo = None  # type: ctypes.c_ubyte
        self.DetectionWindowLength = None  # type: ctypes.c_ushort
        self.QualityFactor = None  # type: ctypes.c_ubyte
        self.DCorr = None  # type: ctypes.c_byte
        self.TravelTime = None  # type: ctypes.c_float
        self.Reflectivity = None  # type: ctypes.c_short
        self.CleaningInfo = None  # type: ctypes.c_byte
        self.Spare = None  # type: ctypes.c_ubyte
    def get_detection_info(self):
        pass
    def has_valid_detection(self):
        pass
    def is_compensated(self) -> bool:
        pass
    def to_bytes(self):
        pass


class KMRawRangeAngle78(KMBase):
    NumberOfBytes = None  # type: CField
    StartID = None  # type: CField
    DatagramType = None  # type: CField
    EMModelNumber = None  # type: CField
    Date = None  # type: CField
    Time = None  # type: CField
    PingCounter = None  # type: CField
    SerialNumber = None  # type: CField
    SoundSpeed = None  # type: CField
    Ntx = None  # type: CField
    Nrx = None  # type: CField
    ValidDetectionsNum = None  # type: CField
    SamplingFrequency = None  # type: CField
    DScale = None  # type: CField
    TX = None  # type: CField
    RX = None  # type: CField
    Spare = None  # type: CField
    EndID = None  # type: CField
    Checksum = None  # type: CField

    def __init__(self):
        self.NumberOfBytes = None  # type: ctypes.c_uint
        self.StartID = None  # type: ctypes.c_ubyte
        self.DatagramType = None  # type: ctypes.c_ubyte
        self.EMModelNumber = None  # type: ctypes.c_ushort
        self.Date = None  # type: ctypes.c_uint
        self.Time = None  # type: ctypes.c_uint
        self.PingCounter = None  # type: ctypes.c_ushort
        self.SerialNumber = None  # type: ctypes.c_ushort
        self.SoundSpeed = None  # type: ctypes.c_ushort
        self.Ntx = None  # type: ctypes.c_ushort
        self.Nrx = None  # type: ctypes.c_ushort
        self.ValidDetectionsNum = None  # type: ctypes.c_ushort
        self.SamplingFrequency = None  # type: ctypes.c_float
        self.DScale = None  # type: ctypes.c_uint
        self.TX = None  # type: ctypes.Array[KMRawRangeAngle78_TX]
        self.RX = None  # type: ctypes.Array[KMRawRangeAngle78_RX]
        self.Spare = None  # type: ctypes.c_ubyte
        self.EndID = None  # type: ctypes.c_ubyte
        self.Checksum = None  # type: ctypes.c_ushort
    def get_time(self):
        pass
    def to_bytes(self):
        pass


