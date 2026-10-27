#!/usr/bin/env python3
"""
========================================================================
TESIoT - ALAT 4: DIGITAL I/O STATION (Raspberry Pi)
========================================================================
Deskripsi:
Skrip Python ini menguji seluruh tombol digital input dan LED output:
1. 8x Push Buttons (Button 0 s/d Button 7)
2. 8x LEDs (LED 0 s/d LED 7)

Fitur:
- Mode Interaktif: Tekan Button [X] -> LED [X] seketika menyala.
- Mode Demo Otomatis: Jika idle lebih dari 4 detik, LED masuk ke mode
  animasi Running LED (Knight Rider Chaser) dan Counter Biner 8-bit.

Kebutuhan Library:
  pip3 install RPi.GPIO
========================================================================
"""

import time
import sys
import RPi.GPIO as GPIO

# ----------------- KONFIGURASI PIN RASPBERRY PI (BCM) -----------------
# 8 Pin Input Tombol (Pull-up internal, ditekan = LOW / 0)
BUTTON_PINS = [
    14,  # Button 0 (Pin Fisik 8)
    15,  # Button 1 (Pin Fisik 10)
    18,  # Button 2 (Pin Fisik 12)
    23,  # Button 3 (Pin Fisik 16)
    24,  # Button 4 (Pin Fisik 18)
    25,  # Button 5 (Pin Fisik 22)
    8,   # Button 6 (Pin Fisik 24)
    7    # Button 7 (Pin Fisik 26)
]

# 8 Pin Output LED (HIGH / 1 = Menyala)
LED_PINS = [
    12,  # LED 0 (Pin Fisik 32)
    16,  # LED 1 (Pin Fisik 36)
    20,  # LED 2 (Pin Fisik 38)
    21,  # LED 3 (Pin Fisik 40)
    26,  # LED 4 (Pin Fisik 37)
    19,  # LED 5 (Pin Fisik 35)
    13,  # LED 6 (Pin Fisik 33)
    6    # LED 7 (Pin Fisik 31)
]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup Button Pins dengan Internal PULL_UP
for btn in BUTTON_PINS:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup LED Pins sebagai Output
for led in LED_PINS:
    GPIO.setup(led, GPIO.OUT)
    GPIO.output(led, GPIO.LOW)

def set_all_leds(state):
    """Menghidupkan atau mematikan seluruh 8 LED."""
    for led in LED_PINS:
        GPIO.output(led, GPIO.HIGH if state else GPIO.LOW)

def write_binary_to_leds(number):
    """Menampilkan angka desimal (0-255) dalam format biner pada 8 LED."""
    for i in range(8):
        bit = (number >> i) & 1
        GPIO.output(LED_PINS[i], GPIO.HIGH if bit else GPIO.LOW)

def main():
    print("==============================================")
    print("  TESIoT - ALAT 4: DIGITAL I/O STATION (Raspberry Pi)")
    print("==============================================")
    print("-> 8 Buttons : GPIO", BUTTON_PINS)
    print("-> 8 LEDs    : GPIO", LED_PINS)
    print("==============================================")

    # Blink pembuka 2x
    for _ in range(2):
        set_all_leds(True)
        time.sleep(0.15)
        set_all_leds(False)
        time.sleep(0.15)

    print("Sistem siap!")
    print("- Tekan salah satu Button 0 s/d 7 untuk menyalakan LED pasangannya.")
    print("- Jika tidak ada tombol ditekan selama 4 detik, mode demo animasi aktif otomatis.\n")

    last_activity_time = time.time()
    chaser_idx = 0
    chaser_dir = 1
    last_demo_tick = time.time()

    try:
        while True:
            any_pressed = False

            # 1. Pindai status ke-8 tombol
            for i in range(8):
                # Karena INPUT_PULLUP, saat ditekan pin bernilai LOW (0)
                if GPIO.input(BUTTON_PINS[i]) == GPIO.LOW:
                    any_pressed = True
                    GPIO.output(LED_PINS[i], GPIO.HIGH)
                    print(f"[INPUT] Button {i} ditekan -> LED {i} AKTIF")
                else:
                    # Jika dalam mode interaktif, matikan LED jika tombol dilepas
                    if time.time() - last_activity_time < 4.0:
                        GPIO.output(LED_PINS[i], GPIO.LOW)

            if any_pressed:
                last_activity_time = time.time()
                time.sleep(0.05) # Debounce
                continue

            # 2. Mode Demo Otomatis (Jika idle > 4 detik)
            if time.time() - last_activity_time >= 4.0:
                if time.time() - last_demo_tick >= 0.08:
                    last_demo_tick = time.time()

                    # Animasi bolak-balik (Knight Rider style)
                    set_all_leds(False)
                    GPIO.output(LED_PINS[chaser_idx], GPIO.HIGH)

                    chaser_idx += chaser_dir
                    if chaser_idx >= 7:
                        chaser_dir = -1
                    elif chaser_idx <= 0:
                        chaser_dir = 1

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[STOP] Program dihentikan pengguna.")
    finally:
        set_all_leds(False)
        GPIO.cleanup()
        print("[CLEANUP] Seluruh LED dimatikan dan GPIO dibersihkan.")

if __name__ == "__main__":
    main()
