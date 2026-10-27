/*
  ========================================================================
  TESIoT - ALAT 3: ACTUATOR & POWER STATION (Pengujian Semua Motor & Relay)
  ========================================================================
  Deskripsi:
  Skrip ini menguji seluruh aktuator mekanik dan sakelar beban listrik:
  1. 4-Channel Relay Module (Relay 1 s/d Relay 4)
  2. Servo Motor (SG90)
  3. Motor DC + Driver L9110S (Kontrol Arah Maju/Mundur & Kecepatan PWM)

  Library yang dibutuhkan (Install via Arduino Library Manager):
  - ESP32Servo by Kevin Harrington
  ========================================================================
*/

#include <ESP32Servo.h>

// ----------------- KONFIGURASI PIN ESP32 -----------------
// 1. Modul 4-Channel Relay
// Catatan: Modul relay umumnya Active LOW (LOW = Relay ON, HIGH = Relay OFF)
#define RELAY1_PIN      26
#define RELAY2_PIN      27
#define RELAY3_PIN      14
#define RELAY4_PIN      12

const int relayPins[4] = {RELAY1_PIN, RELAY2_PIN, RELAY3_PIN, RELAY4_PIN};
#define RELAY_ON        LOW
#define RELAY_OFF       HIGH

// 2. Servo Motor
#define SERVO_PIN       13
Servo myServo;

// 3. Motor DC (Driver L9110S)
#define MOTOR_IN1       18
#define MOTOR_IN2       19

// Variabel Kontrol State Mesin
unsigned long lastActuatorStep = 0;
int currentStep = 0;

void setRelay(int index, bool state) {
  digitalWrite(relayPins[index], state ? RELAY_ON : RELAY_OFF);
}

void allRelaysOff() {
  for (int i = 0; i < 4; i++) {
    setRelay(i, false);
  }
}

void allRelaysOn() {
  for (int i = 0; i < 4; i++) {
    setRelay(i, true);
  }
}

// Kontrol Motor DC
void motorForward(int speed) {
  analogWrite(MOTOR_IN1, speed);
  analogWrite(MOTOR_IN2, 0);
}

void motorReverse(int speed) {
  analogWrite(MOTOR_IN1, 0);
  analogWrite(MOTOR_IN2, speed);
}

void motorStop() {
  analogWrite(MOTOR_IN1, 0);
  analogWrite(MOTOR_IN2, 0);
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==============================================");
  Serial.println("  TESIoT - ALAT 3: ACTUATOR STATION STARTED   ");
  Serial.println("==============================================");

  // Inisialisasi Pin Relay
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], RELAY_OFF); // Matikan semua relay di awal
  }
  Serial.println("[RELAY] 4-Channel Relay siap.");

  // Inisialisasi Servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  myServo.setPeriodHertz(50); // Standar 50Hz servo
  myServo.attach(SERVO_PIN, 500, 2400); // 500us s/d 2400us rentang pulse SG90
  myServo.write(0);
  Serial.println("[SERVO] Motor servo siap pada GPIO 13.");

  // Inisialisasi Motor DC
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  motorStop();
  Serial.println("[MOTOR DC] Driver L9110S siap pada GPIO 18 & 19.");

  Serial.println("Memulai simulasi urutan aktuator secara terprogram...\n");
}

void loop() {
  // Jalankan siklus tes bertahap setiap 2 detik
  if (millis() - lastActuatorStep >= 2000) {
    lastActuatorStep = millis();
    currentStep = (currentStep + 1) % 6;

    switch (currentStep) {
      case 0:
        Serial.println(">>> STEP 1: Running Relay (Relay 1 ON, Servo 0°)");
        allRelaysOff();
        setRelay(0, true);
        myServo.write(0);
        motorStop();
        break;

      case 1:
        Serial.println(">>> STEP 2: Running Relay (Relay 2 ON, Servo 45°, Motor DC Maju)");
        allRelaysOff();
        setRelay(1, true);
        myServo.write(45);
        motorForward(180); // Kecepatan sedang (~70%)
        break;

      case 2:
        Serial.println(">>> STEP 3: Running Relay (Relay 3 ON, Servo 90°, Motor DC Full Speed)");
        allRelaysOff();
        setRelay(2, true);
        myServo.write(90);
        motorForward(255); // Kecepatan penuh
        break;

      case 3:
        Serial.println(">>> STEP 4: Running Relay (Relay 4 ON, Servo 135°, Motor DC Berhenti)");
        allRelaysOff();
        setRelay(3, true);
        myServo.write(135);
        motorStop();
        break;

      case 4:
        Serial.println(">>> STEP 5: Semua Relay ON, Servo 180°, Motor DC Putar Mundur (Reverse)");
        allRelaysOn();
        myServo.write(180);
        motorReverse(200);
        break;

      case 5:
        Serial.println(">>> STEP 6: Cooldown (Semua Relay OFF, Servo 0°, Motor DC Stop)");
        allRelaysOff();
        myServo.write(0);
        motorStop();
        break;
    }
  }
}
