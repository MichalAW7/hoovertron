# HooverTron User Manual

Welcome to the HooverTron User Manual. This guide provides detailed instructions on how to set up, operate, and analyze data using the HooverTron application, an advanced tool for conducting the Hoover's Sign Test with integrated sensor hardware.

## Table of Contents
1. [Introduction](#introduction)
2. [Hardware Power & Setup](#hardware-power--setup)
3. [Connecting the Device](#connecting-the-device)
4. [Entering Patient Information](#entering-patient-information)
5. [Conducting the Hoover's Sign Test](#conducting-the-hoovers-sign-test)
    - [Step 1: Unaffected Leg Extension](#step-1-unaffected-leg-extension)
    - [Step 2: Affected Leg Voluntary Extension](#step-2-affected-leg-voluntary-extension)
    - [Step 3: Affected Leg Involuntary Extension](#step-3-affected-leg-involuntary-extension)
    - [Refining Data: Selecting a Time Period](#refining-data-selecting-a-time-period)
6. [Viewing Results and Analysis](#viewing-results-and-analysis)
7. [Managing Data (Files and Database)](#managing-data-files-and-database)
8. [Settings and Filtering](#settings-and-filtering)

---

## Introduction

HooverTron is a specialized desktop application designed to capture, visualize, and calculate objective force measurements during the Hoover's Sign Test. By communicating with external sensors, HooverTron plots real-time extension force and automatically calculates the Involuntary/Voluntary Ratio (IVVR) to provide a high-confidence objective measurement.

## Hardware Power & Setup

Before connecting the device to your computer, ensure the physical hardware is powered on and functioning.

1. **Power On**: Press the small **white button** on the device. 
    * *Verification*: You should see the green light on the Arduino Nano BLE 33 begin to flash. Additionally, the battery pack's level indicator lights will glow blue.
2. **Power Off**: When finished with the HooverTron, double-press the small **white button**.
    * *Verification*: Both the flashing green Arduino light and the blue battery pack lights will turn off.

## Connecting the Device

Once the HooverTron hardware is powered on, connect the software:

1. **Bluetooth (BLE) Connection**:
   - Go to the top menu bar and select **Connection > Bluetooth**.
   - Select your device from the list of available BLE devices and click connect.
2. **USB (Serial) Connection**:
   - Alternatively, connect via USB.
   - Go to **Connection > USB Connection > COM Port** and select the appropriate port for your device.
   - You can also adjust the baud rate under **Connection > USB Connection > Baud** (default is typically 19200).

## Entering Patient Information

Once the device is connected, begin by entering the patient's information in the first tab.

1. Navigate to the **Patient Information** tab.
2. Fill out all relevant fields:
   - **Name** & **Preferred Name**
   - **Date of Birth** & **Date of Visit** (The patient's age will be calculated automatically).
   - **Sex**, **Reason for Visit**, and **Notes**.
   - **Examiner Name**.
   - Select the **Dominant Leg** and the **Selected Leg** (the leg primarily being evaluated) from the dropdown menus.

## Conducting the Hoover's Sign Test

Navigate to the **Hoover's Sign Test** main tab. This tab contains three sub-tabs for the different steps of the test, plus a dedicated Results tab. 

### Step 1: Unaffected Leg Extension
This step establishes a baseline using the patient's strong/unaffected leg.
1. Instruct the patient according to the infographic on the left.
2. Click the green **Record** button to begin capturing force data. The button text will change to **Stop**.
3. The graph will populate with real-time force measurements (in Newtons) over time.
4. Click **Stop** when the capture is complete. 
5. The application automatically detects the peak Extension force and displays it in the Measurements box on the right.
6. Enter any specific observations in the Notes box.

### Step 2: Affected Leg Voluntary Extension
This step evaluates the voluntary strength of the patient's weak/affected leg.
1. Navigate to the **Step 2** tab.
2. Instruct the patient to perform voluntary extension on their affected leg.
3. Click **Record** to begin capturing, and click **Stop** when done.
4. Both the **Force Average** (dashed line) and **Force Peak** of the chosen time range will be automatically captured and displayed.

### Step 3: Affected Leg Involuntary Extension
This step evaluates the reflex/involuntary extension of the patient's weak leg while they flex their strong leg.
1. Navigate to the **Step 3** tab.
2. Instruct the patient as per the clinical guidelines for Hoover's Sign.
3. Click **Record** and perform the procedure, then click **Stop**.
4. The system will record the **Force Peak** of the involuntary extension.

### Refining Data: Selecting a Time Period
In any of the steps (1, 2, or 3), you might capture more data than needed (e.g., noise before or after the actual extension effort). You can isolate the valid data:
1. On the graph, you will see a shaded vertical region.
2. Drag the edges of this shaded region over the peaks representing the true effort.
3. Alternatively, specify exact timestamps in the **Start Time** and **End Time** boxes below the graph and click the red **Select Time Period** button.
4. The peak (and average) measurements will automatically update to reflect *only* the data within your selected time period.

> [!WARNING]
> Use the **Clear Data** button carefully; it will permanently wipe the data graph and measurements for that specific step.

## Viewing Results and Analysis

Once all three steps are complete, navigate to the **Results** tab.

1. Review the Raw Data section to ensure that the un-affected leg extension, affected leg voluntary extension (V), and affected leg involuntary extension (IV) are populated correctly.
2. Click the large blue **Calculate Results** button.
3. The software will automatically calculate the **Involuntary/Voluntary Ratio (IVVR)** using the formula: `IVVR = IV / V`.
4. An analysis summary will populate at the bottom right, and you can record final overarching comments in the **Observations** box.

## Managing Data (Files and Database)

HooverTron allows you to save individual patient files as well as aggregate data into a single, comprehensive database.

### Saving an Individual Patient File
- **File > New**: Create and save a new individual `.csv` file for the current session.
- **File > Save**: Overwrite the currently opened `.csv` file with the latest changes.
- **File > Open**: Open a previously saved patient `.csv` file. It will auto-populate the graphs, patient info, and results.

### Managing the Master Database
The Database function aggregates summary rows (one row per test) for bulk export and analysis.
- **Database > Create Database**: Start a new master `.csv` file. This establishes the headers and inserts the current test as Test #1.
- **Database > Open Database**: Link the application to an existing master database file so new records can be appended.
- **Database > Update Database**: Appends the *current* test data (Patient Info, Peak Forces, and IVVR) as a new row at the bottom of the active database file.

## Settings and Filtering

To ensure clean and readable charts, especially in environments susceptible to noise or tremors, HooverTron features adjustable signal filtering.

- Go to **Edit > Filter Frequency** to select the smoothing level.
- **Heavy (5 Hz)**: Recommended for noisy environments or patients with tremors. Visually smooths the line heavily.
- **Standard (10 Hz)**: The default setting, providing a balance of responsiveness and smoothness.
- **Responsive (20 Hz)**: Best for analyzing rapid, minute movements without losing high-frequency data spikes.
