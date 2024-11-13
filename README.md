# Sparkfun DataLogger IoT IMU Data Streaming and Visualization

This repository contains code to stream data from a SparkFun DataLogger IoT 9-DoF IMU to a computer via UDP and visualize it in real-time. The IMU data is transmitted over Wi-Fi using the ESP32 microcontroller on a SparkFun board. The Python code listens for incoming UDP packets on a specified port, processes the IMU gyroscope data, and displays it as a real-time plot.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Hardware Setup](#hardware-setup)
- [Arduino Code](#arduino-code)
- [Python Code](#python-code)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

1. **Arduino IDE**:
   - Download and install the [Arduino IDE](https://www.arduino.cc/en/software).
   - Add the ESP32 board to the Arduino IDE by going to **File > Preferences** and adding the following URL to **Additional Board Manager URLs**:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to **Tools > Board > Board Manager...**, search for "ESP32" by Espressif, and install it.
   - Install the **SparkFun ISM330DHCX** library through **Tools > Manage Libraries...**, and search for "SparkFun ISM330DHCX" to install.

2. **Python 3**:
   - Install Python 3 from [python.org](https://www.python.org/).
   - Ensure `matplotlib` and `argparse` are installed. You can install these using:
     ```bash
     pip install matplotlib argparse
     ```
     or
     ```bash
     conda env create -f IMU_UDP.yml
     ```     


3. **SparkFun IMU Hardware**:
   - A SparkFun DataLogger IoT 9-DoF or similar ESP32-based board with an ISM330DHCX IMU.

---

## Hardware Setup

1. **Wiring**:
   - Connect the SparkFun ESP32 DataLogger to your computer via USB.
   - Ensure your board is set up to connect to a Wi-Fi network for transmitting data.

2. **Wi-Fi Setup**:
   - In the Arduino code, replace `"YOUR_SSID"` and `"YOUR_PASSWORD"` with your Wi-Fi credentials.

---

## Arduino Code

1. **Upload the Code**:
   - Open the Arduino code in this repository in the Arduino IDE.
   - Select your board and port:
     - Go to **Tools > Board** and select **SparkFun ESP32 Thing Plus C**.
     - Go to **Tools > Port** and select the port corresponding to your ESP32 board.
   - Click **Upload** to upload the code to the ESP32.

2. **Configuration**:
   - The Arduino code is configured to send IMU data via UDP to a specified IP address and port.
   - By default, it sends data to `192.168.1.100` on port `1234`. Adjust this IP address to match your computer's IP.
   - The code reads from the ISM330DHCX IMU connected using the onboard SPI connection transmits this data via UDP.

---

## Python Code

1. **Setting Up**:
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/VishLeap21/Sparkfun-DataLogger-IMU-Streaming.git
     cd Sparkfun-DataLogger-IMU-Streaming
     ```

2. **Running the Python Script**:
   - Use the command below to run the Python script, specifying the UDP port on which to listen (e.g., `1234`):
     ```bash
     python read_imu_udp.py --port 1234
     ```
   - The script:
     - Listens for UDP packets on the specified port.
     - Decodes the IMU data, calculates the gyroscope magnitude, and plots it in real-time.
     - Changes the plot color if the gyroscope magnitude exceeds a threshold.

---

## Usage

### Starting the System

1. **Start the Arduino Code**:
   - Power up your ESP32 board and ensure it connects to Wi-Fi.
   - The board will begin streaming IMU data to the IP and port configured in the Arduino code.

2. **Run the Python Script**:
   - Start the Python visualization script on your computer using the command shown above.
   - The script will wait for incoming UDP packets from the IMU and display the gyroscope data in a plot.
   - If no data is received initially, the script will print a message indicating it is waiting for data.

3. **Changing Ports**:
   - To change the port used by the Python script, specify a different port using the `--port` option. Ensure the Arduino code matches the same port.

### Expected Behavior

- **Plot**: You should see a real-time plot of the gyroscope magnitude.
- **Color Change**: If the magnitude exceeds a threshold, the plot line changes colour.

---

## Troubleshooting

1. **No Data Received**:
   - Ensure that the ESP32 is connected to Wi-Fi and is streaming to the correct IP address and port.
   - Check your computer's firewall settings, as they may block incoming UDP packets.
   - Verify that the IP address in the Arduino code matches your computer's IP address.

2. **Incorrect Port**:
   - Make sure the Python script is listening on the same port that the ESP32 is transmitting to.
   - You can adjust the port in the Arduino code and specify the matching port with `--port` when running the Python script.

3. **Socket Timeout Errors**:
   - These errors indicate that the Python script isn’t receiving data within the expected timeframe.
   - If the ESP32 stops streaming or loses Wi-Fi connection, the script will wait and periodically print a message indicating it is waiting for data.

4. **Wi-Fi Connection Issues**:
   - Ensure the Wi-Fi credentials in the Arduino code are correct.
   - Try moving the ESP32 closer to the router to improve connectivity.

---

This README should guide you through setting up and using the IMU data streaming and visualization.
