#include <Servo.h>

Servo myServo;  // Создание объекта Servo

void setup() {
  Serial.begin(9600); // Инициализация последовательной связи
  myServo.attach(9);  // Подключение сервомотора к пину 9
  myServo.write(0);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input.startsWith("servo:")) {
      int angle = input.substring(6).toInt();
      myServo.write(angle);
    }
  }
}
