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
        file.write(now_time+' Start of log \n')
        self.file=file
        self.sightingFile=''
        self.sightingList=list()
            
    def setSightingFile(self, sightingFile=None):
        if (not isinstance(sightingFile,str)) or (len(sightingFile)==0):
            raise ValueError('Fix.setSightingFile: the file name violate parameter specification')
        try:
            pattern = re.compile(r'(^\w+\.xml$)')
        except:
            raise ValueError('Fix.setSightingFile: log file can not be created or appended')
        ifmatch = pattern.match(sightingFile)
        if not ifmatch:
            raise ValueError('Fix.setSightingFile: the file name violate parameter specification')
        now_time=self.gettime()
        self.file.write(now_time+' Start of sighting file '+sightingFile + '\n')
        self.sightingFile=sightingFile
        return sightingFile
        

        
    def getSightings(self):
        if self.sightingFile == '':
            raise ValueError('Fix.getSightings: no sighting file in instance')
        try:
            dom=xml.parse(self.sightingFile)
        except:
            raise ValueError('Fix.getSightings: parse xml file failed')
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
                raise ValueError('Fix.getSightings: missing mandatory tag')
            
            bodydata = self.getText(body[0].childNodes)
            if len(bodydata) == 0:
                raise ValueError('Fix.getSightings: no body information')
            OneSighting.setBody(bodydata)
            datedata = self.getText(date[0].childNodes)
            pattern=re.compile(r'(^\d\d\d\d-\d\d-\d\d$)')
            ifmatch = pattern.match(datedata)
            if not ifmatch:
                raise ValueError('Fix.getSightings: date format is incorrect')
            self.datecheck(datedata)
            OneSighting.setDate(datedata)
            timedata = self.getText(time[0].childNodes)
            pattern=re.compile(r'(^\d\d:\d\d:\d\d$)')
            ifmatch = pattern.match(timedata)
            if not ifmatch:
                raise ValueError('Fix.getSightings: time format is incorrect')
            self.timecheck(timedata)
            OneSighting.setTime(timedata)
            obvdata = self.getText(obv[0].childNodes)
            angle=Angle.Angle()
            anglecheck=Angle.Angle()
            self.anglecheck(obvdata)
            obvdata=angle.setDegreesAndMinutes(obvdata)
            checkdata=anglecheck.setDegreesAndMinutes('0d0.1')
            if obvdata < checkdata:
                raise ValueError('Fix.getSightings: observation altitude is less than 0d0.1')
            obvdatarad=obvdata*math.pi/180
            if not (len(height) == 0 or self.getText(height[0].childNodes)==''):
                heightdata=self.getText(height[0].childNodes)
                heightdata=float(heightdata)
                if heightdata < 0:
                    raise ValueError('Fix.getSightings: height has to be greater than or equal to 0')
                OneSighting.setheight(heightdata)
            if not (len(temt) == 0 or self.getText(temt[0].childNodes)==''):    
                temtdata = self.getText(temt[0].childNodes)
                temtdata = int(temtdata)
                if temtdata < -20 or temtdata > 120:
                    raise ValueError('Fix.getSightings: temperature has to be greater than or equal -20 or less than or equal to 120')
                OneSighting.setTemt(temtdata)
            if not (len(pres) == 0 or self.getText(pres[0].childNodes)==''):  
                presdata = self.getText(pres[0].childNodes)
                presdata = int(presdata)
                if presdata < 100 or presdata > 1100:
                    raise ValueError('Fix.getSightings: pressure has to be greater than or equal to 100 or less than or equal to 1100')
                OneSighting.setPres(presdata)
            if not (len(horz) == 0 or self.getText(horz[0].childNodes)==''):  
                horzdata = self.getText(horz[0].childNodes)
                if not (horzdata == 'Artificial' or  horzdata == 'artificial' or horzdata == 'Natural' or horzdata == 'natural'):
                    raise ValueError('Fix.getSightings: horizon has to be artificial or natural')
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
        self.sightingList.sort(key=attrgetter('date','time','body'))
        for sighting in self.sightingList:
            self.file.write(self.gettime()+ '\t' + sighting.body + '\t' + sighting.date + '\t' + sighting.time + '\t' + sighting.adjAtl + '\n')
        self.file.write(self.gettime() + '\t' + 'End of sighting file:' + '\t' + self.sightingFile + '\n')
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
            raise ValueError('Fix.getSightings: observation violates the parameter specifications')
        else:
            for index in range(len(obv)):
                if obv[index]=='d':
                    break
            deg=int(obv[ :index])
            dec=float(obv[index+1: ])
        if (deg < 0 or deg >= 90) or (dec<0.0 or dec >= 60.0):
            raise ValueError('Fix.getSightings: degree violates the limit')
        return
    
    def datecheck(self,date):
        month=date[5:7]
        if int(month)>12:
            raise ValueError('Fix.getSightings: date value violates the specification')
        day=date[8:10]
        if int(day)>31:
            raise ValueError('Fix.getSightings: date value violates the specification')
        
    def timecheck(self,time):
        hour=time[:2]
        if int(hour)>24:
            raise ValueError('Fix.getSightings: time value violates the specification')
        minute=time[3:5]
        if int(minute)>60:
            raise ValueError('Fix.getSightings: time value violates the specification')
        second=time[6:]
        if int(second) > 60:
            raise ValueError('Fix.getSightings: time value violates the specification')
        
    
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
    