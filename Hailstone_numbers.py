'''
3N+1 problem

'''
import numpy as np
import matplotlib.pyplot as plt
number = int(input('\nEnter the number for which you want the HAILSTONE NUMBER SERIES: '))

count = 0
array = []
while number != 1:
    if number%2 == 0:
        number = number / 2
        count = count + 1
        array.append(number)
    else:
        number = (3*number)+1
        count = count + 1
        array.append(number)

xaxis = np.arange(count)

plt.plot(array)
# plt.scatter(xaxis,array)


