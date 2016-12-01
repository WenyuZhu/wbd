'''
Created on Oct 9, 2016

@author: artha
'''
import re
import xml.dom.minidom as xml
import Navigation.prod.Angle as Angle
import math
import time
from _operator import attrgetter
import os

class Fix():
    '''
    classdocs
    '''


    def __init__(self, logFile='log.txt'):
        '''
        Constructor
        '''
        if (not isinstance(logFile, str)) or len(logFile)==0:
            raise ValueError('Fix.__init__: input has to be string')
        name=logFile
        try:
            file=open(name,'a')
        except:
            raise ValueError('Fix.__init__: log file can not be created or appended')
        now_time=self.gettime()
        file.write(now_time+' Log file:'+'\t'+os.path.abspath(name)+'\n')
        file.close()
        logFile=None
        self.name=name
        self.sightingFile=''
        self.ariesFile=''
        self.starFile=''
        self.sightingList=list()
        self.errorNumber=0
        
    def setSightingFile(self, sightingFile=None):
        if (not isinstance(sightingFile,str)) or (len(sightingFile)==0):
            raise ValueError('Fix.setSightingFile: the file name violate parameter specification')
        pattern = re.compile(r'(^\w+\.xml$)')
        ifmatch = pattern.match(sightingFile)
        if not ifmatch:
            raise ValueError('Fix.setSightingFile: the file name violate parameter specification')
        FilePath=os.path.abspath(sightingFile)
        now_time=self.gettime()
        logFile=open(self.name,'a')
        logFile.write(now_time+' Sighting file:'+'\t'+FilePath+'\n')
        logFile.close()
        self.sightingFile=sightingFile
        return FilePath
        
    def setAriesFile(self,ariesFile=None):
        if (not isinstance(ariesFile, str)) or len(ariesFile)==0:
            raise ValueError('Fix.setAriesFile: the file name violate parameter specification')
        pattern = re.compile(r'(^\w+\.txt$)')
        ifmatch = pattern.match(ariesFile)
        if not ifmatch:
            raise ValueError('Fix.setAriesFile: the file name violate parameter specification')
        try:
            file=open(ariesFile,'r')
        except:
            raise ValueError('Fix.setAriesFile: the aries file doesnt exist')
        file.close()
        FilePath=os.path.abspath(ariesFile)
        now_time=self.gettime()
        logFile=open(self.name,'a')
        logFile.write(now_time+' Aries file:'+'\t'+FilePath+'\n')
        logFile.close()
        self.ariesFile=ariesFile
        return FilePath 
    
    def setStarFile(self,starFile=None):
        if (not isinstance(starFile, str)) or len(starFile)==0:
            raise ValueError('Fix.setStarFile: the file name violate parameter specification')
        pattern = re.compile(r'(^\w+\.txt$)')
        ifmatch = pattern.match(starFile)
        if not ifmatch:
            raise ValueError('Fix.setStarFile: the file name violate parameter specification')
        try:
            file=open(starFile,'r')
        except:
            raise ValueError('Fix.setStarFile: the aries file doesnt exist')
        file.close()
        FilePath=os.path.abspath(starFile)
        now_time=self.gettime()
        logFile=open(self.name,'a')
        logFile.write(now_time+' Star file:'+'\t'+FilePath+'\n')
        logFile.close()
        self.starFile=starFile
        return FilePath 

        
    def getSightings(self,assumedLatitude='0d0.0',assumedLongitude='0d0.0'):
        if (not isinstance(assumedLatitude, str) or not isinstance(assumedLongitude, str)):
            raise ValueError('Fix.getSightings: both assumedLatitude and assumedLongitude have to be str')
        if assumedLatitude[0]=='S' or assumedLatitude[0]=='N':
            checkLatitude=assumedLatitude[1:]
            if not self.anglecheck(checkLatitude):
                raise ValueError('Fix.getSightings: not valid Latitude')
            if assumedLatitude[0]=='S':
                assumedLatitude='-'+checkLatitude
            else:
                assumedLatitude=checkLatitude
        else:
            if not assumedLatitude=='0d0.0':
                raise ValueError('Fix.getSightings: not valid Latitude')
        if not self.angleNewcheck(assumedLongitude):
            raise ValueError('Fix.getSightings: not valid Longitude')
        if self.sightingFile == '':
            raise ValueError('Fix.getSightings: no sighting file in instance')
        if self.ariesFile == '':
            raise ValueError('Fix.getSightings: no aries file in instance')
        if self.starFile == '':
            raise ValueError('Fix.getSightings: no aries file in instance')
        try:
            dom=xml.parse(self.sightingFile)
        except:
            raise ValueError('Fix.getSightings: parse xml file failed')
        try:
            starFile=open(self.starFile,'r')
        except:
            raise ValueError('Fix.getSightings: starfile can not be found in directory')
        try:
            ariesFile=open(self.ariesFile,'r')
        except:
            raise ValueError('Fix.getSightings: ariesfile can not be found in directory')
        sightings=dom.getElementsByTagName('sighting')
        
        for sight in sightings:
            OneSighting = Sighting()
            #getting information from xml file
            body = sight.getElementsByTagName('body')
            date = sight.getElementsByTagName('date')
            time = sight.getElementsByTagName('time')
            obv = sight.getElementsByTagName('observation')
            height = sight.getElementsByTagName('height')
            temt = sight.getElementsByTagName('temperature')
            pres = sight.getElementsByTagName('pressure')
            horz = sight.getElementsByTagName('horizon')
            
            #check mandatory tag format and pass data in to sighting instances
            if len(body)==0 or len(date)==0 or len(time)==0 or len(obv)==0:
                self.errorNumber+=1
                continue
            
            bodydata = self.getText(body[0].childNodes)
            if len(bodydata) == 0:
                self.errorNumber+=1
                continue
            OneSighting.setBody(bodydata)
            datedata = self.getText(date[0].childNodes)
            pattern=re.compile(r'(^\d\d\d\d-\d\d-\d\d$)')
            ifmatch = pattern.match(datedata)
            if not ifmatch:
                self.errorNumber+=1
                continue
            if not self.datecheck(datedata):
                self.errorNumber+=1
                continue
            OneSighting.setDate(datedata)
            timedata = self.getText(time[0].childNodes)
            pattern=re.compile(r'(^\d\d:\d\d:\d\d$)')
            ifmatch = pattern.match(timedata)
            if not ifmatch:
                self.errorNumber+=1
                continue
            if not self.timecheck(timedata):
                self.errorNumber+=1
                continue
            OneSighting.setTime(timedata)
            obvdata = self.getText(obv[0].childNodes)
            angle=Angle.Angle()
            anglecheck=Angle.Angle()
            if not self.anglecheck(obvdata):
                self.errorNumber+=1
                continue
            obvdata=angle.setDegreesAndMinutes(obvdata)
            checkdata=anglecheck.setDegreesAndMinutes('0d0.1')
            if obvdata < checkdata:
                self.errorNumber+=1
                continue
            obvdatarad=obvdata*math.pi/180
            if not (len(height) == 0 or self.getText(height[0].childNodes)==''):
                heightdata=self.getText(height[0].childNodes)
                try:
                    heightdata=float(heightdata)
                except:
                    self.errorNumber+=1
                    continue
                if heightdata < 0:
                    self.errorNumber+=1
                    continue
                OneSighting.setheight(heightdata)
            if not (len(temt) == 0 or self.getText(temt[0].childNodes)==''):    
                temtdata = self.getText(temt[0].childNodes)
                temtdata = int(temtdata)
                if temtdata < -20 or temtdata > 120:
                    self.errorNumber+=1
                    continue
                OneSighting.setTemt(temtdata)
            if not (len(pres) == 0 or self.getText(pres[0].childNodes)==''):  
                presdata = self.getText(pres[0].childNodes)
                try:
                    presdata = int(presdata)
                except:
                    self.errorNumber+=1
                    continue
                
                if presdata < 100 or presdata > 1100:
                    self.errorNumber+=1
                    continue
                OneSighting.setPres(presdata)
            if not (len(horz) == 0 or self.getText(horz[0].childNodes)==''):  
                horzdata = self.getText(horz[0].childNodes)
                if not (horzdata == 'Artificial' or  horzdata == 'artificial' or horzdata == 'Natural' or horzdata == 'natural'):
                    self.errorNumber+=1
                    continue
                OneSighting.setHorz(horzdata)
            #Calculation of adjusted altitude
            if OneSighting.horz == 'Artificial' or OneSighting.horz == 'artificial':
                dip = 0
            else:
                dip = (-0.97*math.sqrt(OneSighting.height))/60
            refc=((-0.00452*OneSighting.pres)/(273+(OneSighting.temt-32)*5/9))/math.tan(obvdatarad)
            adjAlt=obvdata+dip+ refc
            angle.setDegrees(adjAlt)
            adjAlt=angle.getString()
            OneSighting.setAdjAtl(adjAlt)
            self.sightingList.append(OneSighting)
        file=open(self.name,'a')
        self.sightingList.sort(key=attrgetter('date','time','body'))
        #Start calculating latitude and longitude
        self.getLatitudeAndSHA(starFile)
        self.getGHA(ariesFile)
        self.getLongitude()
        self.getLHA(assumedLongitude)
        self.getCorrectAltitude(assumedLatitude)
        self.getDistanceAdj()
        self.getAzimuthAdj(assumedLatitude)
        
        
        for sighting in self.sightingList:
            if sighting.valid==True:
                file.write(self.gettime()+ '\t' + sighting.body + '\t' + sighting.date + '\t' + sighting.time + '\t' + sighting.adjAtl + '\t' + sighting.latitude + '\t' +sighting.longitude + '\t'+ assumedLatitude + '\t'+ assumedLongitude + '\t' + sighting.azi + '\t' + sighting.disAl + '\n')
        approxLa=self.getAppLa(assumedLatitude)
        approxLo=self.getAppLo(assumedLongitude)
        
        if approxLa[0]=='-':
            approxLa='S'+approxLa[1:]
        else:
            approxLa='N'+approxLa
        
        file.write(self.gettime() + '\t' + 'Sighting errors:' + '\t' + str(self.errorNumber) + '\n')
        file.write(self.gettime() + '\t' + 'Approximate latitude:' + '\t' + approxLa+ '\t' + 'Approximate Longitude:' + '\t' + approxLo + '\n')
        file.close()
        approximateLatitude = approxLa
        approximateLongitude = approxLo
        return (approximateLatitude,approximateLongitude)
    
    def gettime(self):
        now='LOG: '+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+('-' if time.timezone > 0 else '+')+time.strftime('%H:%M',time.gmtime(abs(time.timezone)))
        return now
        
        
    def getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    def anglecheck(self,obv):
        pattern = re.compile(r'(^-?\d+d\d+\.\d$)|(^-?\d+d\d+$)')
        ifmatch = pattern.match(obv)
        if not ifmatch:
            return False
        else:
            for index in range(len(obv)):
                if obv[index]=='d':
                    break
            deg=int(obv[ :index])
            dec=float(obv[index+1: ])
        if (deg < 0 or deg >= 90) or (dec<0.0 or dec >= 60.0):
            return False
        return True

    def angleNewcheck(self,obv):
        pattern = re.compile(r'(^\d+d\d+\.\d$)|(^\d+d\d+$)')
        ifmatch = pattern.match(obv)
        if not ifmatch:
            return False
        else:
            for index in range(len(obv)):
                if obv[index]=='d':
                    break
            deg=int(obv[ :index])
            dec=float(obv[index+1: ])
        if (deg < 0 or deg >= 360) or (dec<0.0 or dec >= 60.0):
            return False
        return True
    
    def angleTwoNewcheck(self,obv):
        pattern = re.compile(r'(^-?\d+d\d+\.\d$)|(^-?\d+d\d+$)')
        ifmatch = pattern.match(obv)
        if not ifmatch:
            return False
        else:
            for index in range(len(obv)):
                if obv[index]=='d':
                    break
            deg=int(obv[ :index])
            dec=float(obv[index+1: ])
        if (deg < -90 or deg >= 90) or (dec<0.0 or dec >= 60.0):
            return False
        return True
    
    def datecheck(self,date):
        month=date[5:7]
        if int(month)>12:
            return False
        day=date[8:10]
        if int(day)>31:
            return False
        return True
    
    def dateNewcheck(self,date):
        month=date[0:2]
        if int(month)>12:
            return False
        day=date[3:5]
        if int(day)>31:
            return False
        return True
        
    def timecheck(self,time):
        hour=time[:2]
        if int(hour)>24:
            return False
        minute=time[3:5]
        if int(minute)>60:
            return False
        second=time[6:]
        if int(second) > 60:
            return False
        return True
    
    def transform(self,degree):
        for index in range(len(degree)):
            if degree[index]=='d':
                break
        deg=int(degree[:index])
        dec=float(degree[index+1:])
        dec=dec/60
        if deg < 0:
            deg = deg - dec
        else:
            deg = deg + dec
        return deg
        
    def getLatitudeAndSHA(self,starFile):
        starFileContent=starFile.readlines()
        for sighting in self.sightingList:
            if sighting.valid == True:
                try:
                    sightingArray=list()
                    body=sighting.body
                    bodyLen=len(body)
                    date=sighting.date
                    year=date[0:4]
                    year=year[2:4]
                    month=date[5:7]
                    day=date[8:10]
                    date=month+'/'+day+'/'+year
                    for star in starFileContent:
                        star=star[0:len(star)-1]
                        if star[0:bodyLen] == body:
                            sightingArray.append(star)
                    if len(sightingArray) == 0:
                        raise ValueError('Fix.getSightings: There is no specified body in star file')
                    for index in range(len(sightingArray)):
                        sightingArray[index]=sightingArray[index].split('\t')
                        if not self.dateNewcheck(sightingArray[index][1] ):
                            raise ValueError('Fix.getSightings: Date violates the specification')
                        
                    for entry in range(len(sightingArray)):
                        if date<sightingArray[entry][1]:
                            if not self.angleNewcheck(sightingArray[entry-1][2]):
                                raise ValueError('Fix.getSightings: Longitude violates the specification')
                            if not self.angleTwoNewcheck(sightingArray[index][3]):
                                raise ValueError('Fix.getSightings: Latitude violates the specification')
                            sighting.SHA=sightingArray[entry-1][2]
                            sighting.latitude=sightingArray[entry-1][3]
                            break
                except:
                    self.errorNumber+=1
                    sighting.valid=False
                    continue
            
            
                        
    def getGHA(self,ariesFile):
        ariesFileContent=ariesFile.readlines()
        for dates in range(len(ariesFileContent)):
            ariesFileContent[dates]=ariesFileContent[dates][0:len(ariesFileContent[dates])-1]
        for index in range(len(ariesFileContent)):
            ariesFileContent[index]=ariesFileContent[index].split('\t')
        for sighting in self.sightingList:
            if sighting.valid == True:
                try:
                    date=sighting.date
                    year=date[0:4]
                    year=year[2:4]
                    month=date[5:7]
                    day=date[8:10]
                    time=sighting.time
                    hour=time[0:2]
                    if hour[0]=='0':
                        hour=hour[1:]
                    minute=time[3:5]
                    second=time[6:8]
                    date=month+'/'+day+'/'+year
                    GHA1=''
                    GHA2=''
                    for entry in range(len(ariesFileContent)):
                        if not self.dateNewcheck(ariesFileContent[entry][0] ):
                            raise ValueError('Fix.getSightings: Date violates the parameter specification')
                        if int(ariesFileContent[entry][1]) > 23 or int(ariesFileContent[entry][1]) <0:
                            raise ValueError('Fix.getSightings: Time violates the parameter specification')
                        if date == ariesFileContent[entry][0] and hour == ariesFileContent[entry][1]:
                            if not self.angleNewcheck(ariesFileContent[entry][2]):
                                raise ValueError('Fix.getSightings: Aries angle violates the specification')
                            GHA1=ariesFileContent[(entry)][2]
                            GHA2=ariesFileContent[(entry+1)][2]
                    past=int(minute)*60+int(second)
                    angleGHA1=Angle.Angle()
                    angleGHA2=Angle.Angle()
                    GHA1=angleGHA1.setDegreesAndMinutes(GHA1)
                    GHA2=angleGHA2.setDegreesAndMinutes(GHA2)
                    GHA=GHA1+(abs(GHA2 - GHA1)*(past/3600))
                    angleGHA = Angle.Angle()
                    angleGHA.setDegrees(GHA)
                    GHA=angleGHA.getString()
                    sighting.GHA=GHA
