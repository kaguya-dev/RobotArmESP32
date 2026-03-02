#include <Arduino.h>
#include <ESP32Servo.h>
#define pin0 13
#define pin1 12
#define pin2 14
Servo baseServo;
Servo s1,s2;

int xc, yc, zc;

void setup() {
  Serial.begin(115200);
  delay(300);

  Serial.println("Send: x y z");

  xc = 0;
  yc = 0;
  zc = 0;

  baseServo.setPeriodHertz(50);
  baseServo.attach(pin0);
  baseServo.write(90);
  s1.setPeriodHertz(50);
  s1.attach(pin1);
  s1.write(90);
  s2.setPeriodHertz(50);
  s2.attach(pin2);
  s2.write(90);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    int x, y, z;
    int parsed = sscanf(line.c_str(), "%d%*[ ,]%d%*[ ,]%d", &x, &y, &z);

    if (parsed == 3) {
      xc = x;
      yc = y;
      zc = z;

      xc = constrain(xc, 0, 180);
      yc = constrain(yc,  0, 180);
      zc = constrain(zc,  0, 180);

      baseServo.write(xc);
      s1.write(yc);
      s2.write(zc);

      Serial.println("Angle x:" + String(xc) +
               " |    Angle y:" + String(yc) +
               " |    Angle z:" + String(zc));
    } else {
      Serial.println("Invalid input. Use: x y z");
    }
  }
}