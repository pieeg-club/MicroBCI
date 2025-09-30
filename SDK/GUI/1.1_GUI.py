import asyncio
from bleak import BleakClient
import matplotlib.pyplot as plt
from collections import deque
import time
from scipy.signal import butter, filtfilt

FIRST_NAME_ID = "0000fe42-8e22-4541-9d4c-21edae82ed19"
address = "00:80:E1:27:96:0B"

# ---------------------
# Filter design (Band-pass 1–40 Hz, Fs=250 Hz)
# ---------------------
fs = 250.0  # Sampling frequency
lowcut = 1.0
highcut = 40.0
order = 4

nyquist = 0.5 * fs
low = lowcut / nyquist
high = highcut / nyquist
b, a = butter(order, [low, high], btype="band")

def bandpass_filter(data):
    """Apply zero-phase band-pass filter."""
    if len(data) < order * 3:
        return data
    return filtfilt(b, a, data)

# ---------------------
# Data buffers
# ---------------------
buffer_size = 1000
data_buffers = [deque([0]*buffer_size, maxlen=buffer_size) for _ in range(8)]
temp_buffer = []
update_buffer = [[] for _ in range(8)]

# Keep previous 250 samples for filtering
data_before_only_for_band_pass = [[0 for _ in range(250)] for _ in range(8)]

# ---------------------
# Matplotlib setup
# ---------------------
plt.ion()
fig, axes = plt.subplots(8, 1, figsize=(15, 12), sharex=True)

x_axis = list(range(buffer_size))
lines = [axes[i].plot(x_axis, list(data_buffers[i]))[0] for i in range(8)]

for i, ax in enumerate(axes):
    ax.set_ylabel(f"Ch {i+1}")
axes[-1].set_xlabel("Samples")
plt.tight_layout()
plt.show(block=False)

start_time = None

# ---------------------
# Callback for BLE data
# ---------------------
def callback(_, data):
    global start_time, temp_buffer, update_buffer, data_before_only_for_band_pass

    if start_time is None:
        start_time = time.perf_counter()

    num_bytes = len(data)
    if num_bytes < 3:
        return

    num_samples = num_bytes // 3
    idx = 0
    for _ in range(num_samples):
        b1, b2, b3 = data[idx], data[idx+1], data[idx+2]
        idx += 3
        raw = (b1 << 16) | (b2 << 8) | b3
        value = 16777214 - raw if (raw | 0x7FFFFF) == 0xFFFFFF else raw
        scaled = round(1000000 * 4.5 * (value / 16777215), 2)
        temp_buffer.append(scaled)

        if len(temp_buffer) == 8:
            for ch in range(8):
                update_buffer[ch].append(temp_buffer[ch])
            temp_buffer = []

    # Process when 250 new samples are ready
    if len(update_buffer[0]) == 250:
        for ch in range(8):
            data_for_band_pass = data_before_only_for_band_pass[ch] + update_buffer[ch]
            data_before_only_for_band_pass[ch] = update_buffer[ch]

            filtered = bandpass_filter(data_for_band_pass)
            new_samples = filtered[-250:]

            # Extend buffer instead of overwriting
            data_buffers[ch].extend(new_samples)
            update_buffer[ch] = []

        # Update plot with only new data
        for i, line in enumerate(lines):
            line.set_ydata(list(data_buffers[i]))
            mean = sum(data_buffers[i]) / len(data_buffers[i])
            axes[i].set_ylim(mean - 100, mean + 100)

        fig.canvas.draw_idle()
        fig.canvas.flush_events()

# ---------------------
# Main async function
# ---------------------


async def main():
    async with BleakClient(address) as client:
        await client.start_notify(FIRST_NAME_ID, callback)
        print("Connected and streaming data... Ctrl+C to stop")
        try:
            while True:
                await asyncio.sleep(0.1)
        finally:
            await client.stop_notify(FIRST_NAME_ID)
            print("Stopped notifications")

asyncio.run(main())
