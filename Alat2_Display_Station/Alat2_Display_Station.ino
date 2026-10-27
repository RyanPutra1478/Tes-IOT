/*
  ========================================================================
  TESIoT - ALAT 2: DISPLAY STATION (Pengujian Semua Layar/Tampilan)
  ========================================================================
  Deskripsi:
  Skrip ini menguji dan menjalankan ke-4 display yang ada pada papan trainer:
  1. LCD 20x4 I2C
  2. OLED 1.3 Inch I2C (SSD1306 / SH1106)
  3. 7-Segment Display (TM1637)
  4. LED Matrix 8x8 (MAX7219)

  Library yang dibutuhkan (Install via Arduino Library Manager):
  - LiquidCrystal I2C by Frank de Brabander
  - Adafruit SSD1306 & Adafruit GFX Library
  - TM1637 by Avishay Orpaz
  - LedControl by Eberhard Fahle
  ========================================================================
*/

#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <TM1637Display.h>
#include <LedControl.h>

// ----------------- KONFIGURASI PIN ESP32 -----------------
// 1. I2C Bus (LCD 20x4 dan OLED berbagi jalur SDA & SCL)
#define I2C_SDA         21
#define I2C_SCL         22

// Inisialisasi LCD 20x4 (Alamat standar 0x27, 20 kolom, 4 baris)
LiquidCrystal_I2C lcd(0x27, 20, 4);

// Inisialisasi OLED 1.3" (Resolusi 128x64, alamat standar 0x3C)
#define SCREEN_WIDTH    128
#define SCREEN_HEIGHT   64
#define OLED_RESET      -1
Adafruit_SSD1306 oled(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// 2. 7-Segment Display (TM1637)
#define TM_CLK          19
#define TM_DIO          18
TM1637Display tm(TM_CLK, TM_DIO);

// 3. LED Matrix 8x8 (MAX7219)
#define MATRIX_DIN      23
#define MATRIX_CLK      14
#define MATRIX_CS       5
// LedControl(DIN, CLK, CS, jumlah_modul)
LedControl lc = LedControl(MATRIX_DIN, MATRIX_CLK, MATRIX_CS, 1);

// Pola Gambar Wajah Senyum untuk LED Matrix 8x8
const byte smileFace[8] = {
  B00111100,
  B01000010,
  B10100101,
  B10000001,
  B10100101,
  B10011001,
  B01000010,
  B00111100
};

// Pola Gambar Hati untuk LED Matrix 8x8
const byte heart[8] = {
  B00000000,
  B01100110,
  B11111111,
  B11111111,
  B01111110,
  B00111100,
  B00011000,
  B00000000
};

// Variabel Waktu
unsigned long lastUpdate = 0;
int counter = 0;
bool toggleIcon = false;

void drawMatrix(const byte pattern[8]) {
  for (int row = 0; row < 8; row++) {
    lc.setRow(0, row, pattern[row]);
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==============================================");
  Serial.println("  TESIoT - ALAT 2: DISPLAY STATION STARTED   ");
  Serial.println("==============================================");

  // Inisialisasi I2C Bus
  Wire.begin(I2C_SDA, I2C_SCL);

  // 1. Inisialisasi LCD 20x4
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(2, 0);
  lcd.print("TESIoT SIMULATOR");
  lcd.setCursor(0, 1);
  lcd.print("====================");
  lcd.setCursor(1, 2);
  lcd.print("DISPLAY TEST STATION");
  lcd.setCursor(0, 3);
  lcd.print("Counter: 0 s");

  // 2. Inisialisasi OLED
  if (!oled.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("[OLED] Gagal menginisialisasi SSD1306 pada alamat 0x3C");
  } else {
    oled.clearDisplay();
    oled.setTextSize(1);
    oled.setTextColor(SSD1306_WHITE);
    oled.setCursor(15, 10);
    oled.println("OLED 1.3 INCH");
    oled.setCursor(15, 25);
    oled.println("Status: ACTIVE OK");
    oled.drawRect(5, 5, 118, 54, SSD1306_WHITE);
    oled.display();
  }

  // 3. Inisialisasi 7-Segment (TM1637)
  tm.setBrightness(0x0f); // Brightness maksimum
  tm.showNumberDec(0, true);

  // 4. Inisialisasi LED Matrix (MAX7219)
  lc.shutdown(0, false);   // Bangunkan MAX7219 dari power saving
  lc.setIntensity(0, 8);   // Kecerahan level sedang (0-15)
  lc.clearDisplay(0);
  drawMatrix(smileFace);

  Serial.println("Semua 4 modul display berhasil diinisialisasi!\n");
}

void loop() {
  if (millis() - lastUpdate >= 1000) {
    lastUpdate = millis();
    counter++;

    // 1. Update LCD 20x4 (Update baris ke-4)
    lcd.setCursor(9, 3);
    lcd.printf("%4d s", counter);

    // 2. Update 7-Segment (Hitung angka maju 0000 - 9999)
    tm.showNumberDec(counter % 10000, true);

    // 3. Update OLED (Animasi progress bar & teks berganti)
    oled.clearDisplay();
    oled.drawRect(2, 2, 124, 60, SSD1306_WHITE);
    oled.setCursor(15, 10);
    oled.setTextSize(1);
    oled.println("TESIoT DISPLAY DEMO");
    oled.setCursor(15, 24);
    oled.printf("Uptime : %d detik", counter);

    // Progress bar bergerak
    int progressWidth = (counter % 10) * 10;
    oled.drawRect(15, 40, 98, 12, SSD1306_WHITE);
    oled.fillRect(17, 42, progressWidth, 8, SSD1306_WHITE);
    oled.display();

    // 4. Update LED Matrix (Berganti icon senyum <-> hati setiap 2 detik)
    if (counter % 2 == 0) {
      toggleIcon = !toggleIcon;
      if (toggleIcon) {
        drawMatrix(heart);
      } else {
        drawMatrix(smileFace);
      }
    }

    Serial.printf("[DISPLAY UPDATE] Uptime: %d detik | 7-Seg: %04d\n", counter, counter % 10000);
  }
}
