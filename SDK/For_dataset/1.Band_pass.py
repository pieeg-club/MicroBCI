import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt

# -----------------------------
# Load CSV and rename columns
# -----------------------------
col_names = [f'ch{i}' for i in range(1, 9)]
df = pd.read_csv('alphas.csv', names=col_names, header=None)

# -----------------------------
# Remove any empty or NaN rows
# -----------------------------
df = df.dropna()  # drops rows with any NaN
df = df.reset_index(drop=True)  # reset index after dropping rows

# -----------------------------
# Band-pass filter design
# -----------------------------
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# -----------------------------
# Filter parameters
# -----------------------------
fs = 250.0       # Sampling frequency (Hz)
lowcut = 8  # Low cutoff (Hz)
highcut = 12   # High cutoff (Hz)

# -----------------------------
# Select channel for visualisation   
# -----------------------------
ch8 = df['ch2'].values


# -----------------------------
# Apply band-pass filter
# -----------------------------
filtered_ch8 = bandpass_filter(ch8, lowcut, highcut, fs)

# -----------------------------
# Plot filtered channel
# -----------------------------
plt.figure(figsize=(12, 5))
plt.plot(filtered_ch8, label='Filtered ch8 (1-30 Hz)')
plt.title('Band-pass Filtered EEG Channel 8')
plt.xlabel('Sample number')
plt.ylabel('Amplitude (scaled)')
plt.legend()
plt.ylim([-20, 20]) 
plt.grid(True)
plt.show()
