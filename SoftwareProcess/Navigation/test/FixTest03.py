'''
Created on Oct 27, 2016

@author: artha
'''
import unittest
import Navigation.prod.Fix as F
import os
import uuid

class Test(unittest.TestCase):


    def setUp(self):
        self.className = "Fix."
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.DEFAULT_LOG_FILE = "log.txt"
        pass


    def tearDown(self):
        pass



# Acceptance test:100
#         Analysis - constructor
#             input:
#             string or none
#             output:
#             instance of Fix
#             
#             state change:
#             add time, 'start of log', 'Log file: and absolute file path' in file
#             create a file handler
#
#             Sad path:
#             input is not string
# 
#             Happy path:
#             create a logfile if it doesn't exist
#             or append to the file if it already exist
#             start with time, 'start of log', 'Log file: and absolute file path'
            

    def test100_010_ShouldConstructFixWithoutNamedFile(self):
        theFix = F.Fix()
        try:
            theLogFile = open('log.txt', 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find('Log file:'+'\t'+os.path.abspath('log.txt')))
        except IOError:
            self.fail()
        os.remove(self.DEFAULT_LOG_FILE) 
        
    def test100_020_ShouldConstructFixWithNamedFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find('Log file:'+'\t'+os.path.abspath(self.RANDOM_LOG_FILE)))
        except IOError:
            self.fail()
        self.cleanup()  
 
# Acceptance test:200
#         Analysis - setSightingFile
#             input f.xml:
#             a string as a filename
#             f-> str
#             .xml->Mandatory
#             output:
#             absolute file path
#             
#             state change:
#             write absolute file path in to log file
#             
#             
#             
#             Happy path:
#             setSightingFile('CA02_200_ValidStarSightingFile.xml') return pathfile

    def test200_010_ShouldSetValidSightingFile(self):
        theFix = F.Fix()
        result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
        self.assertEquals(result,os.path.abspath("CA02_200_ValidStarSightingFile.xml"))
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath("CA02_200_ValidStarSightingFile.xml")))
        theLogFile.close()
        os.remove(self.DEFAULT_LOG_FILE) 

# Acceptance test:300
#         Analysis - setAriesFile
#             input f.txt:
#             a string as a filename
#             f-> str

#             output:
#             absolute file path
#             
#             state change:
#             write absolute file path in to log file
#             #    Sad tests:
#        sightingFile:
#            nonstring -> setAriesFile(42)
#            length error -> setAriesFile(".txt")
#            nonXML -> setAriesFile("aries.xml")
#            missing -> setAriesFile()
#            nonexistent file -> setAriesFile("missing.txt")
#             
#             
#             Happy path:
#             setAriesFile('aries.txt') return pathfile

    def test300_910_ShouldRaiseExceptionOnNonAriesFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        os.remove(self.DEFAULT_LOG_FILE)

    def test300_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE) 
        
    def test300_930_ShouldRaiseExceptionOnNonTXTFile1(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("sighting.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE) 
        
    def test300_940_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile('missing.txt')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test300_010_ShouldSetValidAriesFile(self):
        theFix = F.Fix()
        result = theFix.setAriesFile('aries.txt')
        self.assertEquals(result,os.path.abspath('aries.txt'))
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath('aries.txt')))
        theLogFile.close()
        os.remove(self.DEFAULT_LOG_FILE)

# Acceptance test:400
#         Analysis - setStarFile
#             input f.txt:
#             a string as a filename
#             f-> str

#             output:
#             absolute file path
#             
#             state change:
#             write absolute file path in to log file
#             #    Sad tests:
#        sightingFile:
#            nonstring -> setStarFile(42)
#            length error -> setStarFile(".txt")
#            nonXML -> setStarFile("aries.xml")
#            missing -> setStarFile()
#            nonexistent file -> setStarFile("missing.txt")
#             
#             
#             Happy path:
#             setStarFile('stars.txt') return pathfile

    def test400_910_ShouldRaiseExceptionOnNonStarFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])  
        os.remove(self.DEFAULT_LOG_FILE)

    def test400_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE) 
        
    def test400_930_ShouldRaiseExceptionOnNonTXTFile1(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("sighting.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE) 
        
    def test400_940_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = F.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile('missing.txt')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE)

    def test400_010_ShouldSetValidStarFile(self):
        theFix = F.Fix()
        result = theFix.setStarFile('stars.txt')
        self.assertEquals(result,os.path.abspath('stars.txt'))
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath('stars.txt')))
        theLogFile.close()
        os.remove(self.DEFAULT_LOG_FILE)
        
