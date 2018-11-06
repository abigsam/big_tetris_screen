/*
 * GreenPAK SLG46855V
 * Arduino UNO I2C pins is:
 * SDA --> A4
 * SCL --> A5
*/


#include <Arduino.h>
#include <Wire.h>

#define GREENPAK_ADDR     (0x08)
#define CNT2_REG_ADDR     (0x9a) //Red
#define CNT3_REG_ADDR     (0x9c) //Green
#define CNT4_REG_ADDR     (0x9e) //Blue

#define DEBUG_ON          (1)

/* Variables */
uint8_t red = 0u, green = 0u, blue = 0u;
uint8_t is_count_up = 1u;

/* Prototypes */
void send_byte_gpak(uint8_t byte_addr, uint8_t byte_data);
void send_rgb(uint8_t red_pwm, uint8_t green_pwm, uint8_t blue_pwm);

void setup() {
  // put your setup code here, to run once:
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  send_rgb(red, green, blue);
  delay(100);
  
  if (is_count_up) {
    red += 17u;
    if (255u == red) {
      red = 0u;
      green += 17u;
      if (255u == green) {
        green = 0u;
        blue += 17u;
        if (255u == blue) {
          blue = 0u;
        }
      }
    }
  }
  else {
    red -= 17u;
    if (0u == red) {
      red = 255u;
      green -= 17u;
      if (0u == green) {
        green = 255u;
        blue -= 17u;
        if (0u == blue) {
          blue = 255u;
        }
      }
    }
  }

  if (is_count_up && 0u == red && 0u == green && 0u == blue) {
    is_count_up = 0u;
    red = 255u;
    green = 255u;
    blue = 255u;
  }

  if (!is_count_up && 255u == red && 255u == green && 255u == blue) {
    is_count_up = 1u;
    red = 0u;
    green = 0u;
    blue = 0u;
  }

}

/**
 * @brief 
 * 
 * @param red_pwm 
 * @param green_pwm 
 * @param blue_pwm 
 */
void send_rgb(uint8_t red_pwm, uint8_t green_pwm, uint8_t blue_pwm)
{
  send_byte_gpak(CNT2_REG_ADDR, red_pwm);   //Send Red
  if (DEBUG_ON) { Serial.println("Set red to %d", red_pwm); }
  send_byte_gpak(CNT3_REG_ADDR, green_pwm); //Send Green
  if (DEBUG_ON) { Serial.println("Set green to %d", green_pwm); }
  send_byte_gpak(CNT4_REG_ADDR, blue_pwm);  //Send Blue
  if (DEBUG_ON) { Serial.println("Set blue to %d", blue_pwm); }
}

/**
 * @brief 
 * 
 * @param byte_addr 
 * @param byte_data 
 */
void send_byte_gpak(uint8_t byte_addr, uint8_t byte_data)
{
  Wire.beginTransmission(GREENPAK_ADDR);
  Wire.write(byte_addr);
  Wire.write(byte_data);
  Wire.endTransmission();
}