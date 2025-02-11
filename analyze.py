import numpy as numpy
import matplotlib.pyplot as plt

backLegSensorValues = numpy.load("data/back_leg_sensor_values.npy")
frontLegSensorValues = numpy.load("data/front_leg_sensor_values.npy")


plt.plot(backLegSensorValues, label="back Leg sensor values", linewidth=3)
plt.plot(frontLegSensorValues, label="front Leg sensor values")
plt.title("Back leg and front leg sensor values")
plt.legend()
plt.savefig("plot.png", dpi=300, bbox_inches='tight')
plt.show()
