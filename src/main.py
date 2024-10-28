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
        return temperature, humidity
        
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
    print("Distância: {:.2f} cm".format(distance))
    return distance


def read_pir():
    # Check the PIR sensor state
    has_motion = pir.value() == 1
    if has_motion:
        print("Movimento detectado!")
    else:
        print("Nenhum movimento detectado.")

    return has_motion


def classify_light(light_level):
    for c, level in light_classification[::-1]:
        if light_level >= level:
            return c
    
    return "Muito escuro"


def read_ldr():
    # Read the LDR value (0-4095)
    value = ldr.read()
    # print("LDR value: {}".format(value))
    resistance = calculate_resistance(value)
    light_level = calculate_lux(resistance)
    print("Luminosidade: {}".format(light_level))

    light_classification = classify_light(light_level)
    # print("Light classification: {}".format(light_classification))
    
    return light_level

#########################################################
##### Start: Code to check motion and control alarm #####
#########################################################

# Initial alarm state and storage for motion detection history
alarm_active = False

motion_history = []  # Stores last 5 minutes of motion data (assuming a 5-second interval)
MAX_LEN = 5 * 60 // 5   # Five minutes of motion (assuming a 5-second interval)

def append_with_limit(dq, item):
    global MAX_LEN
    dq.append(item)
    if len(dq) > MAX_LEN:
        dq.pop(0)  # Remove the oldest item
    return dq

def check_invasion(motion_detected):
    """
    Checks motion history over the last 5 minutes.
    
    If motion is detected in more than 2 readings, it triggers the invasion alarm.
    
    Otherwise, if no motion was detected in the readings,
    it deactivates the alarm after 5 minutes of no motion.
    """
    global alarm_active, motion_history
    
    # Append current motion detection status to the history
    motion_history = append_with_limit(motion_history, motion_detected)
    
    # Count recent motion detections (in last 5 minutes)
    recent_motion_detections = sum(motion_history)
    
    # Condition to activate the alarm if more than 2 motion detections are observed in the last 5 minutes
    if recent_motion_detections > 2:
        if not alarm_active:
            activate_alarm()
    
    # Condition to deactivate the alarm if there has been no motion for the last 5 minutes
    elif recent_motion_detections == 0 and alarm_active:
        deactivate_alarm()

def activate_alarm():
    """
    Activates the invasion alarm, for example by triggering an alert or sending a notification.
    """
    global alarm_active
    alarm_active = True
    print("Alerta: Movimento detectado mais de 2 vezes nos últimos 5 minutos! Alarme ativado.")

def deactivate_alarm():
    """
    Deactivates the invasion alarm
    """
    global alarm_active
    alarm_active = False
    print("Alerta desativado. A área está segura.")

#######################################################
##### End: Code to check motion and control alarm #####
#######################################################


while True:
    print("\nNova leitura:")
    temperature, humidity = read_dht()              # Read and print DHT22 data
    reservoir_level = read_hcsr04()                 # Read and print HC-SR04 data
    detected_motion = read_pir()                    # Read and print PIR sensor state
    light_level = read_ldr()                        # Read and print LDR light level
    
    check_invasion(detected_motion)
    time.sleep(5)                                   # Wait for 5 seconds before repeating
