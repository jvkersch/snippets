from scipy import ndimage
import numpy as np
import time

def transform(output_coordinates, shift):
    input_coordinates = output_coordinates[0] - shift, output_coordinates[1] - shift
    return input_coordinates

#im = np.arange().reshape(4, 3).astype(np.float64)

im = np.random.randn(1000, 1000)

shift = 0.5

start = time.time()
ndimage.geometric_transform(im, transform, extra_arguments=(shift,))
stop = time.time()

print(stop - start)
