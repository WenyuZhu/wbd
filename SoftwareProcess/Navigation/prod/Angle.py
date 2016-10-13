'''
Created on Sep 1, 2016

@author: Wenyu Zhu
'''
from math import degrees
from _ast import Num
import re

class Angle():
    def __init__(self):
        # self.angle = ...       set to 0 degrees 0 minutes
        self.angle_value = 0.0;
        pass
    
    def setDegrees(self, degrees=0.0):
        if not (isinstance(degrees, int) or isinstance(degrees, float)):
            raise ValueError('Angle.setDegrees:  Value is not integer or float, please retry')
        degrees = (float)(degrees)
#         degrees = round(degrees,1)
        
        if degrees < 0 :
            dec=degrees%(-1.0)
            dec=dec*60
            dec=round(dec,1)
            dec=dec/60
            degrees = int(degrees)
            degrees = degrees + dec
            degrees = -degrees
            degrees = degrees % 360
            degrees = 360 - degrees
        else:
            dec=degrees%1.0
            dec=dec*60
            dec=round(dec,1)
            dec=dec/60
            degrees=int(degrees)
            degrees = degrees + dec
            degrees = degrees % 360
        degrees=(float)(degrees)
        self.angle_value = degrees
        
        return self.angle_value
        pass
    
    def DegreeTransform(self, degrees):
        pattern = re.compile(r'(^-?\d+d\d+\.\d$)|(^-?\d+d\d+$)')
        ifmatch = pattern.match(degrees)
        if not ifmatch:
            raise ValueError('Angle.setDegreesAndMinutes: angleString violates the parameter specifications')
        else:
            for index in range(len(degrees)):
                if degrees[index]=='d':
                    break
            deg=int(degrees[ :index])
            dec=float(degrees[index+1: ])
        carrier = int(dec / 60)
        dec = dec % 60
        dec = dec / 60 + carrier
        if deg < 0:
            deg = deg - dec
        else:
            deg = deg + dec
        return deg
        pass
    
    def setDegreesAndMinutes(self, degrees):
        # a,b=0
        a = self.DegreeTransform(degrees)
        if a < 0:
            a = -a
            a = a % 360
            a = 360 - a
        else:
            a = a % 360
        self.angle_value = a
        return self.angle_value
        pass
    
    def add(self, angle=None):
        if angle==None:
            raise ValueError('Angle.add: angle is needed')
        if not isinstance(angle, Angle):
            raise ValueError('Angle.add:  angle is not a instance of Angle')
        angleOut = angle.getDegrees()
        res = self.angle_value + angleOut
        if res < 0:
            res = -res
            res = res % 360
            res = 360 - res
        else:
            res = res % 360
        self.angle_value = res
        return self.angle_value
        pass
    
    def subtract(self, angle=None):
        if angle==None:
            raise ValueError('Angle.subtract: angle is needed')
        if not isinstance(angle, Angle):
            raise ValueError('Angle.subtract:  angle is not a instance of Angle')
        angleOut = angle.getDegrees()
        res = self.angle_value - angleOut
        if res < 0:
            res = -res
            res = res % 360
            res = 360 - res
        else:
            res = res % 360
        self.angle_value = res
        return self.angle_value
        pass
    
    def compare(self, angle=None):
        if angle == None:
            raise ValueError('Angle.compare: angle is needed')
        if not isinstance(angle, Angle):
            raise ValueError('Angle.compare:  angle is not a instance of Angle')
        angleOut = angle.getDegrees()
        if self.angle_value > angleOut:
            return 1
        elif self.angle_value == angleOut:
            return 0
        else:
            return -1
        pass
    
    def getString(self):
        anglenum = self.angle_value
        num = int(anglenum / 1)
        dec = anglenum - num
        dec = round(dec * 60, 1)
        res = str(num) + 'd' + str(dec)
        return res
        pass
    
    def getDegrees(self):
        return self.angle_value
#         return round(self.angle_value,1)
        pass
    