# 500 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting, two txt of aries and stars
#        outputs:
#            returns:    ("0d0.0", "0d0.0")
#            via file:    writes valid body /t date /t time /t adjusted altitude /t geographic position latitude /t geographic position longitude in sorted order
#        entry criterion:
#            setSightingsFile, setAriesFile and set StarFile must be called first
#
#    Happy tests:
#        sighting file 
#            valid file with any sightings, aries and stars -> should return ("0d0.0", "0d0.0")
#        sighting file contents
#            valid file with several invalid elements -> report the number of invalid sighting
#            valid file with valid bodies -> geographic position latitude and geographic position longitude following previous content
#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            aries file not previously set
#            star file not previously set

    def test500_910_ShouldRaiseExceptionOnNotSettingAriesFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setSightingFile('CA02_300_ValidOneStarWithDefaultValues.xml')
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_920_ShouldRaiseExceptionOnNotSettingAriesFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = F.Fix()
        theFix.setSightingFile('CA02_300_ValidOneStarWithDefaultValues.xml')
        theFix.setAriesFile('aries.txt')
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_930_ShouldRaiseExceptionOnMissingMandatoryTag(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidWithMissingMandatoryTags.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_940_ShouldRaiseExceptionOnInvalidBody(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidBody.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_950_ShouldRaiseExceptionOnInvalidDate(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidDate.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_960_ShouldRaiseExceptionOnInvalidTime(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidTime.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)

    def test500_970_ShouldRaiseExceptionOnInvalidObservation(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidObservation.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_980_ShouldRaiseExceptionOnInvalidHeight(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidHeight.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_990_ShouldRaiseExceptionOnInvalidTemperature(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidTemperature.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_991_ShouldRaiseExceptionOnInvalidPressure(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidPressure.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_992_ShouldRaiseExceptionOnInvalidHorizon(self):
        theFix = F.Fix()
        theFix.setSightingFile("CA02_300_InvalidHorizon.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
#         os.remove(self.DEFAULT_LOG_FILE)
        
    def test500_010_ShouldLogMultipleSightingsWithSameDateTime(self):       
        targetStringList = [
            ["Acrux", "2016-03-01", "00:05:05"],
            ["Sirius", "2016-03-01", "00:05:05"],
            ["Canopus", "2016-03-02", "23:40:01"]
            ]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("CA02_300_ValidMultipleStarSightingSameDateTime.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
         
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        # find entry with first star
        entryIndex = self.indexInList(targetStringList[0][0], logFileContents)
        self.assertLess(-1, entryIndex, 
                           "failure to find " + targetStringList[0][0] +  " in log")
        for index in range(entryIndex+1, len(targetStringList)):
            entryIndex += 1
            if(not(targetStringList[index][0] in logFileContents[entryIndex])):
                self.fail("failure to find star in log")
        self.cleanup()   
        
    def test500_020_ShouldLogMultipleSightingsWithInvalidAngleInAriesFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("CA02_300_ValidMultipleStarSightingSameDateTime.xml")
        theFix.setAriesFile('arieswithwrongangle.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
         
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        # find entry with first star
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'2'))
        self.cleanup()  
        
    def test500_030_ShouldLogMultipleSightingsWithInvalidAngleInStarFile(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("CA02_300_ValidMultipleStarSightingSameDateTime.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('starswithwrongangle.txt')
        theFix.getSightings()
         
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        # find entry with first star
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'1'))
        self.cleanup()  
        
        
    def test500_040_ShouldLogMultipleSightingsWithValidAngle(self):
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile("CA03_500_ValidMultipleStarSighting.xml")
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.getSightings()
         
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        # find entry with first star
        self.assertNotEquals(-1,logFileContents[-1].find('Sighting errors:'+'\t'+'0'))
        self.cleanup() 
        
#  helper methods
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  
            
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1