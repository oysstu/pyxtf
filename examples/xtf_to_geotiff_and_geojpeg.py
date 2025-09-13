"""
Example of how to convert a single-channel sonar sidescan XTF file to a georeferenced tiff and jpeg with sidecar-files.
Toggle resize_half_width if your image width needs to be resized to half width.
Toggle concatenate_channel weighted argument to fit your data requirements.
"""

import math
import numpy as np
from PIL import Image
from haversine import inverse_haversine, Unit
import rasterio
import xml.etree.ElementTree as ET

import pyxtf

xtf_input = "test.xtf" # Input XTF file
bitdepth = 8 # Use 8 or 16 bits to store the pixel values
resize_half_width = False # Resize image, half width
weighted = False # Toggle concatenate_channel weighted argument to fit your data input requirements

# Output filepaths
tif_output = f"{xtf_input}.tif"
jpeg_output = f"{xtf_input}.jpeg"
jgw_output = f"{xtf_input}.jgw"
aux_xml_output = f"{xtf_input}.jpeg.aux.xml"
geotiff_output = f"{xtf_input}_geotiff.tif"

def _write_jgw(jgw_output, transform):
    tfw = open(jgw_output, 'wt')
    tfw.write(f"{transform.a}\n")
    tfw.write(f"{transform.d}\n")
    tfw.write(f"{transform.b}\n")
    tfw.write(f"{transform.e}\n")
    tfw.write(f"{transform.c}\n")
    tfw.write(f"{transform.f}\n")
    tfw.close()

def _write_pam_aux_xml(aux_xml_output, srs_txt, transform):
    root = ET.Element("PAMDataset")
    srs = ET.SubElement(root, "SRS", attrib={"dataAxisToSRSAxisMapping": "2,1"}) # Input to GDAL, "2,1" tells that the first data axis (rows) shall be interpreted as second SRS axis (Y/Latitude); and the other way around
    srs.text = srs_txt
    geotransform = ET.SubElement(root, "GeoTransform")
    geotransform.text = f"{transform.c}, {transform.a}, {transform.b}, {transform.f}, {transform.d}, {transform.e}"
    metadata = ET.SubElement(root, "Metadata")
    mdi_area = ET.SubElement(metadata, "MDI", attrib={"key": "AREA_OR_POINT"})
    mdi_area.text = "Area"
    pamrasterband = ET.SubElement(root, "PAMRasterBand", attrib={"band": "1"})
    band_metadata = ET.SubElement(pamrasterband, "Metadata", attrib={"domain": "IMAGE_STRUCTURE"})
    mdi_compression = ET.SubElement(band_metadata, "MDI", attrib={"key": "COMPRESSION"})
    mdi_compression.text = "JPEG"

    ET.indent(root)

    tree = ET.ElementTree(root)
    tree.write(aux_xml_output, encoding="utf-8", xml_declaration=False)

def _calculate_acoustic_bearing_radians(SensorHeading, BEARING_90_DEG_STARBOARD):
    # Calculate offset to sensor heading, this is acoustic bearing (radians), depends on channel port or starboard
    acoustic_bearing_radians = None
    if BEARING_90_DEG_STARBOARD:
        acoustic_bearing_radians = math.radians(SensorHeading + 90)
    else:
        acoustic_bearing_radians = math.radians(SensorHeading - 90)

    return acoustic_bearing_radians

def _calculate_outermost_latlon(sensor_lat, sensor_lon, acoustic_bearing_radians, groundrange):
    # Calculate the latitude and longitude of the GroundRange outermost point, in the acoustic bearing
    p1 = (sensor_lat, sensor_lon)
    p2 = inverse_haversine(p1, groundrange, acoustic_bearing_radians, Unit.METERS)
    return p2

