import dht
from machine import Pin
import time

# Configuração do sensor DHT22 no pino 12
dht_sensor = dht.DHT22(Pin(12))

while True:
    try:
        # Inicia a leitura dos dados do sensor
        dht_sensor.measure()
        
        # Captura os valores de temperatura e umidade
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        
        # Exibe os valores no console
        print("Temperatura:", temperature, "°C")
        print("Umidade:", humidity, "%")
        
    except OSError as e:
        print("Erro ao ler o sensor DHT22:", e)
    
    # Aguarda 5 segundos antes de ler novamente
    time.sleep(5)
