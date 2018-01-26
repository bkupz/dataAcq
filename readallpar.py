import datetime
import time
import cPickle as pickle #could use to read and write from file
import piplates.DAQC2plate as DAQ
import Queue
import threading
import csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
	

def main():
    L = list()
    start_time = time.time()
    stop_write = threading.Event()
    count = 4
    fw = open('test.txt','ab')
    my_queue = Queue.Queue(maxsize=0)
    e = threading.Event()

    worker = threading.Thread(target=write_file, args=(fw, my_queue, e, stop_write))
    worker.setDaemon(True)
    worker.start()
    
    raw_input("hit enter to read data")

    for x in xrange(count):
    	print("reading data")
    	for y in range(1,100):
                    r = DAQ.getADCall(1) + [DAQ.getFREQ(0)]#+ DAQ.getADCall(0) 
                    r.append( time.time()-start_time)
                    L.append((r))
                    time.sleep(.0025)
        my_queue.put(L)
        e.set()
    print("shutting down the write thread")	
    stop_write.set()
    e.set()
    worker.join()
    fw.close()
    print("worker joined")	
    
    
    fr = open('test.txt', 'r+b')
    for x in xrange(count):
    	L += pickle.load(fr)
    print('file had %d rows' % len(L))
    
    with open('NewdataAqc.csv', 'wb') as myF:
        wr = csv.writer(myF, quoting=csv.QUOTE_ALL)
        wr.writerow(L)
    
    
    df = pd.DataFrame(np.array(L).reshape(len(L),len(L[1])), columns = list("123456789t"))
    print(df)
    #"12345678abcdefght"
    df.plot(x="t", y="1", kind="scatter")
    df.plot(x="t", y="2", kind="scatter")
    df.plot(x="t", y="3", kind="scatter")
    df.plot(x="t", y="4", kind="scatter")
    df.plot(x="t", y="5", kind="scatter")
    df.plot(x="t", y="6", kind="scatter")
    df.plot(x="t", y="7", kind="scatter")
    df.plot(x="t", y="8", kind="scatter")
    df.plot(x="t", y="9", kind="scatter")
    #df.plot(x="t", y="a", kind="scatter")
    #df.plot(x="t", y="b", kind="scatter")
    #f, (ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8) = plt.subplots(8,sharex=True,sharey=True)    
    #ax1 = df.plot(x="t", y="1", kind="scatter")
    #ax2 = df.plot(x="t", y="2", kind="scatter")
    #ax3 = df.plot(x="t", y="3", kind="scatter")
    #f.subplots_adjust(hspace=0)

    plt.show()

if __name__ == '__main__':
    main()