def _create_gcps(sensor_pos_first_ping, sensor_pos_last_ping, outer_pos_first_ping, outer_pos_last_ping, is_starboard, height, width):
    # Create GroundControlPoint, four points used to translate the image pixels onto the map
    #
    # Assumptions:
    # Data captured from starboard:
    # Bottom left pixel is sensor position first ping
    # Top left pixel is sensor position last ping
    #
    # Data captured from port:
    # Bottom right pixel is sensor position first ping
    # Top right pixel is sensor position last ping

    gcps = None
    if is_starboard == True:
        gcps = [ # X is longitude, Y is latitude
            rasterio.control.GroundControlPoint(row=0,         col=0,         x=sensor_pos_last_ping[0],         y=sensor_pos_last_ping[1],    z=0), # top left pixel
            rasterio.control.GroundControlPoint(row=0,         col=width - 1, x=outer_pos_last_ping[0],   y=outer_pos_last_ping[1],    z=0), # top right pixel
            rasterio.control.GroundControlPoint(row=height - 1, col=width - 1, x=outer_pos_first_ping[0],   y=outer_pos_first_ping[1], z=0), # bottom right pixel
            rasterio.control.GroundControlPoint(row=height - 1, col=0,         x=sensor_pos_first_ping[0],         y=sensor_pos_first_ping[1], z=0) # bottom left pixel
        ]
    else: # Port
        gcps = [ # X is longitude, Y is latitude
            rasterio.control.GroundControlPoint(row=0,         col=0,         x=outer_pos_last_ping[0],         y=outer_pos_last_ping[1],    z=0), # top left pixel
            rasterio.control.GroundControlPoint(row=0,         col=width - 1, x=sensor_pos_last_ping[0],   y=sensor_pos_last_ping[1],    z=0), # top right pixel
            rasterio.control.GroundControlPoint(row=height - 1, col=width - 1, x=sensor_pos_first_ping[0],   y=sensor_pos_first_ping[1], z=0), # bottom right pixel
            rasterio.control.GroundControlPoint(row=height - 1, col=0,         x=outer_pos_first_ping[0],         y=outer_pos_first_ping[1], z=0) # bottom left pixel
        ]
    return gcps

def calculate_outermost_latlon_from_ping(file_header: pyxtf.XTFFileHeader, ping_header: pyxtf.XTFPingChanHeader, is_starboard=None):
    sensor_lat, sensor_lon = ping_header.SensorYcoordinate, ping_header.SensorXcoordinate
    acoustic_bearing_radians = _calculate_acoustic_bearing_radians(ping_header.SensorHeading, is_starboard)
    
    ping_chan_header = ping_header.ping_chan_headers[0]
    GroundRange = ping_chan_header.GroundRange

    outermost_lat, outermost_lon = _calculate_outermost_latlon(sensor_lat, sensor_lon, acoustic_bearing_radians, GroundRange)
    return sensor_lat, sensor_lon, outermost_lat, outermost_lon

def make_sidescan_sonar_image(fh, p, bitdepth=8, resize_half_width=False, weighted=False):
    # make_sonar_image()
    # Will read any bitdepth that pyxtf accepts and scale values to 8 or 16 bits

    upper_limit_16bit = 2 ** 16 - 1 # 0-65535
    upper_limit_8bit = 2 ** 8 - 1 # 0-255

    np_chan = pyxtf.concatenate_channel(p[pyxtf.XTFHeaderType.sonar], file_header=fh, channel=0, weighted=weighted)
    np_chan.clip(0, upper_limit_16bit, out=np_chan) # Clipping values outside valid range
    np_chan = np.log10(np_chan + 1, dtype=np.float32)

    vmin = np_chan.min()
    vmax = np_chan.max()

    if bitdepth==8:
        np_chan = ((np_chan - vmin) / (vmax - vmin)) * upper_limit_8bit # Scaling values to fit datatype uint8
        np_chan = np.clip(np_chan, 0, upper_limit_8bit) # Clipping values outside valid range
        img = Image.fromarray(np_chan.astype(np.uint8))
    elif bitdepth==16: 
        np_chan = ((np_chan - vmin) / (vmax - vmin)) * upper_limit_16bit # Scaling values to fit datatype uint16
        np_chan = np.clip(np_chan, 0, upper_limit_16bit) # Clipping values outside valid range
        img = Image.fromarray(np_chan.astype(np.uint16))
    else:
        print("make_sonar_image() invalid bitdepth, only 8 or 16 accepted. Is", bitdepth)
        exit(-1)

    if resize_half_width: # Some sonar data may be wrong ratio, this will reduce width by half
        img = img.resize((int(img.size[0]/2), img.size[1]))

    return img

