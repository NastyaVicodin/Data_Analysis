import numpy as np
import scipy
import scipy.stats

alpha = 0.95
N = 10
n = 1000
rv = scipy.stats.uniform(0, 1)

# one-factor experiment table
A = np.array([
    1.0 * N + rv.rvs(size=n),
    0.5 * N + rv.rvs(size=n),
    0.8 * N + rv.rvs(size=n),
    1.4 * N + rv.rvs(size=n),
    2.0 * N + rv.rvs(size=n)
])

s2_i = A.var(ddof=1, axis=1)
print('Dispersions for each factor:', s2_i)

g = np.max(s2_i) / np.sum(s2_i)
print('g =', g)
g_alpha = 0.33

if g > g_alpha:
    print("The null hypothesis on the equality of dispersions is rejected.")
else:
    print("There is no reason to reject the null hypothesis")

k = len(A)

s2_0 = (np.sum(np.sum(A ** 2, axis=1), axis=0) -
        np.sum(np.sum(A, axis=1) ** 2, axis=0) / n) /  \
       (k * (n - 1))
print('Dispersion evaluation:', s2_0)
s2 = (np.sum(np.sum(A ** 2, axis=1), axis=0) -
      np.sum(np.sum(A, axis=1), axis=0) ** 2 / (n * k)) / \
     (k * n - 1)
print('Selective dispersion:', s2)

x_i = np.sum(A, axis=1) / n
x_ = np.sum(x_i, axis=0) / k
s2_a = n * np.sum((x_i - x_)**2, axis=0) / (k - 1)
print('Dispersion evaluation (factor changes):', s2_a)

f = s2_a / s2_0
print('Factor evaluation:', f)
f_alpha = 2.37
if f > f_alpha:
    print("The influence is significant")
else:
    print("The influence isn't significant")

# two-factor experiment table
n = 100
B = np.array([
    [
        1.0 * N + rv.rvs(n),
        3.5 * N + rv.rvs(n),
        3.8 * N + rv.rvs(n),
        1.4 * N + rv.rvs(n),
        2.0 * N + rv.rvs(n)
    ],
    [
        1.0 * N + rv.rvs(n),
        2.5 * N + rv.rvs(n),
        2.8 * N + rv.rvs(n),
        2.4 * N + rv.rvs(n),
        3.0 * N + rv.rvs(n)
    ],
    [
        1.0 * N + rv.rvs(n),
        1.5 * N + rv.rvs(n),
        1.8 * N + rv.rvs(n),
        3.4 * N + rv.rvs(n),
        4.0 * N + rv.rvs(n)
    ],
    [
        1.0 * N + rv.rvs(n),
        0.5 * N + rv.rvs(n),
        0.8 * N + rv.rvs(n),
        4.4 * N + rv.rvs(n),
        5.0 * N + rv.rvs(n)
    ]
])
print('---------------')
x_avg = np.mean(B, axis=2)
print('Average:\n', x_avg)

m = len(B)
k = len(B[0])

q1 = np.sum(np.sum(x_avg**2, axis=1), axis=0)

xi = np.sum(x_avg.T, axis=1)
xj = np.sum(x_avg, axis=1)

q2 = np.sum(xi**2, axis=0) / m
q3 = np.sum(xj**2, axis=0) / k
q4 = (np.sum(xi))**2 / (m * k)

s20 = (q1 - q2 - q3 + q4) / ((k - 1) * (m - 1))
s2a = (q2 - q4) / (k - 1)
s2b = (q3 - q4) / (m - 1)
print('Disp eval 0:', s20)
print('Disp eval A:', s2a)
print('Disp eval B:', s2b)

fa = 2.37
f1 = s2a / s20
if f1 > fa:
    print("The influence A is significant")
else:
    print("The influence A isn't significant")
fb = 3.26
f2 = s2b / s20

if f2 > fb:
    print("The influence B is significant")
else:
    print("The influence B isn't significant")

q5 = np.sum(B ** 2)
s2ab = (q5 - n * q1) / (m * k * (n - 1))

fab = 3.49
f3 = n * s20 / s2ab
if f3 > fab:
    print("Interaction of AB factors is significant")
else:
    print("Interaction of AB factors isn't significant")
