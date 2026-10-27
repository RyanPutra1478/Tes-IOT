#!/usr/bin/env python3
"""
========================================================================
TESIoT - ALAT 3: ACTUATOR & POWER STATION (Raspberry Pi)
========================================================================
Deskripsi:
Skrip Python ini menguji seluruh aktuator mekanik dan sakelar beban:
1. 4-Channel Relay Module (Relay 1 s/d Relay 4)
2. Servo Motor (SG90 - PWM Sweep)
3. Motor DC + Driver L9110S (Kontrol Arah Maju/Mundur & Kecepatan)

Kebutuhan Library:
  pip3 install RPi.GPIO
========================================================================
"""

import time
import sys
import RPi.GPIO as GPIO

# ----------------- KONFIGURASI PIN RASPBERRY PI (BCM) -----------------
# 1. Modul 4-Channel Relay
# Umumnya modul relay Active LOW (0 / False = ON, 1 / True = OFF)
RELAY_PINS = [5, 6, 13, 19]  # GPIO 5, 6, 13, 19
RELAY_ON = GPIO.LOW
RELAY_OFF = GPIO.HIGH

# 2. Servo Motor SG90
SERVO_PIN = 18               # GPIO 18 (Hardware PWM0 / Pin Fisik 12)

# 3. Motor DC Driver L9110S
MOTOR_IN1 = 20               # GPIO 20 (Pin Fisik 38)
MOTOR_IN2 = 21               # GPIO 21 (Pin Fisik 40)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup Pin Relay
for pin in RELAY_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, RELAY_OFF)

# Setup Servo PWM (Frekuensi 50Hz)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# Setup Motor DC PWM (Frekuensi 1000Hz)
GPIO.setup(MOTOR_IN1, GPIO.OUT)
GPIO.setup(MOTOR_IN2, GPIO.OUT)
motor_pwm1 = GPIO.PWM(MOTOR_IN1, 1000)
motor_pwm2 = GPIO.PWM(MOTOR_IN2, 1000)
motor_pwm1.start(0)
motor_pwm2.start(0)

def set_relay(index, state):
    """Menyetel status relay tunggal (index 0 - 3)."""
    GPIO.output(RELAY_PINS[index], RELAY_ON if state else RELAY_OFF)

def all_relays(state):
    """Menyetel status semua relay sekaligus."""
    for pin in RELAY_PINS:
        GPIO.output(pin, RELAY_ON if state else RELAY_OFF)

def set_servo_angle(angle):
    """
    Menggerakkan servo ke sudut (0 - 180 derajat).
    Duty cycle: 0 deg ~ 2.5%, 180 deg ~ 12.5%
    """
    duty = 2.5 + (angle / 180.0) * 10.0
    servo_pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    servo_pwm.ChangeDutyCycle(0) # Hindari servo mendengung/panas

def motor_forward(speed_percent=80):
    motor_pwm1.ChangeDutyCycle(speed_percent)
    motor_pwm2.ChangeDutyCycle(0)

def motor_reverse(speed_percent=80):
    motor_pwm1.ChangeDutyCycle(0)
    motor_pwm2.ChangeDutyCycle(speed_percent)

def motor_stop():
    motor_pwm1.ChangeDutyCycle(0)
    motor_pwm2.ChangeDutyCycle(0)

def main():
    print("==============================================")
    print("  TESIoT - ALAT 3: ACTUATOR STATION (Raspberry Pi)")
    print("==============================================")
    print(f"-> 4-Channel Relay : GPIO {RELAY_PINS}")
    print(f"-> Servo Motor     : GPIO {SERVO_PIN} (50Hz PWM)")
    print(f"-> Motor DC Driver : IN1=GPIO {MOTOR_IN1}, IN2=GPIO {MOTOR_IN2}")
    print("==============================================")
    print("Memulai pengujian urutan aktuator secara terprogram...\n")

    steps = [
        {"desc": "STEP 1: Relay 1 ON | Servo 0° | Motor Stop",
         "action": lambda: (all_relays(False), set_relay(0, True), set_servo_angle(0), motor_stop())},
        
        {"desc": "STEP 2: Relay 2 ON | Servo 45° | Motor Maju (Kecepatan 60%)",
         "action": lambda: (all_relays(False), set_relay(1, True), set_servo_angle(45), motor_forward(60))},
        
        {"desc": "STEP 3: Relay 3 ON | Servo 90° | Motor Maju (Kecepatan 100%)",
         "action": lambda: (all_relays(False), set_relay(2, True), set_servo_angle(90), motor_forward(100))},
        
        {"desc": "STEP 4: Relay 4 ON | Servo 135° | Motor Stop",
         "action": lambda: (all_relays(False), set_relay(3, True), set_servo_angle(135), motor_stop())},
        
        {"desc": "STEP 5: Semua Relay ON | Servo 180° | Motor Putar Mundur (Reverse 80%)",
         "action": lambda: (all_relays(True), set_servo_angle(180), motor_reverse(80))},
        
        {"desc": "STEP 6: Cooldown | Semua Relay OFF | Servo 0° | Motor Stop",
         "action": lambda: (all_relays(False), set_servo_angle(0), motor_stop())}
    ]

    try:
        while True:
            for step in steps:
                print(f">>> {step['desc']}")
                step["action"]()
                time.sleep(2.5)
            print("--- Siklus aktuator selesai, mengulang kembali ---\n")

    except KeyboardInterrupt:
        print("\n[STOP] Program dihentikan pengguna.")
    finally:
        all_relays(False)
        motor_stop()
        servo_pwm.stop()
        motor_pwm1.stop()
        motor_pwm2.stop()
        GPIO.cleanup()
        print("[CLEANUP] Aktuator dinonaktifkan dan GPIO dibersihkan.")

if __name__ == "__main__":
    main()
