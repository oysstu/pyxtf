from typing import Union

import numpy as np


def datetime64_to_utc(dt64: Union[np.datetime64, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Converts from numpy.datetime64 to UTC (fractional seconds)
    :param dt64: A signgle numpy.datetime64 object or an array of datetimes
    :return: Floating point utc (seconds9
    """
    return (dt64 - np.datetime64('1970-01-01T00:00:00.00Z')) / np.timedelta64(1, 's')



if __name__ == '__main__':
    import time
    t = time.time()
    x = np.datetime64(int(time.time()), 's') + np.timedelta64(int((t - int(time.time()))*10**6), 'us')
    y = datetime64_to_utc(x)
    print('time.time(): {}\ndatetime64: {}\nutc: {}'.format(t, x, y))


