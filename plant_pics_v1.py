# https://thinkingofpi.com/getting-started/rgb-led/

import RPi.GPIO as GPIO
import RPi.GPIO as GPIO2
import time
import random
from picamera import PiCamera
from datetime import datetime# as dt2
import sqlite3
from datetime import timedelta 
from signal import pause

camera = PiCamera()
#pins = (11,12,13) # R = 11, G = 12, B = 13
#pins = (13, 15, 16) # R = 11, G = 12, B = 13
#pins = {'pin_R':13, 'pin_G':16, 'pin_B':15}
pins = {'pin_R':17, 'pin_G':18, 'pin_B':22}

class Holder(object):
    def set(self, value):
        self.value = value
        return value
    def get(self):
        return self.value

plant_dt = Holder()
water_dt = Holder()
pic_dt = Holder()

#plant_dt.set(dt2.now())
#water_dt = datetime.now()
#pic_dt = datetime.now()

con = sqlite3.connect("example.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cur = con.cursor()


# dateTimeObj = dt2.now().strftime("%Y%m%d%H%M%S")
# file_location = '/home/pi/Desktop/pic_files/' + str(dateTimeObj) + '_pic.jpg'               
# Insert a row of data

cur.execute("select ts from plant_log where event = 'took pic' order by ts desc LIMIT 1")
records = cur.fetchall()	

# water_ts = records[0][0]
pic_dt.set(records[0][0])



cur.execute("select ts from plant_log where event = 'planted seed' order by ts LIMIT 1")
records = cur.fetchall()
#print('seed was planted' + records[0,0])

# plant_ts = records[0][0]
plant_dt.set(records[0][0])

cur.execute("select ts from plant_log where event = 'pump ran' order by ts desc LIMIT 1")
records = cur.fetchall()	

# water_ts = records[0][0]
water_dt.set(records[0][0])

hours_to_add = random.randint(15,55)
next_water = water_dt.get() + timedelta(seconds = hours_to_add)
water_dt.set(next_water)


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8




# photoresistor connected to adc #0
photo_ch = 0
light_meter_ch = 1

ledPin = 11    # define ledPin
buttonPin = 12    # define buttonPin

         
#read SPI data from MCP3008(or MCP3204) chip,8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)	

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# def turn_on_photo_meter():
  

# def init():
         # GPIO.setwarnings(False)
         # GPIO.cleanup()			#clean up at the end of your script
         # GPIO.setmode(GPIO.BCM)		#to specify whilch pin numbering system
         # # set up the SPI interface pins
         # GPIO.setup(SPIMOSI, GPIO.OUT)
         # GPIO.setup(SPIMISO, GPIO.IN)
         # GPIO.setup(SPICLK, GPIO.OUT)
         # GPIO.setup(SPICS, GPIO.OUT)
         
def setup_rgb():
    global p_R,p_G,p_B
    print ('Program is starting ... ')
    #GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.cleanup()			#clean up at the end of your script
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.setup(pins[i], GPIO.OUT)
        GPIO.output(pins[i], GPIO.HIGH) #to off led
    p_R = GPIO.PWM(pins['pin_R'], 2000)
    p_G = GPIO.PWM(pins['pin_G'], 2000)
    p_B = GPIO.PWM(pins['pin_B'], 2000)
    p_R.start(0)
    p_G.start(0)
    p_B.start(0)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    
def setup_button(ledPin, buttonPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ledPin, GPIO.OUT)   # set ledPin to OUTPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set buttonPin to PULL UP INPUT mode

def setColor(r_val,g_val,b_val):   
    p_R.ChangeDutyCycle(r_val)
    p_G.ChangeDutyCycle(g_val)
    p_B.ChangeDutyCycle(b_val)
     
def loop():
  #init()
  #setup()
  while True :
    setup_button(ledPin, buttonPin)
    dt2 = datetime.now()
    now = dt2.now()
    if GPIO.input(buttonPin)==GPIO.LOW: # if button is pressed
        GPIO.output(ledPin,GPIO.HIGH)   # turn on led
        print ('led turned on >>>')     # print information on terminal
        #now = dt2.now()
        cur.execute("INSERT INTO plant_log (ts, event, filename) VALUES ( ?,?,?)",(now, 'watered','NA'))
        con.commit()
        time.sleep(5)
    else : # if button is relessed
        GPIO.output(ledPin,GPIO.LOW) #
        #print ('led turned off <<<') 
        
    if pic_dt.get() < now:
        setup_rgb()
        
        adc_value=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
        light_meter_value = readadc(light_meter_ch, SPICLK, SPIMOSI, SPIMISO, SPICS)
        
        r=100
        g=5
        b=5
        setColor(r,g,b)
        
        
        #now = dt2.now()
        #dateTimeObj = now.strftime("%Y%m%d%H%M%S")
        dateTimeObj= now.strftime("%Y%m%d%H%M%S")
        file_location = '/home/pi/Desktop/gpio_stuff/pic_files/' + str(dateTimeObj) + '_pic.jpg'
        take_pic(file_location)
        out_row = str(now) + ' photo taken - stored at: ' + file_location + "\n"
        
        print(out_row)	
#         f = open('/home/pi/Desktop/plant_pic_log/plant_pic_log.txt', 'a')
#         f.write(out_row)
#         f.close()

        con = sqlite3.connect("example.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = con.cursor()
        #~ dateTimeObj = dt2.now().strftime("%Y%m%d%H%M%S")
        # file_location = '/home/pi/Desktop/pic_files/' + str(dateTimeObj) + '_pic.jpg'               
        # Insert a row of data
        cur.execute("INSERT INTO plant_log (ts, event, filename) VALUES ( ?,?,?)",(now, 'took pic',file_location))
        con.commit()
        #con.close()
        
        hours_to_add = 60
        next_pic = now + timedelta(seconds = hours_to_add)
        pic_dt.set(next_pic)
        print(str(now) + ' next pic: ' + str(pic_dt.get()))
        

        # dt2 = datetime.now()

        #now = dt2.now()
        #dateTimeObj = now.strftime("%Y%m%d%H%M%S")
        dateTimeObj = now
        file_location = '/home/pi/Desktop/gpio_stuff/pic_files/' + str(dateTimeObj) + '_pic.jpg'
        take_pic(file_location)
        print ('r=%d, g=%d, b=%d ' %(r ,g, b))

        #dateTimeObj = datetime.now()
        dateTimeObj = now
        water_diff = now - water_dt.get()
        print('time since last water: ' + str(water_diff))
        out_row = str(dateTimeObj) + " | water level: "+str("%.1f"%(adc_value/100.*100))+ "% | " +  " | " +  " | Red: " + str(r) + " | Green: " + str(g)+ " | Blue: " + str(b) + " | light level: " + str("%.1f"%(light_meter_value/200.*100)) +"\n"
        light_row = str(dateTimeObj) + " | light level: " + str("%.1f"%(light_meter_value/100.*100))
        print(light_row)
        print(out_row)
       
        destroy_rgb()     
        time.sleep(5)
        
    #else:
        #print(str(dt2.now()) + ' no pic taken - next pic at: ' + str(pic_dt.get()))
        
        
    
    

    
def destroy_rgb():  
    p_R.stop()
    p_G.stop()
    p_B.stop()
    GPIO.cleanup()
  
def take_pic(pic_file):
	my_file = open(pic_file, 'wb')
	#camera = PiCamera()
	camera.resolution = (1024, 768)
	camera.start_preview()	
	# Camera warm-up time
	time.sleep(2)
	camera.capture(my_file)
	my_file.close()
	camera.stop_preview()  

if __name__ == '__main__':
  #setup()
  try:
    loop()
  except KeyboardInterrupt:
    destroy()
