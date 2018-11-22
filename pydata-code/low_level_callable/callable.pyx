from libc.math cimport INFINITY
from numpy cimport npy_intp

cdef api int nbmin(double *buffer, npy_intp filter_size,
                   double *return_value, void *user_data):

    cdef npy_intp i

    return_value[0] = INFINITY
    for i in range(filter_size):
        if buffer[i] < return_value[0]:
            return_value[0] = buffer[i]
    return 1
