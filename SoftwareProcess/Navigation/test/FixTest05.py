'''
Created on Nov 23, 2016

@author: artha
'''
import unittest
import os
import uuid
import Navigation.prod.Fix as F

class Test(unittest.TestCase):

    def setUp(self):
        self.className = "Fix."
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.ariesFileName = "CA03_Valid_Aries.txt"
        self.starFileName = "CA03_Valid_Stars.txt"
        pass


    def tearDown(self):
        pass
    
    
# Acceptance test:100
# Fix.getSightings
#         Analysis
#             input:
#             string(assumdeLatitude,assumedLongitude)
#             output:
#             a tuple of two string
#             
#             state change:
#             add assumedLatitude, assumedLongitude, azimuthAdjustment and distanceAdjustment into logfile
#             add conclusion at the end line
#
#             Sad path:
#             input is not string
#             assumdeLatitude input degree larger than or equal to 90, Input an degree 0 with h as N or S, Input an valid degree without h
#             assumedLongitude input degree larger than or equal to 360
#
# 
#             Happy path:
#             add assumedLatitude, assumedLongitude, azimuthAdjustment and distanceAdjustment into logfile
#             add conclusion at the end line
#             return a tuple of latitude and longitude
    def test100_910_ShouldRaiseExceptionOnNonStringInput(self):
        expectedDiag = self.className + "getSightings:"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile("CA02_300_ValidMultipleStarSighting.xml")
            theFix.setAriesFile(self.ariesFileName)
            theFix.setStarFile(self.starFileName)
            theFix.getSightings(12,30)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.cleanup() 
    
    def test100_920_ShouldRaiseExceptionOnOneNonStringInput(self):
        expectedDiag = self.className + "getSightings:"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile("CA02_300_ValidMultipleStarSighting.xml")
            theFix.setAriesFile(self.ariesFileName)
            theFix.setStarFile(self.starFileName)
            theFix.getSightings(30)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.cleanup() 
        
    def test100_930_ShouldRaiseExceptionOnInvalidInput(self):
        expectedDiag = self.className + "getSightings:"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile("CA02_300_ValidMultipleStarSighting.xml")
            theFix.setAriesFile(self.ariesFileName)
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('N30d2.6','1000d3.2')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.cleanup() 
        
    def test100_940_ShouldRaiseExceptionOnInvalidInput2(self):
        expectedDiag = self.className + "getSightings:"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile("CA02_300_ValidMultipleStarSighting.xml")
            theFix.setAriesFile(self.ariesFileName)
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('100d2.6','4000d3.2')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        self.cleanup() 
    
    def test100_010_ShouldReturnATuple(self):
        expectedResult = ("S20d15.5", "79d19.9")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("Fix05Test.xml")
        theFix.setAriesFile(self.ariesFileName)
        theFix.setStarFile(self.starFileName)
        result = theFix.getSightings('N27d59.5','85d33.4')
        print(self.RANDOM_LOG_FILE)
        self.assertTupleEqual(expectedResult, result)
        self.cleanup() 
        
    def test100_011_ShouldReturnATupleWithThreeSightingInput(self):
        expectedResult = ("S13d28.0", "101d42.2")
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("Fix05Test2.xml")
        theFix.setAriesFile(self.ariesFileName)
        theFix.setStarFile(self.starFileName)
        result = theFix.getSightings('S53d38.4','74d35.3')
        print(self.RANDOM_LOG_FILE)
        self.assertTupleEqual(expectedResult, result)
        self.cleanup() 
    
    
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  

