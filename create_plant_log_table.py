import sqlite3
import datetime
from datetime import timedelta 
import time
import csv
from datetime import datetime #as dt2
from picamera import PiCamera
import RPi.GPIO as GPIO
import random


dt2 = datetime.now()
now = dt2.now()

con = sqlite3.connect("example.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()



#cur.execute("drop table if exists plant_log")
#cur.execute("create table plant_log( ts timestamp, event text, filename text)")
dt1 = datetime.now()#.strftime('%Y%m%d %H:%M:%S.%m')
now_ts = dt1
file_location = 'NA'
print(str(now_ts ))
cur.execute("INSERT INTO plant_log (ts, event, filename) VALUES ( ?,?,?)",(now_ts, 'took pic',file_location))
cur.execute("INSERT INTO plant_log (ts, event, filename) VALUES ( ?,?,?)",(now_ts, 'planted seed',file_location))
cur.execute("INSERT INTO plant_log (ts, event, filename) VALUES ( ?,?,?)",(now_ts, 'pump ran',file_location))
con.commit()
con.close()
# cur.execute("select ts from plant_log where event = 'planted seed' order by ts LIMIT 1")
# 
# cur.execute("select ts from plant_log where event = 'pump ran' order by ts desc LIMIT 1")

