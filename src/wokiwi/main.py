import dht
from machine import Pin, ADC
import time
import math


# Define pins
DHT_PIN = 12          # DHT22 data pin connected to GPIO 15
TRIG_PIN = 0          # HC-SR04 Trig pin connected to GPIO 5
ECHO_PIN = 2          # HC-SR04 Echo pin connected to GPIO 18
PIR_PIN = 4           # PIR sensor data pin connected to GPIO 4
LDR_PIN = 33          # LDR sensor connected to GPIO 36 (ADC1 channel 0)

# Initialize DHT22 sensor
dht_sensor = dht.DHT22(Pin(DHT_PIN))

# Initialize HC-SR04 pins
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

# Initialize PIR sensor pin
pir = Pin(PIR_PIN, Pin.IN)

# LDR reference: https://wokwi.com/projects/372429832828226561

# Initialize LDR as an analog input
ldr = ADC(Pin(LDR_PIN)) 
ldr.atten(ADC.ATTN_11DB)  # Set attenuation for maximum range (0-3.3V)

rl10 = 50e3     #LDR resistance at 10lux
gamma = 0.7     #log(Ra/Rb) / log(La/Lb) 

#R2 =  R1 * Vout / (Vin - Vout)
def calculate_resistance(ldr_value):
    voltage_ratio = ldr_value / (4095 - ldr_value)
    return 10e3 * voltage_ratio

#R = R_10 * (lux / 10) ^ -γ => R10/​R​=(10/lux​)^−γ => R/R10​​=(10/lux​)^γ => (R10​​/R)^(1/γ​)=10/lux​ => lux=10*(R10/R​​)^(1/γ)​
def calculate_lux(resistance):
  return 10 * math.pow(rl10/resistance, 1/gamma)


light_classification = [
    ["Escuro", 0.0],
    ["Lua cheia", 0.1],
    ["Crepúsculo profundo", 1],
    ["Crepúsculo", 10],
    ["Monitor do computador", 50],
    ["Iluminação da escada", 100],
    ["Iluminação do escritório", 400],
    ["Dia nublado", 1000],
    ["Luz do dia", 10000],
    ["Luz direta do sol", 100000]
]

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


def classify_light(light_level):
    for c, level in light_classification[::-1]:
        if light_level >= level:
            return c
    
    return "Muito escuro"


def read_ldr():
    # Read the LDR value (0-4095)
    value = ldr.read()
    print("LDR value: {}".format(value))
    resistance = calculate_resistance(value)
    light_level = calculate_lux(resistance)
    print("Light level: {}".format(light_level))

    light_classification = classify_light(light_level)
    print("Light classification: {}".format(light_classification))


while True:
    read_dht()       # Read and print DHT22 data
    read_hcsr04()    # Read and print HC-SR04 data
    read_pir()       # Read and print PIR sensor state
    read_ldr()       # Read and print LDR light level
    time.sleep(5)    # Wait for 2 seconds before repeating
