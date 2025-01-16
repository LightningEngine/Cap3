import serial
import time
import schedule
import csv
import pandas as pd
from matplotlib import pyplot as pt
import matplotlib.animation as animation

fig, (ax1, ax2, ax3) = pt.subplots(1,3)
list_values = []
list_in_float = []
shelflife = 10368000
shelflife2 = 0
time = 30

def ConvertSectoDay(n): 
    day = n // (24 * 3600) 
    n = n % (24 * 3600) 
    hour = n // 3600
    n %= 3600
    minutes = n // 60
    n %= 60
    seconds = n // 1
    return(str(day)+"days "+str(hour)+"hours "+str(minutes)+"minutes "+str(seconds)+"seconds ") 

def Animate(i):
    global shelflife
    global shelflife2
    global time
    
    
    err = False  #Used to stop writing in the CSV if there was an error
    rowcount = 0  #Gets the number of rows of the current CSV file
    arduino = serial.Serial('com11', 9600)  #Connects to Arduino UNO's serial
    print('Arduino connected succesfully')
    arduino_data = arduino.readline()  #Reads the last line in the Arduino serial
    
    csvfile = open("CSV.csv",'a',newline='')  #Opens the CSV file
    writer = csv.writer(csvfile)  #It is used to insert data to the CSV file

    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))  #Decodes the Arduino data and transforms it into a string
    list_values = decoded_values.split('x')  #Splits the values that were read into 3 values divided by 'x'

    if(float(list_values[0])>60):
        err = True
    for item in list_values:
        if item and err == False:  # Check if item is not empty
            list_in_float.append(float(item))
        else:
            print(f"Warning: Could not convert '{item}' to float.")
            err = True

    for row in open("CSV.csv"): 
        rowcount+= 1
    if err == False:
        list_in_float.insert(0, rowcount)
        writer.writerow(list_in_float)
    arduino.data = 0
    list_values.clear()
    list_in_float.clear()
    arduino.close()
    csvfile.close()
    
    
    Pyes = 0  #Used to get if the pressure exceeded the threshold or not
    #clear each axes for updating
    ax1.clear()
    ax2.clear()
    ax3.clear()
    #read the CSV file
    Cf = pd.read_csv('CSV.csv')
    lastrow = Cf.iloc[-1].tolist()
    print(lastrow)
    #Get each value for time, temperature, humidity, pressure
    i = Cf['Index']  #Time
    t = Cf['t']  #Temperature
    h = Cf['h']  #Humidity
    p = Cf['p']  #Pressure
    #Draw the graphs for each value using time as the x-axis
    if lastrow[1] < 4:
        ax1.plot(i,t,'g')
        ax1.set_ylabel('Temperature[Safe]')
    else:
        ax1.plot(i,t,'r')
        ax1.set_ylabel('Temperature[Danger]')
    
    if lastrow[2] > 90:
        ax2.plot(i,h,'g')
        ax2.set_ylabel('Humidity[Safe]')
    else:
        ax2.plot(i,h,'r')
        ax2.set_ylabel('Humidity[Danger]')
    
    if lastrow[3] < 0.933:
        ax3.plot(i,p,'g')
        ax3.set_ylabel('Pressure[Safe]')
        Pyes = 1
    else:
        ax3.plot(i,p,'r')
        ax3.set_ylabel('Pressure[Danger]')
        Pyes = 0
    #shelflife calculations
    factorT=2**((4-lastrow[1])/10)
    factorH=1-((95-lastrow[2])/100)
    factorP=(100+(20*Pyes))/100
    shelflife2=shelflife*factorT*factorH*factorP - time
    shelflife=shelflife2/(factorT*factorH*factorP)
    #Error bars that change in size according to accurancy
    ax1.errorbar(i,t,0.5,None,ecolor='black',errorevery=20,fmt=' ')
    ax2.errorbar(i,h,2,None,ecolor='black',errorevery=20,fmt=' ')
    ax3.errorbar(i,p,0.001,None,ecolor='black',errorevery=20,fmt=' ')
    #labels for the x-axis that is time
    ax1.set_xlabel('Time/30')
    ax2.set_xlabel('Time/30')
    ax3.set_xlabel('Time/30')
    #Setting the limits for the graphs
    ax1.set_ylim(ymin=0,ymax=75)
    ax2.set_ylim(ymin=0,ymax=100)
    ax3.set_ylim(ymin=0,ymax=1.25)
    #Name for the figure
    fig.suptitle("Time left: "+ConvertSectoDay(shelflife2))

    
    

ani = animation.FuncAnimation(fig, Animate, interval=time*1000)
pt.show()

while True:
    schedule.run_pending()
    time.sleep(1)
