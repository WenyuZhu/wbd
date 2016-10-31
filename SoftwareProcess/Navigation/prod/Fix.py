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
<<<<<<< HEAD
        file.write(now_time+' Start of log \n')
=======
        file.write(now_time+' Log file:'+'\t'+os.path.abspath(name)+'\n')
>>>>>>> refs/heads/CA03
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
<<<<<<< HEAD
        
        pattern = re.compile(r'(^\w+\.xml$)')
        ValueError('Fix.setSightingFile: log file can not be created or appended')
=======
        pattern = re.compile(r'(^\w+\.xml$)')
>>>>>>> refs/heads/CA03
        ifmatch = pattern.match(sightingFile)
        if not ifmatch:
            raise ValueError('Fix.setSightingFile: the file name violate parameter specification')
        FilePath=os.path.abspath(sightingFile)
        now_time=self.gettime()
        logFile=open(self.name,'a')
<<<<<<< HEAD
        logFile.write(now_time+' Start of sighting file '+sightingFile + '\n')
=======
        logFile.write(now_time+' Sighting file:'+'\t'+FilePath+'\n')
>>>>>>> refs/heads/CA03
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

        
    def getSightings(self):
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
<<<<<<< HEAD
                    raise ValueError('Fix.getSightings: height has to be greater than or equal to 0')
=======
                    self.errorNumber+=1
                    continue
>>>>>>> refs/heads/CA03
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
<<<<<<< HEAD
                    raise ValueError('Fix.getSightings: pressure has to be integer')
=======
                    self.errorNumber+=1
                    continue
>>>>>>> refs/heads/CA03
                
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
<<<<<<< HEAD
        logFile=open()
=======
        file=open(self.name,'a')
>>>>>>> refs/heads/CA03
        self.sightingList.sort(key=attrgetter('date','time','body'))
        self.getLatitudeAndSHA(starFile)
        self.getGHA(ariesFile)
        self.getLongitude()
        
        for sighting in self.sightingList:
<<<<<<< HEAD
            logFile.write(self.gettime()+ '\t' + sighting.body + '\t' + sighting.date + '\t' + sighting.time + '\t' + sighting.adjAtl + '\n')
        
        logFile.write(self.gettime() + '\t' + 'End of sighting file:' + '\t' + self.sightingFile + '\n')
        logFile.close()
=======
            if sighting.valid==True:
                file.write(self.gettime()+ '\t' + sighting.body + '\t' + sighting.date + '\t' + sighting.time + '\t' + sighting.adjAtl + '\t' + sighting.latitude + '\t' +sighting.longitude + '\n')
        
        file.write(self.gettime() + '\t' + 'Sighting errors:' + '\t' + str(self.errorNumber) + '\n')
        file.close()
>>>>>>> refs/heads/CA03
        approximateLatitude = '0d0.0'
        approximateLongitude = '0d0.0'
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
    