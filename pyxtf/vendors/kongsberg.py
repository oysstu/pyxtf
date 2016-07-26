'''
This file contains some of the kongsberg datagram formats.
Based on Kongsberg Document 850-160692 (EM Series Datagram Formats) Rev.U (June 2015)

The following echosounders: EM3002, EM710, EM302, EM122, EM2040, EM2040C and ME70BO
use little endian byte ordering. Beware that others might not.
'''

# TODO: Implement automatic byte order check, and covert each field to little endian (or change the base class)

import ctypes
from enum import IntEnum, unique
from io import IOBase, BytesIO
from pyxtf.xtf_ctypes import XTFBase
import warnings


@unique
class KMDatagramType(IntEnum):
    depth = 0x44
    xyz_88 = 0x58
    extra_detections = 0x6C
    central_beams_echogram = 0x4B
    raw_range_and_angle_F = 0x46
    raw_range_and_angle_f = 0x66
    raw_range_and_angle_78 = 0x4E
    seabed_image_diagram = 0x53
    seabed_image_data_Y = 0x59
    water_column = 0x6B
    quality_factor = 0x4F
    attitude = 0x41
    network_attitude_velocity = 0x6E
    clock = 0x43
    pressure_or_height = 0x68
    heading = 0x48
    position = 0x50
    single_beam_echo_sounder_depth = 0x45
    tide = 0x54
    sound_speed = 0x47
    sound_speed_profile = 0x55
    ssp_output = 0x57
    installation_param_start = 0x49
    installation_param_stop = 0x69
    installation_param_remote = 0x70
    runtime_param = 0x52
    mechanical_transducer_tilt = 0x4A
    extra_param = 0x33
    pu_id_output = 0x30
    pu_status = 0x31
    pu_bist_result = 0x42


class KMOutputDatagramHeader(XTFBase):
    '''
    Common starting header for all EM output datagrams
    '''
    _pack_ = 1
    _fields_ = [
        ('NumberOfBytes', ctypes.c_uint32),
        ('StartID', ctypes.c_uint8),
        ('DatagramType', ctypes.c_uint8),
        ('EMModelNumber', ctypes.c_uint16),
        ('Date', ctypes.c_uint32),  # Year*10000 + Month*100 + Day
        ('Time', ctypes.c_uint32)  # Time since midnight in milliseconds
    ]

    def __new__(cls, buffer: IOBase = None):
        return super().__new__(cls, buffer=buffer)

    def __init__(self, buffer: IOBase = None, *args, **kwargs):
        super().__init__(buffer=buffer, *args, **kwargs)


class KMRawRangeAngle78_TX(XTFBase):
    '''
    Structure that is repeated Ntx times in the KMRawRangeAngle78 class
    '''
    _pack_ = 1
    _fields_ = [
        ('TiltAngle', ctypes.c_int16),  # In 0.01 deg
        ('FocusRange', ctypes.c_uint16),  # In 0.1m (0 = no focusing applied)
        ('SignalLength', ctypes.c_float),  # In seconds
        ('TransmitDelay', ctypes.c_float),  # Sector transmit delay re first TX pulse, in seconds
        ('CentreFrequency', ctypes.c_float),  # In Hz
        ('MeanAbsorptionCoeff', ctypes.c_uint16),  # In 0.01 dB/km
        ('SignalWaveformId', ctypes.c_uint8),  # 0 to 99 (0 = cw, 1 = FM up sweep, 2 = FM down sweep)
        ('SectorNumber', ctypes.c_uint8),  # Transmit sector number / TX array index
        ('SignalBandwidth', ctypes.c_float)  # In Hz
    ]

    def __new__(cls, buffer: IOBase = None):
        return super().__new__(cls, buffer=buffer)

    def __init__(self, buffer: IOBase = None, *args, **kwargs):
        super().__init__(buffer=buffer, *args, **kwargs)


class KMRawRangeAngle78_RX(XTFBase):
    '''
    Structure that is repeated Nrx times in the KMRawRangeAngle78 class
    '''
    _pack_ = 1
    _fields_ = [
        ('BeamAngle', ctypes.c_int16),  # Beam pointing angle, in 0.01 deg
        ('SectorNumber', ctypes.c_uint8),  # Transmit sector number
        ('DetectionInfo', ctypes.c_uint8),
        ('DetectionWindowLength', ctypes.c_uint16),
        ('QualityFactor', ctypes.c_uint8),
        ('DCorr', ctypes.c_int8),
        ('TravelTime', ctypes.c_float),  # Two way travel time
        ('Reflectivity', ctypes.c_int16),  # in 0.1 dB
        ('CleaningInfo', ctypes.c_int8),  # Real time cleaning info
        ('Spare', ctypes.c_uint8)
    ]

    def __new__(cls, buffer: IOBase = None):
        return super().__new__(cls, buffer=buffer)

    def __init__(self, buffer: IOBase = None, *args, **kwargs):
        super().__init__(buffer=buffer, *args, **kwargs)

    def has_valid_detection(self):
        return not bool(self.DetectionInfo & 0b10000000)

    def get_detection_info(self):
        info = self.DetectionInfo & 0x0F
        if self.has_valid_detection():
            if info == 0:
                return 'Amplitude'
            elif info == 1:
                return 'Phase'
        else:
            if info == 0:
                return 'Normal'
            elif info == 1:
                return 'Interpolated/Extrapolated'
            elif info == 2:
                return 'Estimated'
            elif info == 3:
                return 'Rejected'
            elif info == 4:
                return 'No data available'

        return 'Unknown'

    def is_compensated(self) -> bool:
        '''
        Is reflectivity correction for Lamberts law and for normal incidence used?
        :return: bool
        '''
        return bool(self.DetectionInfo & 0x10)


