# 🍷 Vinheria Agnello IoT Monitor: Adega Inteligente 🌡️💧💡

<p align="center">
  <img src="https://i.imgur.com/your-image-url.png" alt="Montagem do Projeto IoT Vinheria Agnello" width="700"/>
</p>

**Tagline:** _Monitoramento em tempo real de temperatura, umidade e luz para garantir a qualidade perfeita dos seus vinhos._

---

<p align="center">
  <img src="https://img.shields.io/badge/ESP32-purple?style=for-the-badge&logo=espressif" alt="Hardware ESP32">
  <img src="https://img.shields.io/badge/MQTT-red?style=for-the-badge&logo=mqtt" alt="Protocolo MQTT">
  <img src="https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python" alt="Backend Python">
  <img src="https://img.shields.io/badge/Flask-black?style=for-the-badge&logo=flask" alt="Framework Flask">
  <img src="https://img.shields.io/badge/Wokwi-cyan?style=for-the-badge" alt="Simulado no Wokwi">
</p>

---

## 📖 Sobre o Projeto

O **Vinheria Agnello IoT Monitor** é um sistema inteligente projetado para monitorar as condições ambientais cruciais dentro de uma adega de vinhos. Utilizando um microcontrolador **ESP32** conectado a sensores de **temperatura e umidade (DHT11/DHT22)** e **luminosidade (LDR)**, o sistema coleta dados vitais em tempo real.

**Por que isso é importante?** A qualidade e o envelhecimento do vinho são extremamente sensíveis a variações de temperatura, umidade e exposição à luz. Manter essas condições estáveis é essencial para preservar o sabor, o aroma e as propriedades da bebida.

**Como funciona?**

1.  O **ESP32** lê os dados dos sensores.
2.  Conecta-se à rede **Wi-Fi** local.
3.  Envia os dados (com timestamp) para um servidor central (Broker MQTT) usando o protocolo leve **MQTT**.
4.  Um **aplicativo backend em Python** (usando Flask e Paho-MQTT) "escuta" essas mensagens do Broker MQTT.
5.  O backend processa os dados e os envia em tempo real para um **dashboard web**, permitindo a visualização fácil e imediata das condições da adega.

Este projeto foi desenvolvido como parte das atividades acadêmicas na **FIAP**, demonstrando a aplicação prática de conceitos de Internet das Coisas (IoT), comunicação de rede, desenvolvimento de hardware embarcado (ESP32/Arduino) e backend (Python/Flask).

---

## ✨ Funcionalidades Principais

- 🌡️ **Leitura de Temperatura e Umidade:** Utiliza o sensor DHT11 ou DHT22 para medições precisas.
- 💡 **Leitura de Luminosidade:** Usa um sensor LDR para monitorar a intensidade da luz.
- 📶 **Conectividade Wi-Fi:** O ESP32 conecta-se à rede local para enviar os dados.
- 📡 **Comunicação MQTT:** Envio eficiente dos dados dos sensores para um broker MQTT central.
- 🕒 **Timestamping:** Cada leitura de sensor inclui data e hora exatas.
- 🐍 **Backend Python/Flask:** Recebe os dados via MQTT, processa e disponibiliza para o frontend.
- 📊 **Dashboard Web em Tempo Real:** Interface simples (criada com Flask e Socket.IO) que exibe os dados dos sensores instantaneamente no navegador.
- ✨ **Conversão para Porcentagem:** A luminosidade é convertida e exibida em um formato intuitivo de porcentagem (0-100%).

---

## 📸 Telas (Exemplos)

- **Montagem no Wokwi:** Visualização da conexão dos componentes na simulação.
  <img src="https://i.imgur.com/your-wokwi-image.png" alt="Simulação do Projeto no Wokwi" width="700"/>
- **Dashboard Web:** Como os dados são exibidos no navegador.
  <img src="https://i.imgur.com/your-dashboard-image.png" alt="Dashboard Web com dados dos sensores" width="700"/>

> **Nota:** Substitua as URLs de exemplo (`https://i.imgur.com/...`) pelos links das suas próprias imagens.

---

## 🛠️ Tecnologias Utilizadas

