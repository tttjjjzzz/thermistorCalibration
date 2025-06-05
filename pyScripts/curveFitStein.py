import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

fileName = "thermistor_data.csv"  
dataFrame = pd.read_csv(fileName, header=None, names=["Resistance", "Temperature"])  #

R = dataFrame["Resistance"].values
T = dataFrame["Temperature"].values  

minTemp = 25  
maxTemp = 27  


dataFrame_filtered = dataFrame[(dataFrame["Temperature"] > minTemp) & (dataFrame["Temperature"] < maxTemp)]
R_filtered = dataFrame_filtered["Resistance"].values
T_filtered = dataFrame_filtered["Temperature"].values


T_kelvin = T_filtered + 273.15


def steinhart_hart(R, A, B, C):
    return 1 / (A + B * np.log(R) + C * (np.log(R))**3)


initial_guess = [1e-3, 1e-4, 1e-7]  # Initial estimates for A, B, C
params, covariance = curve_fit(steinhart_hart, R_filtered, T_kelvin, p0=initial_guess)
A, B, C = params


T_fit = np.linspace(min(T_filtered), max(T_filtered), 500)
R_fit = np.exp(((1/T_fit) - A) / (B + C * np.log(T_fit)**2))


plt.scatter(T_filtered, R_filtered, label="data", color="blue", s=10)
plt.plot(T_fit, R_fit, label="Steinhart-Hart fit", color="red", linewidth=2)
plt.xlabel("Temperature (C)")
plt.ylabel("Resistance (Ohms)")
plt.legend()
plt.title("Thermistor Steinhart-Hart Fit")
plt.grid()


plt.show()


print(f"Steinhart-Hart Coefficients: A={A:.6e}, B={B:.6e}, C={C:.6e}")


coefFileName = 'steinhart_hart_coefficients.txt'
with open(coefFileName, 'w') as f:
    f.write("Steinhart-Hart Coefficients:\n")
    f.write(f"A: {A:.6e}\n")
    f.write(f"B: {B:.6e}\n")
    f.write(f"C: {C:.6e}\n")

print(f"Steinhart-Hart coefficients saved to {coefFileName}.")
