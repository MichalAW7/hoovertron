#include <ArduinoBLE.h>

// BLE Service and Characteristic
BLEService sensorService("180D"); // Custom service UUID
BLECharacteristic sensorDataCharacteristic("2A37", BLERead | BLENotify, 64); // Custom characteristic UUID with larger payload

// Variables
float xn1 = 0;
float yn1 = 0;
float xn2 = 0;
float yn2 = 0;
float xna1 = 0;
float xna2 = 0;
float Time = 0;
float alpha = 0; 
float beta = 0;  
float f = 10; // Default frequency

void setup() {
  Serial.begin(115200); // Keep serial for debugging
  
  // NANO 33 BLE SPECIFIC: Set ADC resolution to 12-bit (0-4095) for better precision
  analogReadResolution(12); 

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set advertised local name and service UUID
  BLE.setLocalName("HooverTron");
  BLE.setAdvertisedService(sensorService);

  // Add the characteristic to the service
  sensorService.addCharacteristic(sensorDataCharacteristic);

  // Add service
  BLE.addService(sensorService);

  // Start advertising
  BLE.advertise();

  Serial.println("BLE device active, waiting for connections...");

  float temp = 2 * 3.14 * 0.001 * f;
  alpha = (2 - temp) / (temp + 2);
  beta = temp / (temp + 2);

  Serial.print("frequency: ");
  Serial.println(f);
  Serial.print("Alpha: ");
  Serial.println(alpha);
  Serial.print("Beta: ");
  Serial.println(beta);
}

void loop() {
  // Check for BLE connection
  BLEDevice central = BLE.central();

  // Handle Serial commands (Frequency update)
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    if (command.startsWith("F")) {
      f = command.substring(1).toFloat();
      float temp = 2 * 3.14 * 0.001 * f;
      alpha = (2 - temp) / (temp + 2);
      beta = temp / (temp + 2);
      Serial.print("Frequency updated to: ");
      Serial.println(f);
      
      // Send confirmation via BLE if connected
      if (central && central.connected()) {
        String confirmMsg = "Frequency updated to: " + String(f);
        sensorDataCharacteristic.writeValue(confirmMsg.c_str());
      }
    }
  }

  Time = millis();

  // Read pin A0
  int analogValue1 = analogRead(A0);
  
  // CONVERSION: The Nano 33 BLE is 12-bit (0-4095).
  float xnb1 = (analogValue1 * 5.0 / 4095.0); 

  // Read pin A1
  int analogValue2 = analogRead(A1);
  float xnb2 = (analogValue2 * 5.0 / 4095.0); 

  // Change voltage to force signal 1 and sensor 2
  xna1 = 0.8259 * exp(0.8623 * xnb1) + 0.00009463 * exp(3.163 * xnb1) - 0.825; 
  xna2 = 0.8259 * exp(0.8623 * xnb2) + 0.00009463 * exp(3.163 * xnb2) - 0.825; 
 
  // Compute the first filtered signal
  float yna1 = alpha * yn1 + beta * xna1 + beta * xn1; 

  // Compute the second filtered signal
  float yna2 = alpha * yn2 + beta * xna2 + beta * xn2; 
   
  // Store the previous values
  xn1 = xna1;
  yn1 = yna1;

  xn2 = xna2;
  yn2 = yna2;

  // Format data as comma-separated string
  String dataString = String(Time) + "," + 
                      String(xna1, 4) + "," + 
                      String(xna2, 4) + "," + 
                      String(yna1, 4);

  // Output to Serial (Always)
  Serial.println(dataString);

  // Output to BLE (If connected)
  if (central && central.connected()) {
     sensorDataCharacteristic.writeValue(dataString.c_str());
  }

  delay(10); 
}