import dht
from machine import Pin, ADC
import time
import math


#######################################
##### Start: Code to read sensors #####
#######################################


# Define pins
DHT_PIN = 12  # DHT22 data pin connected to GPIO 15
TRIG_PIN = 0  # HC-SR04 Trig pin connected to GPIO 5
ECHO_PIN = 2  # HC-SR04 Echo pin connected to GPIO 18
PIR_PIN = 4  # PIR sensor data pin connected to GPIO 4
LDR_PIN = 33  # LDR sensor connected to GPIO 36 (ADC1 channel 0)

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

rl10 = 50e3  # LDR resistance at 10lux
gamma = 0.7  # log(Ra/Rb) / log(La/Lb)


# R2 =  R1 * Vout / (Vin - Vout)
def calculate_resistance(ldr_value):
    voltage_ratio = ldr_value / (4095 - ldr_value)
    return 10e3 * voltage_ratio


# R = R_10 * (lux / 10) ^ -γ => R10/​R​=(10/lux​)^−γ => R/R10​​=(10/lux​)^γ => (R10​​/R)^(1/γ​)=10/lux​ => lux=10*(R10/R​​)^(1/γ)​
def calculate_lux(resistance):
    return 10 * math.pow(rl10 / resistance, 1 / gamma)

"""
There are four types of sensors used in this project:

1. DHT22: Digital temperature and humidity sensor
    - Used to measure temperature and humidity in the environment

2. HC-SR04: Ultrasonic distance sensor
    - Used to measure the water level in the reservoir

3. PIR: Passive Infrared Motion Sensor
    - Used to detect motion in the area

4. LDR: Light Dependent Resistor
    - Used to measure the light intensity in the environment
"""


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
    print("Nível do reservatório: {:.2f} cm".format(distance))
    return distance


def read_pir():
    # Check the PIR sensor state
    has_motion = pir.value() == 1
    if has_motion:
        print("Movimento detectado!")
    else:
        print("Nenhum movimento detectado.")

    return has_motion


def read_ldr():
    # Read the LDR value (0-4095)
    value = ldr.read()
    resistance = calculate_resistance(value)
    light_level = calculate_lux(resistance)
    print("Luminosidade: {}".format(light_level))

    return light_level


#####################################
##### End: Code to read sensors #####
#####################################


#########################################################
##### Start: Code to check motion and control alarm #####
#########################################################


# Initial alarm state and storage for motion detection history
alarm_active = False

motion_history = (
    []
)  # Stores last 5 minutes of motion data (assuming a 5-second interval)
MAX_LEN = 5 * 60 // 5  # Five minutes of motion (assuming a 5-second interval)


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
    print(
        "Alerta: Movimento detectado mais de 2 vezes nos últimos 5 minutos! Alarme ativado."
    )


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


###################################################
##### Start: Code to control irrigation level #####
###################################################



# TODO: incluir na documentação
# Informação de irrigação: https://chatgpt.com/c/671f0c05-3a38-8009-83bf-ecd5d41506e7

irrigation_level = 0  # 0 para desativada, 1 para fraca, 2 para moderada, 3 para forte


def check_conditions(humidity, reservoir_level, light_level):
    # Boolean variables for soil moisture levels
    humidity_low = humidity < 40  # Low moisture when humidity is below 40%
    humidity_medium = 40 <= humidity < 70  # Medium moisture between 40% and 69%
    humidity_high = humidity >= 70  # High moisture when humidity is 70% or higher

    # Boolean variables for reservoir levels
    reservoir_full = (
        reservoir_level > 100
    )  # Full reservoir when water level is above 100 cm
    reservoir_moderate = (
        60 <= reservoir_level <= 100
    )  # Moderate reservoir level between 60 cm and 100 cm
    reservoir_low = (
        reservoir_level < 60
    )  # Low reservoir when water level is below 60 cm

    # Boolean variables for light intensity levels
    light_high = light_level > 1000  # High light intensity above 1000 lux (daylight)
    light_moderate = (
        10 <= light_level <= 1000
    )  # Moderate light intensity between 10 lux (dusk) and 1000 lux (cloudy day)
    light_low = light_level < 10  # Low light intensity below 10 lux (dusk)

    print("\n")
    print(
        "Umidity:", "low" if humidity_low else "medium" if humidity_medium else "high"
    )
    print(
        "Reservoir:",
        "full" if reservoir_full else "moderate" if reservoir_moderate else "low",
    )
    print("Light:", "high" if light_high else "moderate" if light_moderate else "low")

    # Return all condition variables for use in decision-making
    return (
        humidity_low,
        humidity_medium,
        humidity_high,
        reservoir_full,
        reservoir_moderate,
        reservoir_low,
        light_high,
        light_moderate,
        light_low,
    )


