#include <DHT.h>
#include <Wire.h>

#define DHT_PIN 12       // DHT22 data pin connected to GPIO 12
#define DHT_TYPE DHT22   // DHT sensor type is DHT22
#define TRIG_PIN 0       // HC-SR04 Trig pin connected to GPIO 0
#define ECHO_PIN 2       // HC-SR04 Echo pin connected to GPIO 2
#define PIR_PIN 4        // PIR sensor data pin connected to GPIO 4
#define LDR_PIN A0       // LDR sensor connected to A0 (analog input)

DHT dht(DHT_PIN, DHT_TYPE);
int irrigation_level = 0;   // 0 for off, 1 for light, 2 for moderate, 3 for strong

const double rl10 = 50000.0; // LDR resistance at 10 lux
const double ldrGamma = 0.7;

bool alarm_active = false;
bool motion_history[60] = { false };
int history_index = 0;

// Function prototypes
void activate_strong_irrigation();
void activate_moderate_irrigation();
void activate_light_irrigation();
void deactivate_irrigation(const char* reason);
void keep_irrigation_level();

void setup() {
    Serial.begin(9600);

    // Initialize DHT sensor
    dht.begin();

    // Initialize pins
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    pinMode(PIR_PIN, INPUT);
}

void loop() {
    Serial.println("\nNova leitura:");
    double temperature = 0, humidity = 0;
    read_dht(temperature, humidity);
    double reservoir_level = read_hcsr04();
    bool detected_motion = read_pir();
    double light_level = read_ldr();

    check_invasion(detected_motion);
    check_irrigation(humidity, reservoir_level, light_level);

    delay(5000);  // Wait for 5 seconds before repeating
}

/////////////////////////////////////////
///// Start: Code to read sensors  //////
/////////////////////////////////////////

void read_dht(double &temperature, double &humidity) {
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    if (isnan(temperature) || isnan(humidity)) {
        Serial.println("Erro ao ler o sensor DHT22");
    } else {
        Serial.print("Temperatura: ");
        Serial.print(temperature);
        Serial.println(" °C");

        Serial.print("Umidade: ");
        Serial.print(humidity);
        Serial.println(" %");
    }
}

double read_hcsr04() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH);
    double distance = duration * 0.034 / 2;
    Serial.print("Nível do reservatório: ");
    Serial.print(distance);
    Serial.println(" cm");

    return distance;
}

bool read_pir() {
    bool has_motion = digitalRead(PIR_PIN) == HIGH;
    if (has_motion) {
        Serial.println("Movimento detectado!");
    } else {
        Serial.println("Nenhum movimento detectado.");
    }
    return has_motion;
}

double calculate_resistance(int ldr_value) {
    double voltage_ratio = ldr_value / (4095.0 - ldr_value);
    return 10000.0 * voltage_ratio;
}

double calculate_lux(double resistance) {
    return 10.0 * pow(rl10 / resistance, 1.0 / ldrGamma);
}

double read_ldr() {
    int value = analogRead(LDR_PIN);
    double resistance = calculate_resistance(value);
    double light_level = calculate_lux(resistance);
    Serial.print("Luminosidade: ");
    Serial.println(light_level);
    return light_level;
}

/////////////////////////////////////
///// End: Code to read sensors /////
/////////////////////////////////////

////////////////////////////////////////////////////////
///// Start: Code to check motion and control alarm ////
////////////////////////////////////////////////////////

void append_with_limit(bool* motion_history, bool item) {
    motion_history[history_index++] = item;
    if (history_index >= 60) {
        history_index = 0;
    }
}

void check_invasion(bool motion_detected) {
    append_with_limit(motion_history, motion_detected);

    int recent_motion_detections = 0;
    for (int i = 0; i < 60; i++) {
        recent_motion_detections += motion_history[i];
    }

    if (recent_motion_detections > 2) {
        if (!alarm_active) {
            activate_alarm();
        }
    } else if (recent_motion_detections == 0 && alarm_active) {
        deactivate_alarm();
    }
}

