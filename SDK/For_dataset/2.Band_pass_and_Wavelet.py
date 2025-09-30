import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import pywt

# =======================

# 1. Load Excel file

# =======================

filename = "EEG_data.xlsx"   # <-- change if needed
data = pd.read_excel(filename)

# Assume columns are ch1 ... ch8

channels = [f"ch{i}" for i in range(1, 9)]
fs = 250  # Hz (sampling rate, adjust if known)

# =======================

# 2. Bandpass filter (1-40 Hz)

# =======================

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a

def bandpass_filter(signal, lowcut=1, highcut=40, fs=250, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, signal)
    return y

# =======================

# 3. Create time axis

# =======================

n_samples = data.shape[0]
time = np.arange(n_samples) / fs

# =======================

# 4. Wavelet transform (PyWavelets)

# =======================

def compute_cwt(sig, fs, freqs=np.arange(1, 41)):
    """
    Continuous Wavelet Transform using Morlet wavelet.
    freqs = frequencies of interest (Hz)
    """
    scales = pywt.central_frequency('morl') * fs / freqs
    cwtmatr, _ = pywt.cwt(sig, scales, 'morl', sampling_period=1/fs)
    return np.abs(cwtmatr), freqs

# =======================

# 5. Plot results

# =======================

fig, axes = plt.subplots(4, 4, figsize=(12, 6), constrained_layout=True)


# Band Pass Filter
low = 8
high =12
 
for i, ch in enumerate(channels):
    row = (i // 4) * 2 # 0 or 2
    col = i % 4

    # Bandpass filter
    
    filtered = bandpass_filter(data[ch].values, low, high, fs)

    # --- Plot filtered signal ---
    axes[row, col].plot(time, filtered, color="black", linewidth=0.8)
    axes[row, col].set_title(f"{ch} (1–40 Hz)", fontsize=10)
    axes[row, col].set_xlabel("Time [s]")
    axes[row, col].set_ylabel("Amp")

    # --- Compute and plot wavelet ---
    cwtmatr, freqs = compute_cwt(filtered, fs)
    im = axes[row + 1, col].imshow(
        cwtmatr,
        extent=[time[0], time[-1], freqs[-1], freqs[0]],
        cmap="viridis",
        aspect="auto",
        interpolation="bilinear",
    )
    axes[row + 1, col].set_title(f"{ch} Wavelet", fontsize=10)
    axes[row + 1, col].set_xlabel("Time [s]")
    axes[row + 1, col].set_ylabel("Freq [Hz]")

    #Add one colorbar for all wavelet plots

cbar = fig.colorbar(im, ax=axes, orientation="horizontal", fraction=0.05, pad=0.05)
cbar.set_label("Power")

plt.show()
