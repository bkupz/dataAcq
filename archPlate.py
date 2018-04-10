###
#  Brandon Kupczyk
#  Sr. Design Group M94
###

import datetime
import time
import msgpack
import piplates.DAQC2plate as DAQ
import Queue
import threading
import sys, traceback
import csv
import os
import RPi.GPIO as GPIO
from Adafruit_BNO055 import BNO055


def my_except_hook(exctype, value, tracebac):
        sys.__excepthook__(exctype, value, traceback)
        log = open('/home/pi/Desktop/sr_design/startupLog.txt','ab')
        tb = ''.join(traceback.format_tb(tracebac))
        log.write(tb)
        
        log.close()
        GPIO.cleanup()
        sys.exit(-1)

def initBno():
        initCnt = 0
        while initCnt <= 10:
		bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
		try:
	       		bno.begin()
		except RuntimeError as re:
		        initCnt+= 1
		        continue 
		sys, gyro, accel, mag = bno.get_calibration_status()
		status, self_test, error = bno.get_system_status()
		print('System status: {0}'.format(status))
		print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
                # Print out an error if system status is in error mode.
                if status == 0x01:
                        print('System error: {0}'.format(error))
                        print('See BNO055 datasheet section 4.3.59 for the meaning.')
		        initCnt+= 1
		        time.sleep(.75)
		        continue
		break
        return bno

def write_file(fw, the_queue, the_event, stop_write):
        while True:
		if not stop_write.isSet():
                        the_event.wait()
                        the_event.clear()
                while (the_queue.empty()!=True):
                        L = the_queue.get(True)
                        msgpack.pack(L,fw)
        	if stop_write.isSet():
	        	if the_queue.empty():
                        	print("stopping the write thread")
	                	break

def main():
        global ButtonPlate
        ButtonPlate = 0
        sys.excepthook = my_except_hook

        global kill_app
        global fw
        global fn
        global load
        
        bno = initBno()
        

        fn = '/home/pi/Desktop/sr_design/data/{:%Y_%m_%d@%H_%M_%S}.RAW'.format(datetime.datetime.now())
        fw = open(fn,'ab')
        kill_app = threading.Event()

        my_queue = Queue.Queue(maxsize=0)
        data_added_to_q = threading.Event()

        worker= threading.Thread(target=write_file, args=(fw, my_queue, data_added_to_q, kill_app))
        worker.setDaemon(True)

        print("Flip the switch to start recording")

        offSignal = DAQ.getDINbit(ButtonPlate, 0)
        while offSignal != 1:
		offSignal = DAQ.getDINbit(ButtonPlate, 0)

        worker.start()
        start_time = time.time()

        while not kill_app.isSet():
                print("reading data")
		L = []
                for y in range(1,100):
                        #time.sleep(.001)
	        	try:
                                r = DAQ.getADCall(0) + DAQ.getADCall(1) + DAQ.getADCall(2) + DAQ.getADCall(3)
                        except IndexError:
                                print("indexError occured")
	                	continue
                        r.extend( [DAQ.getFREQ(0),DAQ.getFREQ(1),DAQ.getFREQ(2),DAQ.getFREQ(3),bno.read_linear_acceleration(),bno.read_quaternion(), (time.time()-start_time)])
	        	L.append((r))
                my_queue.put(L)
		######check for stop signal#############
		try:
                        offSignal = DAQ.getDINbit(ButtonPlate, 1)
		except IndexError:
	        	print("indexError Ocurred shutting down system Switch was thrown")
	        	offSignal=1
                if offSignal == 1:
	        	kill_app.set()
		######################################## 
                data_added_to_q.set()
                if time.time() > (start_time+(1*60)):
	        	kill_app.set()

        worker.join()
        fw.close()
        print("worker joined")  

	#restarting program
        main()

if __name__ == '__main__':
        main()
