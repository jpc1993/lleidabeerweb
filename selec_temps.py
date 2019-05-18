#!/usr/bin/python
from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import date, datetime

app = Flask(__name__) #create the Flask app



@app.route('/')
def Taula_actual():

	conn = sqlite3.connect('lleidabeer.db')
	print("Opened database successfully")	
	llista =[]
	cursor = conn.execute("SELECT tdate,ttime,tempbeer,tempferm,capferm,capbeer,mixer,heater,valferm,valbeer from sensors")
	for row in cursor:
	   llista.append(row)
	#print (llista)   
	print("Operation done successfully")
        llista = llista[-1:]
        
            	
	conn.close()
	return  render_template("page.html",llista=llista)


@app.route('/ftank')
def Taula_ferm():

	conn = sqlite3.connect('lleidabeer.db')
	print("Opened database successfully")	
	llista =[]
	cursor = conn.execute("SELECT tdate,ttime,tempferm,capferm,mixer,heater,valferm from sensors")
	for row in cursor:
	   llista.append(row)
	#print (llista)   
	print("Operation done successfully")

	conn.close()
	return  render_template("fermhistoric.html",llista=llista)


@app.route('/btank')
def Taula_beer():

	conn = sqlite3.connect('lleidabeer.db')
	print("Opened database successfully")	
	llista =[]
	cursor = conn.execute("SELECT tdate,ttime,tempbeer,capbeer,valbeer from sensors")
	for row in cursor:
	   llista.append(row)
	  
	print("Operation done successfully")

	conn.close()
	return  render_template("beerhistoric.html",llista=llista)


@app.route('/relays', methods=['GET','POST'])
def Relays():

	
		
	conn = sqlite3.connect('lleidabeer.db')
	print("Opened database successfully")	
	
	


	if request.method == "GET":
			llista =[]
			cursor = conn.execute("SELECT  tdate,ttime,mixer,heater,valferm,valbeer from sensors")
			for row in cursor:
				llista.append(row)
			   
			print("Operation done successfully")
			llista = llista[-1:]

			conn.close()
			return  render_template("relays.html",llista=llista)


	elif request.method == "POST":
		llista =[]
		cursor = conn.execute("SELECT  tdate,ttime,tempbeer,tempferm,capferm,capbeer,mixer,heater,valferm,valbeer from sensors")	
		for row in cursor:
				llista.append(row)
			
		llista = llista[-1:]

                time = datetime.now().strftime("%H:%M:%S")
		data= date.today()		
 		temperaturabirra = llista[0][2]
		temperaturaferm = llista[0][3]
		capaciferm = llista[0][4]
                capacibeer = llista[0][5]
                mix = llista[0][6]
                heat = llista[0][7]
                valvuferm = llista[0][8]
                valvubeer = llista[0][9]
                

		var='OFF'


		hsname = request.form.get("Heater")
		if hsname== 'OFFH':
			heat= 'OFF'
		if hsname== 'ONH':
				heat='ON'

				
		hsname = request.form.get("Mixer")
		if hsname== 'OFFM':
				mix= 'OFF'
		if hsname== 'ONM':
				mix='ON'

		hsname = request.form.get("Beerval")
		if hsname== 'OFFB':
				valvubeer= 'OFF'
		if hsname== 'ONB':
				valvubeer='ON'
		
		hsname = request.form.get("Fermval")
		if hsname== 'OFFF':
		   	valvuferm= 'OFF'
		if hsname== 'ONF':
			valvuferm='ON'			
		
		cursor = conn.execute("insert into sensors (tdate,ttime,tempbeer,tempferm,capferm,capbeer,mixer,heater,valferm,valbeer) values (?,?,?,?,?,?,?,?,?,?)",(data,time,temperaturabirra,temperaturaferm,capaciferm,capacibeer,mix,heat,valvuferm,valvubeer))
		

		conn.commit()
		conn.close()
		return redirect("/relays")
		














	
		






	

if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000
   
