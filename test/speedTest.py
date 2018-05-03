import datetime
import time
import cPickle as pickle #could use to read and write from file
import piplates.DAQC2plate as DAQ
import Queue
import threading
import csv
import os
from numba import jit


def write_file(fw, the_queue, the_event, stop_write):
    t = threading.currentThread()
    while True:
        the_event.wait()
        the_event.clear()
        while (the_queue.empty()!=True):
            print("saving to file")
            L = the_queue.get(True)
            pickle.dump(L,fw)
	print("q was empty")
	if stop_write.isSet():
            print("stoping the write thread")
            break   
@jit
def read_data(my_queue, L, e, numOfReads):
    start_time = time.time()
    for x in xrange(numOfReads):
    	print("reading data")
    	for y in range(1,100):
                    r = DAQ.getADCall(0) + DAQ.getADCall(1)
                    r.extend((DAQ.getFREQ(0),DAQ.getFREQ(1),(time.time()-start_time)))
                    L.append((r))
                    time.sleep(.0005)
        my_queue.put(L)
        e.set()

def main():
    L = list()
    numOfReads = 5
    stop_write = threading.Event()

    fw = open('test.txt','ab')
    my_queue = Queue.Queue(maxsize=0)
    e = threading.Event()

    worker = threading.Thread(target=write_file, args=(fw, my_queue, e, stop_write))
    worker.setDaemon(True)
    worker.start()
    
    raw_input("hit enter to read data")
    
    read_data(my_queue, L, e, numOfReads)

    print("shutting down the write thread")	
    stop_write.set()
    e.set()
    worker.join()
    fw.close()
    print("worker joined")	
    
    
    fr = open('test.txt', 'r+b')
    for x in xrange(numOfReads):
    	L += pickle.load(fr)
    print('file had %d rows' % len(L))
    
    fn = '{:%Y-%m-%d~%H:%M:%S}.txt'.format(datetime.datetime.now())
    with open(fn, "w+") as f:
        writer = csv.writer(f)
        writer.writerows(L)
    fr.close()
    f.close()
    os.remove('test.txt')

if __name__ == '__main__':
    main()