#                     print(sighting.GHA)
                except:
                    self.errorNumber+=1
                    sighting.valid=False
                    continue
                    
            
    def getLongitude(self):
        for sighting in self.sightingList:
            if sighting.valid == True:
                angleGHA=Angle.Angle()
                GHA=angleGHA.setDegreesAndMinutes(sighting.GHA)
                angleSHA=Angle.Angle()
                SHA=angleSHA.setDegreesAndMinutes(sighting.SHA)
                longi=SHA+GHA
                angleLongi=Angle.Angle()
                angleLongi.setDegrees(longi)
                longi=angleLongi.getString()
                sighting.longitude=longi
                
    def getLHA(self,assumedLongitude):
        for sighting in self.sightingList:
            if sighting.valid == True:
                angleLo=Angle.Angle()
                asLo=angleLo.setDegreesAndMinutes(assumedLongitude)
                Lo=angleLo.setDegreesAndMinutes(sighting.longitude)
                LHA=Lo+asLo
                sighting.LHA=LHA
                
    def getCorrectAltitude(self,assumedLatitude):
        for sighting in self.sightingList:
            if sighting.valid == True:
                angleLa=Angle.Angle()
                La=angleLa.setDegreesAndMinutes(sighting.latitude)
                La=La*math.pi/180
                asLa=angleLa.setDegreesAndMinutes(assumedLatitude)
                asLa=asLa*math.pi/180
                sinLa=math.sin(La)*math.sin(asLa)
                cosLa=math.cos(La)*math.cos(asLa)*math.cos(sighting.LHA*math.pi/180)
                coral=math.asin(sinLa+cosLa)
                coral=coral*180/math.pi
                sighting.coral=coral
                sighting.interdis=sinLa+cosLa
                
                
    def getDistanceAdj(self):
        for sighting in self.sightingList:
            if sighting.valid == True:
                angleAl=Angle.Angle()
                adjAl=angleAl.setDegreesAndMinutes(sighting.adjAtl)
                corAl=sighting.coral
                disAl=corAl-adjAl
                disAl=round(disAl*60,0)
                disAl=int(disAl)
                sighting.disAl=str(disAl)
                
    def getAzimuthAdj(self, assumedLatitude):
        for sighting in self.sightingList:
            if sighting.valid == True:
                angleLa=Angle.Angle()
                La=angleLa.setDegreesAndMinutes(sighting.latitude)
                La=La*math.pi/180
                asLa=angleLa.setDegreesAndMinutes(assumedLatitude)
                asLa=asLa*math.pi/180
                corAl=sighting.coral
                corAl=corAl*math.pi/180
                interDis=sighting.interdis
                sinLa=math.sin(La)-math.sin(asLa)*interDis
                cosLa=math.cos(asLa)*math.cos(corAl)
                aziAdj=math.acos(sinLa/cosLa)
                aziAdj=aziAdj*180/math.pi
                angleLa.setDegrees(aziAdj)
                aziStr=angleLa.getString()
                sighting.azi=aziStr
                
    def getAppLa(self,assumedLatitude):
        tempSum=0
        angleLa=Angle.Angle()
        asLa=self.transform(assumedLatitude)
        for sighting in self.sightingList:
            if sighting.valid == True:
                disAl=int(sighting.disAl)
                azi=angleLa.setDegreesAndMinutes(sighting.azi)
                azi=azi*math.pi/180
                tempSum=tempSum+disAl*math.cos(azi)
        asLa=tempSum/60+asLa
        if asLa<0:
            dec=asLa%-1
            dec=-dec
        else:
            dec=asLa%1
        dec=dec*60
        dec=round(dec,1)
        degree=int(asLa)
        if dec<10:
            dec='0'+str(dec)
        else:
            dec=str(dec)
        approxLa=str(degree)+'d'+dec
        return approxLa
    
    def getAppLo(self,assumedLongitude):
        tempSum=0
        angleLo=Angle.Angle()
        asLo=angleLo.setDegreesAndMinutes(assumedLongitude)
        for sighting in self.sightingList:
            if sighting.valid == True:
                disAl=int(sighting.disAl)
                azi=angleLo.setDegreesAndMinutes(sighting.azi)
                azi=azi*math.pi/180
                tempSum=tempSum+disAl*math.sin(azi)
        asLo=(tempSum/60)+asLo
        angleLo.setDegrees(asLo)
        approxLo=angleLo.getString()
        return approxLo
    
class Sighting():
    def __init__(self):
        self.body=''
        self.date=''
        self.time=''
        self.height=0
        self.temt=72
        self.pres=1010
        self.horz='Natural'
        self.adjAtl=''
        self.latitude=''
        self.SHA=''
        self.GHA=''
        self.longitude=''
        self.valid=True
        self.LHA=0
        self.coral=0
        self.disAl=''
        self.azi=''
        self.interdis=0
        
    def setBody(self,body):
        self.body=body
        return
            
    def setDate(self,date):
        self.date=date
        return
            
    def setTime(self,time):
        self.time=time
        return
            
    def setheight(self,height):
        self.height=height
        return
            
    def setTemt(self,temt):
        self.temt=temt
        return
            
    def setPres(self,pres):
        self.pres=pres
        return
            
    def setHorz(self,horz):
        self.horz=horz
        return
        
    def setAdjAtl(self,adjAtl):
        self.adjAtl=adjAtl
        return
    