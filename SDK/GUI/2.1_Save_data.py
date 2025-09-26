import asyncio
import sys
from bleak import BleakClient
import time
from matplotlib import pyplot as plt
import pandas as pd

data_f = []
FIRST_NAME_ID = '0000fe42-8e22-4541-9d4c-21edae82ed19'
address =  "00:80:E1:27:96:0B"  #"EAREEG" #"00:80:E1:26:62:B7" # "00:80:E1:26:62:70"

#global data_for_graph
data_for_graph = []
data_df = pd.DataFrame(columns=[f"ch{i+1}" for i in range(8)])

axis_x = 0 
async def main(address):
    async with BleakClient(address) as client:
        def callback(FIRST_NAME_ID, data):
            global stop_program, data_for_graph, data_df

            data_check = 0xFFFFFF
            data_test  = 0x7FFFFF
            data_received = data

            num_bytes = len(data_received)
            print (num_bytes)
            if num_bytes < 3:
                return  # too short to contain even one sample

            num_samples = num_bytes // 3  # number of complete 3-byte samples

            idx = 0
            for _ in range(num_samples):
                b1 = data_received[idx]
                b2 = data_received[idx+1]
                b3 = data_received[idx+2]
                idx += 3

                data_result = (b1 << 16) | (b2 << 8) | b3
                convert_data = data_result | data_test
                if convert_data == data_check:
                    result = 16777214 - data_result
                else:
                    result = data_result

                result = round(1000000*4.5*(result/16777215), 2)
                data_for_graph.append(result)

                # Append one row when 8 channels collected
                if len(data_for_graph) == 8:
                    data_df.loc[len(data_df)] = data_for_graph
                    data_for_graph = []
                    print(f"Rows collected: {len(data_df)}")

                    if len(data_df) >= 250:
                        filename = "EEG_datas.xlsx"
                        data_df.to_excel(filename, index=False)
                        print(f"✅ Data saved to {filename}")
                        sys.exit()
                        break 


                        
        await client.start_notify(FIRST_NAME_ID, callback)
        print ("was connected")
        
        while 1: 
          if not event.is_set():    
              await event.wait()  
          await asyncio.sleep(0.01)
          event.clear()
          
event = asyncio.Event()
print('address:', address)
asyncio.run(main(address))
