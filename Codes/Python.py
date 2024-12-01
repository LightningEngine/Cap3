import serial
import time
import schedule
import csv

list_values = []
list_in_float = []

def main_func():
    
    err = False
    rowcount = 0
    arduino = serial.Serial('com8', 9600)
    print('Arduino connected succesfully')
    arduino_data = arduino.readline()
    
    csvfile = open("CSV.csv",'a',newline='')
    writer = csv.writer(csvfile)

    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('x')
    #try:
    #    if float(list_values[0]):
    #        print(list_values[0])
    #except ValueError:
    #    print("???")
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

schedule.every(2).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)