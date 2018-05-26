import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

rv = scipy.stats.uniform()
N = 51
n = 1000
ng = 10
x = np.arange(n) + (rv.rvs(size=n) * N) / ng
y = N * rv.rvs(size=n) * x + ng * rv.rvs(size=n) + N

# Нахождение коэффициентов методом наименьших квадратов

# вычисление коэффициентов многочлена
z = np.polyfit(x, y, deg=1)

# формирование линейной фукнции и собственно аппроксимации
f = np.poly1d(z)
y_ = f(x)

plt.figure(figsize=(7, 5))
plt.scatter(x, y)
plt.plot(x, y_, color="r")
plt.show()

# Перевірити наявність викидів у регресії

e = y - y_
S = np.sum(e**2, axis=0) / (n - 2) * \
    (1 - 1/n - (x - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
r = np.max(e / np.sqrt(S), axis=0)
r_delta = 4

if r < r_delta:
    print("No emissions")
else:
    print("Emissions are present")

# Перевірити гіпотези про відповідність оцінок коефіцієнтів істинним
# значенням та адекватність моделі.

a, b = z

S2 = np.sum((y - y_)**2) / (n - 2)
S = np.sqrt(S2)

S2_x = np.sum(x - np.mean(x))**2 / (n-1)
S_x = np.sqrt(S2_x)

S2_y = np.sum(y - np.mean(y))**2 / (n-1)
S_y = np.sqrt(S2_y)

S2_beta = S / (S_x * np.sqrt(n - 1))
S_beta = np.sqrt(S2_beta)

S2_alpha = S * np.sqrt(1 / n + np.mean(x) ** 2 / ((n - 1) * S2_x))
S_alpha = np.sqrt(S2_alpha)

t_delta = 0.1257
F_delta = 1.25

print(np.abs(b))
print(t_delta * S_beta)
if np.abs(b) > t_delta * S_beta:
    print('Value b is significant')
else:
    print('Value b is not significant')

if np.abs(a) > t_delta * S_alpha:
    print('Value a is significant')
else:
    print('Value a is not significant')

if S2 / S2_y > F_delta:
    print('Model is adequate')
else:
    print('Model is not adequate')

# Методом найменших квадратів знайти найкращу функціональну
# залежність: лінійна, поліноміальна(другого та третього порядків).

# lineal
z1 = np.polyfit(x, y, deg=1)
f1 = np.poly1d(z1)
y_1 = f1(x)
S2_1 = np.sum((y - y_1)**2) / (n - 2)
print("lineal:", z1)
# polynomial 2
z2 = np.polyfit(x, y, deg=2)
f2 = np.poly1d(z2)
y_2 = f2(x)
S2_2 = np.sum((y - y_2)**2) / (n - 2)
print("square:", z2)
# polynomial 3
z3 = np.polyfit(x, y, deg=3)
f3 = np.poly1d(z3)
y_3 = f3(x)
S2_3 = np.sum((y - y_3)**2) / (n - 2)
print("cub:", z3)
plt.figure(figsize=(7, 5))
plt.scatter(x, y)

plt.plot(x, y_1, color="r")
plt.plot(x, y_2, color="g")
plt.plot(x, y_3, color="m")

plt.show()
print("----------------------")
print("Lineal:", S2_1)
print("Polynomial (2):", S2_2)
print("Polynomial (3):", S2_3)