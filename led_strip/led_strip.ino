#include <FastLED.h>

#define LED_PIN 33
#define LED_TYPE WS2812
#define NUM_LEDS 15
#define INPUT_1 32
#define INPUT_2 31
#define INPUT_3 30

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS);
  pinMode(INPUT_1, INPUT_PULLUP);  // Pull-up jumper
  pinMode(INPUT_2, INPUT_PULLUP);  // Pull-up jumper
  pinMode(INPUT_3, INPUT_PULLUP);  // Pull-up jumper
}

void loop() {

  if (digitalRead(INPUT_1))   // If jumper is removed
    rainbow();
  else if (digitalRead(INPUT_2))
    pastel_rainbow();
  else if (digitalRead(INPUT_3))
    brightness_scale();
  else
    fill_solid(leds, NUM_LEDS, CRGB(0, 0, 0));
  
  FastLED.show();
  delay(5);
}

void pastel_rainbow() {
  // float brightness : normalized brightness value (0 to 255)
  static uint8_t hue = 0;
  uint8_t brightness = 100;
  hue++;
  fill_gradient(leds, NUM_LEDS, CHSV(hue, 150, brightness), CHSV(hue-1, 150, brightness), LONGEST_HUES);
}

void rainbow() {
  static uint8_t hue = 0;
  uint8_t brightness = 100;
  hue++;
  fill_gradient(leds, NUM_LEDS, CHSV(hue, 255, brightness), CHSV(hue-1, 255, brightness), LONGEST_HUES);
  // uint8_t hueStep = 255 / NUM_LEDS;
  // fill_rainbow(leds, NUM_LEDS, 0, hueStep);
}

void brightness_scale() {
  fill_gradient(leds, NUM_LEDS, CHSV(0, 0, 255), CHSV(0, 0, 0));
}