# IoT_Big_Data_Analysis_Project
The project involves the use of a smart thermostat system to regulate the temperature of a living room, using a temperature sensor and warning alerts for extreme temperatures. A machine learning model is used for temperature forecasting, and a real-time dashboard is implemented to visualize the temperature data. Overall, the project aims to create a comfortable indoor environment and ensure the safety of individuals in extreme temperature conditions.

See our presentation - ![Link](https://www.canva.com/design/DAFh4VpQKJc/h8ul_FF6yVEsvCU7TuvDVw/view?utm_content=DAFh4VpQKJc&utm_campaign=share_your_design&utm_medium=link&utm_source=shareyourdesignpanel) 

## Tasks of the project
1. Sense the current ambient temperature (T) and relative humidity (RH).
2. Depending on the current temperature and Relative Humidity, move an indicator on a display gauge to indicate the current heat index classification.
3. Display a visualization of, Current RH data coming from the sensors, Predicted past 12 months RH and Predicted RH 12 months ahead on a Node-RED dashboard. Use the ARIMA model for predictions.
## System architecture
![system architecture2](https://github.com/nesa12/IoT_Big_Data_Analysis_Project/assets/87229466/243d70dd-19b2-4409-91db-35574f1e596a)
Architecture Description

## List of hardware

a.	Sensors
•	DHT11 v1.0 Sensor

b.	Actuators
•	LED 5mm Red Diffused
•	LED 5mm Yellow Diffused
•	Frasers 9 Steering Gear SG90 9g Tower Pro Servo 25cm

c.	Other Devices
•	male to male 40 jumper ribbon 20cm
•	male to female 40 jumper wire (40 pin,20cm length)
•	Raspberry Pi 3B+
•	830 Tie Points Breadboard
•	330 Ohm 1/4W, 5% Axial Resistor
•	4 Pin Micro Switch (Short Handle) 6*6'4.3mm
•	2.0 Normal Card Reader
•	Micro SDHC Card 8GB

Below components will be used in our proposed system:
•	DHT11 v1.0 sensor
•	Raspberry Pi 3 B+
•	LED Bulbs
•	Frasers 9 Steering Gear SG90 9g Tower pro Servo 25cm (180 degree)

Technical Specifications
•	70℉ to 135℉ range
•	3.0V to 5.0V operating voltage
•	750 ms sampling
•	64-bit unique address
•	One-Wire communication protocol

## Project Setup
![proj1](https://github.com/nesa12/IoT_Big_Data_Analysis_Project/assets/87229466/4585082a-4b5a-45f8-b384-d4d6d580d8c8) ![proj2](https://github.com/nesa12/IoT_Big_Data_Analysis_Project/assets/87229466/9a89ac99-17c0-4bea-8ea0-79d651404ff9)

In this system, the speed of the buzzer is automatically adjusted according to the temperature changes and two LED bulbs indicate the caution and extreme caution temperatures. First the Tower Pro Servo will connect with Raspberry PI and then after the wiring is done, the Tower Pro servo should be programmed with Python. The DS18B20 Digital Temperature Sensor must be connected to the Raspberry PI, and only one wire is needed to send data to the PI. This sensor outputs temperature data to a ssh terminal such as a putty and then returns it to the Display Gauge. The Red and Yellow LED bulbs are connected to GPIO 2 and GPIO 3 in Raspberry PI to indicate Danger temperature and Caution temperature and the Motor Driver IC is connected between PI and DC Motor. Once the circuit is connected to the power supply, if the temperature is higher than 103 degrees Fahrenheit, the Red LED bulb will light up, and when the temperature drops below 103 degrees Fahrenheit, the red LED will automatically turn off and the Yellow bulb will turn on. If the starting temperature is 103 degrees Fahrenheit, the buzzer will buzz at a certain speed. If the temperature rises, the speed of the buzzer will increase, and if the temperature drops below 103 degrees Fahrenheit, the buzzer will be turned off.  And five different temperature levels (Normal, Caution, Extreme Caution, Danger, Extreme Danger) will be displayed in display Gauge. MQTT protocol will be used to publish-subscribe and transport messages between Raspberry PI and dashboard. The Node-Red dashboard, running on Node.js server. Latest humidity, past data visualization and humidity prediction will be displayed in Node-red Dashboard.
