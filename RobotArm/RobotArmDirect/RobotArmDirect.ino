#include <Arduino.h>
#include <ESP32Servo.h>
#define pin0 13
#define pin1 12
#define pin2 14
#define pin3 27
#define pin4 26
Servo baseServo;
Servo s1,s2,s3;
Servo sClaw;

int xc, yc, zc, wc;
bool claw;

void setup() {
  Serial.begin(115200);
  delay(300);

  Serial.println("Send: x y z w and claw(0 = Closed | -1 = Opened)");

  xc = 0;
  yc = 0;
  zc = 0;
  wc = 0;
  claw = 0;

  baseServo.setPeriodHertz(50);
  baseServo.attach(pin0);
  baseServo.write(90);
  s1.setPeriodHertz(50);
  s1.attach(pin1);
  s1.write(90);
  s2.setPeriodHertz(50);
  s2.attach(pin2);
  s2.write(90);
  s3.setPeriodHertz(50);
  s3.attach(pin3);
  s3.write(90);
  sClaw.setPeriodHertz(50);
  sClaw.attach(pin4);
  sClaw.write(90);
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    int x, y, z, w, clawOp;
    int parsed = sscanf(line.c_str(), "%d%*[ ,]%d%*[ ,]%d%*[ ,]%d%*[ ,]%d", &x, &y, &z, &w, &claw);

    if (parsed == 5) {
      xc = x;
      yc = y;
      zc = z;
      wc = w;
      claw = claw;
      
      xc = constrain(xc, 0, 180);
      yc = constrain(yc,  0, 180);
      zc = constrain(zc,  0, 180);
      wc = constrain(wc, 0 ,180);

      baseServo.write(xc);
      s1.write(yc);
      s2.write(zc);
      s3.write(wc);

      //if(claw) sClaw.write(180);
      //else sClaw.write(0);

      Serial.println("Angle x:" + String(xc) +
               " |    Angle y:" + String(yc) +
               " |    Angle z:" + String(zc) +
               " |    Angle w:" + String(wc) +
               " |    Claw Op:" + String(claw));
    } else {
      Serial.println("Invalid input. Use: x y z w claw(0/1)");
    }
  }
}