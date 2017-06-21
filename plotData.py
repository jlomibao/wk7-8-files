#File Name: plotData.py
#Author: John Francis Lomibao
#PID: A11591509

import sys

#Usage: "python plotData.py <pos_ctrl_file> <neg_ctrl_file>"
pos_ctrl_file = sys.argv[1]
neg_ctrl_file = sys.argv[2]


with open(pos_ctrl_file, 'r') as file:
	pos_ctrl_data = [int(line.strip()) for line in file]
	
with open(neg_ctrl_file, 'r') as file:
	neg_ctrl_data = [int(line.strip()) for line in file]

from scipy.stats import gaussian_kde

def kde_scipy(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    # Note that scipy weights its bandwidth by the covariance of the
    # input data.  To make the results comparable to the other methods,
    # we divide the bandwidth by the sample standard deviation here.
    kde = gaussian_kde(x, bw_method=bandwidth, **kwargs)
    return kde.evaluate(x_grid)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.distributions import norm

#kde = density(pos_ctrl_data, adjust=0.5)
#LL = approxfun(kde)
#for i in range(1000):
#	print LL(i)

x = np.array(pos_ctrl_data)
y = np.array(neg_ctrl_data)
'''
lenx = len(x)
x = x*len(y)
y = y*lenx
'''
print len(x), len(y)


fig, ax = plt.subplots(1, 2, sharey=False,
                       figsize=(15, 5))
					   
fig.subplots_adjust(wspace=0.3)

x_grid = np.linspace(-50, 4800, 1000)
pdf1 = kde_scipy(x, x_grid, bandwidth=0.25)
pdf2 = kde_scipy(y, x_grid, bandwidth=0.5)


ax[0].plot(x_grid, pdf1, color='green', alpha=0.5, lw=3)
ax[0].set_title('positive control')
#set min and max x-axis
ax[0].set_xlim(-20, 450)
ax[0].hist(x, 40, fc='gray', histtype='stepfilled', alpha=0.3, normed=True)

ax[1].plot(x_grid, pdf2, color='red', alpha=0.5, lw=3)
ax[1].hist(y, 25, fc='gray', histtype='stepfilled', alpha=0.3, normed=True)
ax[1].set_title('negative control')
#set min and max x-axis
ax[1].set_xlim(-20, 2250)
plt.show()
'''
c = a + b
plt.plot(x_grid,a,'r')
plt.plot(x_grid,b,'b')
plt.plot(x_grid,c,'g')
plt.plot()
'''