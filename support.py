import requests
import ast
import datetime
from time import strftime

'''Python support class for the flask server and app'''

'''Function used to book a locker'''
def book(locker,token,length,username):
	#Get start and end times of reservation
	start = str((datetime.datetime.now()+datetime.timedelta(minutes = 1)).time())[:5]
	end = str((datetime.datetime.now()+datetime.timedelta(minutes = 1,hours = length)).time())[:5]
	start_date = str(strftime('%Y-%m-%d'))+' '+str(start)
	
	#Check if date is correct
	if(int(start[0:2])+length >= 24):
		date = str(datetime.date.today() + datetime.timedelta(days=1))[-2:]
		end_date = date + str(strftime('%Y-%m-%d'))[2:]+' '+str(end)
	else:
		end_date = str(strftime('%Y-%m-%d'))+' '+str(end)
	
	#Book Locker for user	
	reservation_url = 'https://lockit.cs.uct.ac.za/api/v1/reservation/'+str(username)
	book_locker = requests.post(reservation_url,data={"start":start_date,"end":end_date,"locker_id":int(locker)},auth=(username,token),verify=False)
	print(book_locker.text, book_locker.status_code)
	if(book_locker.status_code == 200):
		return True
	else:
		return False
	
	
'''Used to authenticate users'''		
def authenticate(username,passw):
	r = requests.get('https://lockit.cs.uct.ac.za/api/v1/get-auth-token',auth=(username,passw),verify=False)
	if(r.status_code == 200):
		token_dict = ast.literal_eval(r.text)
		token = token_dict['token']
		return token
	else:
		return ""
	

'''Returns a list of avaliable lockers so users can choose'''	
def get_avaliable_lockers(token):
	lockerURI = 'https://lockit.cs.uct.ac.za/api/v1/lockers/available'
	r = requests.get(lockerURI,auth=(token,""),verify=False)
	list_available = []
	list_lockers = [] 
	list_available = ast.literal_eval(r.text)['Free lockers']
	for i in list_available:
		list_lockers.append(int(i))
	return list_lockers
			

'''Checks if a user has a locker'''
def has_locker(username,token):
	reservationURI = 'https://lockit.cs.uct.ac.za/api/v1/students/'+str(username)
	r = requests.get(reservationURI,auth=(token,""),verify=False)
	student_dict = ast.literal_eval(r.text)
	if(student_dict['reservation_url'] == ""):
		return False
	else:
		return True


'''Returns a users locker'''		
def get_locker(username,token):
	reservationURI = 'https://lockit.cs.uct.ac.za/api/v1/students/'+str(username)
	r = requests.get(reservationURI,auth=(token,""),verify=False)
	student_dict = ast.literal_eval(r.text)	
	locker = student_dict['reservation_url']
	r = requests.get(locker,auth=(token,""),verify=False)
	user = ast.literal_eval(r.text)
	return user['locker']


'''Opens the config file'''
def open_file():
	config_file = open('config.txt','r')
	lines = config_file.readlines()
	config_file.close()
	return lines
	
'''Returns a list of GPIO pins used for the locks'''
def get_pins():
	lines = open_file()
	pin_array = []
	for line in lines:
		if(line == ''):
			continue
		else:
			if(not line[0].isnumeric()):
				line = line[line.find('=')+1:].strip()
				pin_array.append(line)
	return pin_array


'''Returns a list of locks installed'''	
def get_lockers():
	lines = open_file()
	locker_array = []
	for line in lines:
		if(line == ''):
			continue
		else:
			if(line[0].isnumeric()):
				line = line[line.find('=')+1:].strip()
				locker_array.append(line)
	return locker_array			
				 
	


		



	


		

	

