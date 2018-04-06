import shutil
import os
import datetime
import time
import logging

logging.basicConfig(filename="/home/pi/Desktop/sr_design/log.log", level=logging.INFO)
logging.info("starting")
time.sleep(5)

# File to be copied
source = "/home/pi/Desktop/sr_design/data"

# USB name must be changed to 'USB1' in order for auto copy to work
usbLoc = "/media/pi/"
try:
    usbs = os.listdir(usbLoc)
except e:
    logging.exception(e)

logging.info("got usbs")
logging.info(usbs)

for usb in usbs:
    dest = usbLoc+usb+"/data"
    logging.info(dest)

    try:
   # Copy file to destination
	shutil.move(source, dest)
   # E.g. source and destination is the same location
    except shutil.Error as e:
	logging.exception(e)
   # E.g. source or destination does not exist
    except IOError as e:
	logging.exception(e)