void activate_alarm() {
    alarm_active = true;
    Serial.println("Alerta: Movimento detectado mais de 2 vezes nos últimos 5 minutos! Alarme ativado.");
}

void deactivate_alarm() {
    alarm_active = false;
    Serial.println("Alerta desativado. A área está segura.");
}

/////////////////////////////////////////////////////
///// End: Code to check motion and control alarm ////
/////////////////////////////////////////////////////

//////////////////////////////////////////////////
///// Start: Code to control irrigation level /////
//////////////////////////////////////////////////

void check_conditions(double humidity, double reservoir_level, double light_level, bool &humidity_low, bool &humidity_medium, bool &humidity_high, bool &reservoir_full, bool &reservoir_moderate, bool &reservoir_low, bool &light_high, bool &light_moderate, bool &light_low) {
    humidity_low = humidity < 40;
    humidity_medium = (humidity >= 40 && humidity < 70);
    humidity_high = humidity >= 70;

    reservoir_full = reservoir_level > 100;
    reservoir_moderate = (reservoir_level >= 60 && reservoir_level <= 100);
    reservoir_low = reservoir_level < 60;

    light_high = light_level > 1000;
    light_moderate = (light_level >= 10 && light_level <= 1000);
    light_low = light_level < 10;
}

void check_irrigation(double humidity, double reservoir_level, double light_level) {
    bool humidity_low, humidity_medium, humidity_high;
    bool reservoir_full, reservoir_moderate, reservoir_low;
    bool light_high, light_moderate, light_low;

    check_conditions(humidity, reservoir_level, light_level, humidity_low, humidity_medium, humidity_high, reservoir_full, reservoir_moderate, reservoir_low, light_high, light_moderate, light_low);

    if (humidity_low && reservoir_full) {
        if (light_high) {
            activate_strong_irrigation();
        } else if (light_moderate) {
            activate_moderate_irrigation();
        } else {
            activate_light_irrigation();
        }
    } else if (humidity_low && reservoir_moderate) {
        if (light_high) {
            activate_moderate_irrigation();
        } else {
            activate_light_irrigation();
        }
    } else if (humidity_medium && (reservoir_full || reservoir_moderate)) {
        if (light_low) {
            activate_light_irrigation();
        } else {
            activate_moderate_irrigation();
        }
    } else if (humidity_high) {
        deactivate_irrigation("umidade elevada do solo");
    } else if (reservoir_low && !humidity_high) {
        deactivate_irrigation("nível baixo do reservatório");
    }
}

void activate_strong_irrigation() {
    if (irrigation_level == 3) {
        keep_irrigation_level();
        return;
    }
    irrigation_level = 3;
    Serial.println("Ativando irrigação forte.");
}

void activate_moderate_irrigation() {
    if (irrigation_level == 2) {
        keep_irrigation_level();
        return;
    }
    irrigation_level = 2;
    Serial.println("Ativando irrigação moderada.");
}

void activate_light_irrigation() {
    if (irrigation_level == 1) {
        keep_irrigation_level();
        return;
    }
    irrigation_level = 1;
    Serial.println("Ativando irrigação leve.");
}

void deactivate_irrigation(const char* reason) {
    if (irrigation_level == 0) {
        keep_irrigation_level();
        return;
    }
    irrigation_level = 0;
    Serial.print("Desativando irrigação. Motivo: ");
    Serial.println(reason);
}

void keep_irrigation_level() {
    if (irrigation_level == 3) {
        Serial.println("Mantenha irrigação forte");
    } else if (irrigation_level == 2) {
        Serial.println("Mantenha irrigação moderada");
    } else if (irrigation_level == 1) {
        Serial.println("Mantenha irrigação leve");
    }
}

////////////////////////////////////////////////
///// End: Code to control irrigation level /////
////////////////////////////////////////////////
