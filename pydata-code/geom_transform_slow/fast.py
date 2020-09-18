import ctypes
import numpy as np
from scipy import ndimage, LowLevelCallable
import time

from example import get_transform

im = np.random.randn(1000, 1000)
shift = 0.5

user_data = ctypes.c_double(shift)
ptr = ctypes.cast(ctypes.pointer(user_data), ctypes.c_void_p)
callback = LowLevelCallable(get_transform(), ptr)

start = time.time()
ndimage.geometric_transform(im, callback)
stop = time.time()

print(stop - start)
