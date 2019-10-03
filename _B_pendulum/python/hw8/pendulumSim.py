import sys
sys.path.append('..')  # add parent directory
import matplotlib.pyplot as plt
import pendulumParam as P
from hw_b.pendulumDynamics import pendulumDynamics
from pendulumController import pendulumController
from hw_a.signalGenerator import signalGenerator
from hw_a.pendulumAnimation import pendulumAnimation
from hw_a.plotData import plotData

# instantiate pendulum, controller, and reference classes
pendulum = pendulumDynamics()
ctrl = pendulumController()
reference = signalGenerator(amplitude=0.5, frequency=0.02)

# instantiate the simulation plots and animation
dataPlot = plotData()
animation = pendulumAnimation()

t = P.t_start  # time starts at t_start
while t < P.t_end:  # main simulation loop
    # Get referenced inputs from signal generators
    ref_input = reference.square(t)
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot
    while t < t_next_plot: # updates control and dynamics at faster simulation rate
        u = ctrl.update(ref_input, pendulum.state)  # Calculate the control value
        pendulum.update(u)  # Propagate the dynamics
        t = t + P.Ts  # advance time by Ts
    # update animation and data plots
    animation.update(pendulum.state)
    dataPlot.update(t, ref_input, pendulum.state, u)
    plt.pause(0.0001)  # the pause causes the figure to be displayed during the simulation

# Keeps the program from closing until the user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()