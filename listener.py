from flask import Flask, render_template_string
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import json
import time

# ==== MQTT ====
# O MESMO broker do seu script original
MQTT_BROKER = "18.217.188.69"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
# TÓPICO: Mudei para um tópico mais claro.
# O SEU ESP32 DEVE PUBLICAR NESTE MESMO TÓPICO!
MQTT_TOPIC = "/TEF/device001/attrs/p"

# ==== Flask / SocketIO ====
app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading", cors_allowed_origins="*")

ultimo_valor = {}

# ---- Callbacks MQTT (API V1) ----
def on_connect(client, userdata, flags, rc):
    print("[MQTT] Conectado. rc =", rc)
    # Subscreve ao tópico do projeto
    client.subscribe(MQTT_TOPIC)
    print(f"[MQTT] Subscribed: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    global ultimo_valor
    raw = msg.payload  # bytes
    print(f"[MQTT] Mensagem recebida: {raw}")

    try:
        # Decodifica a mensagem (esperamos um JSON)
        decoded = raw.decode("utf-8", errors="replace").strip()
        
        # Tenta carregar o JSON
        # Esperamos algo como: {"temp": 25.5, "hum": 60.1, "lum": 850, "ts": "..."}
        ultimo_valor = json.loads(decoded)

        # Envia os dados completos para o front-end via SocketIO
        socketio.emit("novo_dado", {"valor": ultimo_valor})
        print(f"[MQTT] Dados processados: {ultimo_valor}")

    except json.JSONDecodeError:
        print(f"[MQTT] Erro: A mensagem não era um JSON válido. Payload: {raw}")
    except Exception as e:
        print(f"[MQTT] Erro ao processar payload: {e}")

# ---- Configura cliente MQTT ----
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
client.loop_start()

# ---- Página Web (HTML/JS) ----
@app.route("/")
def index():
    # Este HTML foi modificado. Removemos o gauge e colocamos 3 spans
    # para mostrar os 3 valores + o timestamp.
    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Dashboard Vinheria Agnello</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
    <style>
        body { background-color: #f4f4f4; }
        .container { max-width: 800px; }
        .card { margin-top: 20px; }
        .card-title { font-weight: bold; }
        .valor-sensor {
            font-size: 3.5rem;
            font-weight: 300;
            line-height: 1.2;
        }
        #timestamp { font-size: 0.9rem; color: #6c757d; text-align: center; margin-top: 15px;}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mt-5 text-center">Dashboard - Vinheria Agnello</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">🌡️ Temperatura</h5>
                        <p class="valor-sensor">
                            <span id="val-temp">--</span> °C
                        </p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">💧 Umidade</h5>
                        <p class="valor-sensor">
                            <span id="val-hum">--</span> %
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">💡 Luminosidade</h5>
                        <p class="valor-sensor">
                            <span id="val-lum">--</span> % 
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="timestamp">
            Última leitura: <span id="val-ts">Aguardando dados...</span>
        </div>
    </div>

    <script>
        $(function() {
            const socket = io({ transports: ['websocket', 'polling'] });
            
            socket.on('novo_dado', (data) => {
                let dados = data.valor;

                // Verificamos se os dados existem antes de tentar acessá-los
                if (dados) {
                    // Atualiza os valores nos spans
                    $('#val-temp').text(dados.temp !== undefined ? dados.temp : '--');
                    $('#val-hum').text(dados.hum !== undefined ? dados.hum : '--');
                    $('#val-lum').text(dados.lum !== undefined ? dados.lum : '--');
                    $('#val-ts').text(dados.ts !== undefined ? dados.ts : '...');
                }
            });
        });
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    # host='0.0.0.0' permite acessar de outra máquina na mesma rede
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)