import sys
import subprocess
import matplotlib.pyplot as plt
import threading

# Determine if the OS is Windows
assert sys.platform == 'win32', 'This code runs on Windows only'

# Define PowerShell script
script = r"""
netsh.exe wlan show interfaces |
    Select-String "Signal" |
    ForEach-Object { $_ -replace '\D+(\d+)%.*', '$1' }
"""

# Variables
x = 0

def get_signal_strength():
    """Return the signal strength of the Wi-Fi connection in percent."""
    process = subprocess.Popen(['powershell.exe', '-Command', script], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    signal_strength = int(output.decode().strip())
    return signal_strength

# Initialize empty lists to store data
x_data = []
y_data = []

# Create the figure and axis objects
fig, ax = plt.subplots()

# Create the initial empty plot
line, = ax.plot(x_data, y_data)

# Set the axis labels and title
ax.set_xlabel('Time (s)')
ax.set_ylabel('Wi-Fi Signal Strength (%)')
ax.set_title('Wi-Fi Signal Strength')

# Function to update the graph
def update_graph():
    # Generate 
    global x
    y = get_signal_strength()

    # Append the new data to the lists
    x_data.append(x)
    y_data.append(y)

    # Update the plot data
    line.set_data(x_data, y_data)

    # Adjust the plot limits
    ax.relim()
    ax.autoscale_view()

    # Redraw the plot
    fig.canvas.draw()

    # Call the update_graph function again after 500 milliseconds
    threading.Timer(0.5, update_graph).start()
    x+=0.5

# Start the initial update
update_graph()

# Show the plot
plt.show()