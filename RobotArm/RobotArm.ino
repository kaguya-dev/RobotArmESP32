#include <Arduino.h>
#include <BluetoothSerial.h>
#include <ESP32Servo.h>

BluetoothSerial serialBT;
Servo baseServo;

float xc, yc, zc;

void setup() {
  Serial.begin(115200);
  serialBT.begin("Chisa");
  delay(300);

  Serial.println("Controller Setted!");
  Serial.println("Send: x y z");

  xc = 0;
  yc = 0;
  zc = 0;

  baseServo.setPeriodHertz(50);
  baseServo.attach(13, 500, 2500);
  baseServo.write(90);
}

void loop() {
  if (serialBT.available()) {
    String line = serialBT.readStringUntil('\n');
    line.trim();

    float x, y, z;
    int parsed = sscanf(line.c_str(), "%f%*[ ,]%f%*[ ,]%f", &x, &y, &z);

    if (parsed == 3) {
      // Increment properly
      xc += x;
      yc += y;
      zc += z;

      // Constrain AFTER increment
      xc = constrain(xc, -1.0f, 1.0f);
      yc = constrain(yc,  0.0f, 1.0f);
      zc = constrain(zc,  0.0f, 1.0f);

      float thetaRad = atan2(yc, xc);
      float thetaDeg = thetaRad * 180.0 / PI;

      int servoAngle = (int)(thetaDeg + 90.0f);
      servoAngle = constrain(servoAngle, 0, 180);

      baseServo.write(servoAngle);

      Serial.print("Theta (deg): ");
      Serial.println(thetaDeg);
      Serial.print("Servo angle: ");
      Serial.println(servoAngle);
      Serial.print("Cx = ");
      Serial.println(xc);
      Serial.print("Cy = ");
      Serial.println(yc);
    } else {
      Serial.println("Invalid input. Use: x y z");
    }
  }
}
