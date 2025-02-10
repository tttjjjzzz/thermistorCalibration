import serial
import csv
import time

# Change the COM port and baud rate to match your Arduino setup
ser = serial.Serial('/dev/cu.usbserial-2130', 9600, timeout=1)  # Replace with your actual port
time.sleep(2)  # Allow time for the serial connection to initialize

# Open a CSV file for writing (without headers)
with open('thermistor_data.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()  # Read a line from serial
            if line:  
                writer.writerow([float(line.split(',')[0]), float(line.split(',')[1])])  # Write the raw serial data to the CSV file
                print(line)  # Print the same data to the console

    except KeyboardInterrupt:
        print("Data collection stopped.")

ser.close()  # Close the serial connection
