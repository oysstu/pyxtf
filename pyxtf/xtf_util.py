from typing import Union, List
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from pyxtf import xtf_read, XTFHeaderType, XTFHeaderNavigation


def datetime64_to_utc(dt64: Union[np.datetime64, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Converts from numpy.datetime64 to UTC (fractional seconds)
    :param dt64: A signgle numpy.datetime64 object or an array of datetimes
    :return: Floating point utc (seconds9
    """
    return (dt64 - np.datetime64('1970-01-01T00:00:00.00Z')) / np.timedelta64(1, 's')


def plot_navigation(paths: List[str] = None):
    # TODO: Plot navigation from other packets if navigation packets not present.

    # Open file dialog if paths not specified
    if not paths:
        root_gui = tk.Tk()
        root_gui.withdraw()
        paths = filedialog.askopenfilenames(
            title='Select XTF files...',
            filetypes= [('eXtended Triton Files (XTF)', '.xtf')]
        )

    nav = []  # type: List[pyxtf.XTFHeaderNavigation]
    for path in paths:
        (fh, p) = xtf_read(path, types=[XTFHeaderType.navigation])
        if XTFHeaderType.navigation in p:
            nav.extend(p[XTFHeaderType.navigation])

    # Sort by time
    if nav:
        nav.sort(key=XTFHeaderNavigation.get_time)
        x = [p.RawXcoordinate for p in nav]
        y = [p.RawYcoordinate for p in nav]

        plt.plot(x, y)
        plt.show()
    else:
        print('No navigation packets present in XTF files')


if __name__ == '__main__':
    import time
    t = time.time()
    x = np.datetime64(int(time.time()), 's') + np.timedelta64(int((t - int(time.time()))*10**6), 'us')
    y = datetime64_to_utc(x)
    print('time.time(): {}\ndatetime64: {}\nutc: {}'.format(t, x, y))

    plot_navigation()


