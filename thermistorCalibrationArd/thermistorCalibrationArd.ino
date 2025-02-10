#include <Wire.h>

#define lm75a_add 0x48 // temperature register address of lm75a
#define numThermistors 3 


const int ntcPin = A0;

// Reference resistor value (should be precision 1% or better)
const float rRef = 10000.0; // 10kΩ reference resistor

// ADC voltage (adjust if using ESP32 with different attenuation)
const float vSupp = 5;  

void setup() {
    Serial.begin(9600);
    Wire.begin(); // Start I2C communication
}

void loop() {
    // Read temperature from LM75A
    float tempC = readLM75A();

    // Read and calculate resistance for each thermistor
    float vOut = analogRead(ntcPin) * (vSupp / 1023.0); // convert ADC value to voltage. since arduino uno adc is 10 bit resolution, there are 1024 discrete values, so 1023 is max
                                                    //adc valkue of 1023 would correspond to 
    float rNTC = rRef * ((vSupp / vOut) - 1.0); // Calculate thermistor resistance

    Serial.print(rNTC);
    Serial.print(",");
    Serial.print(tempC);
    Serial.println();
    delay(200); // Wait before next reading
}


// Function to read LM75A temperature sensor
float readLM75A() {
    Wire.beginTransmission(lm75a_add);
    Wire.write(0x00); // Temperature register
    Wire.endTransmission();
    Wire.requestFrom(lm75a_add, 2); // Read 2 bytes

    if (Wire.available() == 2) {
        int16_t rawTemp = (Wire.read() << 8) | Wire.read(); 
        return rawTemp / 256.0; // Convert to °C
    }
    
    return -100.0; // Error value
}
