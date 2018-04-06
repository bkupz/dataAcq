import msgpack
import csv
import datetime
import sys

#"c:\Python27\python.exe" yourprogram.py %1 # FOR DRAG AND DROP BATCH FILE

fileName  = sys.argv[1]
fr = open(fileName, 'r+b')
unpacker = msgpack.Unpacker(fr)


fn = fileName + '.csv'
with open(fn, "w") as f:
    writer = csv.writer(f)
    for o in unpacker:
        writer.writerows(o)
