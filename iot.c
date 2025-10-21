#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>
#include <time.h> // Para o Timestamp

// --- CONFIGURAÇÕES DO ALUNO ---
// WI-FI (Use a rede padrão do Wokwi)
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASS = "";

// MQTT (O mesmo do seu script Python)
const char* MQTT_BROKER = "18.217.188.69";
const int   MQTT_PORT = 1883;
const char* MQTT_TOPIC = "/TEF/device001/attrs/p"; 
const char* MQTT_CLIENT_ID = "esp32-vinheria-wokwi"; // ID único

// SENSORES (Baseado nas conexões acima)
#define DHT_PIN 15  // Pino D15
#define LDR_PIN 35  // Pino D35 (ADC1_CH7)

// --- MUDANÇA IMPORTANTE ---
// Mudei de DHT11 para DHT22 (AM2302)
#define DHT_TYPE DHT22
// -------------------------

DHT dht(DHT_PIN, DHT_TYPE);
// ------------------------------

// NTP (Para Timestamp - Requisito 2)
const char* NTP_SERVER = "pool.ntp.org";
const long  GMT_OFFSET_SEC = -3 * 3600; // Offset -3h (São Paulo)
const int   DAYLIGHT_OFFSET_SEC = 0;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;

// --- FUNÇÃO: SETUP WI-FI ---
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("[WIFI] Conectando em ");
    Serial.println(WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("");
    Serial.println("[WIFI] Conectado!");
    Serial.print("[WIFI] IP: ");
    Serial.println(WiFi.localIP());
}

// --- FUNÇÃO: RECONECTAR MQTT ---
void reconnect_mqtt() {
    while (!client.connected()) {
        Serial.print("[MQTT] Tentando conectar...");
        if (client.connect(MQTT_CLIENT_ID)) {
            Serial.println("Conectado!");
        } else {
            Serial.print("Falhou, rc=");
            Serial.print(client.state());
            Serial.println(" Tentando de novo em 5s");
            delay(5000);
        }
    }
}

// --- FUNÇÃO: PEGAR TIMESTAMP ---
String getTimestamp() {
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        Serial.println("[NTP] Falha ao obter hora");
        return "N/A";
    }
    // Formato: YYYY-MM-DDTHH:mm:ssZ (Padrão ISO 8601 / NGSI)
    char timeStringBuff[30];
    strftime(timeStringBuff, sizeof(timeStringBuff), "%Y-%m-%dT%H:%M:%SZ", &timeinfo);
    return String(timeStringBuff);
}


// --- SETUP ---
void setup() {
    Serial.begin(115200);
    pinMode(LDR_PIN, INPUT);
    dht.begin();
    
    setup_wifi(); // Conecta no Wi-Fi
    
    // Configura NTP (Timestamp)
    configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, NTP_SERVER);
    
    client.setServer(MQTT_BROKER, MQTT_PORT); // Configura MQTT
    
    Serial.println("[SYSTEM] Setup completo. Iniciando loop.");
}

// --- LOOP PRINCIPAL ---
void loop() {
    if (!client.connected()) {
        reconnect_mqtt(); // Se desconectar, reconecta
    }
    client.loop(); // Mantém a conexão MQTT ativa

    // Envia uma nova leitura a cada 10 segundos
    long now = millis();
    if (now - lastMsg > 10000) {
        lastMsg = now;

        // 1. Ler Sensores (Tarefa 1)
        float h = dht.readHumidity();
        float t = dht.readTemperature();
        // LDR: O módulo analógico no Wokwi dá valores de ~0 (escuro) a ~4095 (claro)
        int ldr_value_raw = analogRead(LDR_PIN);

        long ldr_percent = map(ldr_value_raw, 0, 4095, 0, 100);

        // Checa se as leituras falharam
        if (isnan(h) || isnan(t)) {
            Serial.println("Falha ao ler DHT22!");
            return;
        }

        // 2. Pegar Timestamp (Requisito 2)
        String ts = getTimestamp();

        // 3. Montar JSON (NGSI-like)
        StaticJsonDocument<256> doc;
        doc["temp"] = t;
        doc["hum"] = h;
        doc["lum"] = ldr_percent;
        doc["ts"] = ts;

        char payload[256];
        serializeJson(doc, payload); // Converte o JSON para String

        // 4. Enviar via MQTT (Requisito 1)
        Serial.print("[MQTT] Publicando mensagem: ");
        Serial.println(payload);
        client.publish(MQTT_TOPIC, payload);
    }
}