import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Initialize the figure and axis
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot([], [], 'r-')  # Create an empty line object

# Set axis limits so the plot doesn't compress automatically
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)

def update(frame):
    # Simulate receiving new data points (e.g., from a sensor or API)
    x_data.append(frame)
    y_data.append(random.uniform(1, 9))
    
    # Keep the visible window moving once data exceeds limits
    if frame > 100:
        ax.set_xlim(frame - 100, frame)
        
    # Update the data of the existing line object (highly efficient)
    line.set_data(x_data, y_data)
    return line,

# Secret sauce: call FuncAnimation to refresh every 100 milliseconds
ani = FuncAnimation(fig, update, frames=range(200), interval=100, blit=True)

plt.show()
