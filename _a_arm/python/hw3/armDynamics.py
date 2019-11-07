import numpy as np 
import random
import armParam as P


class armDynamics:
    def __init__(self):
        # Initial state conditions
        self.state = np.array([
            [P.theta0],      # initial angle
            [P.thetadot0]
        ])  # initial angular rate
        #################################################
        # The parameters for any physical system are never known exactly.  Feedback
        # systems need to be designed to be robust to this uncertainty.  In the simulation
        # we model uncertainty by changing the physical parameters by a uniform random variable
        # that represents alpha*100 % of the parameter, i.e., alpha = 0.2, means that the parameter
        # may change by up to 20%.  A different parameter value is chosen every time the simulation
        # is run.
        alpha = 0.2  # Uncertainty parameter
        self.m = P.m * (1.+alpha*(2.*np.random.rand()-1.))  # Mass of the arm, kg
        self.ell = P.ell * (1.+alpha*(2.*np.random.rand()-1.))  # Length of the arm, m
        self.b = P.b * (1.+alpha*(2.*np.random.rand()-1.))  # Damping coefficient, Ns
        self.g = P.g  # the gravity constant is well known and so we don't change it.
        self.Ts = P.Ts  # sample rate at which the dynamics are propagated
        self.torque_limit = P.tau_max

    def update(self, u):
        # This is the external method that takes the input u at time
        # t and returns the output y at time t.
        # saturate the input torque
        u = self.saturate(u, self.torque_limit)
        self.rk4_step(u)  # propagate the state by one time sample
        y = self.h()  # return the corresponding output
        return y

    def f(self, state, tau):
        # Return xdot = f(x,u), the system state update equations
        # re-label states for readability
        theta = state.item(0)
        thetadot = state.item(1)
        xdot = np.array([
            [thetadot],
            [(3.0/self.m/self.ell**2) *
             (tau - self.b*thetadot
              - self.m*self.g*self.ell/2.0*np.cos(theta))],
        ])
        return xdot

    def h(self):
        # return the output equations
        # could also use input u if needed
        theta = self.state.item(0)
        y = np.array([
            [theta],
        ])
        return y

    def rk4_step(self, u):
        # Integrate ODE using Runge-Kutta RK4 algorithm
        F1 = self.f(self.state, u)
        F2 = self.f(self.state + self.Ts / 2 * F1, u)
        F3 = self.f(self.state + self.Ts / 2 * F2, u)
        F4 = self.f(self.state + self.Ts * F3, u)
        self.state += self.Ts / 6 * (F1 + 2 * F2 + 2 * F3 + F4)

    def saturate(self, u, limit):
        if abs(u) > limit:
            u = limit*np.sign(u)
        return u