import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

filename = "highpitchedhum_data"
data = np.load(filename + ".npy")
fs = 44800

# Plot sound
plt.figure(1)
plt.plot(data[0], 'b')

plt.figure(2)
plt.plot(data[2], data[1], 'r')
plt.axis([0, 2000, 0, max(data[1])*1.2])

fgap = 50   # gap in Hz required between peeks
peaks, _ = signal.find_peaks(data[1], threshold=10, distance=(fgap/(fs/data[0].size)))


plt.figure(3)
plt.plot(data[2], data[1], data[2][peaks], data[1][peaks], 'o')
plt.axis([0, 2000, 0, max(data[1])*1.2])
plt.show()