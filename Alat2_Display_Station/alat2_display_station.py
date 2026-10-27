#!/usr/bin/env python3
"""
========================================================================
TESIoT - ALAT 2: DISPLAY STATION (Raspberry Pi)
========================================================================
Deskripsi:
Skrip Python ini menguji dan menjalankan ke-4 layar/display:
1. LCD 20x4 I2C (Alamat I2C: 0x27)
2. OLED 1.3 Inch I2C (SSD1306/SH1106, Alamat I2C: 0x3C)
3. 7-Segment Display (TM1637)
4. LED Matrix 8x8 (MAX7219 SPI / GPIO)

Kebutuhan Library:
  pip3 install RPLCD luma.oled luma.led_matrix raspberrypi-tm1637 pillow smbus2
========================================================================
"""

import time
import sys
import RPi.GPIO as GPIO

# Inisialisasi status modul display
has_lcd = False
has_oled = False
has_tm1637 = False
has_matrix = False

# ----------------- 1. KONFIGURASI LCD 20x4 I2C -----------------
lcd = None
try:
    from RPLCD.i2c import CharLCD
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=20, rows=4)
    lcd.clear()
    lcd.cursor_mode = 'hide'
    has_lcd = True
    print("[LCD 20x4] Modul I2C 0x27 siap.")
except Exception as e:
    print(f"[LCD 20x4 NOTICE] {e}")

# ----------------- 2. KONFIGURASI OLED 1.3" I2C -----------------
oled_device = None
try:
    from luma.core.interface.serial import i2c
    from luma.oled.device import sh1106, ssd1306
    from PIL import Image, ImageDraw, ImageFont
    
    serial_i2c = i2c(port=1, address=0x3C)
    # Kebanyakan modul OLED 1.3" menggunakan driver SH1106 (atau SSD1306)
    try:
        oled_device = sh1106(serial_i2c)
    except Exception:
        oled_device = ssd1306(serial_i2c)
    has_oled = True
    print("[OLED 1.3] Display I2C 0x3C siap.")
except Exception as e:
    print(f"[OLED 1.3 NOTICE] {e}")

# ----------------- 3. KONFIGURASI 7-SEGMENT TM1637 -----------------
# Pin BCM: CLK -> GPIO 23 (Pin 16), DIO -> GPIO 24 (Pin 18)
TM_CLK_PIN = 23
TM_DIO_PIN = 24
tm_display = None
try:
    import tm1637
    tm_display = tm1637.TM1637(clk=TM_CLK_PIN, dio=TM_DIO_PIN)
    tm_display.brightness(7)
    has_tm1637 = True
    print("[7-SEGMENT] Modul TM1637 siap.")
except Exception as e:
    print(f"[7-SEGMENT NOTICE] {e}")

# ----------------- 4. KONFIGURASI LED MATRIX MAX7219 -----------------
matrix_device = None
try:
    from luma.core.interface.serial import spi, noop
    from luma.led_matrix.device import max7219
    from luma.core.render import canvas

    # SPI Port 0, Device 0 (CE0: GPIO 8, SCLK: GPIO 11, MOSI: GPIO 10)
    serial_spi = spi(port=0, device=0, gpio=noop())
    matrix_device = max7219(serial_spi, cascaded=1, block_orientation=0)
    matrix_device.contrast(64)
    has_matrix = True
    print("[LED MATRIX] MAX7219 SPI siap.")
except Exception as e:
    print(f"[LED MATRIX NOTICE] {e}")

def main():
    print("\n==============================================")
    print("  TESIoT - ALAT 2: DISPLAY STATION (Raspberry Pi)")
    print("==============================================")
    print("Memulai siklus update tampilan serentak...\n")

    counter = 0

    try:
        while True:
            counter += 1

            # 1. Update LCD 20x4
            if has_lcd and lcd:
                try:
                    lcd.cursor_pos = (0, 0)
                    lcd.write_string("== TESIoT SIMULATOR ==")
                    lcd.cursor_pos = (1, 0)
                    lcd.write_string("DISPLAY TEST STATION")
                    lcd.cursor_pos = (2, 0)
                    lcd.write_string(time.strftime("Jam: %H:%M:%S"))
                    lcd.cursor_pos = (3, 0)
                    lcd.write_string(f"Uptime: {counter:4d} detik")
                except Exception as e:
                    print(f"[LCD ERROR] {e}")

            # 2. Update 7-Segment (Tampilkan angka counter naik 0-9999)
            if has_tm1637 and tm_display:
                try:
                    tm_display.number(counter % 10000)
                except Exception as e:
                    print(f"[7-SEG ERROR] {e}")

            # 3. Update OLED (Grafis teks dan progress bar dinamis)
            if has_oled and oled_device:
                try:
                    with canvas(oled_device) as draw:
                        draw.rectangle((2, 2, 126, 62), outline="white", fill="black")
                        draw.text((10, 8), "TESIoT OLED DEMO", fill="white")
                        draw.text((10, 22), f"Uptime: {counter}s", fill="white")
                        draw.text((10, 34), time.strftime("%H:%M:%S"), fill="white")

                        # Progress bar bergerak
                        bar_w = (counter % 10 + 1) * 10
                        draw.rectangle((10, 48, 110, 56), outline="white")
                        draw.rectangle((12, 50, 10 + bar_w, 54), fill="white")
                except Exception as e:
                    print(f"[OLED ERROR] {e}")

            # 4. Update LED Matrix (Berganti pola senyum & kotak)
            if has_matrix and matrix_device:
                try:
                    with canvas(matrix_device) as draw:
                        if counter % 2 == 0:
                            # Gambar kotak luar & titik tengah
                            draw.rectangle((0, 0, 7, 7), outline="white")
                            draw.point((3, 3), fill="white")
                            draw.point((4, 4), fill="white")
                        else:
                            # Gambar silang / X
                            draw.line((0, 0, 7, 7), fill="white")
                            draw.line((0, 7, 7, 0), fill="white")
                except Exception as e:
                    print(f"[MATRIX ERROR] {e}")

            print(f"[DISPLAY UPDATE] Uptime: {counter}s | Status: Aktif")
            time.sleep(1.0)

    except KeyboardInterrupt:
        print("\n[STOP] Program dihentikan pengguna.")
    finally:
        if has_lcd and lcd:
            try:
                lcd.clear()
            except Exception:
                pass
        if has_tm1637 and tm_display:
            try:
                tm_display.numbers(0, 0, 0, 0)
            except Exception:
                pass
        GPIO.cleanup()
        print("[CLEANUP] Display dan GPIO dibersihkan.")

if __name__ == "__main__":
    main()
