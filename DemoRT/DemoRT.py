import thumby
import math
import random
import time
import sys
import machine
import array

sys.path.append("/Games/DemoRT")

emulator = None
try:
    import emulator
except ImportError:
    pass

if not emulator:
    import thumbyrt

machine.freq(270000000)
thumby.display.setFPS(30)

lightpos = [0, -800, -1500]
nativewidth     = 72
nativeheight    = 40

colorlist = [0] * nativewidth * nativeheight
arr = array.array('B', colorlist)

#############################################

class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, a):
        if isinstance(a, self.__class__):
            return vec3(self.x + a.x, self.y + a.y, self.z + a.z)
        elif isinstance(a, float):
            return vec3(self.x + a, self.y + a, self.z + a)
        else:
            return self
            
    def __sub__(self, a):
        if isinstance(a, self.__class__):
            return vec3(self.x - a.x, self.y - a.y, self.z - a.z)
        elif isinstance(a, float):
            return vec3(self.x - a, self.y - a, self.z - a)
        else:
            return self
            
    def __mul__(self, a):
        if isinstance(a, self.__class__):
            return vec3(self.x * a.x, self.y * a.y, self.z * a.z)
        elif isinstance(a, float):
            return vec3(self.x * a, self.y * a, self.z * a)
        else:
            return self
            
    def __truediv__(self, a):
        if isinstance(a, self.__class__):
            return vec3(self.x / a.x, self.y / a.y, self.z / a.z)
        elif isinstance(a, float):
            return vec3(self.x / a, self.y / a, self.z / a)
        else:
            return self
            
    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)
            
    def dot(self, a):
        return self.x * a.x + self.y * a.y + self.z * a.z
        
    def getnormalized(self):
        mag = math.sqrt(self.dot(self))
        if (mag == 0.0):
            return self
        return self/mag
    
class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.getnormalized()

    def point_at_parameter(self, t):
        return self.origin + self.direction * t

class Sphere:
    def __init__(self, acenter, aradius):
        self.center = acenter
        self.radius = aradius

    def intersect(self, ray):
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4.0 * a * c
        if (discriminant < 0.0):
            return [False, 0.0]
        else:
            t = (-b - math.sqrt(discriminant)) / (2.0 * a)
            return [True, t]
            
class Plane:
    def __init__(self, aposition, anormal):
        self.position = aposition
        self.normal = anormal
        
    def intersect(self, ray):
        denom = self.normal.dot(ray.direction)
        if (denom > 0.0001):
            p0l0 = self.position - ray.origin
            t = p0l0.dot(self.normal) / denom
            if t >= 0.0:
                return [True, t]
            else:
                return [False, 0.0]
        return [False, 0.0]
      
@micropython.native
def visiblecheck(ray, spheres, numspheres, minlength):
    bvis = True
    for i in range(0, numspheres, 1):
        t = 0.0
        bintersect, t = spheres[i].intersect(ray)
        if bintersect:
            if t <= minlength:
                bvis = False
    return bvis


def find_closest(x, y, c0):
    dither44 = [
        [  0.0 / 16.0, 12.0 / 16.0,  3.0 / 16.0, 15.0 / 16.0 ],
        [  8.0 / 16.0,  4.0 / 16.0, 11.0 / 16.0,  7.0 / 16.0 ],
        [  2.0 / 16.0, 14.0 / 16.0,  1.0 / 16.0, 13.0 / 16.0 ],
        [ 10.0 / 16.0,  6.0 / 16.0,  9.0 / 16.0,  5.0 / 16.0 ]]

    limit = 0.0
    if x < 4:
        limit = dither44[x][y]
    if c0 <= limit:
        return 0.0
    return 1.0

def dithershadeintodisplay():
    for x in range(0, nativewidth, 1):
        for y in range(0, nativeheight, 1):
            shadeestimate = arr[x * nativeheight + y]
            color = find_closest(x % 4, y % 4, shadeestimate / 255.0)
            color = color * 255.0
            if (int(color) > 0):
                thumby.display.setPixel(x, y, 1);


