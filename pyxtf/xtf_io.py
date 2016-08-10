import pickle
from heapq import merge  # Used to merge sorted lists (file pos)
from itertools import repeat
from os.path import splitext, isfile
from typing import Tuple, Any, Dict, Union, Generator, Iterable
from warnings import warn

from pyxtf.xtf_ctypes import *


def xtf_padding(size: int) -> int:
    """
    Calculates the necessary padding to make the XTF packet align on a 64byte multiple.
    This padding is optional, but can improve performance.
    :param size: The number of bytes of the packet.
    :return: Padding required to align with a 64byte multiple.
    """
    return ((size + 63) // 64) * 64


def xtf_idx_pos_iter(
        xtf_idx: Dict[XTFHeaderType, List[int]],
        types: List[XTFHeaderType]) -> Iterable[Tuple[int, XTFHeaderType]]:
    """
    Returns an iterator of tuples (file_pos, header_type) sorted by file position (merges the header types)
    :param xtf_idx: The dictionary index object
    :param types: The packet types to return, None returns all types
    :return: Generator object
    """
    if types:
        xtf_idx_iters = [zip(xtf_idx[key], repeat(key)) for key in types if key in xtf_idx]
    else:
        xtf_idx_iters = [zip(val, repeat(key)) for key, val in xtf_idx.items()]

    # Use the heapq.merge function to return sorted iterator of file indices
    return merge(*xtf_idx_iters)


def xtf_read_gen(path: str, types: List[XTFHeaderType] = None) -> Generator[
    Union[XTFFileHeader, XTFPacket], None, None]:
    """
    Generator object which iterates over the XTF file, return first the file header and then subsequent packets
    :param path: The path to the XTF file
    :param types: Optional list of XTFHeaderTypes to keep. Default (None) returns all types. Can improve performance
    :return: None
    """
    # Read index file if it exists
    (path_root, _) = splitext(path)
    path_idx = path_root + '.pyxtf_idx'
    has_idx = isfile(path_idx)
    if has_idx:
        with open(path_idx, 'rb') as f_idx:
            xtf_idx = pickle.load(f_idx)  # type: Dict[XTFHeaderType, List[int]]
    else:
        xtf_idx = {}

    # Read XTF file
    with open(path, 'rb') as f:
        # Read initial file header
        file_header = XTFFileHeader(buffer=f)

        n_channels = file_header.channel_count()
        if n_channels > 6:
            raise NotImplementedError("Support for more than 6 channels not implemented.")

        # Return the file header before starting packet iteration
        yield file_header

        # Loop through XTF packets and handle according to type
        if has_idx:
            # Only return packets that matches types arg (if None, return all)
            for packet_start_loc, p_headertype in xtf_idx_pos_iter(xtf_idx, types):
                f.seek(packet_start_loc)

                # Get the class associated with this header type (if any)
                # How to read and construct each type is implemented in the class (default impl. in XTFBase.__new__)
                p_class = XTFPacketClasses.get(p_headertype, None)
                if p_class:
                    p_header = p_class(buffer=f, file_header=file_header)
                    yield p_header
                else:
                    warning_str = 'Unsupported packet type \'{}\' encountered'.format(str(p_headertype))
                    warn(warning_str)
        else:
            # Preallocate, as it is assigned to at every iteration
            p_start = XTFPacketStart()

            while True:
                # Test for file end without advancing the file position
                if not f.peek(1):
                    break

                # Save packet start location
                packet_start_loc = f.tell()

                # Read the first few shared packet bytes without advancing file pointer
                bytes_read = f.readinto(p_start)
                if bytes_read < ctypes.sizeof(XTFPacketStart):
                    raise RuntimeError('XTF file shorter than expected while reading packet.')

                # Only return packets that matches types arg (if None, return all)
                p_headertype = XTFHeaderType(p_start.HeaderType)
                if not types or p_headertype in types:
                    f.seek(packet_start_loc)

                    # Get the class associated with this header type (if any)
                    # How to read and construct each type is implemented in the class (default impl. in XTFBase.__new__)
                    p_class = XTFPacketClasses.get(p_headertype, None)
                    if p_class:
                        p_header = p_class(buffer=f, file_header=file_header)
                        yield p_header
                    else:
                        warning_str = 'Unsupported packet type \'{}\' encountered'.format(str(p_headertype))
                        warn(warning_str)

                # Skip over any data padding before next iteration
                f.seek(packet_start_loc + p_start.NumBytesThisRecord)

                # Store index file information
                try:
                    xtf_idx[p_headertype].append(packet_start_loc)
                except KeyError:
                    xtf_idx[p_headertype] = [packet_start_loc]

            # Pickle index file
            with open(path_idx, mode='wb') as f_idx:
                pickle.dump(xtf_idx, f_idx)

        return


def xtf_read(path: str, types: List[XTFHeaderType] = None) -> Tuple[XTFFileHeader, Dict[XTFHeaderType, List[Any]]]:
    """
    Wrapper around the read generator object, which sorts the packet types into a dictionary
    :param path: The path of the XTF file
    :param types: Optional list of XTFHeaderTypes to keep. Default (None) returns all types. Can improve performance
    :return:
    """
    # Intialize generator and read file header (first item)
    gen = xtf_read_gen(path, types)
    file_header = next(gen)

    # Loop through XTF packets, sort into dict
    packets = {}  # type: Dict[XTFHeaderType, List[Any]]
    for packet in gen:
        p_headertype = XTFHeaderType(packet.HeaderType)
        try:
            packets[p_headertype].append(packet)
        except KeyError:
            packets[p_headertype] = [packet]

    return file_header, packets


def concatenate_channel(
        pings: List[XTFPingHeader],
        file_header: XTFFileHeader,
        channel: int,
        weighted: bool = False) -> np.ndarray:
    """
    Concatenates the list of individual pings, and pads as necessary on the correct side to form a dense representation.
    :param pings: A list of ping packets to concatenate
    :param file_header: The file header header (used to determine channel types, stbd/port sonar)
    :param channel: The channel number to concatenate
    :param weighted: If true, the data is multiplied with the ping chan header weight parameter, 2 ** -N
    :return: The sonar image as a dense numpy array
    """
    # Sort pings by time
    pings.sort(key=XTFPingHeader.get_time)

    # find array of largest size
    sizes = [ping.data[channel].shape[0] for ping in pings]
    min_sz, max_sz = min(sizes), max(sizes)

    # Use numpy.vstack if the sizes are all the same
    if min_sz == max_sz:
        out_array = np.vstack([ping.data[channel] for ping in pings[::-1]])
    else:
        # Get type of this channel
        chan_type = file_header.ChanInfo[pings[0].ping_chan_headers[channel].ChannelNumber].TypeOfChannel

        out_array = np.empty(shape=(len(pings), max_sz), dtype=pings[0].data[0].dtype)
        for i, ping in enumerate(pings[::-1]):
            sz = ping.data[channel].shape[0]

            if chan_type == XTFChannelType.stbd:
                out_array[i, :sz] = ping.data[channel]
                out_array[i, sz:] = 0
            elif chan_type == XTFChannelType.port:
                out_array[i, :max_sz - sz] = 0
                out_array[i, max_sz - sz:] = ping.data[channel]
            else:
                # All other types: pad each side equally
                pad_div = (max_sz - sz) // 2
                remainder = 1 if (max_sz - sz) % 2 else 0
                out_array[i, :pad_div] = 0
                out_array[i, pad_div:max_sz - (pad_div + remainder)] = ping.data[channel]
                out_array[i, -pad_div:] = 0

    if weighted:
        weight_factors = [ping.ping_chan_headers[channel].Weight for ping in pings[::-1]]
        out_array *= (2 ** -np.array(weight_factors)).astype(out_array.dtype)[:, np.newaxis]

    return out_array


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Read file header and packets
    test_path = r'..\data\DemoFiles\Isis_Sonar_XTF\Reson7125.XTF'
    (fh, p) = xtf_read(test_path)

    print('The following (supported) packets are present (XTFHeaderType:count): \n\t' +
          str([key.name + ':{}'.format(len(v)) for key, v in p.items()]))

    # Get multibeam (xyza) if present
    if XTFHeaderType.bathy_xyza in p:
        np_mb = [[y.fDepth for y in x.data] for x in p[XTFHeaderType.bathy_xyza]]
        np_mb = np.vstack(np_mb)
        # Transpose if the longest axis is vertical
        np_mb = np_mb if np_mb.shape[0] < np_mb.shape[1] else np_mb.T
        plt.figure()
        plt.imshow(np_mb, cmap='hot')

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
        np_chan1 = np.log10(np_chan1 + 1)
        np_chan2 = np.log10(np_chan2 + 1)

        # Transpose so that the largest axis is horizontal
        np_chan1 = np_chan1 if np_chan1.shape[0] < np_chan1.shape[1] else np_chan1.T
        np_chan2 = np_chan2 if np_chan2.shape[0] < np_chan2.shape[1] else np_chan2.T

        # The following plots the waterfall-view in separate subplots
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.imshow(np_chan1, cmap='gray', vmin=0, vmax=np.log10(upper_limit))
        ax2.imshow(np_chan2, cmap='gray', vmin=0, vmax=np.log10(upper_limit))

        # The following plots a signal-view of the 100th ping (in the file)
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

    plt.show()

