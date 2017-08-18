import contextlib
import time

from numba import cfunc
from scipy.integrate import quad
from scipy._lib._ccallback import LowLevelCallable

from math import sin

a, b = 0.01, 100


@contextlib.contextmanager
def timing():
    s = time.time()
    yield
    print('Time: {}s'.format(time.time() - s))


def func(x):
    return sin(1/x)


optimized_func = cfunc("float64(float64)")(func)

print('Optimized version')
with timing():
    out1 = quad(LowLevelCallable(optimized_func.ctypes), a, b)
    print(out1)

print('Optimized version')
with timing():
    out1 = quad(LowLevelCallable(optimized_func.ctypes), a, b)
    print(out1)


print('Standard version')
with timing():
    out2 = quad(func, a, b)
    print(out2)
