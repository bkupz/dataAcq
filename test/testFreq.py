import piplates.DAQC2plate as DAQ
import time

while True:
	print("freq 0: " + str(DAQ.getFREQ(0)) + " freq 1: " +str(DAQ.getFREQ(1))+ " freq 2: "+str(DAQ.getFREQ(2)) + " freq 3: "+str(DAQ.getFREQ(3)))
	time.sleep(.1)