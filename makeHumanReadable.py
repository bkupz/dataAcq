import msgpack
import csv
import datetime
import sys
import os

#"c:\Python27\python.exe" yourprogram.py %1 # FOR DRAG AND DROP BATCH FILE

fileName  = sys.argv[1]
fr = open(fileName, 'r+b')
unpacker = msgpack.Unpacker(fr)


fn = fileName + '.csv'
fileCnt = 1
f = open(fn, "w+")
writer = csv.writer(f)

for o in unpacker:
    if os.path.getsize(fn) >= 30000000:
        f.close()
        fn = fileName+str(fileCnt)+'.csv'
        f = open(fn, "w+")
        writer = csv.writer(f)
        fileCnt = fileCnt + 1
    writer.writerows(o)

f.close()
