import matplotlib.pyplot as plt

from cmath import exp, pi
import numpy as np

ROOTS = np.array([1.0, exp(2*pi*1j/3.0), exp(-2*pi*1j/3.0)])


def compute_escape(xs, ys, num=100):
    """ This gets executed in the child process. Inputs
    and possible outputs must be pickleable.

    """
    zs = xs + 1j * ys
    for _ in xrange(num):
        zs += (zs**-2 - zs) / 3.0
    dist = np.absolute(zs[:, :, np.newaxis] - ROOTS)
    return dist.argmin(axis=-1)


if __name__ == '__main__':
    xs = np.linspace(-1, 1, 1000)
    ys = np.linspace(-1, 1, 1000)
    X, Y = np.meshgrid(xs, ys)
    Z = compute_escape(X, Y)

    plt.imshow(Z, interpolation='nearest')
    plt.show()
