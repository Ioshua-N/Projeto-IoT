#include <WiFi.h>
#include "ThingSpeak.h"

const char* ssid = "My ASUS";
const char* password = "12345678";
<<<<<<< Updated upstream
WiFiClient client;
unsigned long myChannelNumber = 2513861;
const char * myWriteAPIKey = "6ELN470NIZ5JZ6CM";
unsigned long lastTime = 0;
unsigned long timerDelay = 30000;
float temperatureC;
float umidade;
=======
const char* serverName = "http://yourusername.pythonanywhere.com/";
>>>>>>> Stashed changes

void setup()
{
    // put your setup code here, to run once:
    Serial.begin(115200);
<<<<<<< Updated upstream
    WiFi.mode(WIFI_STA);
    ThingSpeak.begin(client);
=======

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Tentando conexão...");
    }

    Serial.println("Conectado ao Wifi");
>>>>>>> Stashed changes
}

void loop()
{
<<<<<<< Updated upstream
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
    
    temperatureC = 25;
    Serial.print("Temperatura: ");
    Serial.println(temperatureC);
    umidade = 0.8;
    Serial.print("Umidade: ");
    Serial.println(umidade);
    ThingSpeak.setField(1, temperatureC);
    ThingSpeak.setField(2, umidade);

    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);

    if(x == 200)
    {
        Serial.println("Channel update successful.");
    }
    else
    {
        Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
=======
    if (WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;

        http.begin(serverName);
        http.addHeader("Content-Type", "application/json");

        float temperature = 25.0; // pegar do sensor
        float humidity = 60.0; // pegar do sensor

        String json = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";

        int httpResponseCode = http.POST(jsonPayload);

        if(httpResponseCode > 0)
        {
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response);
        }
        else
        {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }

        http.end();
    }

    delay(1000); // enviar a cada 10s
>>>>>>> Stashed changes
}