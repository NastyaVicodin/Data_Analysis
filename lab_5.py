import numpy as np
import matplotlib.pyplot as plt
NG = 51
M = 10
n = NG / 8
N = 2 ** n
M1 = N

i = np.arange(N)

s1 = 2 * np.random.uniform(0, 1) + NG * np.cos(2 * M * np.pi * i / N) * (1 + 0.1 * np.random.uniform(0, 1)) + \
     17 * np.cos(4 * M * np.pi * i / N + np.random.uniform(0, 1)) + \
     3 * np.cos(7 * M * np.pi * i / N) * (np.random.uniform(0, 1) + NG)

Gauss = True
Haar = False

# Батьківський вейвлет
def g1(t):
    global Gauss, Haar
    if Gauss:
        return np.exp(- (t ** 2) / 2)
    elif Haar:
        if 0 <= t <= 1 / 2:
            return 1
        elif 1 / 2 <= t <= 1:
            return -1
        else:
            return 0


def f2(j, k, x):
    return 2 ** (j / 2) * g1((2 ** j) * x - k)

# Пряме перетворення
def W(l, j):
    return np.sum(s1[i] * f2(l, j, i) for i in range(0, int(N)))

# Обернене перетворення
def pr(i, l):
    return np.sum(W(l, j) * f2(l, j, i) / 2 ** (2 * l) for j in range(0, int(M1 + 1)))


def d(i):
    return np.sum(pr(i, l) for l in range(0, M + 1))


d = np.array([d(i) for i in np.arange(N)])

print('Array D: ', d)
print('Array S1: ', s1)

plt.plot(s1, color="m")
plt.plot(d, color="b")
plt.show()

plt.plot(s1, color="m")
plt.plot(d/8.2, color="b")
plt.show()

def W1(l):
    return np.sum(W(l, j) for j in range(0,int(M1+1)))
W2 = np.array([W1(l) for l in range(0,M+1)])

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


fig = plt.figure(figsize = (15,10))
ax = fig.gca(projection='3d')


l = np.arange(1, M+1)
j = np.arange(1, M1+1)

X, Y = np.meshgrid(l, j)
zs = np.array([W(l,j) for l,j in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.summer,
                       linewidth=0, antialiased=False)

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

ax.view_init(90, 30)

plt.show()