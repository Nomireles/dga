from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

CA_PATH = "../certs/gustavo/AmazonRootCA1.pem"                      # Ruta al certificado raíz (CA)
CERT_PATH = "../certs/gustavo/certificate.pem.crt"                  # Ruta al certificado del dispositivo
KEY_PATH = "../certs/gustavo/private.pem.key"                       # Ruta a la clave privada

# Configurar el cliente MQTT de AWS IoT
client = AWSIoTMQTTClient("EC2_Client")
client.configureEndpoint("a39ingai1advkv-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

# Función de callback que maneja los mensajes
def messageCallback(client, userdata, message):
    print(f"Mensaje recibido en el tema {message.topic}: {message.payload.decode('utf-8')}")

# Conectar al servidor de IoT
client.connect()

# Suscribirse al tema
client.subscribe("Prueba", 1, messageCallback)

# Mantener la conexión abierta para recibir mensajes
while True:
    time.sleep(1)
