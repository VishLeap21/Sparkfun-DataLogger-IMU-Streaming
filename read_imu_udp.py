import socket
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


# UDP settings
UDP_PORTS = [1231, 1232, 1233, 1234]
UDP_IP = "0.0.0.0"    # Listen on all available IP addresses
TIMEOUT = 0.01        # Timeout in seconds for non-blocking

# Set up sockets for all IMUs
sockets = []
for port in UDP_PORTS:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, port))
    sock.settimeout(TIMEOUT)
    sockets.append(sock)

# Buffer length for history
buffer_length = 500  # Reduced buffer size for faster updates

# Data buffers for binary outputs from all IMUs
binary_outputs = [np.zeros(buffer_length) for _ in range(4)]

# Set up the plot
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# Plot setup for binary outputs
ax.set_title("Sequence of Touching of Toys")
ax.set_xlim(0, buffer_length)
ax.set_ylim(-0.25, 1.25)  # Scale y-axis for binary values (0 or 1)
# ax.set_ylabel("Touching or Not")
ax.get_xaxis().set_visible(False)  # Hide the x-axis ticks

# Replace y-axis numbers with custom labels
ax.set_yticks([0, 1])  # Positions for "Stationary" and "Touching"
ax.set_yticklabels(["Stationary", "Moving"])  # Custom text labels


# Create plot lines for all IMUs
colors = ['turquoise', 'lime', 'purple', 'red']
toy_labels = ['Ball', 'Cube', 'Ball', 'Cube' ]
lines = [
    ax.plot(binary_outputs[i], label=toy_labels[i], color=colors[i], linewidth=3)[0]
    for i in range(4)
]
ax.legend(loc="upper right")

# Threshold for binary output
threshold = 5

def update_plot(frame):
    global binary_outputs

    for i, sock in enumerate(sockets):
        try:
            data, _ = sock.recvfrom(1024)
            values = data.decode().split(",")

            if len(values) == 3:  # Expecting exactly 6 values (accel + gyro)
                gyro_x = float(values[0])
                gyro_y = float(values[1])
                gyro_z = float(values[2])
                magnitude = (gyro_x**2 + gyro_y**2 + gyro_z**2)**0.5

                # Determine binary output (1 if above threshold, 0 otherwise)
                binary_value = 1 if magnitude > threshold else 0

                # Shift all values one position to the left (rolling buffer)
                binary_outputs[i] = np.roll(binary_outputs[i], -1)
                binary_outputs[i][-1] = binary_value

                # Update the plot line for the current IMU
                lines[i].set_ydata(binary_outputs[i])

        except socket.timeout:
            pass  # No data received; continue

        except Exception as e:
            print(f"Error with IMU {i + 1}: {e}")

    return lines

# Animate the plot with a rolling buffer
ani = FuncAnimation(fig, update_plot, interval=20)  # Reduced interval for faster updates
plt.tight_layout()
plt.show()
