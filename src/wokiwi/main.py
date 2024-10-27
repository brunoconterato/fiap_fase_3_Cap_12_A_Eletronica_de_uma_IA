import dht
from machine import Pin
import time


# Define pins
DHT_PIN = 12          # DHT22 data pin connected to GPIO 15
TRIG_PIN = 0          # HC-SR04 Trig pin connected to GPIO 5
ECHO_PIN = 2          # HC-SR04 Echo pin connected to GPIO 18
PIR_PIN = 4           # PIR sensor data pin connected to GPIO 4

# Initialize DHT22 sensor
dht_sensor = dht.DHT22(Pin(DHT_PIN))

# Initialize HC-SR04 pins
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Initialize PIR sensor pin
pir = Pin(PIR_PIN, Pin.IN)


def read_dht():
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


def read_hcsr04():
    # Send a 10µs pulse to the trigger pin
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    # Measure the duration of the echo pin being high
    while echo.value() == 0:
        pulse_start = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()

    # Calculate the distance based on pulse duration
    duration = time.ticks_diff(pulse_end, pulse_start)
    distance = duration * 0.034 / 2
    print("Distance: {:.2f} cm".format(distance))


def read_pir():
    # Check the PIR sensor state
    if pir.value() == 1:
        print("Motion detected!")
    else:
        print("No motion detected.")


while True:
    read_dht()       # Read and print DHT22 data
    read_hcsr04()    # Read and print HC-SR04 data
    read_pir()       # Read and print PIR sensor state
    time.sleep(5)    # Wait for 2 seconds before repeating
