#include <Servo.h>
int ledPin = 6;
int brightness = 0;
int deel = 650;
Servo myServo;
String command = "";

void setup() {
  myServo.attach(9); // signal wire on pin 9
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // check if there's input from Serial Monitor
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n'); // read input until Enter is pressed
    command.trim(); // remove any extra spaces/newlines\
    
    String cmd = command;
    // Example: Digital 6 ON
    if (cmd.startsWith("Digital")) {
      int space1 = cmd.indexOf(' ');
      int space2 = cmd.indexOf(' ', space1 + 1);
      int pin = cmd.substring(space1 + 1, space2).toInt();
      String mode = cmd.substring(space2 + 1);
      pinMode(pin, OUTPUT);
      if (mode.equals("ON")){ digitalWrite(pin, HIGH);}
      if (mode.equals("OFF")){ digitalWrite(pin, LOW);}
  }

    // Example: Analog 4 255
    else if (cmd.startsWith("Analog")) {
      int space1 = cmd.indexOf(' ');
      int space2 = cmd.indexOf(' ', space1 + 1);
      int pin = cmd.substring(space1 + 1, space2).toInt();
      int value = cmd.substring(space2 + 1).toInt();
      pinMode(pin, OUTPUT);
      analogWrite(pin, value);
  }

    //Example Servo 9 90
    else if (cmd.startsWith("Servo")) {
      int space1 = cmd.indexOf(' ');
      int space2 = cmd.indexOf(' ', space1 + 1);
      int pin = cmd.substring(space1 + 1, space2).toInt();
      int value = cmd.substring(space2 + 1).toInt();
      myServo.attach(pin);
      myServo.write(value);
  }
    //Example Sleep 6
    else if (cmd.startsWith("Sleep")) {
      int space1 = cmd.indexOf(' ');
      int val = cmd.substring(space1 + 1).toInt();
      val=val*1000;
      delay(val);
  }

    else {
      Serial.println("Unknown command");
    }
  }
}


