from math import cos, sin
from math import pi as _PI
import matplotlib.pyplot as plt
import numpy as np

_TIMESTEP = 0.001
_NUMFRAMES = 1000
_NUMSTEPS = 100
_DETAIL = 400
_GRAV = 1


def rescale(n,a,b,c,d):
    return (((n - a) * (d - c)) / (b - a)) + c


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
        return dict(t1=self.t1,t2=self.t2,dt1=self.dt1,dt2=self.dt2,a1=self.a1,a2=self.a2)

    def toCSV(self):
        return ", ".join((str)(n) for n in self.vars())

    def color(self):
        r = (int)(rescale(self.t1,-1*_PI,_PI,0,255))
        g = 128
        b = (int)(rescale(self.t2,-1*_PI,_PI,0,255))
        return (r,g,b)

class Fractal():
    def __init__(self,path,w,h=-1):
        self.path = path
        if(h == -1):
            h = w
        self.w = w
        self.h = h
        self.frame = 0
        self.frames = []
        self.pends = []
        for x in range(self.w):
            t1 = -1*_PI + 2*_PI*(x/self.w)
            row = []
            for y in range(self.h):
                t2 = -1*_PI + 2*_PI*(y/self.h)
                row.append(Pendulum(t1,t2))
            self.pends.append(row)

    def image(self):
        with open(self.path + (str)(self.frame) + ".ppm","w") as im:
            im.write("P3\n" + (str)(self.w) + " " + (str)(self.h) + "\n255\n")
            for y in range(self.h):
                for x in range(self.w):
                    c = self.pends[x][y].color()
                    im.write(" ".join((str)(i) for i in c))
                    im.write("  ")
                im.write("\n")

    def step(self):
        self.image()
        for i in range(_NUMSTEPS):
            for x in range(self.w):
                for y in range(self.h):
                    self.pends[x][y].step()
        self.frame += 1
        
                
def plotData(data):
    d1 = []
    d2 = []
    for i in range(len(data)):
        d1.append(data[i]['t1'])
        d2.append(data[i]['t2'])
    plt.plot(np.array(d1),np.array(d2))
    plt.xlabel("theta1")
    plt.ylabel("theta2")
    plt.show()
    #plt.plot(range(len(data1)),data1,label="theta1")
    #plt.plot(range(len(data2)),data2,label="theta2")

def main():
    F = Fractal("save/",_DETAIL)
    for i in range(_NUMFRAMES):
        print(i/_NUMFRAMES)
        F.step()

if __name__=="__main__":
    main()
