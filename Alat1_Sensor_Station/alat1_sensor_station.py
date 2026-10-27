#!/usr/bin/env python3
"""
========================================================================
TESIoT - ALAT 1: SENSOR STATION (Raspberry Pi)
========================================================================
Deskripsi:
Skrip Python ini menguji dan memvalidasi ke-4 sensor pada trainer kit TESIoT:
1. Sensor Suhu & Kelembaban (DHT11/DHT22)
2. Sensor Gas MQ-Series (Digital Output / DO Pin)
3. Sensor Ultrasonik HC-SR04 (Jarak cm)
4. Modul I2C (I2C Scanner / RTC DS3231)

Kebutuhan Library:
  pip3 install RPi.GPIO adafruit-circuitpython-dht smbus2
========================================================================
"""

import time
import sys
import RPi.GPIO as GPIO

# Coba import modul I2C dan DHT
try:
    import smbus2
    I2C_AVAILABLE = True
except ImportError:
    I2C_AVAILABLE = False

try:
    import board
    import adafruit_dht
    DHT_CIRCUIT_AVAILABLE = True
except ImportError:
    DHT_CIRCUIT_AVAILABLE = False

# ----------------- KONFIGURASI PIN RASPBERRY PI (BCM) -----------------
DHT_PIN = 4          # GPIO 4 (Pin Fisik 7)
MQ_DO_PIN = 17       # GPIO 17 (Pin Fisik 11) - Digital Output MQ
TRIG_PIN = 27        # GPIO 27 (Pin Fisik 13) - Trig Ultrasonik
ECHO_PIN = 22        # GPIO 22 (Pin Fisik 15) - Echo Ultrasonik (disarankan pembagi tegangan 5V->3.3V)
I2C_BUS_NUM = 1      # I2C Bus 1 (SDA: GPIO 2 / Pin 3, SCL: GPIO 3 / Pin 5)

# Setup GPIO Mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup Pin Sensor
GPIO.setup(MQ_DO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)

# Setup DHT jika library tersedia
dht_device = None
if DHT_CIRCUIT_AVAILABLE:
    try:
        # Default DHT11 pada GPIO4 (board.D4)
        dht_device = adafruit_dht.DHT11(board.D4)
    except Exception as e:
        print(f"[DHT WARNING] Inisialisasi CircuitPython DHT gagal: {e}")

# ----------------- FUNGSI BACA JARAK ULTRASONIK -----------------
def read_ultrasonic_distance():
    """Mengukur jarak objek menggunakan HC-SR04 dengan satuan cm."""
    # Kirim pulsa trigger 10us
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    timeout_start = pulse_start

    # Tunggu sinyal Echo HIGH (dengan timeout 0.04 detik)
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.04:
            return None

    pulse_end = pulse_start
    timeout_end = pulse_start
    # Tunggu sinyal Echo LOW kembali
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_end > 0.04:
            return None

    pulse_duration = pulse_end - pulse_start
    # Kecepatan suara = 34300 cm/s -> jarak = (durasi * 34300) / 2
    distance = (pulse_duration * 34300) / 2
    return round(distance, 1)

# ----------------- FUNGSI I2C SCANNER -----------------
def scan_i2c():
    """Memindai seluruh alamat I2C yang aktif pada Raspberry Pi."""
    found_devices = []
    if not I2C_AVAILABLE:
        return ["Library smbus2 belum diinstal"]

    try:
        bus = smbus2.SMBus(I2C_BUS_NUM)
        for address in range(0x08, 0x78):
            try:
                bus.write_quick(address)
                found_devices.append(hex(address))
            except OSError:
                pass
        bus.close()
    except Exception as e:
        return [f"Gagal akses I2C Bus: {e}"]
    return found_devices

def main():
    print("==============================================")
    print("  TESIoT - ALAT 1: SENSOR STATION (Raspberry Pi)")
    print("==============================================")
    print(f"-> DHT Pin         : GPIO {DHT_PIN} (BCM)")
    print(f"-> MQ Gas DO Pin   : GPIO {MQ_DO_PIN} (BCM)")
    print(f"-> Ultrasonik Trig : GPIO {TRIG_PIN} | Echo: GPIO {ECHO_PIN}")
    print("-> I2C Port        : GPIO 2 (SDA), GPIO 3 (SCL)")
    print("==============================================")

    # Lakukan scan I2C di awal
    i2c_list = scan_i2c()
    print(f"[I2C SCANNER] Perangkat terdeteksi: {', '.join(i2c_list) if i2c_list else 'Tidak ada'}\n")
    print("Memulai pembacaan sensor berkala (Ctrl+C untuk berhenti)...\n")

    try:
        while True:
            print("----------------------------------------------")
            print(f"[TIMESTAMP] {time.strftime('%Y-%m-%d %H:%M:%S')}")

            # 1. Baca Sensor Suhu & Kelembaban (DHT)
            if dht_device:
                try:
                    temp = dht_device.temperature
                    humidity = dht_device.humidity
                    if temp is not None and humidity is not None:
                        print(f"[DHT11] Suhu: {temp:.1f} °C | Kelembaban: {humidity:.1f} %")
                    else:
                        print("[DHT11] Data tidak terbaca, mencoba ulang di siklus berikutnya...")
                except RuntimeError:
                    print("[DHT11] Sedang membaca sensor...")
                except Exception as e:
                    print(f"[DHT11 ERROR] {e}")
            else:
                print("[DHT11] Mode simulasi (instal adafruit-circuitpython-dht untuk membaca sensor fisik)")

            # 2. Baca Sensor Gas MQ
            mq_state = GPIO.input(MQ_DO_PIN)
            # Modul sensor MQ aktif LOW saat mendeteksi konsentrasi gas di atas batas trimpot
            if mq_state == GPIO.LOW:
                print("[MQ GAS] STATUS: ⚠️ BAHAYA! Terdeteksi Gas/Asap di atas ambang batas!")
            else:
                print("[MQ GAS] STATUS: ✅ NORMAL (Udara Bersih)")

            # 3. Baca Sensor Ultrasonik
            dist = read_ultrasonic_distance()
            if dist is not None:
                print(f"[ULTRASONIK] Jarak Objek: {dist} cm")
            else:
                print("[ULTRASONIK] Objek di luar jangkauan atau sensor terhalang")

            print("----------------------------------------------\n")
            time.sleep(1.5)

    except KeyboardInterrupt:
        print("\n[STOP] Program dihentikan pengguna.")
    finally:
        if dht_device:
            dht_device.exit()
        GPIO.cleanup()
        print("[CLEANUP] GPIO dibersihkan.")

if __name__ == "__main__":
    main()