def check_irrigation(humidity, reservoir_level, light_level):
    global irrigation_level

    # Obtain boolean conditions for soil moisture, reservoir level, and light intensity
    (
        humidity_low,
        humidity_medium,
        humidity_high,
        reservoir_full,
        reservoir_moderate,
        reservoir_low,
        light_high,
        light_moderate,
        light_low,
    ) = check_conditions(humidity, reservoir_level, light_level)

    # Decision logic for irrigation control based on conditions:

    # Case 1: Low soil moisture and full reservoir
    if humidity_low and reservoir_full:
        if light_high:
            activate_strong_irrigation()  # Activate strong irrigation for high evaporation risk
        elif light_moderate:
            activate_moderate_irrigation()  # Activate moderate irrigation for moderate light conditions
        else:
            activate_light_irrigation()  # Activate light irrigation if light is low

    # Case 2: Low soil moisture and moderate reservoir level
    elif humidity_low and reservoir_moderate:
        if light_high:
            activate_moderate_irrigation()  # Moderate irrigation to conserve water with high light
        else:
            activate_light_irrigation()  # Light irrigation for low or moderate light to save water

    # Case 3: Medium soil moisture and full or moderate reservoir level
    elif humidity_medium and (reservoir_full or reservoir_moderate):
        if light_low:
            activate_light_irrigation()  # Light irrigation due to low evaporation risk
        else:
            activate_moderate_irrigation()  # Moderate irrigation for medium moisture and moderate/high light

    # Case 4: High soil moisture
    elif humidity_high:
        deactivate_irrigation(
            "umidade elevada do solo"
        )  # Deactivate irrigation if soil is moist enough

    # Case 4:  Low reservoir level
    elif reservoir_low and not humidity_high:
        deactivate_irrigation(
            "nível baixo do reservatório"
        )  # Deactivate irrigation if water is low


def activate_strong_irrigation():
    """
    Ativa irrigação forte.
    """
    global irrigation_level
    if irrigation_level == 3:
        keep_irrigation_level()
        return
    irrigation_level = 3
    print("Ativando irrigação forte.")


def activate_moderate_irrigation():
    """
    Ativa irrigação moderada.
    """
    global irrigation_level
    if irrigation_level == 2:
        keep_irrigation_level()
        return
    irrigation_level = 2
    print("Ativando irrigação moderada.")


def activate_light_irrigation():
    """
    Ativa irrigação leve.
    """
    global irrigation_level
    if irrigation_level == 1:
        keep_irrigation_level()
        return
    irrigation_level = 1
    print("Ativando irrigação leve.")


def deactivate_irrigation(reason):
    """
    Desativa o sistema de irrigação.
    """
    global irrigation_level
    if irrigation_level == 0:
        keep_irrigation_level()
        return
    irrigation_level = 0
    print(f"Desativando irrigação. Motivo: {reason}")


def keep_irrigation_level():
    global irrigation_level
    if irrigation_level == 3:
        print("Mantenha irrigação forte")
    elif irrigation_level == 2:
        print("Mantenha irrigação moderada")
    elif irrigation_level == 1:
        print("Mantenha irrigação leve")


#################################################
##### End: Code to control irrigation level #####
#################################################


#############################################################
##### Start: Main loop to read sensors  every 5 seconds #####
#############################################################


while True:
    print("\nNova leitura:")
    temperature, humidity = read_dht()  # Read and print DHT22 data
    reservoir_level = read_hcsr04()  # Read and print HC-SR04 data
    detected_motion = read_pir()  # Read and print PIR sensor state
    light_level = read_ldr()  # Read and print LDR light level

    check_invasion(detected_motion)

    check_irrigation(humidity, reservoir_level, light_level)

    time.sleep(5)  # Wait for 5 seconds before repeating


##########################################################
##### End: Main loop to read sensors every 5 seconds #####
##########################################################
