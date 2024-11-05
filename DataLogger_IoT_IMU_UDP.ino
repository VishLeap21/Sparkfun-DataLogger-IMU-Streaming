#include <WiFi.h>
#include <WiFiUDP.h>
#include <SPI.h>
#include "SparkFun_ISM330DHCX.h"

// Wi-Fi credentials
const char* ssid = "SSID";
const char* password = "Password";

// UDP settings
WiFiUDP udp;
const char* udpAddress = "192.168.0.8"; // IP address of the receiving computer
const int udpPort = 1233;               // Port number of the receiving computer


// SPI instance class call
SparkFun_ISM330DHCX_SPI myISM; 

// Structs for X,Y,Z data
sfe_ism_data_t accelData; 
sfe_ism_data_t gyroData; 

// Set your chip select pin according to your setup. 
byte chipSelect = 5;

void setup(){

	SPI.begin();

	Serial.begin(115200);
	pinMode(chipSelect, OUTPUT);
	digitalWrite(chipSelect, HIGH);


	if( !myISM.begin(chipSelect) ){
		Serial.println("Did not begin.");
	  while(1);
	}

  // Connect to Wi-Fi 
  Serial.print("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected.");

  // Start UDP
  udp.begin(udpPort);
  Serial.println("UDP connection started");

	// Reset the device to default settings. This if helpful is you're doing multiple
	// uploads testing different settings. 
	myISM.deviceReset();

	// Wait for it to finish reseting
	while( !myISM.getDeviceReset() ){ 
		delay(1);
	} 

	Serial.println("Reset.");
	Serial.println("Applying settings.");
	delay(100);
	
	myISM.setDeviceConfig();
	myISM.setBlockDataUpdate();
	
	// Set the output data rate and precision of the accelerometer
	myISM.setAccelDataRate(ISM_XL_ODR_104Hz);
	myISM.setAccelFullScale(ISM_4g); 

	// Set the output data rate and precision of the gyroscope
	myISM.setGyroDataRate(ISM_GY_ODR_104Hz);
	myISM.setGyroFullScale(ISM_500dps); 

	// Turn on the accelerometer's filter and apply settings. 
	myISM.setAccelFilterLP2();
	myISM.setAccelSlopeFilter(ISM_LP_ODR_DIV_100);

	// Turn on the gyroscope's filter and apply settings. 
	myISM.setGyroFilterLP1();
	myISM.setGyroLP1Bandwidth(ISM_MEDIUM);
}

void loop(){

	// Check if both gyroscope and accelerometer data is available.
	if( myISM.checkStatus() ){
    myISM.getAccel(&accelData);
		myISM.getGyro(&gyroData);
    
    // Prepare data message to send over UDP
    String message = String(accelData.xData) + "," + String(accelData.yData) + "," + String(accelData.zData) + "," + String(gyroData.xData) + "," + String(gyroData.yData) + "," + String(gyroData.zData);

    // Send the data over UDP
    udp.beginPacket(udpAddress, udpPort);
    udp.print(message);
    udp.endPacket();

    // Print data to Serial Monitor for debugging
    Serial.println("Sent IMU data - " + message);
	}

	delay(100);
}
