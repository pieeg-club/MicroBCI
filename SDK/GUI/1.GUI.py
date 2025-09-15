
import asyncio
from bleak import BleakScanner, BleakClient
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

DEVICE_NAME = "EAREEG"
FIRST_NAME_ID = '0000fe42-8e22-4541-9d4c-21edae82ed19'

buffer_size = 100
data_buffers = {f"channel_{i+1}": deque([0] * buffer_size, maxlen=buffer_size) for i in range(8)}

# Global variables for plotting
fig, ax = None, None
lines = []

async def find_eareeg_device():
    devices = await BleakScanner.discover()
    return next((device for device in devices if device.name == DEVICE_NAME), None)

async def process_data(data):
    channels = [(data[3*i] << 16) | (data[3*i + 1] << 8) | data[3*i + 2] for i in range(8)]
    processed_channels = []
    for ch in channels:
        voltage = ch - 16777214 if (ch | 0x7FFFFF) == 0xFFFFFF else ch
        result = round(1000000 * 4.5 * (voltage / 16777215), 2)
        processed_channels.append(result)
    return processed_channels

async def update_buffers(processed_channels):
    for i, ch_data in enumerate(processed_channels):
        data_buffers[f"channel_{i+1}"].append(ch_data)

def update_plot():
    global lines, ax
    for i, line in enumerate(lines):
        data = list(data_buffers[f"channel_{i+1}"])
        line.set_ydata(data)
        
        # Autoscale y-axis
        mean = np.mean(data)
        ax[i].set_ylim(mean - 100, mean + 100)
        
    fig.canvas.draw_idle()
    fig.canvas.flush_events()

def setup_plot():
    global fig, ax, lines
    plt.ion()
    fig, ax = plt.subplots(8, 1, figsize=(10, 15), sharex=True)
    fig.canvas.draw()  # Initial draw
    plt.show(block=False)

    x = np.arange(buffer_size)
    for i in range(8):
        line, = ax[i].plot(x, [0] * buffer_size, label=f"Channel {i+1}")
        ax[i].set_ylabel(f"Ch {i+1}")
        ax[i].legend(loc="upper right")
        lines.append(line)
    ax[-1].set_xlabel("Time")
    plt.tight_layout()

async def main():
    print(f"Scanning for {DEVICE_NAME}...")
    eareeg_device = await find_eareeg_device()
    
    if eareeg_device is None:
        print(f"{DEVICE_NAME} not found.")
        return

    print(f"Found {DEVICE_NAME} at address: {eareeg_device.address}")
    
    setup_plot()

    async with BleakClient(eareeg_device.address) as client:
        print(f"Connected to {DEVICE_NAME}")

        update_counter = 0
        async def callback(sender, data):
            nonlocal update_counter
            processed_channels = await process_data(data)
            await update_buffers(processed_channels)
            update_counter += 1
            if update_counter % 10 == 0:  # Update plot every 10 data points
                update_plot()

        await client.start_notify(FIRST_NAME_ID, callback)
        print("Notification started. Press Ctrl+C to stop.")
        
        try:
            while True:
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pass
        finally:
            await client.stop_notify(FIRST_NAME_ID)
            print("Notification stopped.")

asyncio.run(main())
