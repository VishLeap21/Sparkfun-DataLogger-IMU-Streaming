import socket
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

# Parse command-line arguments for UDP port
parser = argparse.ArgumentParser(description="Read IMU data from a specified UDP port.")
parser.add_argument(
    "--port", type=int, default=1233, help="UDP port number to listen on (default: 1233)"
)
args = parser.parse_args()
UDP_PORT = args.port

# UDP settings
UDP_IP = "0.0.0.0"    # Listen on all available IP addresses
TIMEOUT = 1.0         # Timeout in seconds

# Set up the socket for receiving UDP packets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(TIMEOUT)  # Set a timeout for the socket

# Buffer length for longer history
buffer_length = 100

# Data buffer for gyroscope magnitude
gyro_magnitude = np.zeros(buffer_length)

# Set up the plot
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot setup for gyroscope magnitude (longer history)
ax.set_title("Gyroscope Magnitude")
ax.set_xlim(0, buffer_length)
ax.set_ylim(-100, 600)  # Fixed Y-axis range
ax.set_ylabel("Degrees per Second")  # Label for the Y-axis
ax.get_xaxis().set_visible(False)  # Hide the x-axis ticks

# Create initial plot line with red color, no label
line_gyro_magnitude, = ax.plot(gyro_magnitude, color='red')

# Threshold for changing color
threshold = 50

# Initial data check for UDP data availability
print(f"Starting program. Waiting for UDP data on port {UDP_PORT}...")
data_available = False
while not data_available:
    try:
        data, _ = sock.recvfrom(1024)  # Attempt to receive data
        data_available = True  # If data is received, mark as available
    except socket.timeout:
        print("No data received yet. Waiting for UDP data...")
        time.sleep(1)  # Wait a moment before checking again

print("UDP data stream detected. Starting plot...")

def update_plot(frame):
    global gyro_magnitude
    
    # Try to receive UDP data
    try:
        data, _ = sock.recvfrom(1024)  # Buffer size is 1024 bytes
        message = data.decode()
        values = message.split(",")

        # Parse values and calculate magnitude for gyroscope data only
        if len(values) == 6:  # Expecting exactly 6 values (accel + gyro)
            # Get the latest gyroscope readings and convert them to floats
            gyro_x = float(values[3]) / 1000  # Gyro X, scaled
            gyro_y = float(values[4]) / 1000  # Gyro Y, scaled
            gyro_z = float(values[5]) / 1000  # Gyro Z, scaled

            # Calculate the magnitude of the gyroscope vector
            magnitude = (gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5

            # Shift all values one position to the left (rolling buffer)
            gyro_magnitude = np.roll(gyro_magnitude, -1)
            gyro_magnitude[-1] = magnitude

            # Check the threshold and set line color
            if magnitude > threshold:
                line_gyro_magnitude.set_color('green')
            else:
                line_gyro_magnitude.set_color('red')

            # Update plot data for gyroscope magnitude
            line_gyro_magnitude.set_ydata(gyro_magnitude)

    except socket.timeout:
        # If no data is received within the timeout period, do nothing
        print("No data received. Waiting for UDP data...")

    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")

    return line_gyro_magnitude,

# Animate the plot with a rolling buffer
ani = FuncAnimation(fig, update_plot, interval=50)
plt.tight_layout()
plt.show()
