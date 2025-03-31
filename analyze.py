# This file analyzes and visualizes data from the simulation.
# It uses NumPy to load data and Matplotlib to create plots for sensor values and motor target angles.

import numpy as numpy  # Import NumPy for numerical operations
import matplotlib.pyplot as plt  # Import Matplotlib for plotting

# Uncomment the following lines to analyze and plot sensor values for the back and front legs
# backLegSensorValues = numpy.load("data/back_leg_sensor_values.npy")  # Load back leg sensor values from file
# frontLegSensorValues = numpy.load("data/front_leg_sensor_values.npy")  # Load front leg sensor values from file

# Plot the sensor values for the back and front legs
# plt.plot(backLegSensorValues, label="Back Leg Sensor Values", linewidth=3)  # Plot back leg sensor values
# plt.plot(frontLegSensorValues, label="Front Leg Sensor Values")  # Plot front leg sensor values
# plt.title("Back Leg and Front Leg Sensor Values")  # Add a title to the plot
# plt.legend()  # Add a legend to the plot
# plt.savefig("plot.png", dpi=300, bbox_inches='tight')  # Save the plot as a PNG file
# plt.show()  # Display the plot

# Load motor target angles from file
targetAngles = numpy.loadtxt("data/target_angles.txt")  # Load motor target angles from a text file

# Create a time axis (same length as targetAngles)
time_steps = numpy.linspace(0, 2 * numpy.pi, len(targetAngles))  # Generate time steps for the x-axis

# Plot the sinusoidal motor target angles
plt.plot(time_steps, targetAngles, label="Motor Target Angles", linewidth=3)  # Plot motor target angles

# Formatting the plot
plt.xlabel("Time Steps")  # Label the x-axis
plt.ylabel("Target Angle (radians)")  # Label the y-axis
plt.title("Sinusoidal Motor Target Angles")  # Add a title to the plot
plt.legend()  # Add a legend to the plot
plt.grid(True)  # Add a grid to the plot

# Save and display the plot
plt.savefig("data/motor_plot.png", dpi=300, bbox_inches='tight')  # Save the plot as a PNG file
plt.show()  # Display the plot
