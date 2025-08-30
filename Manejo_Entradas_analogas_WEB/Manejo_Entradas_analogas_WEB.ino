
#include <DHT.h>
#include <DHT_U.h>


//            Programacion de entradas analogas.
//--------------------------------------------------------
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//Declaración de variables
int pot1 = A1; //Pot = Potenciometro
int pot2 = A2;
int fotocelda = A3;
int sensorTemp = A0; // Sensor Temperatura

//Declaración de variables almacenadoras de información
int dataPot1;
int dataPot2;
int dataFotocelda;
float dataSensorTemp;

void setup() {
  dht.begin();
  Serial.begin(9600);
  pinMode(pot1, INPUT);
  pinMode(pot2, INPUT);
  pinMode(fotocelda, INPUT);
  pinMode(sensorTemp, INPUT);

}

void loop() {
  int t = dht.readTemperature();
  int h = dht.readHumidity();
  dataPot1 = analogRead(pot1);
  dataPot2 = analogRead(pot2);
  dataFotocelda = analogRead(fotocelda);
  Serial.print(t);
  Serial.print(",");
  Serial.print(h);
  Serial.print(",");
  Serial.print(dataPot1);
  Serial.print(",");
  Serial.print(dataPot2);
  Serial.print(",");
  Serial.println(dataFotocelda);
  delay(5000);
}
