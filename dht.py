import Adafruit_DHT
import os
import time
import RPi.GPIO as GPIO
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
# The DHT_SENSOR_TYPE below may need to be changed depending on which DHT sensor you have:
#  Adafruit_DHT.DHT11 - DHT11 - blue one
#  Adafruit_DHT.DHT22 - DHT22 - DHT22
#  Adafruit_DHT.AM2302 - DHT22 - white one, DHT Pro or AM2302
DHT_SENSOR_TYPE = Adafruit_DHT.AM2302
# Connect the DHT sensor to one of the digital pins (i.e. 2, 3, 4, 7, or 8)
DHT_SENSOR_PIN = 4
# Initial State settings
BUCKET_NAME = "PLACE YOUR INITIAL STATE BUCKET NAME HERE"
BUCKET_KEY = "PLACE YOUR INITIAL STATE BUCKET KEY HERE"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
STREAM_NAME = "PLACE YOUR INITIAL STATE STREAM NAME HERE"
# Set the time between sensor reads
SECONDS_BETWEEN_READS = 1
CONVERT_TO_FAHRENHEIT = True
GPIO_LED_PIN = 18 #GPIO pin for the script LED
GPIO_SWITCH_PIN = 21 #GPIO pin for off switch
# ---------------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_LED_PIN,GPIO.OUT)
GPIO.setup(GPIO_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

while True:
    try:
        [hum, temp_c] = Adafruit_DHT.read_retry(DHT_SENSOR_TYPE,DHT_SENSOR_PIN)
        if isFloat(temp_c):
            if (CONVERT_TO_FAHRENHEIT):
                temp_f = temp_c * 9.0 / 5.0 + 32.0
                # print("Temperature(F) = ", temp_f)
                streamer.log(STREAM_NAME,temp_f)
                GPIO.output(GPIO_LED_PIN,GPIO.HIGH)
            else:
                # print("Temperature(C) = ", temp_c)
                streamer.log(STREAM_NAME,temp_c)
                GPIO.output(GPIO_LED_PIN,GPIO.HIGHT)
        if ((isFloat(hum)) and (hum >= 0)):
    	    # print("Humidity(%) = ", hum)
            streamer.log(":sweat_drops: %d Humidity(%)",hum) % STREAM_NAME
        streamer.flush()
    except IOError:
        print ("Error")
    try:
        ## if button is pressed
        GPIO.wait_for_edge(GPIO_SWITCH_PIN, GPIO.FALLING)
        os.system("sudo shutdown -h now")
    except:
        pass
    GPIO.cleanup()

    time.sleep(SECONDS_BETWEEN_READS)
