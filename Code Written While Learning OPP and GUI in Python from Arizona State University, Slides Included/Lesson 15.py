from ipywidgets import *

slider = widgets.IntSlider()
display(slider)

slider.value

import numpy as np
import matplotlib.pyplot as plt
def myPlot (c):
  x = np.linspace(-5,5,20)
  y = c * x**2  # we are going to have a parabola here.
  plt.plot (x, y, 'r--' ) # let us make a plot using x and y values
  plt.ylabel ('y (x)') # create y label and make It y (x)
  plt.xlabel ('x') # x label and named it x
  plt.ylim([ 0, 80 ])
  plt.xlim ([ -5, 5 ])

myPlot(8)

import time
progress = IntProgress ( description = 'Loading: ' )
progress.orientation = 'horizontal'  #we can use vertical as well.
display(progress)

for i in range (100):
  progress.value = i
  time.sleep (0.1)
