/*
  ========================================================================
  TESIoT - ALAT 4: DIGITAL I/O STATION (Pengujian 8 Tombol & 8 LED)
  ========================================================================
  Deskripsi:
  Skrip ini menguji seluruh komponen digital input dan output:
  1. 8x Push Buttons (Button 0 s/d Button 7)
  2. 8x LEDs (LED 0 s/d LED 7)

  Fitur Skrip:
  - Mode Interaktif: Tekan Button [X] -> LED [X] langsung menyala.
  - Mode Demo Otomatis: Jika tidak ada tombol ditekan selama 4 detik,
    sistem otomatis mendemokan animasi Running LED (Knight Rider)
    dan penghitung biner 8-bit pada LED 0-7.
  ========================================================================
*/

// ----------------- KONFIGURASI PIN ESP32 -----------------
// 8 Pin Tombol (Input Pull-up, ditekan = LOW)
const int buttonPins[8] = {
  32, // Button 0
  33, // Button 1
  25, // Button 2
  26, // Button 3
  27, // Button 4
  14, // Button 5
  12, // Button 6
  13  // Button 7
};

// 8 Pin LED (Output, HIGH = Menyala)
const int ledPins[8] = {
  23, // LED 0
  22, // LED 1
  21, // LED 2
  19, // LED 3
  18, // LED 4
  5,  // LED 5
  17, // LED 6
  16  // LED 7
};

// Variabel Status
unsigned long lastButtonActivity = 0;
const unsigned long DEMO_TIMEOUT = 4000; // 4 detik idle masuk ke demo
int demoAnimationStep = 0;
int chaserDirection = 1;
int currentChaserIndex = 0;
unsigned long lastDemoTick = 0;

void setAllLeds(bool state) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(ledPins[i], state ? HIGH : LOW);
  }
}

void writeBinaryToLeds(byte val) {
  for (int i = 0; i < 8; i++) {
    digitalWrite(ledPins[i], (val & (1 << i)) ? HIGH : LOW);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==============================================");
  Serial.println("  TESIoT - ALAT 4: DIGITAL I/O STATION STARTED");
  Serial.println("==============================================");

  // Inisialisasi 8 Tombol (INPUT_PULLUP)
  for (int i = 0; i < 8; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }

  // Inisialisasi 8 LED (OUTPUT)
  for (int i = 0; i < 8; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  // Tes Awal (Blink semua LED 2x)
  for (int b = 0; b < 2; b++) {
    setAllLeds(true);
    delay(200);
    setAllLeds(false);
    delay(200);
  }

  Serial.println("Inisialisasi selesai!");
  Serial.println("Tekan Button 0 s/d 7 untuk menyalakan LED pasangannya.");
  Serial.println("Jika dibiarkan 4 detik, mode demo otomatis akan aktif.\n");

  lastButtonActivity = millis();
}

void loop() {
  bool anyButtonPressed = false;

  // 1. Cek status setiap tombol
  for (int i = 0; i < 8; i++) {
    // Tombol aktif LOW karena menggunakan INPUT_PULLUP
    if (digitalRead(buttonPins[i]) == LOW) {
      anyButtonPressed = true;
      digitalWrite(ledPins[i], HIGH);
      Serial.printf("[BUTTON PRESS] Button %d ditekan -> LED %d ON\n", i, i);
    } else {
      // Jika mode manual dan tombol tidak ditekan, matikan LED pasangannya
      if (millis() - lastButtonActivity < DEMO_TIMEOUT) {
        digitalWrite(ledPins[i], LOW);
      }
    }
  }

  if (anyButtonPressed) {
    lastButtonActivity = millis();
    delay(50); // Debounce sederhana
    return;
  }

  // 2. Mode Demo Otomatis jika Idle > 4 detik
  if (millis() - lastButtonActivity >= DEMO_TIMEOUT) {
    // Animasi Running LED (Knight Rider Style) berganti setiap 80 ms
    if (millis() - lastDemoTick >= 80) {
      lastDemoTick = millis();

      // Matikan semua LED lalu nyalakan satu yang aktif
      setAllLeds(false);
      digitalWrite(ledPins[currentChaserIndex], HIGH);

      // Geser index chaser bolak-balik antara 0 dan 7
      currentChaserIndex += chaserDirection;
      if (currentChaserIndex >= 7) {
        chaserDirection = -1;
      } else if (currentChaserIndex <= 0) {
        chaserDirection = 1;
      }
    }
  }
}
