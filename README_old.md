# Hoovertron: A Device for the Quantitative Measurement of Hoover's Sign

This repository contains the complete design files and software for the Hoovertron, a portable, floor-based device developed for the standardised, quantitative measurement of Hoover's sign. The project aims to provide a reliable and objective tool to aid in the diagnosis of functional leg weakness, a common feature of Functional Neurological Disorder (FND).

This work is based on the research paper: *Quantitative Measurement of Hoover's sign: development of a standardised sensor, interface procedure and testing in healthy individuals*.

## Project Overview

Hoover's sign is a clinical sign used to help diagnose functional weakness of a leg. It relies on the principle of synergistic contraction: an involuntary downward force (hip extension) is generated in one leg when the opposite leg's hip is actively flexed against resistance. In functional weakness, this involuntary force is often greater than the voluntary force the person can generate, a discrepancy that the Hoovertron is designed to measure.

The Hoovertron provides a reliable method to quantify and record the voluntary and involuntary forces, calculating the Involuntary/Voluntary (IV/V) force ratio to offer an objective measure.

## Repository Structure

This project is organized into the following directories:

*   **/3D Parts - SolidEdge**: Contains the SolidEdge CAD files for the 3D-printed components of the device, including the main housing and footrest.
*   **/PCB - Altium**: Contains the Altium Designer files for the custom Printed Circuit Board (PCB) that houses the sensor interface electronics.
*   **/Arduino - C++**: Contains the firmware source code for the Arduino Nano Every microcontroller. This code is responsible for reading data from the force sensor, processing it, and transmitting it to the PC.
*   **/GUI - Python**: Contains the source code for the desktop Graphical User Interface (GUI) developed in Python with PyQt5. This application receives, visualizes, and analyzes the force data.

## Hardware

### Mechanical Components
The device housing is custom-designed to isolate the heel and ensure that downward force is applied directly to the sensor.
*   **3D Printed Housing:** A custom-made chassis that holds the electronics and force sensor.
*   **Foot Support & Footrest:** Ensures correct placement of the heel on the sensor.


### Electronics
The electronic components are mounted on a custom PCB. The core components include:
*   **Microcontroller:** An Arduino Nano Every is used for data acquisition and communication.
*   **Force Sensor:** An Ohmite FSR01CE Force Sensing Resistor measures the downward pressure exerted by the heel. The PCB is designed to accommodate two sensors (PS1 and PS2), but the current implementation uses only one.
*   **Signal Conditioning:** The signal from the active sensor is conditioned using an MCP6002 Op-Amp. The sensor is configured in a voltage divider circuit with a 180 Ω resistor. Three 100 nF capacitors are used to improve signal stability: one across the resistor for filtering and two for power supply decoupling. The op-amp is connected as a voltage follower to buffer the signal before it is read by the Arduino's analog-to-digital converter, preventing measurement inaccuracies due to loading effects.
*   **Power:** The entire device is powered via the USB connection to the PC.

## Software

### Arduino Firmware
The C++ firmware running on the Arduino Nano Every performs the following tasks:
1.  Reads the analog voltage from the force sensor circuit.
2.  Applies a calibration curve to convert the voltage reading into a force value in Newtons (N).
3.  Implements a digital low-pass filter to provide a stable, averaged output.
4.  Communicates the force data to the host PC via a serial-over-USB connection.

### Python GUI Application
The user-facing application is built using Python and PyQt5. Its features include:
1.  **Serial Communication:** Establishes a connection with the Arduino to receive real-time force data.
2.  **Data Visualization:** Plots the force (N) over time (s) in a user-friendly graph.
3.  **Data Analysis:** Allows the user to select a time period on the graph to determine the maximum force for both voluntary and involuntary measurements.
4.  **IV/V Ratio Calculation:** Automatically calculates the Involuntary/Voluntary force ratio based on the recorded measurements.
5.  **Data Logging:** Saves test results and patient information to CSV files for record-keeping and further analysis.



This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
