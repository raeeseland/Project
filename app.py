import sys
import support
import datetime
import time
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
'''from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *'''
from functools import partial


#Set size of font of a QtWidget
def set_size(layout,size):
	font = layout.font()
	font.setPointSize(size)
	layout.setFont(font)
	
#Reset parameters 	
def reset(self):
	self.lock = 0
	self.student = ""
	self.token=""


#Thread class that allows widgets to get state updates from other classes
class GuiThread(QtCore.QThread):
	gui_connect = QtCore.pyqtSignal(object)
	
	def __init__(self):
		QtCore.QThread.__init__(self)
		
	def run(self):
		time.sleep(3)
		self.emit(gui,object)
		
		

class App(QMainWindow):
				
	def __init__(self):
		
		super().__init__()
		
		#Sets color of application and a windowless frame
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background,QColor("#000080"))
		self.setPalette(palette)
		
		#Using a stack layout to house all the layouts
		self.stacked_layout = QStackedLayout()
		self.login_layout() #Set login layout
		self.stacked_layout.addWidget(self.view_login) #add it to stack
		
		#Status for information for the user 
		self.statusBar()
		self.statusBar().setStyleSheet('color:white')
		
		#Central Widget for stacked Layout 
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.stacked_layout)
		self.setCentralWidget(self.central_widget)
		
		reset(self)
						
		#set resolution for touch screen
		self.resize(800,480)
		
		self.lockers = support.get_lockers()
		
	
			
	'''Methods that sets screen based on user input'''	
	def set_layout(self,index,locker,available_lockers,token,username):
	
		#Books a locker for a student and sets confirmation screen
		if(index == 0):
			self.statusBar().clearMessage()			
			if(support.book(self.lock,str(self.token),self.length_spin.value(),str(self.student))):
				self.info_layout()
				self.stacked_layout.addWidget(self.view_info_layout)
				self.stacked_layout.setCurrentIndex(1)
				self.stacked_layout.removeWidget(self.view_confirm_layout)
			else:
				self.statusBar().showMessage("Error with booking locker")
				
		
		#Sets 'select locker screen' if there is a valid token	
		if(index == 1):
			self.statusBar().clearMessage()
			if(self.token == "" ): #if no token found
				self.token = support.authenticate(self.usernameEdit.text(),self.passwordEdit.text()) #authenticate user
				if(not self.token == ""): 
					if(not support.has_locker(self.usernameEdit.text(),self.token)): #tests if user has a locker
						self.student = self.usernameEdit.text()
						
						self.button_layout()
						self.stacked_layout.addWidget(self.view_button_layout)
						self.stacked_layout.setCurrentIndex(1)
						self.stacked_layout.removeWidget(self.view_login)
					else:
						self.token = ""
						self.statusBar().showMessage("User already has locker")
				else:
					self.statusBar().showMessage("Incorrect username or password")
			# if a valid token is found
			else:
				self.button_layout()
				self.stacked_layout.addWidget(self.view_button_layout)
				self.stacked_layout.setCurrentIndex(1)
				self.stacked_layout.removeWidget(self.view_login)
				
			
		#Sets screen that allows users to select the length of booking											
		if(index == 2):	
			self.statusBar().clearMessage()	
			if locker in available_lockers: # if user selects a locker that is avaliable
				self.lock = locker
				self.set_time_layout()
				self.stacked_layout.addWidget(self.view_time_layout)
				self.locker_label.setText("Booking Locker:"+" "+str(locker))
				self.stacked_layout.setCurrentIndex(1)
				self.stacked_layout.removeWidget(self.view_button_layout)
				
		
		#Checks if time inputed is correct and then sets screen that contains information about user booking	
		if(index == 3):
			self.statusBar().clearMessage()
			if(self.length_spin.value() > 0):
				self.end_time = self.time_hour + self.length_spin.value()
				if(self.end_time >= 24):
					self.end_time = self.end_time-24
				self.confirm_layout()
				self.stacked_layout.addWidget(self.view_confirm_layout)
				self.stacked_layout.setCurrentIndex(1)
				self.stacked_layout.removeWidget(self.view_time_layout)
			else:
				self.statusBar().showMessage("Length Cannot be 0")
				
		#The following 3 options handle when users press the 'back' button on the screen		
		if(index == 4):
			self.statusBar().clearMessage()
			reset(self)
			self.login_layout() # Set login layout
			self.stacked_layout.addWidget(self.view_login)
			self.stacked_layout.setCurrentIndex(1)
			self.stacked_layout.removeWidget(self.view_button_layout)
			
			
		if(index == 5):
			self.statusBar().clearMessage()
			self.button_layout()
			self.stacked_layout.addWidget(self.view_button_layout)
			self.stacked_layout.setCurrentIndex(1)
			self.stacked_layout.removeWidget(self.view_time_layout)
			
		if(index == 6):
			self.statusBar().clearMessage()
			self.set_time_layout()
			self.stacked_layout.addWidget(self.view_time_layout)
			self.locker_label.setText("Booking Locker:"+" "+str(self.lock))
			self.stacked_layout.setCurrentIndex(1)
			self.stacked_layout.removeWidget(self.view_confirm_layout)
			
		
		#Handles the message and sets token when user uses RFID card to login	
		if(index == 7):
			self.statusBar().clearMessage()
			self.statusBar().showMessage("Card Recognized")
			self.token = token
			self.usernameEdit.setText(username)
			self.student = self.usernameEdit.text()
		
		#Sets login screen once booking is complete	
		if(index == 8):
			self.login_layout() 
			reset(self)
			self.stacked_layout.addWidget(self.view_login)
			self.stacked_layout.setCurrentIndex(1)
			self.stacked_layout.removeWidget(self.view_info_layout)
			
			
	'''Contains all the elements of the login screen'''									
	def login_layout(self):
		
		#Define all elements that go on layout
		self.username = QLabel("Username:")
		self.password = QLabel("Password:")
		self.usernameEdit = QLineEdit()
		self.passwordEdit = QLineEdit()
		self.login_button = QPushButton("Login")
		
		self.key = QPushButton("Keyboard")
		self.key.clicked.connect(print('ok'))
		
		#Define a layout and widget for this screen
		self.view_login = QWidget()
		self.grid = QGridLayout()
		self.grid.setSpacing(10)
		
		#Following sets font size of our elements and color
		set_size(self.username,16)
		self.username.setStyleSheet('color:white')
		
		set_size(self.password,16)
		self.password.setStyleSheet('color:white')
		
		
		set_size(self.usernameEdit,16)
		
		set_size(self.passwordEdit,16)
		self.passwordEdit.setEchoMode(QLineEdit.Password) #Password will not be shown
		
		
		
		#Set our button to respond to a click
		self.login_button.clicked.connect(lambda:self.set_layout(1,None,None,None,None))
		set_size(self.login_button,16)
		self.login_button.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		
		#Add widgets to our grid layout
		self.grid.addWidget(self.username,1,0)
		self.grid.addWidget(self.usernameEdit,1,1)
		self.grid.addWidget(self.password,2,0)
		self.grid.addWidget(self.passwordEdit,2,1)
		self.grid.addWidget(self.login_button,3,0,1,2)
		
		#Set our grid layout to be shown on our widget
		self.view_login.setLayout(self.grid)
		
		
	'''Contains all the elements and layout of the 'select a locker' screen'''	
	def button_layout(self):
		
		#Define a layout and widget for this screen
		self.grid_button_layout = QGridLayout()
		self.view_button_layout = QWidget()
		
		#Define elements of this screen
		self.back_login = QPushButton("Back")
		self.unavailable = QLabel("Grey: Unavailable")
		self.select = QLabel("Select a Locker")
		
		#Define charateristics of elemets
		set_size(self.back_login,16)
		self.back_login.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		set_size(self.unavailable,16)
		self.unavailable.setStyleSheet('color:white')
		
		set_size(self.select,16)
		self.select.setStyleSheet('color:white')
		
		
		list_available = support.get_avaliable_lockers(self.token) #Get list of available lockers from server
		self.buttons = []
		for i in range(len(self.lockers)):
			self.buttons.append(i+1)
		
		row = 1
		col = 0
		locker_num = 0
		
		'''Loop that creates buttons for each locker and places then in a grid based on position
		   given by server'''
		for locker in self.lockers:
			array = locker.split(',')
			color = array[1]
			row = int(array[0][:1]) + 1
			col = int(array[0][1:])
			self.buttons[locker_num] = QPushButton(str(locker_num+1))
			self.grid_button_layout.addWidget(self.buttons[locker_num],row,col)
			self.buttons[locker_num].clicked.connect(partial(self.set_layout,2,int(locker_num+1),list_available,None,None))
			set_size(self.buttons[locker_num],16)
			self.buttons[locker_num].setFixedSize(200,100)
			
			if locker_num+1 in list_available:
				self.buttons[locker_num].setStyleSheet("QPushButton { background-color: "+color+"; color:white; }")
			else:
				self.buttons[locker_num].setStyleSheet("QPushButton { background-color: grey; color:white; }")
			
			locker_num = locker_num + 1
			
				
		#Add elements to our grid layout
		self.grid_button_layout.addWidget(self.select,0,0)
		self.grid_button_layout.addWidget(self.unavailable,row+1,0)
		self.grid_button_layout.addWidget(self.back_login ,row+1,2)
		self.back_login.clicked.connect(lambda:self.set_layout(4,None,None,None,None))
			
				
		self.view_button_layout.setLayout(self.grid_button_layout)
		
		
	'''Contains the elements and layout for when users select their reservation time'''	
	def set_time_layout(self):
		
		#Define a layout and widget for this screen
		self.grid_time_layout = QGridLayout()
		self.view_time_layout = QWidget()
		self.grid_time_layout.setSpacing(80)
		
		#Set time to use for booking a locker
		self.now = datetime.datetime.now()
		self.time_hour = datetime.datetime.now().time().hour
		self.time_min = datetime.datetime.now().time().minute
		self.time = "Start Time: "+' '+self.now.strftime("%H:%M")
		
		#Define elements of this screen
		self.hour = QLabel("Hours")
		self.locker_label = QLabel()
		self.length = QLabel("Length:")
		self.length_spin = QSpinBox()
		self.book = QPushButton("Book")
		self.back_locker = QPushButton("Back")
		self.start_time = QLabel(self.time)
		
		
		#Define charateristics of elemets
		
		set_size(self.hour,18) #Font size
		self.hour.setStyleSheet('color:white') #Font color
		
		set_size(self.locker_label,18)
		self.locker_label.setStyleSheet('color:white')
		self.locker_label.move(0,0) #Moves label to pixel 0x0
		
		
		set_size(self.start_time,18)
		self.start_time.setStyleSheet('color:white')
		
		set_size(self.length,18)
		self.length.setStyleSheet('color:white')
		
		self.length_spin.setStyleSheet("QSpinBox::up-button { width: 70px; }" "QSpinBox::down-button { width: 70px; }") #Spin box arrow size
		set_size(self.length_spin,20)
		self.length_spin.setRange(0,10) #Spin box min and max values
		self.length_spin.setWrapping(True)
		self.length_spin.setFixedSize(150,60) #Spin size
		
		set_size(self.book,18)
		self.book.clicked.connect(lambda:self.set_layout(3,None,None,None,None))
		self.book.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		set_size(self.back_locker,18)
		self.back_locker.clicked.connect(lambda:self.set_layout(5,None,None,None,None))
		self.back_locker.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
			
		#Add elements to our grid layout		
		self.grid_time_layout.addWidget(self.start_time, 1,1)
		self.grid_time_layout.addWidget(self.locker_label,0,1)
		self.grid_time_layout.addWidget(self.length, 2,0)
		self.grid_time_layout.addWidget(self.length_spin,2,1)
		self.grid_time_layout.addWidget(self.hour,2,2)
		self.grid_time_layout.addWidget(self.book,5,0)
		self.grid_time_layout.addWidget(self.back_locker,5,2)
		
		self.view_time_layout.setLayout(self.grid_time_layout)
		
	
	'''Contains all the elements of the confirmation screen'''
	def confirm_layout(self):
		
		#Define a layout and widget for this screen
		self.grid_confirm_layout = QGridLayout()
		self.view_confirm_layout = QWidget()
		self.grid_confirm_layout.setSpacing(80)
		
		#Define elements of this screen
		self.booking = QLabel("Your Booking: Locker "+str(self.lock))
		self.end = QLabel("End Time: "+ str(self.end_time)+":"+self.time[-2:])
		self.confirm = QPushButton("Confirm")
		self.back = QPushButton("Back")
		
		#Set characteristics of the elements
		set_size(self.booking,18) #font size
		self.booking.setStyleSheet('color:white') #font color
		
		set_size(self.end ,18)
		self.end.setStyleSheet('color:white')
		
		set_size(self.confirm,18)
		self.confirm.clicked.connect(lambda:self.set_layout(0,None,None,None,None))
		self.confirm.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		set_size(self.back,18)
		self.back.clicked.connect(lambda:self.set_layout(6,None,None,None,None))
		self.back.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		#Add elements to our grid layout
		self.grid_confirm_layout.addWidget(self.booking,0,0)
		self.grid_confirm_layout.addWidget(self.start_time,1,0)
		self.grid_confirm_layout.addWidget(self.end,2,0)
		self.grid_confirm_layout.addWidget(self.confirm,3,0)
		self.grid_confirm_layout.addWidget(self.back,3,1)
		
		self.view_confirm_layout.setLayout(self.grid_confirm_layout)
		
		
	'''Contains elements that show information about users booking'''	
	def info_layout(self):
		
		#Define a layout and widget for this screen
		self.grid_info_layout = QGridLayout()
		self.view_info_layout = QWidget()
		
		#Define elements of this screen
		self.username = QLabel('Student: '+self.student)
		self.locker = QLabel('Locker: '+str(self.lock))
		self.booking_time = QLabel('Start Time: '+str((datetime.datetime.now()+datetime.timedelta(minutes = 1)).time())[:5]+"    "+
		'End Time: '+str((datetime.datetime.now()+datetime.timedelta(minutes = 1 ,hours = int(self.length_spin.value()))).time())[:5])
		self.ok = QPushButton('OK')
		
		#Set characteristics of the elements
		set_size(self.locker ,18)
		self.locker.setStyleSheet('color:white')
		
		set_size(self.username ,18)
		self.username.setStyleSheet('color:white')
		
		set_size(self.booking_time ,18)
		self.booking_time.setStyleSheet('color:white')
		
		set_size(self.ok,18)
		self.ok.clicked.connect(lambda:self.set_layout(8,None,None,None,None))
		self.ok.setStyleSheet("QPushButton { background-color: black; color:white; }")
		
		#Add elements to our grid layout
		self.grid_info_layout.addWidget(self.username,0,0)
		self.grid_info_layout.addWidget(self.locker,1,0)
		self.grid_info_layout.addWidget(self.booking_time,2,0)
		self.grid_info_layout.addWidget(self.ok,3,0,1,2)
		
		self.view_info_layout.setLayout(self.grid_info_layout)
				
							
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	app.exec_()
	
else:
	QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads,True)
	app = QApplication(sys.argv)
	ex = App()
	ex.show()
	
	
	
	
	

      
        



