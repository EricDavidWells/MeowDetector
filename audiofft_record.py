import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack
from scipy.fftpack import fft

fs = 48000

# Get sound recording
duration = 2
print("recording...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
sd.wait()
print("done recording.")
print("playing back...")
sd.play(myrecording, fs)
sd.wait()
print("done playing back.")

data = np.mean(myrecording, axis=1)

# Plot sound
plt.plot(data, 'b')
plt.show()

# Fourier Transform
F = fft(data)
d = round(len(F)/2)
P = abs(F[0:d-1])
T = len(data)/fs  # where fs is the sampling frequency
k = np.arange(d-1)
frqLabel = k/T

plt.plot(frqLabel, P, 'r')
plt.axis([0, 2000, 0, max(P)*1.2])
plt.show()

d = input("do you want to save data? (y/N)")

if d == "y":
    filename = input("name the file:")
    savedata = np.array([data, P, frqLabel])
    np.save(filename+"data", savedata)
