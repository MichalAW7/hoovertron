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
const float f = 10; // Default frequency

void setup() {
  Serial.begin(115200); // Increased baud rate, 19200 is very slow for the BLE
  
  // NANO 33 BLE SPECIFIC: Set ADC resolution to 12-bit (0-4095) for better precision
  analogReadResolution(12); 

  float temp = 2 * 3.14 * 0.001 * f;
  alpha = (2 - temp) / (temp + 2);
  beta = temp / (temp + 2);

  // Allow time for Serial to connect (useful on native USB boards like Nano 33 BLE)
  while (!Serial && millis() < 3000); 

  Serial.print("frequency: ");
  Serial.println(f);
  Serial.print("Alpha: ");
  Serial.println(alpha);
  Serial.print("Beta: ");
  Serial.println(beta);
}

void loop() {
  Time = millis();

  // Read pin A0
  int analogValue1 = analogRead(A0);
  
  // CONVERSION: The Nano 33 BLE is 12-bit (0-4095).
  // We multiply by 5.0 here NOT because the pin has 5V (it has 3.3V), 
  // but to scale the ratio back up to the "5V equivalent" so your 
  // exponential calibration formula below remains accurate.
  float xnb1 = (analogValue1 * 5.0 / 4095.0); 

  // Read pin A1
  int analogValue2 = analogRead(A1);
  float xnb2 = (analogValue2 * 5.0 / 4095.0); 

  // Change voltage to force signal 1 and sensor 2
  // These formulas rely on specific voltage levels, so we fed them the "5V scaled" values above.
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

  // Outputs
  Serial.print(Time);
  Serial.print(",");
  Serial.print(xna1); // displays the unfiltered force signal of sensor 1
  Serial.print(",");
  Serial.print(xna2); // displays the unfiltered force signal of sensor 2
  Serial.print(",");
  Serial.print(yna1); // displays the filtered force signal of sensor 1
  Serial.println();

  delay(10); 
}