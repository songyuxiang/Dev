
import scipy
import scipy.interpolate
from numpy import *
import matplotlib.pyplot as plt
x = linspace(0, 10, 10)
y = sin(x)
z= cos(x+y)
tck = scipy.interpolate.splrep(x, y,z)
x2 = linspace(0, 10, 200)
y2 = scipy.interpolate.splev(x2, tck)
print(tck)