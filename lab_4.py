import numpy as np
import scipy.stats
import scipy.signal

import matplotlib.pyplot as plt
#%matplotlib inline
rv = scipy.stats.uniform()

ng = 51
n = int(ng / 4)

N = 2 ** n
M = 10

i = np.arange(N)

s2 = 2 * rv.rvs(N) \
     + ng * np.cos(2 * M * np.pi * i / N) * (1 + 0.1 * rv.rvs(N)) \
     + 17 * np.cos(4 * M * np.pi * i / N + rv.rvs(N)) \
        + 3 * np.cos(5 * M * np.pi * i / N) * rv.rvs(N) * (rv.rvs(N) + ng)


def transformation(s1):
    i = np.arange(N)

    a = np.array([(2 / N) * np.sum(s1 * np.cos(2 * np.pi * i * l / N))
                  for l in range(1, int(N / 2 - 1))])
    a0 = np.array([(1 / N) * np.sum(s1 * np.cos(0))])
    an = np.array([(1 / N) * np.sum(s1 * np.cos(np.pi * i))])

    a = np.insert(a, 0, a0)
    a = np.append(a, an)

    b = np.array([(2 / N) * np.sum(s1 * np.sin(2 * np.pi * i * j / N))
                  for j in range(int(N / 2))])

    c = np.sqrt(a ** 2 + a ** 2)

    return a, b, c


def reverse_transformation(a, b):
    j = np.arange(int(N / 2))

    return np.array([np.sum(a * np.cos(2 * np.pi * j * i / N))
                     + np.sum(b * np.sin(2 * np.pi * j * i / N))
                     for i in range(N)])


def plot(s1, a, b, r1):
    fig, ax = plt.subplots(3, 1, figsize=(20, 20))
    fig2, ax2 = plt.subplots(2, 1, figsize=(20, 20))
    ax[0].set_title("Actual")
    ax[0].plot(s1)

    ax[1].set_title("A")
    ax[1].plot(a)

    ax[2].set_title("B")
    ax[2].plot(b)

    ax2[0].set_title("Reverse transformation")
    ax2[0].plot(r1)

    ax2[1].set_title("Difference")
    ax2[1].plot(s1 - r1)

    plt.show()

s1 = s2

# Перетворення Фур'є
# variant 1
a, b, c = transformation(s1=s1)
# Обернене перетворення Фур'є
r1 = reverse_transformation(a, b)
plot(s1=s1, a=a, b=b, r1=r1)

va = np.array([0.42 - 0.5 * np.cos(2 * np.pi * i / N) + 0.08 * np.cos(4 * np.pi * i / N)
              for i in range(N)])

# variant 2
s1 = s2 * va

a, b, c = transformation(s1=s1)
r1 = reverse_transformation(a, b)
plot(s1=s1, a=a, b=b, r1=r1)

vb = np.array([0.54 - 0.46 * np.cos(2 * np.pi * i / N) for i in range(N)])

# variant 3

s1 = s2 * vb

a, b, c = transformation(s1=s1)
r1 = reverse_transformation(a, b)
plot(s1=s1, a=a, b=b, r1=r1)
