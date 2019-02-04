import sounddevice as sd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
import time


def animate(_, stream):

    global ydata, xdata
    rawdata, _ = stream.read(1024)
    data = np.mean(rawdata, axis=1)
    ydata = np.roll(ydata, -1024)
    ydata[-1024::] = data

    line1.set_data(xdata, ydata)

    F = fft(ydata)
    d = round(len(F) / 2)
    P = abs(F[0:d - 1])
    T = len(ydata) / fs
    k = np.arange(d - 1)
    frqlabel = k / T

    line2.set_data(frqlabel, P)

    return line1, line2


# set up parameters
fs = 48000
T = 1/fs
timeframe = 0.5
windowsize = round(timeframe*fs)

stream = sd.InputStream(fs)
stream.start()

# set up figure
fig = plt.figure()
fig.set_size_inches(10, 5)

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.set_title("Time Series Data (s)")
ax2.set_title("Frequency Series Data (Hz)")

ax2.set_xlim(0, 2000)
ax2.set_ylim(0, 500)

ax1.set_xlim(-windowsize/fs, 0)
ax1.set_ylim(-1, 1)

line1, = ax1.plot([], [], lw=1)
line2, = ax2.plot([], [], lw=1)

line1.set_color('k')
line2.set_color('r')

plt.tight_layout()

# pre-allocate data
xdata = np.arange(-windowsize, 0, 1)/fs
ydata = np.zeros(windowsize)

# run animation
anim = animation.FuncAnimation(fig, animate, fargs=(stream,), interval=1, blit=True)
plt.show()
