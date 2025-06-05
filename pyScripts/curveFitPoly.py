import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

fileName = "thermistor_data.csv"  #set file name, which is the other script in this directory
dataFrame = pd.read_csv(fileName, header = None, names =[ "Resistance", "Temperature"]) #read the csv file
                                #no header in csv       set names of column

#extract values from each column
R = dataFrame["Resistance"].values #resistance in ohms
T = dataFrame["Temperature"].values  # Temperature in C

minTemp = 25 #define minimum and maximum temperatures to filter out "outliers"
maxTemp = 27 

# Filter the data based on the custom range
dataFrame_filtered= dataFrame[(dataFrame["Temperature"] > minTemp) & (dataFrame["Temperature"] < maxTemp)]
R_filtered = dataFrame_filtered["Resistance"].values
T_filtered = dataFrame_filtered["Temperature"].values



degree = 4 #polynomial degree
#T and R are vectors
coeffs = np.polyfit(T_filtered, R_filtered, degree) #extract coefficients 

# generate fitted scale for T and R
T_fit = np.linspace(min(T_filtered), max(T_filtered), 500) #500 points between min and max value in T
R_fit = np.polyval(coeffs, T_fit)       

# Plot results
plt.scatter(T_filtered, R_filtered, label="data", color="blue", s=10)
plt.plot(T_fit, R_fit, label=f"polynomial fit (degree {degree})", color="red", linewidth=2)
plt.xlabel("temperature C")
plt.ylabel("resistance Ohms")
plt.legend()
plt.title(f"thermistor polynomial fit (degree {degree})")
plt.grid()

# displauy plot
plt.show()

# print polynomial coeffs
print(f"Polynomial Coefficients: {coeffs}")

# save polynomial coeffs to a text file
coefFileName = 'polynomial_coefficients.txt'
with open(coefFileName, 'w') as f:
    f.write("Polynomial Coefficients:\n")
    for i, coeff in enumerate(coeffs):
        f.write(f"Coefficient of T^{degree-i}: {coeff:.6f}\n")

print(f"Polynomial coefficients saved to {coefFileName}.")
