import sounddevice as sd
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import math
import time


def animate(_, stream):

    global ydata, xdata, meowcount, meowdecay, meowflag, meowrange, meowtimer
    rawdata, _ = stream.read(1024)
    data = np.mean(rawdata, axis=1)
    N = data.size
    ydata = np.roll(ydata, -1024)
    ydata[-1024::] = data

    line1.set_data(xdata, ydata)

    F = fft(ydata)
    d = round(len(F) / 2)
    P = abs(F[0:d - 1])*2/N
    T = len(ydata) / fs
    k = np.arange(d - 1)
    frqlabel = k / T

    line2.set_data(frqlabel, P)

    fgap = 50  # gap in Hz required between peeks
    peaks, _ = signal.find_peaks(P, distance=math.ceil(fgap/(fs/N)), prominence=0.2)
    peakvalues = P[peaks]
    line3.set_data(frqlabel[peaks], peakvalues)

    if time.time() - meowtimer > meowdecay:
        meowcount -= 1
        meowcount = max(meowcount, 0)
        meowtimer = time.time()
        print(meowcount)

    if time.time() - meowtimer > 1:
        if peaks.size > 0:
            if meowrange[0] < frqlabel[peaks[0]] < meowrange[1]:
                meowcount += 1
                meowtimer = time.time()
                print(meowcount)

    meowtext = plt.text(1500, 0.5, "mewocount: " + str(meowcount), verticalalignment='center',
                        horizontalalignment='left')

    return line1, line2, line3, meowtext


# set up parameters
fs = 48000
T = 1/fs
timeframe = 0.25
windowsize = round(timeframe*fs)

stream = sd.InputStream(fs)
stream.start()

# set up figure
fig = plt.figure()
fig.set_size_inches(10, 5)

ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)
ax3 = fig.add_subplot(2, 1, 2)

ax1.set_title("Time Series Data (s)")
ax2.set_title("Frequency Series Data (Hz)")

ax2.set_xlim(0, 2000)
ax2.set_ylim(0, 1)

ax1.set_xlim(-windowsize/fs, 0)
ax1.set_ylim(-1, 1)

line1, = ax1.plot([], [], lw=1)
line2, = ax2.plot([], [], lw=1)
line3, = ax3.plot([], [], 'kx')

line1.set_color('k')
line2.set_color('r')
meowtext = plt.text(0, 0, '')

plt.tight_layout()

# pre-allocate data
xdata = np.arange(-windowsize, 0, 1)/fs
ydata = np.zeros(windowsize)

meowcount = 0
meowrange = [300, 1500]
meowdecay = 3
meowflag = 0
meowtimer = time.time()

# # run animation
anim = animation.FuncAnimation(fig, animate, fargs=(stream,), interval=1, blit=True)
plt.show()

while True:

    rawdata, _ = stream.read(1024)
    data = np.mean(rawdata, axis=1)
    N = data.size
    ydata = np.roll(ydata, -1024)
    ydata[-1024::] = data

    line1.set_data(xdata, ydata)

    F = fft(ydata)
    d = round(len(F) / 2)
    P = abs(F[0:d - 1])*2/N
    T = len(ydata) / fs
    k = np.arange(d - 1)
    frqlabel = k / T

    line2.set_data(frqlabel, P)

    fgap = 25  # gap in Hz required between peeks
    peaks, _ = signal.find_peaks(P, prominence=0.2, distance=math.ceil(fgap/(fs/N)))
    line3.set_data(frqlabel[peaks], P[peaks])
