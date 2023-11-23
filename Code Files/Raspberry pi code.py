import Adafruit_DHT as AdaDHT
import RPi.GPIO as GPIO
import pigpio
import time
import paho.mqtt.client as paho
from paho import mqtt

# set up DHT sensor pin and type
DHTSensor = AdaDHT.DHT11
DHTPin = 3
BuzzerPin = 5
ServoPin = 24
YellowLEDPin = 26
RedLEDPin = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BuzzerPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(YellowLEDPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RedLEDPin, GPIO.OUT, initial=GPIO.LOW)

# set up pigpio library to control servo motor
pi = pigpio.pi() 
pi.set_mode (ServoPin, pigpio.OUTPUT)
pi.set_servo_pulsewidth(ServoPin, 2500)
time.sleep(1)#rest

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_message = on_message

# MQTT event handlers
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set("iot046", "iotproject046")
client.connect("09a9c8d11f5c4e5b91c017954acd5127.s2.eu.hivemq.cloud", 8883)

while True:
    # read sensor data
    humidity, temperature = AdaDHT.read_retry(DHTSensor, DHTPin)

    if humidity is not None and temperature is not None:
        # convert temperature to Fahrenheit
        temperature_f = (temperature * 1.8) + 32 
        
        # calculate heat index
        T = temperature_f
        RH = humidity
        HI = (-42.379 + (2.04901523*T) + (10.14333127*RH) - (.22475541*T*RH)
              - (.00683783*T*T) - (.05481717*RH*RH) + (.00122874*T*T*RH) 
              + (.00085282*T*RH*RH) - (.00000199*T*T*RH*RH))
        
        # determine heat index thresholds
        caution_HI = 77.7801064 + (0.02683447*RH) + (0.001007883*RH*RH)
        extreme_caution_HI = 86.6459477 - (0.13186163*RH) + (0.00581763*RH*RH)
        danger_HI = 96.12703022 + (0.0292267*RH) + (0.01191138*RH*RH)
        extreme_danger_HI = 106.90681 + (1.24796752*RH) + (0.02069158*RH*RH)
        
        # print sensor data
        print("Temperature={0:0.1f}°F Humidity={1:0.1f}% Heat Index={2:0.1f}°F".format(temperature_f,humidity, HI))
        
        # send humidity reading to Hivemq
        currentRH_topic = "currentRH"
        currentRH_payload = str(humidity)
        (rc, mid) = client.publish(currentRH_topic, currentRH_payload, qos=1)
        
        # check heat index and ring the buzzer accordingly
        if HI > 125:
            GPIO.output(BuzzerPin, GPIO.HIGH)
            time.sleep(0.1)  # buzzer on for 0.1 seconds
            GPIO.output(BuzzerPin, GPIO.LOW)
            
            GPIO.output(YellowLEDPin, GPIO.LOW)
            GPIO.output(RedLEDPin, GPIO.HIGH)
            
            pi.set_servo_pulsewidth(ServoPin, 700) 
            time.sleep(1)#extreme danger
            
        elif HI > 103:
            GPIO.output(BuzzerPin, GPIO.HIGH)
            time.sleep(0.5)  # buzzer on for 0.5 seconds
            GPIO.output(BuzzerPin, GPIO.LOW)
            
            GPIO.output(YellowLEDPin, GPIO.LOW)
            GPIO.output(RedLEDPin, GPIO.HIGH)
            
            pi.set_servo_pulsewidth(ServoPin, 1100)                        
            time.sleep(1)#danger
            
        elif HI > 90:
            GPIO.output(RedLEDPin, GPIO.LOW)
            GPIO.output(YellowLEDPin, GPIO.HIGH)
            
            pi.set_servo_pulsewidth(ServoPin, 1500)            
            time.sleep(1)#extreme caution
            
        elif HI > 80:
            GPIO.output(RedLEDPin, GPIO.LOW)
            GPIO.output(YellowLEDPin, GPIO.HIGH)
            
            pi.set_servo_pulsewidth(ServoPin, 1900)            
            time.sleep(1)#caution
            
        else:
            GPIO.output(BuzzerPin, GPIO.LOW)
            
            pi.set_servo_pulsewidth(ServoPin, 2200) 
            time.sleep(1)#normal
    else:
        print("Failed to retrieve data from sensor")
        
        # set servo to rest position
        pi.set_servo_pulsewidth(ServoPin, 2500)
        time.sleep(1)#rest

# cleanup
pi.stop()

