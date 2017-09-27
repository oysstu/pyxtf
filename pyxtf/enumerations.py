from enum import IntEnum, unique, Enum


class AutoIntEnum(IntEnum):
    """
    Integer enumeration that automatically increments subsequent elements.
    Comparison with int succeeds.
    """
    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__)
        obj = super(IntEnum, cls).__new__(cls)
        obj._value_ = value
        return obj

    def __int__(self):
        return self.value

    def __eq__(self, other):
        return int(self).__eq__(other) if isinstance(other, int) else Enum.__eq__(self, other)

    def __ne__(self, other):
        return int(self).__ne__(other) if isinstance(other, int) else Enum.__ne__(self, other)

    def __ge__(self, other):
        return int(self).__ge__(other) if isinstance(other, int) else Enum.__ge__(self, other)

    def __gt__(self, other):
        return int(self).__gt__(other) if isinstance(other, int) else Enum.__gt__(self, other)

    def __le__(self, other):
        return int(self).__le__(other) if isinstance(other, int) else Enum.__le__(self, other)

    def __lt__(self, other):
        return int(self).__lt__(other) if isinstance(other, int) else Enum.__lt__(self, other)


@unique
class XTFChannelType(AutoIntEnum):
    subbottom = ()
    port = ()
    stbd = ()
    bathy = ()

@unique
class XTFNavUnits(IntEnum):
    meters = 0
    latlon = 3

@unique
class XTFHeaderType(IntEnum):
    """
    The types of headers.
    """
    sonar = 0                           # Sidescan and subbottom-profiler
    notes = 1                           # Text notes
    bathy = 2                           # Bathymetry data
    attitude = 3                        # Attitude packet (pitch, roll, heave, yaw)
    forward = 4                         # Forward-look data
    elac = 5                            # Elac raw data packet (multibeam)
    raw_serial = 6                      # Raw data from serial port (ASCII)
    embed_head = 7                      # Embedded header record - num samples probably
    hidden_sonar = 8                    # Redundant (overlapping) ping from Klein 5000
    seaview_processed_bathy = 9         # Bathymetry (angles) for Seaview
    seaview_depths = 10                 # Bathymetry from Seaview data (depths)
    rsvd_highspeed_sensor = 11          # Used by Klein, 0=roll, 1=yaw
    echostrength = 12                   # Elac EchoStrength (10 values)
    georec = 13                         # Used to store mosaic parameters
    klein_raw_bathy = 14                # Bathymetry data from te Klein 5000
    highspeed_sensor2 = 15              # High speed sensor from Klein 5000
    elac_xse = 16                       # Elac dual-head
    bathy_xyza = 17
    k5000_bathy_iq = 18                 # Raw IQ data from Klein 5000 server
    bathy_snippet = 19
    gps = 20
    gps_statistics = 21
    single_beam = 22
    gyro = 23                           # Heading/speed sensor
    trackpoint = 24
    multibeam = 25
    q_singlebeam = 26
    q_multitx = 27
    q_multibeam = 28
    navigation = 42                     # Source time-stamped navigation data, holds updates of any nav data
    time = 50
    benthos_caati_sara = 60             # Custom Benthos data
    reson_7125 = 61                    # 7125 bathy data
    reson_7125_snippet = 62            # 7125 Bathy data snippets
    qinsy_r2sonic_bathy = 65            # QINSy R2Sonic bathy data
    qinsy_r2sonic_fts = 66              # QINSy R2Sonic bathy footprint time series (snippets)
    r2sonic_bathy = 68                  # Triton R2Sonic bathy data
    r2sonic_fts = 69                    # Triton R2sonic footprint time series
    coda_echoscope_data = 70            # Custom CODA Echoscope data
    coda_echoscope_config = 71          # Custom CODA Echoscope config
    coda_echoscope_image = 72           # Custom CODA Echoscope image
    edgetech_4600 = 73
    multibeam_raw_beam_angle = 74       # Note: Unsure if this is the correct name for this header-type
    reson_7018_watercolumn = 78
    sourcetime_gyro = 84                # Note: XTF_HEADER_GYRO is defined as 23 (difference is receive/source time)
    reson_position = 100                # Raw position packet, reserved for use by Reson, Inc. RESON ONLY
    bathy_proc = 102
    attitude_proc = 103
    singlebeam_proc = 104
    aux_proc = 105                      # Aux channel + aux altitude + magnetometer
    pos_raw_navigation = 107
    kleinv4_data_page = 108
    custom_vendor_data = 199
    user_defined = 200


class XTFManufacturerID(AutoIntEnum):
    unknown = ()
    benthos = ()
    reson = ()
    edgetech = ()
    klein = ()
    coda = ()
    kongsberg = ()
    cmax = ()
    marine_sonics = ()
    applied_signal = ()
    imagenex = ()
    geoacoustics = ()


class XTFSonarType(AutoIntEnum):
    none = ()
    jamstec = ()
    analog_c31 = ()
    sis1000 = ()
    analog_32chan = ()
    klein2000 = ()
    rws = ()
    df1000 = ()
    seabat = ()
    klein595 = ()
    egg260 = ()
    sonatech_dds = ()
    echoscan = ()
    elac = ()
    klein5000 = ()
    reson_seabat_8101 = ()
    imagenex_858 = ()
    usn_silos = ()
    sonatech = ()
    delph_au32 = ()
    generic_sonar = ()
    simrad_sm2000 = ()
    standard_multimedia_audio = ()
    edgetech_aci_card = ()
    edgetech_black_box = ()
    fugro_deeptow = ()
    cc_edgetech_chirp_conversion = ()
    dti_sas = ()
    fugro_osiris_ss = ()
    fugro_osiris_mb = ()
    geoacoustics_sls = ()
    simrad_em2000_em3000 = ()
    klein_system_3000 = ()
    shrsss_chirp_system = ()
    benthos_c3d_sara_caati = ()
    edgetech_mpx = ()
    cmax = ()
    benthos_sis1624 = ()
    edgetech_4200 = ()
    benthos_sis1500 = ()
    benthos_sis1502 = ()
    benthos_sis3000 = ()
    benthos_sis7000 = ()
    df1000_dcu = ()
    none_sidescan = ()
    none_multibeam = ()
    reson_7125 = ()
    coda_echoscope = ()
    kongsberg_sas = ()
    qinsy = ()
    geoacoustics_dsss = ()
    cmax_usb = ()
    swathplus_bathy = ()
    r2sonic_qinsy = ()
    r2sonic_triton = ()
    swathplus_converted_bathy = ()
    edgetech_4600 = ()
    klein_3500 = ()
    klein_5900 = ()
    em2040 = ()
    klein5kv2 = ()
    dt100 = ()
    kraken62 = ()
    unknown1 = ()
    unknown2 = ()
    kraken65 = ()
    klein_4900 = ()
    fsi_hms622 = ()
    fsi_hms6x4 = ()
    fsi_hms6x5 = ()
    deepvision_osm2 = 250


@unique
class XTFSampleFormat(IntEnum):
    """
    Used in the ChanInfo structures
    """
    legacy = 0
    ibm_float = 1
    int = 2
    word = 3
    float = 5
    byte = 8

assert XTFSonarType.fsi_hms6x5 == 69, 'XTFSonarType enumeration ends on incorrect number'