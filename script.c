#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "My ASUS";
const char* password = "12345678";
const char* serverName = "http://<SEU_IP>:8888";  // servidor Flask

unsigned long lastTime = 0;
unsigned long timerDelay = 30000;
float temperature;
float humidity;

void setup()
{
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.println("Connected to WiFi");
}

void loop()
{
    if ((millis() - lastTime) > timerDelay)
    {
        if (WiFi.status() == WL_CONNECTED)
        {
            HTTPClient http;

            http.begin(serverName);
            http.addHeader("Content-Type", "application/json");

            temperature = 25.0;
            humidity = 0.8;
            String jsonData = "{\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + "}";

            int httpResponseCode = http.POST(jsonData);

            if (httpResponseCode > 0)
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
        else
        {
            Serial.println("WiFi Disconnected");
        }
        lastTime = millis();
    }
}
