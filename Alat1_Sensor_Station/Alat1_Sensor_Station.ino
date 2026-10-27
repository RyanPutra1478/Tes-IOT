/*
  ========================================================================
  TESIoT - ALAT 1: SENSOR STATION (Pengujian Semua Sensor)
  ========================================================================
  Deskripsi:
  Skrip ini menguji dan memvalidasi ke-4 sensor yang ada pada papan trainer:
  1. Sensor Suhu & Kelembaban (DHT11/DHT22)
  2. Sensor Gas (MQ Series - Analog/ADC)
  3. Sensor Ultrasonik HC-SR04 (Jarak)
  4. Sensor I2C (RTC DS3231 / Scan Alamat I2C)

  Library yang dibutuhkan (Install via Arduino Library Manager):
  - DHT sensor library by Adafruit
  - Adafruit Unified Sensor
  - RTClib by Adafruit (jika memakai RTC DS3231)
  ========================================================================
*/

#include <Wire.h>
#include <DHT.h>
#include <RTClib.h>

// ----------------- KONFIGURASI PIN ESP32 -----------------
// 1. Sensor DHT
#define DHTPIN        4       // Pin OUT DHT ke GPIO 4
#define DHTTYPE       DHT11   // Ubah ke DHT22 jika menggunakan DHT22
DHT dht(DHTPIN, DHTTYPE);

// 2. Sensor Gas MQ
#define MQ_PIN        34      // Pin Analog MQ ke GPIO 34 (ADC1)

// 3. Sensor Ultrasonik HC-SR04
#define TRIG_PIN      5       // Pin Trig ke GPIO 5
#define ECHO_PIN      18      // Pin Echo ke GPIO 18

// 4. I2C Bus (RTC DS3231 / Sensor I2C)
#define I2C_SDA       21      // Pin SDA ke GPIO 21
#define I2C_SCL       22      // Pin SCL ke GPIO 22
RTC_DS3231 rtc;
bool rtcFound = false;

// Variabel Waktu
unsigned long lastReadTime = 0;
const unsigned long READ_INTERVAL = 1500; // Baca setiap 1.5 detik

// ----------------- FUNGSI BACA JARAK ULTRASONIK -----------------
float readDistanceCM() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Baca durasi pulsa pantulan (timeout 30ms ~ max 5 meter)
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) {
    return -1.0; // Diluar jangkauan / timeout
  }
  // Rumus: Kecepatan suara 0.034 cm/us, jarak = (durasi * 0.034) / 2
  return (duration * 0.0343) / 2.0;
}

// ----------------- FUNGSI I2C SCANNER -----------------
void scanI2C() {
  Serial.println("[I2C SCAN] Memindai perangkat I2C pada bus...");
  byte count = 0;
  for (byte i = 8; i < 120; i++) {
    Wire.beginTransmission(i);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  -> Ditemukan perangkat I2C di alamat: 0x%02X\n", i);
      count++;
    }
  }
  if (count == 0) {
    Serial.println("  -> Peringatan: Tidak ada perangkat I2C yang terdeteksi!");
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==============================================");
  Serial.println("  TESIoT - ALAT 1: SENSOR STATION STARTED     ");
  Serial.println("==============================================");

  // Inisialisasi I2C
  Wire.begin(I2C_SDA, I2C_SCL);
  scanI2C();

  // Inisialisasi DHT
  dht.begin();
  Serial.println("[DHT] Sensor suhu & kelembaban diinisialisasi.");

  // Inisialisasi Pin Ultrasonik
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
  Serial.println("[HC-SR04] Sensor ultrasonik diinisialisasi.");

  // Inisialisasi Sensor Gas MQ
  pinMode(MQ_PIN, INPUT);
  Serial.println("[MQ GAS] Sensor gas analog diinisialisasi pada GPIO 34.");

  // Cek RTC
  if (rtc.begin()) {
    rtcFound = true;
    Serial.println("[RTC] Modul RTC DS3231 berhasil terhubung!");
    if (rtc.lostPower()) {
      Serial.println("[RTC] Baterai RTC baru/habis, menyetel waktu ke waktu compile...");
      rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }
  } else {
    Serial.println("[RTC] Catatan: Modul RTC DS3231 tidak merespon (dapat dilewati jika modul lain).");
  }

  Serial.println("==============================================");
  Serial.println("Memulai pembacaan sensor berkala...\n");
}

void loop() {
  if (millis() - lastReadTime >= READ_INTERVAL) {
    lastReadTime = millis();

    // 1. Baca Sensor Suhu & Kelembaban (DHT)
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    // 2. Baca Sensor Gas (MQ)
    int gasRaw = analogRead(MQ_PIN);
    float gasVoltage = (gasRaw / 4095.0) * 3.3;

    // 3. Baca Sensor Ultrasonik
    float distance = readDistanceCM();

    // 4. Output Hasil ke Serial Monitor
    Serial.println("----------------------------------------------");
    
    // Tampilkan Waktu RTC jika ada
    if (rtcFound) {
      DateTime now = rtc.now();
      Serial.printf("[WAKTU RTC] %02d/%02d/%04d %02d:%02d:%02d\n",
                    now.day(), now.month(), now.year(),
                    now.hour(), now.minute(), now.second());
    }

    // Output DHT
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("[DHT] Gagal membaca data dari sensor DHT! Periksa kabel OUT.");
    } else {
      Serial.printf("[DHT] Suhu: %.1f °C | Kelembaban: %.1f %%\n", temperature, humidity);
    }

    // Output Gas MQ
    Serial.printf("[MQ GAS] Nilai ADC: %d / 4095 (Tegangan: %.2f V) -> Status: %s\n",
                  gasRaw, gasVoltage, (gasRaw > 1800) ? "BAHAYA / TERDETEKSI ASAP/GAS!" : "NORMAL");

    // Output Jarak Ultrasonik
    if (distance < 0) {
      Serial.println("[ULTRASONIK] Objek diluar jangkauan (> 400 cm) atau sensor terhalang.");
    } else {
      Serial.printf("[ULTRASONIK] Jarak Objek: %.1f cm\n", distance);
    }

    Serial.println("----------------------------------------------\n");
  }
}