class KMRawRangeAngle78(XTFBase):
    _pack_ = 1
    _fields_ = [
        ('NumberOfBytes', ctypes.c_uint32),
        ('StartID', ctypes.c_uint8),
        ('DatagramType', ctypes.c_uint8),
        ('EMModelNumber', ctypes.c_uint16),
        ('Date', ctypes.c_uint32),  # Year*10000 + Month*100 + Day
        ('Time', ctypes.c_uint32),  # Time since midnight in milliseconds
        ('PingCounter', ctypes.c_uint16),
        ('SerialNumber', ctypes.c_uint16),
        ('SoundSpeed', ctypes.c_uint16),  # At transducer, in 0.1 m/s
        ('Ntx', ctypes.c_uint16),  # Number of transmit sectors
        ('Nrx', ctypes.c_uint16),  # Number of receiver beams in datagram
        ('ValidDetectionsNum', ctypes.c_uint16),
        ('SamplingFrequency', ctypes.c_float),  # In Hz
        ('DScale', ctypes.c_uint32),
        ('TX', KMRawRangeAngle78_TX * 0),  # Note: the number of fields is declared in Ntx
        ('RX', KMRawRangeAngle78_RX * 0),  # Note: the number of fields is declared in Nrx
        ('Spare', ctypes.c_uint8),  # Always 0
        ('EndID', ctypes.c_uint8),  # Always 0x03
        ('Checksum', ctypes.c_uint16)  # Checksum of data between STX and ETX
    ]

    def __init__(self, buffer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not buffer:
            self.StartID = 0x02
            self.DatagramType = KMDatagramType.raw_range_and_angle_78.value
            self.EndID = 0x03

    def __new__(cls, buffer: IOBase = None):
        if buffer:
            if type(buffer) in [bytes, bytearray]:
                buffer = BytesIO(buffer)

            # Read bytes up until the variable-sized data
            base_bytes = buffer.read(cls.TX.offset)
            n_bytes = ctypes.c_uint32.from_buffer_copy(base_bytes, cls.NumberOfBytes.offset).value
            n_tx = ctypes.c_uint16.from_buffer_copy(base_bytes, cls.Ntx.offset).value
            n_rx = ctypes.c_uint16.from_buffer_copy(base_bytes, cls.Nrx.offset).value

            # Read remaining bytes
            remaining_bytes = buffer.read(n_bytes - cls.TX.offset + cls.NumberOfBytes.size)

            # Create new class dynamically with string array at the correct size
            new_name = cls.__name__ + '_ntx{}_nrx{}'.format(n_tx, n_rx)
            new_fields = cls._fields_.copy()
            tx_idx = [i for i, (name, type) in enumerate(cls._fields_) if name == 'TX'][0]
            rx_idx = [i for i, (name, type) in enumerate(cls._fields_) if name == 'RX'][0]
            new_fields[tx_idx] = ('TX', KMRawRangeAngle78_TX * n_tx)
            new_fields[rx_idx] = ('RX', KMRawRangeAngle78_RX * n_rx)
            new_cls = type(new_name, (ctypes.LittleEndianStructure,), {
                '__str__': cls.__str__,
                '_pack_': cls._pack_,
                '_fields_': new_fields
            })

            all_bytes = base_bytes + remaining_bytes
            obj = new_cls.from_buffer_copy(all_bytes)

            # Checksum (not crc16, but a straight sum of bytes with overflow)
            chk = (sum(all_bytes[new_cls.DatagramType.offset:new_cls.EndID.offset]) & 0xFFFF)
            if chk != obj.Checksum:
                warning_str = '{}: Checksum failed'.format(cls.__name__)
                warnings.warn(warning_str)

        else:
            obj = super().__new__(cls)

        return obj


if __name__ == '__main__':
    from pyxtf.xtf_io import xtf_read
    from pyxtf.xtf_ctypes import XTFHeaderType
    test_path = r'..\..\data\Survey\27apr\EM2040\em2040-0007-l02-20160427-124929_RAW.xtf'
    (fh, p) = xtf_read(test_path)

    print('The following (supported) packets are present (XTFHeaderType:count): \n\t{}\n'.format(
        str([key.name + ':{}'.format(len(v)) for key, v in p.items()])
    ))

    if XTFHeaderType.multibeam_raw_beam_angle in p:
        # The KMRawRangeAngle78 data is stored as raw bytes in the data field of a XTFPingHeader type
        data_bytes = p[XTFHeaderType.multibeam_raw_beam_angle][0].data
        decoded_data = KMRawRangeAngle78(data_bytes)
        print(decoded_data)