#@micropython.native
def raytracetest():
    aspect = nativewidth / nativeheight
    
    lightpospy = vec3(lightpos[0], lightpos[1], lightpos[2]) * 0.001
    
    visbias = 0.001
    lightsphere = Sphere(lightpospy, 0.1)
    sphere0 = Sphere(vec3(0.5, 0.0, -1.0), 0.5)
    sphere1 = Sphere(vec3(-0.8, 0.0, -1.5), 0.5)
    spheres = [lightsphere, sphere0, sphere1]
    visspheres0 = [ sphere1 ]
    visspheres1 = [ sphere0 ]
    visspheres2 = [ sphere0, sphere1 ]
    visspheres = [ None, visspheres0, visspheres1, visspheres2 ]
    visspheresnum = [0,1,1,2]
    numspheres = 3

    for j in range(0, nativeheight, 1):
        for i in range(0, nativewidth, 1):
            u = float(i) / float(nativewidth)
            v = float(j) / float(nativeheight)
            ray = Ray(vec3(0.0, 0.0, 0.0), vec3((2.0 * u - 1.0 ) * aspect, 2.0 * v - 1.0, -1.0))

            r = 0
            mint = 1000.0
            for spherei in range(0, numspheres, 1):
                bintersect, t = spheres[spherei].intersect(ray)
                if bintersect:
                    if (spherei == 0):
                        if (t < mint):
                            mint = t
                            r = 255
                    else:
                        if (t < mint):
                            point = ray.point_at_parameter(t)
                            normal = (point - spheres[spherei].center).getnormalized();
                            lightvec = -(point - lightpospy).getnormalized();
                            length = math.sqrt((point - lightpospy).dot(point - lightpospy))
                            visray = Ray(point + normal * visbias, lightvec)
                            mint = t
                            if (visiblecheck(visray, visspheres[spherei], visspheresnum[spherei], length)):
                                color = (lightvec.dot(normal) + 1.0) / 2.0
                                r = int(255.99 * color)
						
            plane0 = Plane(vec3(0.0, 1.0, 0.0), vec3(0.0, 1.0, 0.0))
            bintersect, t = plane0.intersect(ray)
            if bintersect:
                if (t < mint):
                    point = ray.point_at_parameter(t)
                    normal = plane0.normal
                    lightvec = (point - lightpospy).getnormalized()
                    length = math.sqrt((point - lightpospy).dot(point - lightpospy))
                    visray = Ray(point + normal * visbias, lightvec)
                    mint = t
                    if (visiblecheck(visray, visspheres[3], visspheresnum[3], length)):
                        color = (lightvec.dot(normal) + 1.0) / 2.0
                        r = int(255.99 * color)

            color = int(r)
            arr[i * nativeheight + j] = color
    dithershadeintodisplay()



@micropython.native
def Main():
    while True:
        thumby.display.fill(0)
        if not emulator:
            # Call into thumbyRT module for raytracing a simple scene
            thumbyrt.productf(lightpos[0], lightpos[1], lightpos[2], arr)
            # This looping over an array is very slow in micro python
            for x in range(nativewidth):
                for y in range(nativeheight):
                    thumby.display.setPixel(x, y, arr[x * nativeheight + y] & 0x1)
        else:
            raytracetest()

        moveamount = 100
        
        if thumby.buttonU.pressed():
            lightpos[2] -= moveamount
        if thumby.buttonD.pressed():
            lightpos[2] += moveamount
        if thumby.buttonL.pressed():
            lightpos[0] -= moveamount
        if thumby.buttonR.pressed():
            lightpos[0] += moveamount
        if thumby.buttonA.pressed():
            lightpos[1] -= moveamount
        if thumby.buttonB.pressed():
            lightpos[1] += moveamount
            
        lightpos[2] = min(lightpos[2], -500)
    
        thumby.display.update()
    
Main()


