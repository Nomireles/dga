import time
import ssl
import json
import paho.mqtt.client as mqtt
import random

# Configuración del cliente MQTT
ENDPOINT = "a39ingai1advkv-ats.iot.us-east-1.amazonaws.com"         # Sustituye con tu endpoint de IoT Core
PORT = 8883
CLIENT_ID = "gustavo"       # Un identificador único para este cliente MQTT
TOPIC = "Prueba"                # El topic al que se publicarán los datos

# Rutas a los certificados y claves
CA_PATH = "../certs/gustavo/AmazonRootCA1.pem"                      # Ruta al certificado raíz (CA)
CERT_PATH = "../certs/gustavo/certificate.pem.crt"                  # Ruta al certificado del dispositivo
KEY_PATH = "../certs/gustavo/private.pem.key"                       # Ruta a la clave privada

# Función para generar datos simulados del flujómetro
def generate_flowmeter_data():
    return {
        "caudal": random.randint(1, 100),  
        "booleano": random.choice([True, False])
    }

# Callback al conectarse al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa al broker MQTT")
    else:
        print(f"Error de conexión. Código de retorno: {rc}")

# Configuración del cliente MQTT
client = client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)

client.on_connect = on_connect

# Configuración SSL/TLS
client.tls_set(ca_certs=CA_PATH,
               certfile=CERT_PATH,
               keyfile=KEY_PATH,
               cert_reqs=ssl.CERT_REQUIRED,
               tls_version=ssl.PROTOCOL_TLSv1_2,
               ciphers=None)

# Conexión al broker
print("Conectando al endpoint MQTT...")
client.connect(ENDPOINT, PORT, keepalive=60)

# Inicia el loop del cliente MQTT
client.loop_start()

# Publicar datos simulados cada 5 segundos
try:
    while True:
        data = generate_flowmeter_data()
        payload = json.dumps(data)
        print(f"Publicando datos: {payload}")
        client.publish(TOPIC, payload)
        time.sleep(5)  # Publica cada 5 segundos
except KeyboardInterrupt:
    print("Deteniendo la simulación...")
finally:
    client.loop_stop()
    client.disconnect()
