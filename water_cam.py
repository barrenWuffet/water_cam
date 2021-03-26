from _datetime import datetime as dt
from _datetime import timedelta as td
import random
import datetime as datetime
import time


time1 = dt.now()
rand_hrs = random.randint(15,25)
time_change = datetime.timedelta(seconds=rand_hrs)
time2 = time1 + time_change
print('current time : ' + str(time1))
print('time advance: ' + str(rand_hrs))
print('next watering time : ' + str(time2))

class Holder(object):
   def set(self, value):
     self.value = value
     return value
   def get(self):
     return self.value

h = Holder()
h.set(time2)
print('H: ' + str(h.get()))

def check_water(time2):
    if dt.now() >= time2:
        print('dt.now: ' + str(dt.now()))
        print('time2: ' + str(time2))
        water()
        #time1 = dt.now()
        rand_increase = random.randint(15, 250)
        time_changer = datetime.timedelta(seconds=rand_increase)
        time3 = dt.now() + time_changer
        h.set(time3)
        print('current time : ' + str(dt.now()))
        print('time advance: ' + str(rand_increase))
        print('next watering time : ' + str(h.get()))
    else:
        print('nothing done ' + str(dt.now()))

def water():
    print('watering!!')

def main():
    while True:
        check_water(h.get())
        time.sleep(30)

if __name__ == "__main__":
   try:
      main()
   except KeyboardInterrupt:
      # do nothing here
      pass
