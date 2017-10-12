import ast
import serial
import time
import requests
import log

'''Python class used by the RFID reader and Raspberry Pi to
scan a users UCT card and returns a value, which is then used
to open a locker or login the user'''

l = log.get_logger()

port = '/dev/ttyACM0'

IP = "137.158.61.9" #Static IP of Raspberry Pi

l.debug("Device setup")

timeout = 9000;#seconds
currentTimeout = timeout
exitFlag = 0
tagLength = 14
value = 0


while True:
    l.debug("Opening serial connection to card reader...")
    try:
        ser = serial.Serial(
            port,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS
        )
    except:
        l.error("Failed to open serial device %s" % port)
        continue

    break    
	
l.debug("Access Logger Started and Ready")
l.debug("Waiting for card scan.")


scan_count = 0

print("%d Present a card." % scan_count)

while True:
    
    if(ser.inWaiting()>0):
        currentTimeout = timeout;
        if(ser.inWaiting()%tagLength == 0):
            value = ser.read(tagLength)
            l.debug("Reading card...")
            value = value.decode("utf-8")
            value = int(value[1:-3],16)  # UCT card ID

            try :          
                auth = requests.get('https://lockit.cs.uct.ac.za/api/v1/card/get-auth-token',auth=(value,""),verify=False)#Authenticate user
                result_dict = ast.literal_eval(auth.text)             
                token = result_dict["token"] 
                uct_id =  result_dict["uct_id"]                        
                open_locker = requests.get('http://'+IP+'/scan/'+token+'/'+uct_id+'/')  #Open locker or login

            except:
                print(auth.status_code,open_locker.status_code)
                
		
        elif (ser.inWaiting() > tagLength):
            l.info("Too much data in buffer - flushing")
            time.sleep(2)
            print(ser.inWaiting())
            print(ser.read(ser.inWaiting())) #flushing the system.
            l.debug("Flushing buffer completed.")

    else:
        l.debug("Sleeping")
        time.sleep(1)
        currentTimeout-=1;
		
ser.close()
