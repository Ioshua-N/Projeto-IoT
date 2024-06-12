#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 16     // Pino IO16 (GPIO16)
#define DHTTYPE DHT11 // Defina o tipo de sensor DHT

#define SENSOR_PIN A0 // Pino analógico onde o sensor de luz está conectado
#define LED_PIN 25    // Pino digital onde o LED está conectado

// Valores de referência para detectar luz e escuridão
#define THRESHOLD 500

DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "My ASUS";
const char* password = "12345678";
const char* serverName = "http://ioshuan.pythonanywhere.com/post_data";

void setup() {
    Serial.begin(115200);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Tentando conexão...");
    }
    Serial.println("Conectado ao Wifi");

    Serial.println("Inicializando sensor DHT...");
    dht.begin();

    // Configura o pino do sensor de luz como entrada
    pinMode(SENSOR_PIN, INPUT);

    // Configura o pino do LED como saída
    pinMode(LED_PIN, OUTPUT);

    // Inicializa o LED como apagado
    digitalWrite(LED_PIN, LOW);
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;

        http.begin(serverName);
        http.addHeader("Content-Type", "application/json");

        float temperature = dht.readTemperature();
        float humidity = dht.readHumidity();

        // Verifique se as leituras são válidas
        if (isnan(temperature) || isnan(humidity)) {
            Serial.println("Falha na leitura do sensor DHT!");
            Serial.print("Temperatura lida: "); Serial.println(temperature);
            Serial.print("Umidade lida: "); Serial.println(humidity);
        } else {
            Serial.print("Temperatura: "); Serial.println(temperature);
            Serial.print("Umidade: "); Serial.println(humidity);
        }

        // Lê o valor do sensor de luz
        int sensorValue = analogRead(SENSOR_PIN);
        Serial.print("Valor do sensor de luz: ");
        Serial.println(sensorValue);

        int lightStatus = (sensorValue > THRESHOLD) ? 1 : 0;

        // Controla o LED com base no valor do sensor de luz
        digitalWrite(LED_PIN, lightStatus == 1 ? HIGH : LOW);

        String evento = "upload de temperatura, umidade e luz";
        String origin = "WEMOS D1 R32";

        // Corrija a formatação do JSON, adicionando temperatura, umidade e valor do sensor de luz
        String json = "{\"evento\":\"" + evento + "\",\"origem\":\"" + origin + "\",\"temperature\":" + String(temperature) + ",\"humidity\":" + String(humidity) + ",\"light\":" + String(lightStatus) + "}";

        int httpResponseCode = http.POST(json);

        if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response);
        } else {
            Serial.print("Erro ao fazer requisição POST: ");
            Serial.println(httpResponseCode);
        }

        http.end();
    }

    delay(15000); // enviar a cada 10s
}
