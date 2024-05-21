#include <WiFi.h>
#include "ThingSpeak.h"

const char* ssid = "My ASUS";
const char* password = "12345678";
WiFiClient client;
unsigned long myChannelNumber = 2513861;
const char * myWriteAPIKey = "6ELN470NIZ5JZ6CM";
unsigned long lastTime = 0;
unsigned long timerDelay = 30000;
float temperature;
float humidity;

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(115200);
    WiFi.mode(WIFI_STA);
    ThingSpeak.begin(client);
}

void loop()
{
    // put your main code here, to run repeatedly:
    if(WiFi.status() != WL_CONNECTED)
    {
        Serial.print("Attempting to connect");
        while(WiFi.status() != WL_CONNECTED)
        {
            WiFi.begin(ssid, password);
            delay(5000);
        }
        Serial.println("\nConnected.");
    }
    
    temperature = 25;
    Serial.print("Temperatura: ");
    Serial.println(temperature);
    humidity = 0.8;
    Serial.print("Umidade: ");
    Serial.println(humidity);
    ThingSpeak.setField(1, temperature);
    ThingSpeak.setField(2, humidity);

    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

    if(x == 200)
    {
        Serial.println("Channel update successful.");
    }
    else
    {
        Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
}