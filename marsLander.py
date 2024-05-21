import matplotlib.pyplot as plt
import math
from marsatm import marsinit
from marsatm import marsatm

marstable = marsinit()

#constants
g0 = -3.711 #m/s2
Kv = 0.05
CdS = 4.92 #m2
Ve = 4400 #m/s
mZFW = 699.0 #kg
VyRef = -2.0 #m/s
t = 0 #s
dt = 0.01 #s
mDotMax = 5 #kg/s

#initial conditions
h = 20 #km
x = 0 #m
gamma = math.radians(-20) #converting this to radians since math.sin uses radians as the input
V = 262 #m/s
vx = V*math.cos(gamma) #m/s
vy = V*math.sin(gamma) #m/s

#store variables in lists
xTab = []
yTab = []
vTab = []
vyTab = []
vxTab = []
aTab = []
ayTab = []
axTab = []
mDotTab = []
gammaTab = []
tTab = []

mFuel = float(input("Fuel mass [kg]: ")) 
hT = float(input("Burn height [km]: ")) 

def thrust(): #creating a function for thrust
    if (mZFW + mFuel) > mZFW and hT >= h > 0.0003:
        deltaVy = VyRef - vy
        mDot = min(((mZFW + mFuel)*g0/Ve + Kv*deltaVy), mDotMax)
        T = mDot * Ve
    else:
        T = 0
        mDot = 0
    return T, mDot


for i in range(10000): #number of iterations this will run through 
    if h > 0: #making sure that the script stops running if h is less than 0
        #forces
        Fg = (mZFW + mFuel) * g0
        D = 0.5 * CdS * marsatm(h, marstable)[1] * V**2
        T, mDot = thrust()

        #accelerations
        ay = (Fg-(D+T)*math.sin(gamma))/(mZFW + mFuel)
        ax = -(D+T)*math.cos(gamma)/(mZFW + mFuel)
        a = math.sqrt(ay**2 + ax**2)
        #velocities
        vy = vy + ay * dt
        vx = vx + ax * dt
        V = math.sqrt(vy**2 + vx**2)

        gamma = math.atan2(vy,vx) #recalculating the angle
        
        x = x + (vx * dt)/1000 #calculating the x distance
        h = h + (vy * dt)/1000 #calculating the height

        t = t + dt #recalculating the time

        #store values
        vTab.append(V)
        vyTab.append(vy)
        vxTab.append(vx)
        aTab.append(a)
        ayTab.append(ay)
        axTab.append(ax)
        gammaTab.append(math.degrees(gamma))
        yTab.append(h)
        xTab.append(x)
        tTab.append(t)
        mDotTab.append(mDot)
    else:
        break

plt.figure()

plt.subplot(231) #position 1 on a 2x3 matrix 
plt.plot(xTab,yTab) #plot with xtab as the x axis values, ytab as the y values
plt.grid(True) #include a grid
plt.title("Trajectory") #include a title
plt.xlabel('Range (km)') #include an x axis label
plt.ylabel('Altitude (km)') #include a y axis label

plt.subplot(232)
plt.plot(vTab,yTab)
plt.grid(True)
plt.title("Speed")
plt.xlabel('Velocity (m/s)')
plt.ylabel('Altitude (km)')

plt.subplot(233)
plt.plot(tTab,mDotTab)
plt.grid(True)
plt.title("Mdot vs time")
plt.xlabel('Time (s)')
plt.ylabel('Mass flow (kg/s)')

plt.subplot(234)
plt.plot(tTab,yTab)
plt.grid(True)
plt.title("Alt vs time")
plt.xlabel('Time (s)')
plt.ylabel('Altitude (km)')

plt.subplot(235)
plt.plot(tTab, vTab)
plt.grid(True)
plt.title("Spd vs time")
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')

plt.subplot(236)
plt.plot(tTab, gammaTab)
plt.grid(True)
plt.title("Gamma vs time")
plt.xlabel('Time (s)')
plt.ylabel('Flight path angle (deg)')

plt.show()