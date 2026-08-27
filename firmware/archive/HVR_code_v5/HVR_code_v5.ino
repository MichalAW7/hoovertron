/*
  Arduino Nano 33 BLE code for a dual-sensor data acquisition system.
  - Adapted for 3.3V Logic and 12-bit ADC resolution.
  - Reads analog data from pins A0 and A1.
  - Converts analog readings to force values.
  - Applies a digital low-pass filter.
  - Communicates via Serial (USB).
*/

#include <Arduino.h> // explicitly include Arduino.h for platform compatibility

// Variables for the digital filter state
float xn1 = 0;
float yn1 = 0;
float xn2 = 0;
float yn2 = 0;

// Variables for current sensor readings
float xna1 = 0;
float xna2 = 0;

// Time and filter coefficients
float Time = 0;
float alpha = 0;
float beta = 0;
float f = 10; // Default frequency in Hz

/**
 * @brief Calculates the filter coefficients alpha and beta.
 */
void calculateFilterCoefficients() {
  // Note: The original code uses 0.001 (1ms) for calculation, 
  // though the loop runs at ~10ms. Kept as-is to maintain behavior 
  // from the original project.
  float temp = 2 * 3.14 * 0.001 * f;
  alpha = (2 - temp) / (temp + 2);
  beta = temp / (temp + 2);

  Serial.print("Frequency updated to: ");
  Serial.println(f);
}

void setup() {
  // Start serial communication.
  // On Nano 33 BLE, the baud rate (19200) is ignored as it uses native USB,
  // but we keep it for compatibility.
  Serial.begin(19200);
  
  // Optional: Wait for Serial to connect so you don't miss startup messages.
  // Comment this out if you want the board to run without a computer attached.
  // while (!Serial); 

  // SET ADC RESOLUTION
  // The Nano 33 BLE supports 12-bit resolution (0-4095).
  // This provides 4x higher precision than the standard Nano.
  analogReadResolution(12);

  // Calculate initial coefficients
  calculateFilterCoefficients();
}

void loop() {
  // --- Check for incoming commands from Python ---
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim(); 

    if (command.startsWith("F")) {
      float newFreq = command.substring(1).toFloat();
      if (newFreq > 0 && newFreq <= 100) {
        f = newFreq; 
        calculateFilterCoefficients(); 
      }
    }
  }

  Time = millis();

  // --- Sensor Reading and Processing ---
  
  // SENSOR 1
  int analogValue1 = analogRead(A0);
  // CONVERSION UPDATE:
  // 1. Multiplier is now 3.3 (Because Nano 33 BLE is a 3.3V board).
  // 2. Divisor is now 4095.0 (Because we set resolution to 12-bit).
  float xnb1 = (analogValue1 * 3.3 / 4095.0); 
  
  // Note: This formula assumes 'xnb1' is the correct voltage. 
  // If your sensors behave differently at 3.3V vs 5V, you may need to recalibrate these constants.
  xna1 = 0.8259 * exp(0.8623 * xnb1) + 0.00009463 * exp(3.163 * xnb1) - 0.825;

  // SENSOR 2
  int analogValue2 = analogRead(A1);
  float xnb2 = (analogValue2 * 3.3 / 4095.0); 
  xna2 = 0.8259 * exp(0.8623 * xnb2) + 0.00009463 * exp(3.163 * xnb2) - 0.825;

  // --- Digital Filtering ---
  float yna1 = alpha * yn1 + beta * xna1 + beta * xn1;
  float yna2 = alpha * yn2 + beta * xna2 + beta * xn2;

  // Store previous values
  xn1 = xna1;
  yn1 = yna1;
  xn2 = xna2;
  yn2 = yna2;

  // --- Send Data to Python ---
  Serial.print(Time);
  Serial.print(",");
  Serial.print(xna1);
  Serial.print(",");
  Serial.print(xna2);
  Serial.print(",");
  Serial.print(yna1);
  Serial.println(); 

  delay(10);
}