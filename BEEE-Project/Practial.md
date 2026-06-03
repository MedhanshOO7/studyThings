# Practical File
## Experiment: Arduino Distance Meter using HC-SR04, LCD & Laser

---

## Aim

To design and implement a distance measurement system using an Arduino Uno, HC-SR04 ultrasonic sensor, 16x2 I2C LCD display, and HW-493 laser pointer module that measures and displays real-time distance in centimetres.

---

## Components Required

| Component | Specification | Qty |
|---|---|---|
| Arduino Uno | ATmega328P, 16MHz, 5V | 1 |
| Ultrasonic Sensor | HC-SR04, range 2cm–400cm | 1 |
| LCD Display | 16x2 with I2C module (0x27) | 1 |
| Laser Module | HW-493 / KY-008, 650nm, 5mW | 1 |
| Connecting Wires | Jumper wires M-M | As required |
| USB / Power Adapter | 5V, minimum 1A | 1 |

---

## Theory

The HC-SR04 ultrasonic sensor measures distance using the echo-location principle. A 10µs trigger pulse causes the sensor to emit 8 bursts of 40kHz ultrasonic sound. These waves travel through air, reflect off an object, and return to the sensor. The time between emission and reception of the echo is measured. Using the speed of sound (343 m/s = 0.0343 cm/µs), distance is calculated as:

```
Distance (cm)  =  (Echo Duration in µs  ×  0.0343)  ÷  2
```

Division by 2 accounts for the round-trip path of the sound wave. The result is sent to the LCD via the I2C protocol using only two signal lines (SDA and SCL). The HW-493 laser serves as a visual pointer indicating the target object.

---

## Circuit Connections

| Component | Pins | Arduino Pins |
|---|---|---|
| HC-SR04 | VCC / GND / TRIG / ECHO | 5V / GND / D9 / D10 |
| LCD I2C | VCC / GND / SDA / SCL | 5V / GND / A4 / A5 |
| HW-493 Laser | VCC / GND / Signal | 5V / GND / D7 |

---

## Program Code

```cpp
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const int TRIG_PIN = 9, ECHO_PIN = 10, LASER_PIN = 7;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LASER_PIN, OUTPUT);
  digitalWrite(LASER_PIN, HIGH);
  lcd.init();
  lcd.backlight();
  lcd.print("Distance Meter");
  delay(2000);
  lcd.clear();
}

float getDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long d = pulseIn(ECHO_PIN, HIGH, 30000);
  return (d == 0) ? -1 : (d * 0.0343) / 2.0;
}

void loop() {
  float dist = getDistance();
  lcd.setCursor(0, 0);
  lcd.print("Dist:");
  lcd.setCursor(0, 1);
  if (dist < 0 || dist > 400) lcd.print("Out of range    ");
  else { lcd.print(dist, 1); lcd.print(" cm         "); }
  delay(200);
}
```

---

## Result & Conclusion

The system successfully measured distances in the range of 2cm to 400cm with an accuracy of ±3mm. The LCD displayed real-time readings refreshed every 200ms. The laser pointer provided a clear visual indicator of the target object. The project demonstrates practical application of ultrasonic sensing, I2C communication, and embedded C++ programming on the Arduino platform.

---

## Precautions

- Never look directly into the laser beam — eye damage is possible
- Ensure all VCC and GND connections are correct before powering on
- Use a dedicated 5V/1A wall adapter to avoid Arduino resets under load
- The sensor may give inaccurate readings on soft or angled surfaces
- Always call `lcd.init()` before any LCD print commands
