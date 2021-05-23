from math import cos, sin
from math import pi as _PI
import matplotlib.pyplot as plt
import numpy as np

_TIMESTEP = 0.001
_GRAV = 1


class Pendulum():
    def __init__(self, t1=0, t2=0, l1=1, l2=1):
        self.t1 = t1
        self.t2 = t2
        self.l1 = l1
        self.l2 = l2
        self.dt1 = 0  # velocities
        self.dt2 = 0
        self.a1 = 0  # accelerations
        self.a2 = 0

    def step(self, step=_TIMESTEP):
        self.a1 = self.acc1()
        self.a2 = self.acc2()
        self.t1 += step*self.dt1
        self.t2 += step*self.dt2
        self.dt1 += step*self.a1
        self.dt2 += step*self.a2

    def pos1(self):  # (x,y) position of upper pendulum
        x = self.l1*sin(self.t1)
        y = -1*self.l1*cos(self.t1)
        return (x, y)

    def pos2(self):  # (x,y) position of lower pendulum
        x = self.l1*sin(self.t1) + self.l2*sin(self.t2)
        y = -1 * (self.l1*cos(self.t1) + self.l2*cos(self.t2))
        return (x, y)

    def acc1(self):  # t1''
        ex1 = -3*_GRAV*sin(self.t1)
        ex2 = -_GRAV*sin(self.t1 - 2*self.t2)
        ex3a = -2*sin(self.t1 - self.t2)
        ex3b = (self.dt2**2)*self.l2+(self.dt1**2)*self.l1*cos(self.t1-self.t2)
        ex4 = self.l1*(3 - cos(2*(self.t1 - self.t2)))
        return (ex1 + ex2 + ex3a*ex3b) / ex4

    def acc2(self):
        ex0  = 2*sin(self.t1-self.t2)
        ex1a = (self.dt1**2)*2*self.l1
        ex1b = 2*_GRAV*cos(self.t1)
        ex1c = (self.dt2**2)*self.l2*cos(self.t1 - self.t2)
        ex2  = self.l1*(3 - cos(2*(self.t1 - self.t2)))
        return ex0*(ex1a + ex1b + ex1c)/ex2

    def __str__(self):
        ret =    "theta1 = " + (str)(self.t1)
        ret += "\ntheta2 = " + (str)(self.t2)
        ret += "\nvel1   = " + (str)(self.dt1)
        ret += "\nvel2   = " + (str)(self.dt2)
        ret += "\nacc1   = " + (str)(self.a1)
        ret += "\nacc2   = " + (str)(self.a2)
        return ret

    def vars(self):
        return {t1:self.t1,t2:self.t2,dt1:self.dt1,dt2:self.dt2,a1:self.a1,a2:self.a2}

    def toCSV(self):
        return ", ".join((str)(n) for n in self.vars())

def plotData(data):
    plt.plot(data.t1,data.t2)
    plt.xlabel("theta1")
    plt.ylabel("theta2")
    

def main():
    p = Pendulum(_PI/6,0)
    data = []
    for i in range(100000):
        p.step()
        data.append(p.vars)

    plotData(data)
    #plt.plot(range(len(data1)),data1,label="theta1")
    #plt.plot(range(len(data2)),data2,label="theta2")
    plt.plot(data1,data2)
    plt.xlabel('time')
    plt.ylabel('angle')
    #plt.legend()
    plt.show()

if __name__=="__main__":
    main()
