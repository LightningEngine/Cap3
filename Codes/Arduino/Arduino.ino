#include <DHT.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

#define DHT22_pin 4
DHT dht(DHT22_pin, DHT22);

#define BMP280_I2C_ADDRESS  0x76
Adafruit_BMP280 bmp280;

int temp;
int hum;

int ledPin_ho = 3;
int ledPin_po = 2;
int ledPin_hi = 6;
int ledPin_pi = 5;
int buzz = 7;

void setup(){
  Serial.begin(9600);
  dht.begin();
  if (!bmp280.begin(BMP280_I2C_ADDRESS))
  {  
    Serial.println("Could not find a valid BMP280 sensor, check wiring!");
    while (1);
  }
  pinMode(ledPin_ho, OUTPUT);
  pinMode(ledPin_po, OUTPUT);
  pinMode(ledPin_hi, OUTPUT);
  pinMode(ledPin_pi, OUTPUT);
  pinMode(buzz, OUTPUT);

}

char text[14]; 

void loop(){
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  float press = (bmp280.readPressure()/101325);

  if (isnan(hum) || isnan(temp) ) {
    Serial.println("DHT not ready!");
    return;
  }

  if(hum<90){
    digitalWrite(ledPin_ho, HIGH);
    digitalWrite(ledPin_hi, LOW);
  }
  else{
    digitalWrite(ledPin_ho, LOW);
    digitalWrite(ledPin_hi, HIGH);
  }
  if(press>0.933){
    digitalWrite(ledPin_po, HIGH);
    digitalWrite(ledPin_pi, LOW);
  }
  else{
    digitalWrite(ledPin_po, LOW);
    digitalWrite(ledPin_pi, HIGH);
  }
  if(temp>4){
    tone(buzz, 200, 250);
  }

  Serial.print(temp, 1);
  Serial.print("x");
  Serial.print(hum, 2);
  Serial.print("x");
  Serial.println(press, 4);
  delay(2000);

}
