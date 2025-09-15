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
  // put your setup code here, to run once:
  Serial.begin(19200);
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
  Time = millis();

  // Read pin A0 and compute the force
  int analogValue1 = analogRead(A0);
  float xnb1 = (analogValue1 * 5.0 / 1023.0); // xnb1 is the voltage analogue signal for sensor 1

  // Read pin A1 and compute the force
  int analogValue2 = analogRead(A1);
  float xnb2 = (analogValue2 * 5.0 / 1023.0); // xnb2 is the voltage analogue signal for sensor 2

  // Change voltage to force signal 1 and sensor 2
  xna1 = 0.8259 * exp(0.8623 * xnb1) + 0.00009463 * exp(3.163 * xnb1) - 0.825; // xna1 is the force value of sensor 1
  xna2 = 0.8259 * exp(0.8623 * xnb2) + 0.00009463 * exp(3.163 * xnb2) - 0.825; // xna2 is the force value of sensor 2
 
  // Compute the first filtered signal
  float yna1 = alpha * yn1 + beta * xna1 + beta * xn1; // yna1 is the filter force signal for sensor 1

  // Compute the second filtered signal
  float yna2 = alpha * yn2 + beta * xna2 + beta * xn2; // yna2 is filtered force signal for sensor 2
   
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

  delay(10); // Maintain a delay of 10 milliseconds between readings for a 100 Hz sampling rate
}
