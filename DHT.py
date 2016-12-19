import Adafruit_DHT
import os
import time
from ISStreamer.Streamer import Streamer

# --------- User Settings ---------
# The DHT_SENSOR_TYPE below may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 - blue one
#  Adafruit_DHT.AM2302 - DHT22 - white one, DHT Pro or AM2302
#  2 - DHT21 - black one, AM2301
DHT_SENSOR_TYPE = Adafruit_DHT.AM2302
# Connect the DHT sensor to one of the digital pins (i.e. 2, 3, 4, 7, or 8)
DHT_SENSOR_PIN = 4
# Initial State settings
BUCKET_NAME = "PLACE YOUR INITIAL STATE BUCKET NAME HERE"
BUCKET_KEY = "PLACE YOUR INITIAL STATE BUCKET KEY HERE"
ACCESS_KEY = "PLACE YOUR INITIAL STATE ACCESS KEY HERE"
# Set the time between sensor reads
MINUTES_BETWEEN_READS = 1
CONVERT_TO_FAHRENHEIT = True
# ---------------------------------

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
        		streamer.log("Temperature(F)",temp_f)
        	else:
        		# print("Temperature(C) = ", temp_c)
        		streamer.log("Temperature(C)",temp_c)
        if ((isFloat(hum)) and (hum >= 0)):
    		# print("Humidity(%) = ", hum)
        	streamer.log(":sweat_drops: Humidity(%)",hum)
        streamer.flush()

    except IOError:
        print ("Error")

    time.sleep(60*MINUTES_BETWEEN_READS)