(fh, p) = pyxtf.xtf_read(xtf_input)

if pyxtf.XTFHeaderType.sonar in p:
    n_channels = fh.channel_count(verbose=True)

    if n_channels > 1:
        print("Not implemented for more than one channel (either port or starboard, not both)")
        exit(-1)

    NavUnits = fh.NavUnits # If 0, then SensorYcoordinate and SensorXcoordinate is in meters. If 3, then in Lat/Long
    if NavUnits != 3:
        print("fh.NavUnits != 3, coordinates are in meters. Not implemented yet.")
        exit(-1)

    is_starboard = None
    ChannelName = str(fh.ChanInfo[0].ChannelName)
    if 'starboard' in ChannelName:
        is_starboard = True
        print("Data detected as starboard")
    elif 'port' in ChannelName:
        is_starboard = False
        print("Data detected as port")
    else:
        print("Unable to detect port or starboard in channel name.")
        exit(-1)

    sonar_image = make_sidescan_sonar_image(fh, p, bitdepth=bitdepth, resize_half_width=resize_half_width, weighted=weighted)

    # Write sonar image data to files, no georeferencing at this stage
    sonar_image.save(f'{tif_output}')
    print("TIF without georeference saved:", tif_output)
    sonar_image.save(f'{jpeg_output}')
    print("JPEG without georeference saved:", jpeg_output)

    sonar_ch = p[pyxtf.XTFHeaderType.sonar]

    first_ping = sonar_ch[0]
    fp_s_lat, fp_s_lon, fp_o_lat, fp_o_lon = calculate_outermost_latlon_from_ping(fh, first_ping, is_starboard)

    last_ping = sonar_ch[-1]
    lp_s_lat, lp_s_lon, lp_o_lat, lp_o_lon = calculate_outermost_latlon_from_ping(fh, last_ping, is_starboard)

    points = [(fp_s_lon, fp_s_lat), (fp_o_lon, fp_o_lat), (lp_s_lon, lp_s_lat), (lp_o_lon, lp_o_lat)]
    print("Outermost points:", points)

    try:
        src = rasterio.open(tif_output) # NotGeoreferencedWarning can be ignored
    except Exception as e:
        print("Unable to load source tif for conversion to geotiff")
        exit(-1)
    
    data = src.read(1)
    height, width = src.height, src.width

    # Copy the source metadata profile for use in the output
    profile = src.profile.copy()
    src.close()

    sensor_pos_first_ping = (fp_s_lon, fp_s_lat)
    sensor_pos_last_ping = (lp_s_lon, lp_s_lat)
    outer_pos_first_ping = (fp_o_lon, fp_o_lat)
    outer_pos_last_ping = (lp_o_lon, lp_o_lat)

    # Calculate and compute an Affine transform
    gcps = _create_gcps(sensor_pos_first_ping, sensor_pos_last_ping, outer_pos_first_ping, outer_pos_last_ping, is_starboard, height, width)
    transform = rasterio.transform.from_gcps(gcps)
    
    # Write worldfiles, sidecar files for the jpeg to position and transform the jpeg in the map
    target_crs = rasterio.CRS.from_epsg(4326)
    srs_wkt = target_crs.to_wkt()
    _write_pam_aux_xml(aux_xml_output, srs_wkt, transform)
    _write_jgw(jgw_output, transform)

    profile.update({
        'crs': target_crs, # EPSG:4326 is assumed
        'transform': transform
    })

    with rasterio.open(geotiff_output, "w", **profile) as dst:
        dst.write(data, 1)
    print("Geotiff output saved:", geotiff_output)