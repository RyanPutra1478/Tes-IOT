# Panduan Penggunaan 4 Skrip Trainer TESIoT (Raspberry Pi)

Repositori ini berisi 4 skrip Python untuk menguji dan mensimulasikan seluruh komponen kit **TESIoT (Trainer/Simulator System & Internet of Things)** menggunakan **Raspberry Pi** (3B, 4B, atau varian lainnya).

Komponen yang sejenis dikelompokkan 100% ke dalam satu alat yang sama tanpa ada pemisahan.

---

## 📁 Struktur File Proyek

```text
e:/Projek/TESIOT/
├── Alat1_Sensor_Station/
│   └── alat1_sensor_station.py    # Menguji 100% Sensor (DHT, MQ Gas, Ultrasonik, I2C RTC)
├── Alat2_Display_Station/
│   └── alat2_display_station.py   # Menguji 100% Layar (LCD 20x4, OLED 1.3", 7-Seg, LED Matrix)
├── Alat3_Actuator_Station/
│   └── alat3_actuator_station.py  # Menguji 100% Aktuator (Relay 1-4, Servo SG90, Motor DC L9110S)
├── Alat4_Digital_IO_Station/
│   └── alat4_digital_io_station.py# Menguji 100% I/O (8 Push Button & 8 LED)
├── requirements.txt               # Daftar paket pip yang dibutuhkan
└── README.md
```

---

## 🛠️ Instalasi Dependensi di Raspberry Pi

Jalankan perintah berikut di terminal Raspberry Pi:

```bash
# 1. Update sistem dan aktifkan antarmuka I2C & SPI
sudo apt-get update
sudo raspi-config
# (Pilih Interfacing Options -> Aktifkan I2C & SPI)

# 2. Instal paket pendukung sistem
sudo apt-get install -y python3-pip python3-dev python3-rpi.gpio libopenjp2-7 libtiff5

# 3. Instal library Python via pip
pip3 install -r requirements.txt
```

---

## 🔌 Panduan Pengkabelan (*Wiring Pinout BCM*)

### 1️⃣ Alat 1: SENSOR STATION
| Komponen di Papan | Pin Modul | Pin Raspberry Pi (BCM) | Pin Fisik Header |
| :--- | :--- | :--- | :--- |
| **Sensor Suhu DHT** | `OUT` | **GPIO 4** | Pin 7 |
| **Sensor Gas MQ** | `DO (Digital Out)` | **GPIO 17** | Pin 11 |
| **Ultrasonik HC-SR04**| `Trig` | **GPIO 27** | Pin 13 |
| | `Echo` | **GPIO 22** *(Gunakan pembagi tegangan 5V->3.3V)* | Pin 15 |
| **Modul I2C (RTC/Sensor)**| `SDA` | **GPIO 2 (SDA)** | Pin 3 |
| | `SCL` | **GPIO 3 (SCL)** | Pin 5 |
| *Power* | `VCC` & `GND` | **3.3V / 5V** & **GND** | Terminal Power Papan |

---

### 2️⃣ Alat 2: DISPLAY STATION
| Komponen di Papan | Pin Modul | Pin Raspberry Pi (BCM) | Pin Fisik Header |
| :--- | :--- | :--- | :--- |
| **LCD 20x4 I2C** (0x27) | `SDA` | **GPIO 2** (Jalur I2C bersama) | Pin 3 |
| | `SCL` | **GPIO 3** (Jalur I2C bersama) | Pin 5 |
| **OLED 1.3" I2C** (0x3C) | `SDA` | **GPIO 2** (Jalur I2C bersama) | Pin 3 |
| | `SCL` | **GPIO 3** (Jalur I2C bersama) | Pin 5 |
| **7-Segment TM1637** | `CLK` | **GPIO 23** | Pin 16 |
| | `DIO` | **GPIO 24** | Pin 18 |
| **LED Matrix MAX7219** | `DIN / MOSI` | **GPIO 10 (SPI0 MOSI)** | Pin 19 |
| | `CLK / SCLK` | **GPIO 11 (SPI0 SCLK)** | Pin 23 |
| | `CS / CE0` | **GPIO 8 (SPI0 CE0)** | Pin 24 |

---

### 3️⃣ Alat 3: ACTUATOR & POWER STATION
| Komponen di Papan | Pin Modul | Pin Raspberry Pi (BCM) | Pin Fisik Header |
| :--- | :--- | :--- | :--- |
| **4-Channel Relay** | `Relay 1` | **GPIO 5** | Pin 29 |
| | `Relay 2` | **GPIO 6** | Pin 31 |
| | `Relay 3` | **GPIO 13** | Pin 33 |
| | `Relay 4` | **GPIO 19** | Pin 35 |
| **Servo Motor SG90** | `PWM / Signal` | **GPIO 18 (PWM0)** | Pin 12 |
| **Motor DC Driver** | `IN1` | **GPIO 20** | Pin 38 |
| | `IN2` | **GPIO 21** | Pin 40 |

---

### 4️⃣ Alat 4: DIGITAL I/O STATION
| Tombol (Input) | Pin BCM (Fisik) | LED (Output) | Pin BCM (Fisik) |
| :--- | :--- | :--- | :--- |
| **Button 0** | **GPIO 14** (Pin 8) | **LED 0** | **GPIO 12** (Pin 32) |
| **Button 1** | **GPIO 15** (Pin 10) | **LED 1** | **GPIO 16** (Pin 36) |
| **Button 2** | **GPIO 18** (Pin 12) | **LED 2** | **GPIO 20** (Pin 38) |
| **Button 3** | **GPIO 23** (Pin 16) | **LED 3** | **GPIO 21** (Pin 40) |
| **Button 4** | **GPIO 24** (Pin 18) | **LED 4** | **GPIO 26** (Pin 37) |
| **Button 5** | **GPIO 25** (Pin 22) | **LED 5** | **GPIO 19** (Pin 35) |
| **Button 6** | **GPIO 8** (Pin 24) | **LED 6** | **GPIO 13** (Pin 33) |
| **Button 7** | **GPIO 7** (Pin 26) | **LED 7** | **GPIO 6** (Pin 31) |

---

## 🚀 Cara Menjalankan Skrip di Raspberry Pi

Cukup masuk ke folder masing-masing lalu jalankan dengan `python3`:

```bash
# Menjalankan Alat 1 (Sensor Station)
python3 Alat1_Sensor_Station/alat1_sensor_station.py

# Menjalankan Alat 2 (Display Station)
python3 Alat2_Display_Station/alat2_display_station.py

# Menjalankan Alat 3 (Actuator Station)
python3 Alat3_Actuator_Station/alat3_actuator_station.py

# Menjalankan Alat 4 (Digital I/O Station)
python3 Alat4_Digital_IO_Station/alat4_digital_io_station.py
```
*(Tekan `Ctrl + C` di terminal untuk menghentikan program)*
