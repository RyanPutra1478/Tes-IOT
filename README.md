# Panduan Penggunaan 4 Skrip Trainer TESIoT

Dokumen ini berisi panduan pengkabelan (*wiring jumper*) dan daftar library untuk menguji seluruh komponen kit **TESIoT** menggunakan **ESP32**.

---

## 📁 Struktur File Proyek

```text
e:/Projek/TESIOT/
├── Alat1_Sensor_Station/
│   └── Alat1_Sensor_Station.ino   # Menguji 100% Sensor (DHT, MQ Gas, Ultrasonik, I2C RTC)
├── Alat2_Display_Station/
│   └── Alat2_Display_Station.ino  # Menguji 100% Display (LCD 20x4, OLED 1.3", 7-Seg, LED Matrix)
├── Alat3_Actuator_Station/
│   └── Alat3_Actuator_Station.ino # Menguji 100% Aktuator (Relay 1-4, Servo, Motor DC)
├── Alat4_Digital_IO_Station/
│   └── Alat4_Digital_IO_Station.ino# Menguji 100% I/O (8 Push Button & 8 LED)
└── README.md
```

---

## 📚 Daftar Library Arduino yang Diperlukan

Buka **Arduino IDE** -> Menu **Tools** -> **Manage Libraries...** (Ctrl+Shift+I), lalu cari dan instal library berikut:

| Skrip | Library yang Harus Diinstal | Pembuat (Author) |
| :--- | :--- | :--- |
| **Alat 1** | `DHT sensor library` | Adafruit |
| | `Adafruit Unified Sensor` | Adafruit |
| | `RTClib` | Adafruit |
| **Alat 2** | `LiquidCrystal I2C` | Frank de Brabander |
| | `Adafruit SSD1306` | Adafruit |
| | `Adafruit GFX Library` | Adafruit |
| | `TM1637` | Avishay Orpaz |
| | `LedControl` | Eberhard Fahle |
| **Alat 3** | `ESP32Servo` | Kevin Harrington |
| **Alat 4** | *(Tidak butuh library eksternal, bawaan ESP32)* | - |

---

## 🔌 Panduan Pengkabelan (Wiring Pinout)

Setiap skrip berjalan mandiri. Hubungkan pin modul di trainer ke pin ESP32 menggunakan kabel jumper sesuai tabel berikut:

### 1️⃣ Alat 1: SENSOR STATION
| Komponen di Papan | Pin Modul | Sambungkan ke Pin ESP32 |
| :--- | :--- | :--- |
| **Sensor Suhu DHT** | `OUT` | **GPIO 4** |
| **Sensor Gas MQ** | `Analog / A0` | **GPIO 34** (ADC) |
| **Ultrasonik HC-SR04**| `Trig` | **GPIO 5** |
| | `Echo` | **GPIO 18** |
| **Modul I2C (RTC)** | `SDA` | **GPIO 21** |
| | `SCL` | **GPIO 22** |
| *Power* | `VCC` -> 3.3V/5V, `GND` -> GND | Terminal VCC & GND Papan |

---

### 2️⃣ Alat 2: DISPLAY STATION
| Komponen di Papan | Pin Modul | Sambungkan ke Pin ESP32 |
| :--- | :--- | :--- |
| **LCD 20x4 I2C** | `SDA` | **GPIO 21** (Jalur I2C bersama) |
| | `SCL` | **GPIO 22** (Jalur I2C bersama) |
| **OLED 1.3" I2C** | `SDA` | **GPIO 21** (Jalur I2C bersama) |
| | `SCL` | **GPIO 22** (Jalur I2C bersama) |
| **7-Segment TM1637**| `CLK` | **GPIO 19** |
| | `DIO` | **GPIO 18** |
| **LED Matrix MAX7219**| `DIN` | **GPIO 23** |
| | `CLK` | **GPIO 14** |
| | `CS` | **GPIO 5** |

---

### 3️⃣ Alat 3: ACTUATOR & POWER STATION
| Komponen di Papan | Pin Modul | Sambungkan ke Pin ESP32 |
| :--- | :--- | :--- |
| **4-Channel Relay** | `Relay 1` | **GPIO 26** |
| | `Relay 2` | **GPIO 27** |
| | `Relay 3` | **GPIO 14** |
| | `Relay 4` | **GPIO 12** |
| **Servo Motor** | `PWM / Signal` | **GPIO 13** |
| **Motor DC Driver** | `IN1` | **GPIO 18** |
| | `IN2` | **GPIO 19** |

---

### 4️⃣ Alat 4: DIGITAL I/O STATION
| Tombol (Input) | Pin ESP32 | LED (Output) | Pin ESP32 |
| :--- | :--- | :--- | :--- |
| **Button 0** | **GPIO 32** | **LED 0** | **GPIO 23** |
| **Button 1** | **GPIO 33** | **LED 1** | **GPIO 22** |
| **Button 2** | **GPIO 25** | **LED 2** | **GPIO 21** |
| **Button 3** | **GPIO 26** | **LED 3** | **GPIO 19** |
| **Button 4** | **GPIO 27** | **LED 4** | **GPIO 18** |
| **Button 5** | **GPIO 14** | **LED 5** | **GPIO 5** |
| **Button 6** | **GPIO 12** | **LED 6** | **GPIO 17** |
| **Button 7** | **GPIO 13** | **LED 7** | **GPIO 16** |

---

## 🚀 Cara Menjalankan
1. Pasang kabel jumper sesuai tabel alat yang ingin Anda uji.
2. Buka file `.ino` yang sesuai di Arduino IDE.
3. Pilih Board: **ESP32 Dev Module** dan tentukan Port COM yang terdeteksi.
4. Klik tombol **Upload** (Tanda panah ke kanan).
5. Buka **Serial Monitor** dengan Baudrate **115200** untuk melihat log aktivitas dan diagnosa sistem.