| Categoria       | Tecnologia                                                                                                                                                                                                                                                                                                                    | Descrição                                                            |
| :-------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- |
| **Hardware**    | <img src="https://img.shields.io/badge/ESP32-purple?logo=espressif" alt="ESP32"> <img src="https://img.shields.io/badge/DHT22-blue" alt="DHT Sensor"> <img src="https://img.shields.io/badge/LDR-orange" alt="LDR Sensor">                                                                                                    | Microcontrolador com Wi-Fi e sensores de ambiente.                   |
| **Firmware**    | <img src="https://img.shields.io/badge/Arduino%20C++-00979D?logo=arduino" alt="Arduino C++">                                                                                                                                                                                                                                  | Código embarcado no ESP32 para leitura e envio de dados.             |
| **Comunicação** | <img src="https://img.shields.io/badge/MQTT-red?logo=mqtt" alt="MQTT"> <img src="https://img.shields.io/badge/Wi--Fi-blue" alt="Wi-Fi">                                                                                                                                                                                       | Protocolo para envio de dados IoT e conexão de rede sem fio.         |
| **Backend**     | <img src="https://img.shields.io/badge/Python-blue?logo=python" alt="Python"> <img src="https://img.shields.io/badge/Flask-black?logo=flask" alt="Flask"> <img src="https://img.shields.io/badge/Socket.IO-grey?logo=socketdotio" alt="Socket.IO"> <img src="https://img.shields.io/badge/Paho--MQTT-yellow" alt="Paho-MQTT"> | Recebe dados via MQTT e os serve para o dashboard web em tempo real. |
| **Simulação**   | <img src="https://img.shields.io/badge/Wokwi-cyan" alt="Wokwi">                                                                                                                                                                                                                                                               | Plataforma online para simular o circuito e o código do ESP32.       |

---

## 🏗️ Arquitetura Simplificada

O fluxo de dados no sistema é o seguinte:

1.  **Sensores (DHT & LDR)** capturam os dados do ambiente.
2.  O **ESP32** lê os sensores, adiciona um timestamp e publica os dados via **MQTT**.
3.  O **Broker MQTT** (um servidor na nuvem, como HiveMQ ou Mosquitto) recebe os dados.
4.  O **Backend Python (Flask)**, que está inscrito no tópico MQTT, recebe os dados do broker.
5.  O Backend envia os dados via **Socket.IO** para o navegador do usuário.
6.  O **Dashboard Web** (HTML/JavaScript no navegador) exibe os dados em tempo real.

