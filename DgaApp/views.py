import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from .models import Data
from threading import Thread
import os
from django.shortcuts import render
from django.http import JsonResponse
import boto3
from django.conf import settings
from .models import Data

dynamodb = boto3.resource('dynamodb', region_name=settings.AWS_REGION_NAME)
table = dynamodb.Table(settings.DYNAMODB_TABLE_NAME)


base_dir = os.path.dirname(os.path.abspath(__file__))

# Configuración de AWS IoT
CA_PATH = os.path.join(base_dir, 'certs/gustavo/AmazonRootCA1.pem')
CERT_PATH = os.path.join(base_dir, 'certs/gustavo/certificate.pem.crt')
KEY_PATH = os.path.join(base_dir, 'certs/gustavo/private.pem.key')

client = AWSIoTMQTTClient("EC2_Client")
client.configureEndpoint("a39ingai1advkv-ats.iot.us-east-1.amazonaws.com", 8883)
client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

def index(request):
    # Obtener todos los datos de la base de datos
    data = Data.objects.all().order_by('-timestamp')
    return render(request, 'index.html', {'data': data})


def messageCallback(client, userdata, message):
    # Guardar el mensaje recibido en la base de datos
    Data.objects.create(message=message.payload.decode('utf-8'))


def start_mqtt_client():
    client.connect()
    client.subscribe("Prueba", 1, messageCallback)
    while True:
        time.sleep(1)

# Ejecutar el cliente MQTT en un hilo separado para que no bloquee la aplicación
def start_mqtt():
    mqtt_thread = Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()

def get_data(request):
    # Obtener los datos de la base de datos
    data = Data.objects.all().order_by('-timestamp')
    # Convertir los datos en formato JSON
    data_list = list(data.values('timestamp', 'message'))
    return JsonResponse({'data': data_list})