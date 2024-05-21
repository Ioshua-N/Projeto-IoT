#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "My ASUS";
const char* password = "12345678";
const char* serverName = "http://yourusername.pythonanywhere.com/";

void setup()
{
    Serial.begin(115200);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Tentando conexão...");
    }

    Serial.println("Conectado ao Wifi");
}

void loop()
{
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

    delay(10000); // enviar a cada 10s
}