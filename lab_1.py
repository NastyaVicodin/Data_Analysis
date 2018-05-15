import numpy as np
import math


def research_calc(m, mg, n, flag):
    array_y = np.random.uniform(10 + m, mg + 2 * m, n)
    if flag == 1:
        array_x = np.random.choice(array_y, size=m, replace=False, p=None)
    else:
        array_x = []
        a = n // m
        r = np.random.choice(array_y[0:a], size=1, replace=False, p=None)
        ind = array_y[0:a].tolist().index(r)
        i = 0
        while ind < n:
            array_x.append(array_y[ind])
            ind += a
            i += 1

    #А). Обчисліть середнє значення і дисперсію для популяції
    y = sum(array_y)
    ys = y / n
    print('Average Ys for population:', ys)
    dy = sum((array_y - ys)**2) / (n - 1)
    print('Dispersion DY^2 for population:', dy)

    #Б). Оцініть суму і середнє значення для популяції за вибіркою
    if flag == 1:
        y_ = n * sum(array_x / m)
    else:
        y_ = 0
        for i in array_x:
            y_ += n * (i / m)
    y_s = sum(array_x) / m
    print('Average Y_s for population (selection):', y_s)
    s = sum((array_x - y_s)**2) / (m - 1)
    print('Sum S^2 for population (selection):', s)

    dy_s = s * (1 - m / n) / m
    print('Dispersion (avg) D(Y_s):', dy_s)
    dy_ = s * n**2 * (1 - m / n) / m
    print('Dispersion (sum) D(Y_):', dy_)

    # interval for average
    z = 1.96
    x1_u = y_s - z * math.sqrt(s * (1 - m / n)) / m
    x2_u = y_s + z * math.sqrt(s * (1 - m / n)) / m
    print('Average interval: [', x1_u, ';', x2_u, ']', sep='')
    print('Length:', x2_u - x1_u)
    # interval for sum
    x1_l = n * y_s - z * n * math.sqrt(s * (1 - m / n) / m)
    x2_l = n * y_s + z * n * math.sqrt(s * (1 - m / n) / m)
    print('Sum interval: [', x1_l, ';', x2_l, ']', sep='')
    print('---------------------------')


m = 10
mg = 51
n = 1000
print('*** M =', m, '***')
research_calc(m, mg, n, 1)

n = 10000
m = 100
print('*** M =', m, '***')
research_calc(m, mg, n, 1)
m = 1000
print('*** M =', m, '***')
research_calc(m, mg, n, 1)

#Г). Сформувати систематичну вибірку таких же розмірів. Порівняти отримані результати.
print('*** System selection ***')
research_calc(m, mg, n, 2)

#Д). Провести аналогічні розрахунки для стратифікованої вибірки.
h = 10
array_y = np.random.uniform(10 + m, mg + 2 * m, n)
div = n // h
array_y_h = []
i = 0
while i < h:
    array_y_h.append(array_y[i * div : (i + 1) * div])
    i += 1
i -= 1
if (i + 1) * div < n:
    k = (i + 1) * div
    array_y_h[h - 1] = np.concatenate((array_y_h[h - 1], array_y[k:n]))

strat_array = []
i = 0
count = 100
s_arr = []
while i < h:
    s_arr.append(np.random.choice(array_y_h[i], size=count, replace=False, p=None))
    strat_array = np.concatenate((strat_array, s_arr[i]))
    i += 1

popul_sum = sum(strat_array)
popul_avg = popul_sum / len(strat_array)


def strat_calc(arr, strat_arr, n, count, h_len, popul_sum, popul_avg):
    w = count / h_len
    print('Selection weight:', w)
    y_avg = sum(arr) / count
    print('Avg value for strat:', y_avg)
    y_sum = sum(arr)
    print('Strat sum:', y_sum)
    print('Population sum:', popul_sum)
    print('Population average:', popul_avg)
    s = sum((arr - y_avg)**2) / (count - 1)
    print('Dispersion in strat:', s)
    w_h = h_len / n
    print('Strat weight:', w_h)
    y_avg_h = sum(strat_arr) / h_len
    print('Strat average evaluation:', y_avg_h)
    y_sum_h = y_avg_h * count
    print('Strat sum evaluation:', y_sum_h)
    s_h = sum((strat_arr - y_avg_h)**2) / (h_len - 1)
    print('Strat dispersion evaluation:', s_h)
    print('-----------------------------------')
    return y_sum_h, s_h


i = 0
y_strat = 0
disp = 0
print('*** Stratification selection ***')
while i < h:
    print('Start #', i)
    l = len(array_y_h[i])
    (s, d) = strat_calc(s_arr[i], array_y_h[i], n, count, l, popul_sum, popul_avg)
    y_strat += s
    disp += (1 - count / l) * count**2 * d / l
    i += 1

print('Strat selection sum evaluation:', y_strat)
y_strat_avg = y_strat / len(strat_array)
print('Strat selection average evaluation:', y_strat_avg)
print('Dispersion sum eval:', disp)
disp_avg = disp / n**2
print('Dispersion avg eval:', disp_avg)
z = 1.96
x1_s = y_strat_avg - z * math.sqrt(disp_avg)
x2_s = y_strat_avg + z * math.sqrt(disp_avg)
print('Interval for average eval: [', x1_s, ';', x2_s, ']', sep='')