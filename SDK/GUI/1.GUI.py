import asyncio
from bleak import BleakClient
import matplotlib.pyplot as plt
from collections import deque
import time

FIRST_NAME_ID = "0000fe42-8e22-4541-9d4c-21edae82ed19"
address = "00:80:E1:27:96:0B"

# ---------------------
# Data buffers for 8 channels
# ---------------------
buffer_size = 1000  # last 1000 samples per channel
data_buffers = [deque([0]*buffer_size, maxlen=buffer_size) for _ in range(8)]
temp_buffer = []  # temporary buffer to collect 8 samples
update_buffer = [[] for _ in range(8)]  # buffer for 250 samples before graph update

# ---------------------
# Matplotlib setup
# ---------------------
plt.ion()
fig, axes = plt.subplots(8, 1, figsize=(15, 12), sharex=True)
lines = [axes[i].plot(range(buffer_size), list(data_buffers[i]))[0] for i in range(8)]
for i, ax in enumerate(axes):
    ax.set_ylabel(f"Ch {i+1}")
axes[-1].set_xlabel("Samples")
plt.tight_layout()
plt.show(block=False)

# ---------------------
# Global timer
# ---------------------
start_time = None

# ---------------------
# Callback for BLE data
# ---------------------
def callback(_, data):
    global start_time, temp_buffer, update_buffer

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

        # When we have 8 samples, append to update_buffer
        if len(temp_buffer) == 8:
            for ch in range(8):
                update_buffer[ch].append(temp_buffer[ch])
            temp_buffer = []

    # Update graph only when each channel has 250 new samples
    if len(update_buffer[0]) >= 250:
        for ch in range(8):
            data_buffers[ch].extend(update_buffer[ch])
            update_buffer[ch] = []  # clear temp update buffer

        # Update matplotlib plot
        for i, line in enumerate(lines):
            line.set_ydata(list(data_buffers[i]))
            mean = sum(data_buffers[i]) / len(data_buffers[i])
            axes[i].set_ylim(mean-100, mean+100)

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
                await asyncio.sleep(0.1)  # main loop sleep
        finally:
            await client.stop_notify(FIRST_NAME_ID)
            print("Stopped notifications")

asyncio.run(main())
