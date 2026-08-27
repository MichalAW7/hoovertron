# Canva Template Generation Prompt

**Instructions for the User:** Copy the text between the dashed lines below and paste it directly into Canva's "Magic Design for Presentations" prompt box (or ChatGPT/Claude, if you are asking them to draft a structured document layout). It is optimized to create a comprehensive, multi-page slide deck template with placeholders specifically designed for your software and hardware screenshots.

--------------------------------------------------------------------------------------------------

Create a highly professional, 12-slide clinical software user manual presentation template for an application called "HooverTron." 

**Design Guidelines:**
* **Visual Style:** Modern, clean, and clinical. Use a professional color palette featuring medical blue (#0078d7), crisp white, and soft light grays. 
* **Typography:** Use a clean, sans-serif font like 'Segoe UI', 'Inter', or 'Roboto'. Headings should be bold and distinct.
* **Layout:** The layout must be heavily image-driven. Every slide from Slide 3 onwards MUST include a prominent, large rectangular "Image Placeholder" occupying at least 40-50% of the slide (to be filled later with hardware photos or software screenshots).

Please generate the following 12 slides with exactly this text and structure:

**Slide 1: Title Slide**
* **Title:** HooverTron User Manual
* **Subtitle:** Objective Measurement for the Hoover's Sign Test
* **Visual:** A sleek cover design with abstract geometric medical shapes or a single large image placeholder in the background.

**Slide 2: Introduction & Overview**
* **Title:** Welcome to HooverTron
* **Body Text:** HooverTron is a specialized desktop application designed to capture, visualize, and calculate objective force measurements during the Hoover's Sign Test. By communicating with external sensors, HooverTron plots real-time extension force and automatically calculates the Involuntary/Voluntary Ratio (IVVR).
* **Layout:** Text on the left, a medium-sized image placeholder on the right.

**Slide 3: Hardware Power & Setup**
* **Title:** Powering the HooverTron Device
* **Body Text:** 
  * Turn On: Press the small white button on the device. The green light on the Arduino Nano BLE 33 will begin to flash, and the battery pack's level lights will glow blue.
  * Turn Off: Double-press the small white button. Both sets of lights will turn off.
* **Layout:** Text on the left, a large Image Placeholder on the right (for a high-quality photograph of the physical HooverTron hardware, specifically showing the white button and lights).

**Slide 4: Connecting the Device**
* **Title:** Hardware Connection
* **Body Text:** 
  1. Bluetooth: Navigate to 'Connection > Bluetooth' to select your BLE device.
  2. USB/Serial: Navigate to 'Connection > USB Connection > COM Port' to select your connected device. Baud rate defaults to 19200.
* **Layout:** Text on one side, large Image Placeholder on the other (for the menu bar drop-down screenshot).

**Slide 5: Registering Patient Information**
* **Title:** Patient Setup
* **Body Text:** Enter standard demographics (Name, DOB). Ensure you select the correct 'Dominant Leg' and 'Selected Leg' before proceeding to the test. Age is calculated automatically.
* **Layout:** Bulleted text list on the left, large Image Placeholder on the right (for the Patient tab screenshot).

**Slide 6: Step 1 - Unaffected Leg Extension**
* **Title:** Step 1: Baseline Strength
* **Body Text:** 
  * Instruct the patient to extend their strong (unaffected) leg.
  * Click 'Record' to capture real-time force data, then click 'Stop'.
  * The system automatically logs the peak extension force.
* **Layout:** Top half for the large Image Placeholder (for the graph/Step 1 tab screenshot), bottom half for the text instructions.

**Slide 7: Step 2 - Affected Leg Voluntary Extension**
* **Title:** Step 2: Voluntary Extension
* **Body Text:** 
  * Move to the Step 2 tab.
  * Instruct the patient to voluntarily perform extension on their weak (affected) leg.
  * Click 'Record'. The system captures both the Force Average and Force Peak.
* **Layout:** Top half for large Image Placeholder (for Step 2 tab screenshot), bottom half for text.

**Slide 8: Step 3 - Affected Leg Involuntary Extension**
* **Title:** Step 3: Involuntary Extension
* **Body Text:** 
  * Move to the Step 3 tab.
  * Perform the clinical Hoover's Sign maneuver: ask the patient to flex their strong leg to trigger involuntary extension in the weak leg.
  * Click 'Record'. The peak involuntary force is captured.
* **Layout:** Top half for large Image Placeholder (for Step 3 tab screenshot), bottom half for text.

**Slide 9: Refining Your Data**
* **Title:** Selecting a Time Period
* **Body Text:** If your recording contains noise, use the vertical shaded region on the graph to isolate the valid effort. You can click and drag the edges on the graph, or type specific Start/End times below and click 'Select Time Period'. Only data within this window is used for measurements.
* **Layout:** Text on the left, large Image Placeholder on the right (focused closely on the graph's shaded region selector).

**Slide 10: Results and IVVR Calculation**
* **Title:** Results and Analysis
* **Body Text:** Once all 3 steps are complete, navigate to the Results tab. Click 'Calculate Results'. The system will automatically compute the Involuntary/Voluntary Ratio (IVVR = IV / V) and provide an analysis summary. You can add distinct clinical observations here.
* **Layout:** Text on the left, very large Image Placeholder on the right (for the Results dashboard screenshot).

**Slide 11: Data Management**
* **Title:** Managing Patient Data
* **Body Text:** 
  * Individual Saves: Use File > Save / Open to manage individual patient CSVs.
  * Master Database: Use Database > Update Database to append the patient's summary metrics and IVVR ratio as a new row into the global FND patient database file.
* **Layout:** Text with icons on the left, Image Placeholder on the right.

**Slide 12: Application Settings**
* **Title:** Filter Frequency Settings
* **Body Text:** Adjust the incoming signal filter for optimal clarity:
  * Heavy (5 Hz): Ideal for patients with tremors or noisy environments.
  * Standard (10 Hz): The default balance of smoothness and fidelity.
  * Responsive (20 Hz): Best for analyzing rapid movement.
* **Layout:** Text on the left, Image Placeholder on the right (for the Edit > Filter Frequency menu screenshot).

--------------------------------------------------------------------------------------------------
