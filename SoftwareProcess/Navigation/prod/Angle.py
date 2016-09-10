from math import degrees
from _ast import Num
class Angle():
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        self.angle_value = 0;
        pass
    
    def setDegrees(self, degrees):
        if not (isinstance(degrees, int) or isinstance(degrees, float)):
            raise ValueError('Value is not integer or float, please retry')
        
        
        
        if degrees < 0 :
            degrees=-degrees
            degrees=degrees%360
            degrees=360-degrees
        else:
            degrees=degrees%360
        self.angle_value=degrees
        
        return self.angle_value
            
        
        pass
    
    def DegreeTransform(self,degrees):
        for index in range(len(degrees)):
            if degrees[index]=='d':
                if index == 0 :
                    raise ValueError('degree portion is needed')
                if index == len(degrees)-1:
                    raise ValueError('minute portion is needed')
                temp=degrees[ :index]
                try:
                    a=int(temp)
                except:
                    raise ValueError('degree portion has to be integer')
                dec=degrees[index+1:]
                try:
                    b=float(dec)
                except:
                    raise ValueError('minute portion has to integer or float')
                if b<0:
                    raise ValueError('minute portion has to be a positive number')
            if index == len(degrees)-1 and not degrees[index] == 'd':
                raise ValueError('the separator d is not found')
        carrier=int(b/60)
        b=b%60
        b=b/60+carrier
        if a<0:
            a=a-b
        else:
            a=a+b
            
        return a
        
        
        pass
    
    def setDegreesAndMinutes(self, degrees):
        #a,b=0
        a=self.DegreeTransform(degrees)
        
                
        if a<0:
            a=-a
            a=a%360
            a=360-a
        else:
            a=a%360
        
                    
        
        
        
        self.angle_value=a
        return self.angle_value
        pass
    
    def add(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError('angle is not a instance of Angle')
        
        angleOut=angle.getDegrees()
        res=self.angle_value+angleOut
        if res<0:
            res=-res
            res=res%360
            res=360-res
        else:
            res=res%360
        self.angle_value=res
        return self.angle_value
        
        
        pass
    
    def subtract(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError('angle is not a instance of Angle')
        angleOut=angle.getDegrees()
        res=self.angle_value-angleOut
        if res<0:
            res=-res
            res=res%360
            res=360-res
        else:
            res=res%360
        self.angle_value=res
        return self.angle_value
        
        pass
    
    def compare(self, angle):
        if not isinstance(angle, Angle):
            raise ValueError('angle is not a instance of Angle')
        angleOut=angle.getDegrees()
        if self.angle_value>angleOut:
            return 1
        elif self.angle_value>angleOut:
            return 0
        else:
            return -1
        
        
        
        
        
        pass
    
    def getString(self):
        anglenum=self.angle_value
        num=int(anglenum/1)
        dec=anglenum-num
        dec=dec*60
        res=str(num)+'d'+str(dec)
        return res
        
        
        pass
    
    def getDegrees(self):
        return self.angle_value
        
        pass
    
    
    
    
    