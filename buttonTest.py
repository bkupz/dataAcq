import piplates.DAQC2plate as DAQ
import RPi.GPIO as GPIO
import threading
import signal
import time
import sys

def main():
    sys.excepthook = my_except_hook
    global kill_app

    kill_app = threading.Event()
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=stop_callback)
    DAQ.enableDINint(0, 0, 'f') 
    DAQ.intEnable(0)
    while not kill_app.isSet():
	time.sleep(.001)
    GPIO.cleanup()
	
def stop_callback(channel):
    time.sleep(.05)
    intNum= DAQ.getINTflags(0)
    print("intNum was " + str(intNum))
    kill_app.set()
    GPIO.cleanup()

def my_except_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    print("i caught the exec")
    GPIO.cleanup()
    sys.exit(0)


if __name__ == '__main__':
    main()