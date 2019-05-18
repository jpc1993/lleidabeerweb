#!/usr/bin/python
import time
import sqlite3
from datetime import date, datetime
import random

def sensortemp(temperaturabirra,temperaturaferm,heater):
	valorAleatoriferm = random.randint(0,5)*0.85
	valorAleatoribirra = random.randint(-2,2)*0.93
	if heater=='OFF'and (temperaturaferm >=20):
		temperaturaferm = temperaturaferm - valorAleatoriferm
	elif heater=='ON':
		temperaturaferm = temperaturaferm + valorAleatoriferm
	
	temperaturabirra = temperaturabirra + valorAleatoribirra
	
	return  temperaturabirra,temperaturaferm

def sensorflow(capaciferm,capacibeer,valvuferm,valvubeer):
	
	if (valvuferm=='ON') and (capaciferm >=0):
		capaciferm=capaciferm-0.2
		capacibeer=capacibeer+0.2
	
	if valvubeer=='ON' and (capacibeer >=0):
		capacibeer=capacibeer-0.5
	
	return  capaciferm, capacibeer

def simulador():
	conn = sqlite3.connect('lleidabeer.db')
	llista =[]
	cursor = conn.execute("SELECT tdate,ttime,tempbeer,tempferm,capferm,capbeer,mixer,heater,valferm,valbeer from sensors")	
	time = datetime.now().strftime("%H:%M:%S")
	for row in cursor:
		llista.append(row)
		llista = llista[-1:]

	time = datetime.now().strftime("%H:%M:%S")
	data= date.today()	
	mix = llista[0][6]
	heat = llista[0][7]
	valvuferm = llista[0][8]
	valvubeer = llista[0][9]
	temperaturabirra = llista[0][2]
	temperaturaferm = llista[0][3]
	capaciferm = llista[0][4]
	capacibeer = llista[0][5]

	temperatures=sensortemp(temperaturabirra,temperaturaferm,heat)
	temperaturabirra=temperatures[0]
	temperaturaferm =temperatures[1]

	flows=sensorflow(capaciferm,capacibeer,valvuferm,valvubeer)
	capaciferm=flows[0]
	capacibeer=flows[1]	
	
	cursor = conn.execute("insert into sensors (tdate,ttime,tempbeer,tempferm,capferm,capbeer,mixer,heater,valferm,valbeer) values (?,?,?,?,?,?,?,?,?,?)",(data,time,temperaturabirra,temperaturaferm,capaciferm,capacibeer,mix,heat,valvuferm,valvubeer))
	conn.commit()
	conn.close()
	return 

while True:		
	a= simulador()
	time.sleep(5)
	print ('Running...')












	
		







