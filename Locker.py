import RPi.GPIO as GPIO
from Crypto.Cipher import AES
from flask import Flask,request
import json
'''from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore'''
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import time
import support
from app import ex,app,GuiThread,App
from threading import Thread
import ast
from Crypto import Random
import hashlib
import base64

'''Python Flask server'''

application=Flask(__name__) 


gui = GuiThread()

GPIO.setmode(GPIO.BCM)


# Used for decrypting messages from server
BS = 32
key = 'The secret password to server pi is this 1'
key_hash = hashlib.sha256(key.encode()).digest()

# Get row and col pins
pin_array = support.get_pins()
locker_array = support.get_lockers()
row = pin_array[0].split(',')
col = pin_array[1].split(',')


# Set GPIO pins to be used
GPIO.setup(10,GPIO.OUT)
GPIO.output(10,GPIO.LOW)

for pin in row:
	GPIO.setup(int(pin),GPIO.OUT)
	GPIO.output(int(pin),GPIO.LOW)
	
for pin in col:
	GPIO.setup(int(pin),GPIO.OUT)
	GPIO.output(int(pin),GPIO.LOW)
	
		
def unpad(s):
	return s[:-ord(s[len(s)-1:])]

'''Send emit signals to the GUI thread to update widgets'''
def layout(username,token):
	gui.gui_connect.emit(ex.set_layout(7,None,None,token,username))
	

'''Open a locker specified'''
def open_locker(locker):
	locker = int(locker)
	open_row = locker_array[locker-1][:1]
	open_col = locker_array[locker-1][1:2]
	
	
	GPIO.output(10,GPIO.HIGH)
	GPIO.output(int(row[int(open_row)]),GPIO.HIGH)
	GPIO.output(int(col[int(open_col)]),GPIO.HIGH)
	time.sleep(2)
	GPIO.output(int(row[int(open_row)]),GPIO.LOW)
	GPIO.output(int(col[int(open_col)]),GPIO.LOW)
	GPIO.output(10,GPIO.LOW)
	
	print("Opened locker "+str(locker))
		
'''Flask Application Routes'''	

	
'''Used to decrypt a message and open a locker'''
@application.route("/open/",methods=['POST'])
def decrypt():	
	enc = request.form['cipherText']
	enc = str(enc)
	enc = base64.b64decode(str(enc))
	iv = enc[:AES.block_size]
	cipher = AES.new(key_hash,AES.MODE_CBC,iv)
	text = unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8') #Decrypt
	try:
		text = ast.literal_eval(text) #Convert text to a dictionary
		if(str(text['date']) == str(time.strftime('%Y-%m-%d'))):
			open_locker(text['locker'])			
	except:
		print("Error decoding message")
	return 'Success'
	

'''Used when an RFID is scanned'''	
@application.route("/scan/<token>/<username>/")
def open_RFID(token,username):
	token = str(token)
	username = str(username)
	if(test.has_locker(username,token)):
		open_locker(test.get_locker(username,token)) #Open Locker		
	else:
		layout(username,token)		#Login into app
	return 'RFID scan success'

	
if __name__ == '__main__':
	app_thread = Thread(target=application.run,args=('0.0.0.0',80))	#Flask Thread
	app_thread.start()
	app.exec_() #GUI Thread
		
	
	
	

	
    
