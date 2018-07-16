from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
import math
import random


# Some global variabes, angle in rad
min_steer = -np.pi/6
max_steer = np.pi/6

inf = np.inf

'''
    Bicycle Car Dynamic model. 
    State represetned by [xg, yg, theta, vy, r], where: 
        xg, yg are the location center of gravity of the car
        theta is orientation of the car
        vy is the lateral speed
        r is the yaw rate/angular velocity

        longitudinal speed vx is viewed as a constant in this model
    Inputs: Xn - current state; a list
            delta_f - steering angle of the car
    Output: dydt
    NOTE: The difference of this model to Car_Dynamic model is that: 
            this model gets rid of cos and sin terms in vy_dot 
            and r_dot by using small angle approximation. 

            But for xg_dot and yg_dot, trignometry terms remain; I am 
            still not sure if this can be seen as a linear model. 
'''
def Car_Linear(Xn, delta_f):
    # Obtain vairables
    xg, yg, theta, vy, r = Xn
    xg = float(xg)
    yg = float(yg)
    theta = float(theta)
    vy = float(vy)
    r = float(r)

    # Some constants; NOTE: subject to variation if a better configuration is found
    # mass of the car, unit: kg
    m = 1500
    # longitudinal velocity, unit: m/s
    vx = 20
    # length of front half of the car, unit: m
    Lf = 1.3
    # length of rear half of the car, unit: m
    Lr = 1.7
    # cornering stiffness coefficient
    Cf = 10000
    Cr = 12000

    # moment of inertia
    Iz = 6000

    cosTheta = np.cos(theta)
    sinTheta = np.sin(theta)

    A = -(Cf+Cr)/(m*vx)
    B = (-Lf*Cf + Lr*Cr)/(m*vx) - vx
    C = (-Lf*Cf + Lr*Cr)/(Iz*vx)
    D = -(Lf*Lf*Cf + Lr*Lr*Cr)/(Iz*vx)
    E = Cf/m
    F = Lf*Iz/m

    xg_dot = vx*cosTheta - vy*sinTheta
    yg_dot = vx*sinTheta + vy*cosTheta
    theta_dot = r
    vy_dot = A*vy + B*r + E*delta_f
    r_dot = C*vy + D*r + F*delta_f

    # Return dy/dt
    dydt = np.array([float(xg_dot), float(yg_dot), float(theta_dot), float(vy_dot), float(r_dot)])
    return dydt 

'''
    randomConfig: this function generates a random point on the space Xfree
    Inputs: height - height of the screen
            width - width of the screen
    Output: a random configuration on the space Xfree
'''
def randomConfig(height, width):
    x = random.random()*width
    y = random.random()*height
    theta = random.random()*2*np.pi
   
    return (x, y, theta, 0, 0)

'''
    This function uses Fourth-Order Runge-Kutta method to calculate next state.
    Inputs: Xn - current state; a list
            delta_f - steering angle of the car 
    Output: Xnew - next state given current state
        
'''
def newState(Xn, delta_f):
    # Fourth-Order Runge-Kutta method
    k1 = Car_Linear(Xn, delta_f)
    k2 = Car_Linear(Xn+k1/2, delta_f)
    k3 = Car_Linear(Xn+k2/2, delta_f)
    k4 = Car_Linear(Xn+k3, delta_f)
    delta_t = 0.2
    Xnew = Xn + (k1 + 2*k2 + 2*k3 + k4)*delta_t/6
    Xnew = [float(Xnew[0]), float(Xnew[1]), float(Xnew[2]), float(Xnew[3]), float(Xnew[4])]
    return Xnew

'''
    This function is calculate the next state for the vehicle dynamics. 
    It tries out the delta_f from min_steer angle to max_steer angle to 
    get the best state available via newState() function. 
    Inputs: Xrand - the random state generated by randomConfig
            Xnear - the nearest state in RRT search tree to Xrand
    Output: the best next state available 
'''
def selectInput(Xrand, Xnear, obs):
    delta_f = min_steer
    bestState = None
    bestDistance = inf
    
    # Loop delta_f from min_steer angle to max_steer 
    while delta_f < max_steer:
        Xnew = newState(Xnear, delta_f)
        # tmp = False
        # for ob in obs:
        #     if distanceChecker(Xnew, ob):
        #         tmp = True
        # if tmp == True:
        #     delta_f += np.pi/60
        #     continue
        distance = dist(Xnew, Xrand)
        if  distance < bestDistance:
            bestState = Xnew
            bestDistance = distance
        delta_f += np.pi/60 # increment of approximately 3 degrees per iteration
            
    return bestState

    # Helper Functions
'''
    This function returns the distance between two given states
    It uses Euclidean distance
'''
def dist(s1, s2):
    x1 = s1[0]
    y1 = s1[1]

    x2 = s2[0]
    y2 = s2[1]
    return np.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

'''
    This function tries out all possible inputs at a given node Xn to 
    calculate all possible outputs

    Inputs: Xn - the state xg, yg, theta, vy, r of the Xn node
    Output: ret - all possible outcomes of Xn with all possible inputs u
'''
def tryInput(Xn):
    delta_f = min_steer
    ret = []
    # Loop delta_f from min_steer angle to max_steer 
    while delta_f < max_steer:
        Xnew = newState(Xn, delta_f)
        delta_f += np.pi/60 # increment of approximately 3 degrees per iteration
        ret.append(Xnew)
    return ret




# -------------------------------- Simulator for test only ---------------------------------





'''
    This simulator is for test only 
    NOTE: need to add 't' argument in the above Car_Dynamic function to perform test
'''
def TC_Simulate(Mode, initial, time_bound):
    time_step = 0.05
    time_bound = float(time_bound)
    initial = [float(tmp)  for tmp in initial]
    number_points = int(np.ceil(time_bound/time_step))
    t = [i*time_step for i in range(0,number_points)]
    if t[-1] != time_step:
		t.append(time_bound)

    newt = [] 
    for step in t:
        newt.append(float(format(step, '.2f')))
    t = newt
    delta = 0
    sol = odeint(Car_Linear, initial, t, args=(delta,), hmax=time_step)

    # Construct the final output
    trace = []
    for j in range(len(t)):
        tmp = []
        tmp.append(t[j])
        tmp.append(float(sol[j, 0]))
        tmp.append(float(sol[j, 1]))
        tmp.append(float(sol[j, 2]))
        tmp.append(float(sol[j, 3]))
        tmp.append(float(sol[j, 4]))
        trace.append(tmp)
    return trace        

if __name__ == "__main__":
	sol = TC_Simulate('Default', [5.0, 5.0, 0, 10, 0], 20)
        for s in sol:
            print s
        a = [row[1] for row in sol]
        b = [row[2] for row in sol]
    
        plt.plot(a, b, '-r')
        plt.show()

