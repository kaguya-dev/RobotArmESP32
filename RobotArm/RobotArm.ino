#include <Arduino.h>
#include <ESP32Servo.h>

Servo baseServo;

float xc, yc, zc;

void setup() {
  Serial.begin(115200);
  delay(300);

  Serial.println("Controller Setted!");
  Serial.println("Send: x y z");

  xc = 0;
  yc = 0;
  zc = 0;

  baseServo.setPeriodHertz(50);
  baseServo.attach(13);
  baseServo.write(90);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
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

      Serial.println("Theta:" + String(thetaDeg) +
               " | Servo:" + String(servoAngle) +
               " | Cx:" + String(xc) +
               " | Cy:" + String(yc));
    } else {
      Serial.println("Invalid input. Use: x y z");
    }
  }
}
