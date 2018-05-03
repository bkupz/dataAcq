import RPi.GPIO as GPIO
import piplates.DAQC2plate as DAQ
from time import sleep

def stop_callback(channel):
    sleep(.01)
    DAQ.getINTflags(1)
    print("pooped")

	
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(22, GPIO.FALLING, callback=stop_callback)
DAQ.enableDINint(1, 0, 'f') 
DAQ.intEnable(1)
i = 0
try:
    while 1:
        i+=1

except KeyboardInterrupt:
    GPIO.cleanup([22])