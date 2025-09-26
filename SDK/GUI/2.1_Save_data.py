import asyncio
from bleak import BleakClient
import pandas as pd
import time  # for timing

FIRST_NAME_ID = "0000fe42-8e22-4541-9d4c-21edae82ed19"
address = "00:80:E1:27:96:0B"

data_for_graph = []
data_df = pd.DataFrame(columns=[f"ch{i+1}" for i in range(8)])

stop_event = None  # will be set inside main()
start_time = None  # global timer start for first data packet


async def main(address):
    global stop_event, start_time
    stop_event = asyncio.Event()

    async with BleakClient(address) as client:

        def callback(_, data):
            global data_for_graph, data_df, stop_event, start_time

            if start_time is None:
                start_time = time.perf_counter()  # start timing when first data arrives

            data_check = 0xFFFFFF
            data_test = 0x7FFFFF

            num_bytes = len(data)
            if num_bytes < 3:
                return # too short to contain even one sample

            num_samples = num_bytes // 3
            idx = 0
            for _ in range(num_samples):
                b1, b2, b3 = data[idx], data[idx+1], data[idx+2]
                idx += 3

                data_result = (b1 << 16) | (b2 << 8) | b3
                convert_data = data_result | data_test
                if convert_data == data_check:
                    result = 16777214 - data_result
                else:
                    result = data_result

                result = round(1000000 * 4.5 * (result / 16777215), 2)
                data_for_graph.append(result)

                if len(data_for_graph) == 8:
                    data_df.loc[len(data_df)] = data_for_graph
                    data_for_graph = []

                    if len(data_df) == 1000:
                        elapsed = time.perf_counter() - start_time
                        filename = "EEG_datas.xlsx"
                        data_df.to_excel(filename, index=False)
                        print(f"✅ Data saved to {filename}")
                        print(f"⏱ Elapsed time: {elapsed:.2f} seconds")
                        stop_event.set()  # signal main loop to stop
                        return

        await client.start_notify(FIRST_NAME_ID, callback)
        print("Connected and collecting data...")

        await stop_event.wait()  # wait until callback signals stop
        await client.stop_notify(FIRST_NAME_ID)
        print("Stopped notifications, exiting.")


asyncio.run(main(address))
