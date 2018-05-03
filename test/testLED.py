import piplates.DAQC2plate as DAQ

def setStatusBlueLED( ButtonPlate ):
	DAQ.setDOUTall( ButtonPlate ,0)
	DAQ.setDOUTbit( ButtonPlate , 5) 

def setStatusRedLED(ButtonPlate):
	DAQ.setDOUTall(ButtonPlate,0)
	DAQ.setDOUTbit(ButtonPlate, 6) 


def setStatusGreenLED(ButtonPlate):
	DAQ.setDOUTall(ButtonPlate,0)
	DAQ.setDOUTbit(ButtonPlate, 7) 


