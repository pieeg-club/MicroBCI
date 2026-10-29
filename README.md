<div align="center">

# MicroBCI

**EEG with an STM32 development board.**

Low-cost 8-channel EEG shield for the STMicroelectronics NUCLEO-WB55, with the TI ADS1299 and Bluetooth LE streaming to Python, Android and the browser.

[📖 Documentation](https://docs.pieeg.com/hardware/devices/microbci/) ·
[🚀 How to Start](https://docs.pieeg.com/hardware/devices/microbci/setup/) ·
[🛒 Buy](https://pieeg.com/microbci/) ·
[💬 Discord](https://discord.gg/5Ps24p47)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_board.jpg" alt="MicroBCI shield on a NUCLEO-WB55 board" width="400">

</div>

> [!WARNING]
> MicroBCI is **not a medical device** and has not been certified by any regulator for use with the human body. It is a tool for research, education and engineering. You use it at your own risk.

> [!CAUTION]
> **Battery only.** While electrodes are on a person, the Nucleo and the shield run from a **small 5 V power bank**. Connect the Nucleo to a computer only to flash the firmware, with no electrodes on anyone. The board has **no isolation**. Read the [Safety page](https://docs.pieeg.com/hardware/devices/microbci/safety/).

## At a glance

| | |
|---|---|
| **Channels** | 8 biosignal inputs, plus reference and bias |
| **Converter** | TI ADS1299, 24-bit, simultaneous sampling |
| **Sample rate** | 250 SPS |
| **Signals** | EEG, EMG, ECG, EOG |
| **Host** | STMicroelectronics NUCLEO-WB55 (STM32WB55, not included) |
| **Wireless** | Bluetooth LE, same protocol as [IronBCI](https://github.com/pieeg-club/ironbci) |
| **Electrodes** | Dry or wet Ag/AgCl, 2.54 mm header |
| **Power** | Small 5 V power bank via the Nucleo's Micro-USB |
| **Software** | Python SDK and Android app (this repo), [PiEEG Cloud](https://cloud.pieeg.com), [PiEEG Server](https://github.com/pieeg-club/PiEEG-server) |

## How it works

```
 Electrodes 1–8 ─┐
 Reference (ear) ┼─► MicroBCI ─SPI─► NUCLEO-WB55 ─BLE─► Python SDK
 Bias (ear) ─────┘   (ADS1299)       (STM32WB55)        ├ Android app
                                          ▲             ├ cloud.pieeg.com
                5 V power bank ───────────┘             └ PiEEG Server
```

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_connection.png" alt="MicroBCI wiring: cap, reference, bias and channels 1–8" width="700">

## Quick start

1. **Flash the Nucleo once** with [STM32CubeProgrammer](https://www.st.com/en/development-tools/stm32cubeprog.html) over its ST-LINK USB port (see [Firmware](#firmware) below).
2. **Mount** the shield on the Nucleo, matching the end pin marked by the arrow in the photo below.
3. **Connect** 8 electrodes, a reference ear clip and a bias ear clip.
4. **Power** the Nucleo from a small 5 V **power bank**. It starts advertising over Bluetooth.
5. **Connect:**

| Option | How |
|---|---|
| **Python** | Set your board's `address` in [`SDK/GUI/1.1_GUI.py`](SDK/GUI/1.1_GUI.py), then `python 1.1_GUI.py` |
| **Android** | Install [`Mobile_SDK/mobile_sdk_Micro_BCI.apk`](Mobile_SDK), choose **8 ch** in settings |
| **Browser** | [cloud.pieeg.com](https://cloud.pieeg.com) in Chrome or Edge → **PiEEG Devices** → **IronBCI** |
| **PiEEG Server** | `pip install "pieeg-server[ironbci]"` then `pieeg-server --device ironbci8` |

> [!IMPORTANT]
> **Pay attention to the alignment.** A shield shifted by one pin won't work. Match the end pin marked by the arrow.

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_alignment.jpg" alt="MicroBCI on the Nucleo: match the end pin marked by the arrow" width="500">

Full walkthrough: **[docs.pieeg.com → MicroBCI → How to Start](https://docs.pieeg.com/hardware/devices/microbci/setup/)** · [PDF manual](Manuals/Micro_BCI_How_To_Start.pdf) · [Video](https://youtu.be/crqOmnJ3Hjg)

## Firmware

The NUCLEO-WB55 needs the **Bluetooth stack** and the **MicroBCI firmware** once. Use the Nucleo's built-in ST-LINK (the right-hand USB port); no extra programmer needed.

1. In **STM32CubeProgrammer**: port **SWD**, programmer **ST-LINK**, click **Connect**.
2. Open **Firmware Upgrade Services** → **Read FUS infos**. Check the FUS version is **v1.2.0.0** or **v1.3.0.0**.
3. Install the stack [`Framework/stm32wb5x_BLE_Stack_full_fw.bin`](Framework) at address **`0x080CE000`** → **Firmware Upgrade**.
4. Back in the main view, open [`Framework/Micro_BCI.hex`](Framework) and click **Download**.
5. Unplug the USB cable. From now on, power the board from the power bank.

Step by step with screenshots: [Firmware docs](https://docs.pieeg.com/hardware/devices/microbci/firmware/) · [PDF manual](Manuals/Micro_BCI_How_To_Start.pdf)

## Wiring

| Input | Electrode | Purpose |
|---|---|---|
| **Channels 1–8** | EEG electrodes in a cap (10-20 system), or EMG / ECG electrodes | Signal |
| **Reference** | Ear clip on one earlobe | Common 0 µV point for all channels |
| **Bias** | Ear clip on the other earlobe | Cancels common-mode noise (mains hum) |

Kits: [dry-electrode EEG cap](https://pieeg.com/cap-eeg-kit/) · [wet-electrode EEG cap](https://pieeg.com/cap-eeg-kit-8-channels-with-wet-electrodes/) · [EMG / ECG kit](https://pieeg.com/kit-to-measure-emg-ecg-ekg/)

## Software

### Python SDK

Scripts built on [`bleak`](https://github.com/hbldh/bleak) in [`SDK/GUI`](SDK/GUI):

| Script | What it does |
|---|---|
| [`1.GUI.py`](SDK/GUI/1.GUI.py) | Live graph of all 8 channels, raw |
| [`1.1_GUI.py`](SDK/GUI/1.1_GUI.py) | Live graph with a 1–40 Hz band-pass filter (recommended) |
| [`2.Save_data.py`](SDK/GUI/2.Save_data.py) | Find the board by name, save 2,000 samples (8 s) to Excel |
| [`2.1_Save_data.py`](SDK/GUI/2.1_Save_data.py) | Connect by address, save 10,000 samples (40 s) to Excel |

```bash
pip install bleak matplotlib numpy scipy pandas openpyxl
cd SDK/GUI
python 1.1_GUI.py
```

The GUI scripts connect to a fixed Bluetooth address written at the top of the file. Change it to yours:

```python
address = "00:80:E1:27:96:0B"     # your board's address
```

To find it, scan once with `bleak` (the board usually appears as `EAREEG`). On macOS, use the UUID that `bleak` shows instead of a MAC address. Details: [Software docs](https://docs.pieeg.com/hardware/devices/microbci/software/#find-your-boards-address).

[`SDK/For_dataset`](SDK/For_dataset) has band-pass and wavelet scripts for analysing recordings.

### Android app

Install [`Mobile_SDK/mobile_sdk_Micro_BCI.apk`](Mobile_SDK) (MIT licence), choose **8 ch** in settings, press **Save** to record and **Stop** to finish, then share the file. The Flutter source is in the same folder.

### BLE protocol

Same as IronBCI: data characteristic `0000fe42-8e22-4541-9d4c-21edae82ed19` (notify), 8 channels × 3 bytes (24-bit big-endian two's complement) per sample. Details: [Specification](https://docs.pieeg.com/hardware/devices/microbci/specification/).

## Example signals

All recorded with **dry electrodes, no gel**, at 250 SPS.

**EEG: alpha test** (electrode at Fz, eyes closed and open, filtered 8–12 Hz)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_alpha.png" alt="Alpha test with MicroBCI" width="700">

**EMG: chewing** (electrode at Fz, 4-3-2-1 times, filtered 0.5–40 Hz)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_emg.png" alt="Chewing artifacts (EMG)" width="700">

**EOG: blinking** (electrodes on the forehead, 4-3-2-1 times, filtered 0.5–40 Hz)

<img src="https://raw.githubusercontent.com/pieeg-club/PiEEG-docs/main/public/images/hardware/2026/10/microbci_eog.png" alt="Blinking (EOG)" width="650">

**Datasets** in [`Dataset`](Dataset): `alpha_2ch.csv` (~92 s), `EMG_Ch_8.csv` (~28 s), `EOG_Ch_8.csv` (~38 s). CSV, 8 columns, **no header row**, µV.

## What's in this repository

| Folder | Content |
|---|---|
| [`Framework`](Framework) | `Micro_BCI.hex` firmware and the STM32WB Bluetooth stack |
| [`SDK/GUI`](SDK/GUI) | Python BLE SDK: live graphs, saving to Excel |
| [`SDK/For_dataset`](SDK/For_dataset) | Band-pass and wavelet analysis scripts |
| [`Mobile_SDK`](Mobile_SDK) | Android app (`.apk`) and Flutter source |
| [`Dataset`](Dataset) | Alpha, EMG and EOG recordings |
| [`Manuals`](Manuals) | PDF quick-start manual |
| [`datasheet`](datasheet) | NUCLEO-WB55 schematic and kit datasheet |
| [`Images`](Images) | Images used in the original README |

## Documentation

| Page | |
|---|---|
| [MicroBCI Intro](https://docs.pieeg.com/hardware/devices/microbci/) | Overview, comparison with other 8-channel boards |
| [What's in the Box](https://docs.pieeg.com/hardware/devices/microbci/required-equipment/) | What you need besides the shield |
| [How to Start](https://docs.pieeg.com/hardware/devices/microbci/setup/) | Flashing, mounting, connecting, first signal |
| [Electrodes & Mounting](https://docs.pieeg.com/hardware/devices/microbci/connections/) | Alignment, wiring, montage |
| [Software](https://docs.pieeg.com/hardware/devices/microbci/software/) | Python SDK, Android, PiEEG Cloud, PiEEG Server |
| [Signals & Datasets](https://docs.pieeg.com/hardware/devices/microbci/examples/) | Example recordings and datasets |
| [Firmware](https://docs.pieeg.com/hardware/devices/microbci/firmware/) | Bluetooth stack and hex file, step by step |
| [Specification](https://docs.pieeg.com/hardware/devices/microbci/specification/) | Hardware, BLE data format, µV conversion |
| [Troubleshooting](https://docs.pieeg.com/hardware/devices/microbci/troubleshooting/) | Flashing, Bluetooth and signal fixes |
| [Safety](https://docs.pieeg.com/hardware/devices/microbci/safety/) | Battery-only operation and responsible use |

## Citation

If you use MicroBCI in research, please cite:

```
I. Rakhmatulin. Low-Cost Shield MicroBCI to Measure EEG with STM32.
Preprints 2025, 2025091345.
```

## Contact

- 🌐 [pieeg.com](https://pieeg.com/)
- 📖 [docs.pieeg.com](https://docs.pieeg.com/)
- 💬 [Discord](https://discord.gg/5Ps24p47)
- ✉️ [pieeg@pieeg.com](mailto:pieeg@pieeg.com)
