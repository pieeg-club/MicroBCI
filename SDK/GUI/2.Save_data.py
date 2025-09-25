import asyncio
from bleak import BleakScanner, BleakClient
import pandas as pd
import time

# Device configuration
DEVICE_NAME = "EAREEG"
FIRST_NAME_ID = '0000fe42-8e22-4541-9d4c-21edae82ed19'
TARGET_SAMPLES = 2000  # Number of samples to collect

# Buffer to store incoming samples
collect_buffer = {f"ch{i+1}": [] for i in range(8)}

async def find_eareeg_device():
    devices = await BleakScanner.discover()
    return next((device for device in devices if device.name == DEVICE_NAME), None)

async def process_data(data):
    """Convert raw BLE data to 8-channel EEG samples."""
    samples = []
    num_samples = len(data) // 24  # 8 channels * 3 bytes per channel
    for s in range(num_samples):
        channels = [
            (data[24*s + 3*i] << 16) | 
            (data[24*s + 3*i + 1] << 8) | 
            data[24*s + 3*i + 2]
            for i in range(8)
        ]
        processed = []
        for ch in channels:
            voltage = ch - 16777214 if (ch | 0x7FFFFF) == 0xFFFFFF else ch
            processed.append(round(1000000 * 4.5 * (voltage / 16777215), 2))
        samples.append(processed)
    return samples

async def main():
    print(f"Scanning for {DEVICE_NAME}...")
    device = await find_eareeg_device()
    if device is None:
        print(f"{DEVICE_NAME} not found.")
        return

    print(f"Found {DEVICE_NAME} at address: {device.address}")

    async with BleakClient(device.address) as client:
        print(f"Connected to {DEVICE_NAME}")

        async def callback(sender, data):
            new_samples = await process_data(data)
            for sample in new_samples:
                for i, ch_val in enumerate(sample):
                    collect_buffer[f"ch{i+1}"].append(ch_val)

        await client.start_notify(FIRST_NAME_ID, callback)
        print("Collecting data...")

        # Record start time
        start_time = time.time()

        # Wait until we have enough samples
        while len(collect_buffer["ch1"]) < TARGET_SAMPLES:
            await asyncio.sleep(0.01)

        # Record end time
        end_time = time.time()

        # Trim extra samples if we got more than TARGET_SAMPLES
        for ch in collect_buffer:
            collect_buffer[ch] = collect_buffer[ch][:TARGET_SAMPLES]

        # Save to Excel
        df = pd.DataFrame(collect_buffer)
        df.to_excel("eareeg_data.xlsx", index=False)

        await client.stop_notify(FIRST_NAME_ID)
        print("Notification stopped.")

        # Print total collection time
        print(f"Total data collection time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
