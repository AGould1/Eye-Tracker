#include <Servo.h>

Servo myPanServo;
Servo myTiltServo;

void setup() {
  // put your setup code here, to run once:
  myPanServo.attach(9);
  myTiltServo.attach(10);
  Serial.begin(9600);
}

String data_message;

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    data_message = Serial.readStringUntil('\n');

    int commaIndex = data_message.indexOf(',');
    String x_position = data_message.substring(0, commaIndex);
    String y_position = data_message.substring(commaIndex + 1);

    int angle_value_x = x_position.toInt();
    int angle_value_y = y_position.toInt();

    myPanServo.write(angle_value_x);
    myTiltServo.write(angle_value_y);

    Serial.print(angle_value_x);
    Serial.print(angle_value_y);
  }
}
