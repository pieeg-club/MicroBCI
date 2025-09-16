# MicroBCI. Shield to Measure EEG with  NUCLEO-WB55 STMicroelectronics Development Boards &amp; Kit. EEG with STM32. 

<div align="center">
  <img src="https://github.com/pieeg-club/MicroBCI/blob/main/Images/micro_bci.png" alt="General View" width="400">
</div>

# Easy start
First, upload the [.hex](https://github.com/pieeg-club/MicroBCI/blob/main/Framework/Micro_BCI.hex)   file and the [Stack](https://github.com/pieeg-club/MicroBCI/blob/main/Framework/stm32wb5x_BLE_Stack_full_fw.bin)    
to the Nucle Board via the Micro USB cable Via [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html)  
Step-by-Step Manual in this Video on [YouTube](https://youtu.be/crqOmnJ3Hjg)    

# Signal Processing 
[SDK](https://github.com/pieeg-club/MicroBCI/tree/main/Mobile_SDK) for Mobile Phone   
[SDK](https://github.com/pieeg-club/MicroBCI/tree/main/SDK) for Python script   

# How connect
Connect the MicroBCI shield to the Nucleo Board and after that connect the device to a battery (power supply) and connect the electrodes. Full galvanic isolation from mains is required.  
To measure the EEG need also EEG cap kit for [dry](https://pieeg.com/cap-eeg-kit/) or [wet](https://pieeg.com/cap-eeg-kit-8-channels-with-wet-electrodes/) electrodes or an EMG [kit](https://pieeg.com/kit-to-measure-emg-ecg-ekg/)      
Connection for the EEG is provided below     
<div align="center">
  <img src="https://github.com/pieeg-club/MicroBCI/blob/main/Images/connections.bmp" alt="Connection View" width="600">
</div>

# Dataset Samples and Data Evaluation
### Dataset     
Samples can be found [here](https://github.com/pieeg-club/MicroBCI/tree/main/Dataset)  Dry Eelctrodes, without Gel     
### Artifact test
The process of measuring chewing using dry electrodes (Fz). Chewing occurred in the following sequence: 4 times, 3 times, 2 times, and 1 time, and the same for the blinking process. The y- axis is the processed EEG signal after passing filter bands of 1-40 Hz in microvolts and with 250 samples per second.  Data after band-pass filter 0.5-40 Hz   
<div align="center">
  <img src="https://github.com/pieeg-club/MicroBCI/blob/main/Images/EMG.bmp" alt="emg" width="600">
</div>

and blinking artifacts, the same protocol, electrodes located on the forehead.  Data after band-pass filter 0.5-40 Hz       
<div align="center">
  <img src="https://github.com/pieeg-club/MicroBCI/blob/main/Images/EOG.bmp" alt="emg" width="600">
</div>

### Alpha test  
The process of recording an EEG signal from an electrode (Fz) with eyes open and closed. The y- axis is the processed EEG signal after passing filter bands of 8-12Hz in microvolts and with 250 samples per second. Data after band-pass filter 8-12 Hz  
<div align="center">
  <img src="https://github.com/pieeg-club/MicroBCI/blob/main/Images/Alpha_8_12Hz.bmp" alt="emg" width="600">  
</div>




#### Citation  
Rakhmatulin, I. Low-Cost Shield MicroBCI to Measure EEG with STM32. Preprints 2025, 2025091345. https://www.preprints.org/manuscript/202509.1345/v1   


#### Contacts   
http://pieeg.com/  
[LinkedIn](https://www.linkedin.com/company/96475004/admin/feed/posts/)   
[Youtube](https://www.youtube.com/channel/UCVF-3Bp34LINLOQsyWNpcow)
  
#### Support
PiEEG [Discord](https://discord.gg/JVBn9HXyRs)  
pieeg.pieeg@com 
  
