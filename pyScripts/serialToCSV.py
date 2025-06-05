## THis py script reads from serial input (connected to microcontroller)
## writes raw serial data into a csv file. CSV file uses other script for data processing
## data processing -> curve fit -> thermistor calibration




import serial
import csv
import time

# configure com port and baud rate MATC microcontrollerf
#this will depednd on computer used
ser = serial.Serial('/dev/cu.usbmodem1201', 9600, timeout=1)  
time.sleep(2)  #give time to initrlizzie


input("press enter to start test...") #user input press enter to start script 

# open csv , no headres in mine from MC
with open('thermistor_data.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # read line from serial input
            if line:  
                writer.writerow([float(line.split(',')[0]), float(line.split(',')[1])])  # write serial data to CSV file
                print(line)  # also print to console to see data read

    except KeyboardInterrupt:
        print("Data collection stopped.")

ser.close()  # terminate serial connection and stop reading data
