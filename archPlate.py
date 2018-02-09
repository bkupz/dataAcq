###
#  Brandon Kupczyk
#  Sr. Design Group M94
###

import datetime
import time
#import cPickle as pickle
import msgpack
import piplates.DAQC2plate as DAQ
import Queue
import threading
import sys
import csv
import os
import RPi.GPIO as GPIO

def my_except_hook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    GPIO.cleanup()
    sys.exit(-1)

def stop_callback(channel):
    time.sleep(.05)
    intNum= DAQ.getINTflags(0)
    print("intNum was " + str(intNum))
    kill_app.set()

def write_file(fw, the_queue, the_event, stop_write):
    global reads
    reads = 0
    t = threading.currentThread()
    while True:
        the_event.wait()
        the_event.clear()
        while (the_queue.empty()!=True):
            print("saving to file")
            L = the_queue.get(True)
            #pickle.dump(L,fw)
            msgpack.pack(L,fw)
            reads+=1
    	print("q was empty")
    	if stop_write.isSet():
	    if the_queue.empty():
                print("stoping the write thread")
	        break

def main():
    sys.excepthook = my_except_hook
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(22, GPIO.FALLING, callback=stop_callback)
    DAQ.enableDINint(0, 0, 'f') 
    DAQ.intEnable(0)

    L = list()

    global kill_app

    stop_write = threading.Event()
    fw = open('rawdata','ab')
    stop_read = threading.Event()
    kill_app = threading.Event()

    my_queue = Queue.Queue(maxsize=0)
    e = threading.Event()

    worker= threading.Thread(target=write_file, args=(fw, my_queue, e, stop_write))
    worker.setDaemon(True)
    worker.start()
    
    raw_input("Press enter to start recording")
    start_time = time.time()
    

    while not kill_app.isSet():
        print("reading data")
        for y in range(1,100):
            time.sleep(.001)
            r = DAQ.getADCall(0) #+ DAQ.getADCall(1) #+ DAQ.getADCall(2)
            r.extend( [DAQ.getFREQ(0), (time.time()-start_time)])#,DAQ.getFREQ(1)
            L.append((r))
        my_queue.put(L)
        e.set()
	#reads+=1

 
    print("shutting down the write thread") 
    stop_write.set()
    


    print("stops were set")
    worker.join()
    fw.close()
    print("worker joined")  
    

    p = []
    fr = open('rawdata', 'r+b')
    #for x in xrange(reads):
        #p = pickle.load(fr)        
    unpacker = msgpack.Unpacker(fr)
    for o in unpacker:
	p+= o

    print('file had %d rows' % len(p))


    fn = '{:%Y-%m-%d~%H:%M:%S}.csv'.format(datetime.datetime.now())
    with open(fn, "w+") as f:
        writer = csv.writer(f)
        writer.writerows(p)
    
    os.remove("rawdata")
    GPIO.cleanup()

if __name__ == '__main__':
    main()