```mermaid
graph LR;
    Sensores[🌡️💧💡 Sensores DHT/LDR] -->|Leitura| ESP32[💻 ESP32];
    ESP32 -->|Wi-Fi| BrokerMQTT[☁️ Broker MQTT];
    BrokerMQTT -->|Subscrição| Backend[🐍 Backend Python/Flask];
    Backend -->|Socket.IO| Dashboard[📊 Dashboard Web];
    Dashboard -->|Visualização| Usuario[👩‍💻 Usuário];

    style Sensores fill:#f9f,stroke:#333,stroke-width:2px;
    style ESP32 fill:#ccf,stroke:#333,stroke-width:2px;
    style BrokerMQTT fill:#fcf,stroke:#333,stroke-width:2px;
    style Backend fill:#ff9,stroke:#333,stroke-width:2px;
    style Dashboard fill:#9cf,stroke:#333,stroke-width:2px;
🚀 Como Rodar o Projeto (Localmente ou no Wokwi)
Siga estas etapas para testar o projeto.

Pré-requisitos
Para o ESP32 (Hardware Real ou Wokwi):

Hardware: ESP32 Dev Kit, Sensor DHT11 ou DHT22, Módulo LDR, jumpers, protoboard.

Software (Real): IDE do Arduino instalada com o suporte para ESP32.

Bibliotecas Arduino: PubSubClient, DHT sensor library (Adafruit), ArduinoJson.

Conta Wokwi (Simulação): Gratuita em wokwi.com.

Para o Backend (Python):

Python: Instalado na sua máquina (versão 3.7+ recomendada). Baixe em python.org.

pip: Gerenciador de pacotes do Python (geralmente vem junto).

Opção 1: Simulação com Wokwi (Mais Fácil)
Abra o Wokwi: Crie um novo projeto ESP32.

Adicione Componentes: Adicione um DHT22 e um LDR Module ao diagrama.

Faça as Conexões: Siga o esquema de ligação:

ESP32 3V3 -> Linha + da protoboard

ESP32 GND -> Linha - da protoboard

DHT22 VCC -> Linha +

DHT22 GND -> Linha -

DHT22 Data -> ESP32 D15

LDR Module VCC -> Linha +

LDR Module GND -> Linha -

LDR Module AO -> ESP32 D35

Adicione os Arquivos de Configuração:

Crie libraries.txt e cole:

PubSubClient
Adafruit Unified Sensor
DHT sensor library
ArduinoJson
Crie wokwi.toml e cole:

Ini, TOML

[wokwi]
version = 1
firmware = ".pio/build/esp32dev/firmware.bin" # Ou o caminho padrão do Wokwi

[conn]
type = "wifi"
ssid = "Wokwi-GUEST"
password = ""
Cole o Código ESP32: Copie o código sketch.ino fornecido anteriormente (o que usa Wokwi-GUEST e DHT22) para o editor do Wokwi. Certifique-se que MQTT_BROKER e MQTT_TOPIC estão corretos!

Execute o Backend Python (Veja abaixo).

Inicie a Simulação: Clique no botão ▶️ (Play) no Wokwi. Verifique o console serial para mensagens de conexão Wi-Fi e MQTT.

Opção 2: Hardware Real
Monte o Circuito: Conecte o ESP32, DHT11/22 e LDR na protoboard conforme o diagrama.

Abra a IDE Arduino: Cole o código C++ do ESP32 fornecido anteriormente.

Configure: MUITO IMPORTANTE: Altere as variáveis WIFI_SSID, WIFI_PASS, MQTT_BROKER e MQTT_TOPIC no código para corresponderem à sua rede Wi-Fi e ao broker/tópico que o backend Python usará. Se estiver usando DHT11, mude #define DHT_TYPE DHT22 para DHT11.

Instale as Bibliotecas: Use o Gerenciador de Bibliotecas da IDE para instalar PubSubClient, DHT sensor library e ArduinoJson.

Compile e Grave: Conecte o ESP32 ao computador, selecione a placa e a porta corretas na IDE e clique em "Carregar".

Abra o Monitor Serial: Verifique se ele conecta ao Wi-Fi e ao MQTT.

Execute o Backend Python (Veja abaixo).

Executando o Backend Python (Comum para Opção 1 e 2)
Clone o Repositório (se ainda não fez):

Bash

git clone URL_DO_SEU_REPOSITORIO # Se aplicável
cd NOME_DA_PASTA_DO_PROJETO/backend # Ou onde estiver seu script Python
(Recomendado) Crie um Ambiente Virtual:

Bash

python -m venv .venv
# Ativação Windows (Git Bash/PowerShell):
source .venv/Scripts/activate
# Ativação Linux/macOS:
# source .venv/bin/activate
Instale as Dependências Python:

Bash

pip install Flask Flask-SocketIO paho-mqtt
Verifique o Script Python: Abra o script (listener.py ou similar) e confirme que MQTT_BROKER e MQTT_TOPIC são exatamente os mesmos que você configurou no código do ESP32.

Execute o Script:

Bash

python listener.py
O terminal deve indicar que está conectado ao MQTT e aguardando mensagens.

Acessando o Dashboard
Com o script Python rodando, abra seu navegador web.

Acesse o endereço http://127.0.0.1:5000 (ou o endereço que aparece no terminal do Python, como http://0.0.0.0:5000/).

Você deverá ver o dashboard com os valores de Temperatura, Umidade e Luminosidade (%) sendo atualizados a cada ~10 segundos.

📡 Tópico MQTT Principal
fiap/vinheria/dados (ou o tópico que você definiu): O ESP32 publica as leituras dos sensores neste tópico em formato JSON. O Backend Python subscreve a este tópico para receber os dados.

Exemplo de Payload JSON enviado pelo ESP32:

JSON

{"temp": 22.5, "hum": 55.1, "lum": 75, "ts": "2025-10-21T19:30:00Z"}
⚠️ Solução de Problemas Comuns
ESP32 não conecta ao Wi-Fi: Verifique se WIFI_SSID e WIFI_PASS no código do ESP32 estão corretos. Verifique se o ESP32 está ao alcance do roteador.

ESP32 não conecta ao MQTT / Backend Python não conecta (TimeoutError):

Confirme que MQTT_BROKER (IP ou hostname) e MQTT_PORT (geralmente 1883) estão idênticos no ESP32 e no Python.

Verifique se o Broker MQTT está online (tente conectar com um cliente MQTT de teste como MQTT Explorer).

Seu firewall (Windows ou da rede) pode estar bloqueando a porta 1883. Tente desativar temporariamente para testar.

Backend Python não recebe mensagens:

Confirme que MQTT_TOPIC é exatamente o mesmo no ESP32 (onde publica) e no Python (onde subscreve). Atenção a maiúsculas/minúsculas e barras (/).

Verifique se o ESP32 está realmente enviando mensagens (olhe o Monitor Serial do Arduino ou o console do Wokwi).

Dashboard não atualiza:

Verifique se o Backend Python está recebendo mensagens MQTT (olhe o terminal do Python).

Verifique o console do navegador (F12) por erros de JavaScript ou de conexão Socket.IO.

Luminosidade não aparece em %: Certifique-se de que o código do ESP32 inclui a linha com ldr_percent = map(ldr_value_raw, 0, 4095, 0, 100); e que o JSON enviado contém "lum": ldr_percent.

👨‍💻 Desenvolvedor / Contato
Gabriel Akira Borges Kiyohara — FIAP (1ESPJ)

Contato: gakirakiyohara@gmail.com

GitHub: Gakira06 (adicione seu link se quiser)

📄 Licença
Este projeto foi desenvolvido para fins acadêmicos. Uso e modificação são permitidos dentro deste contexto. Distribuição ou uso comercial não autorizado é proibido. © 2025 Gabriel Akira Borges Kiyohara.
```
