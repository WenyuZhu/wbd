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
        
        


#  helper methods
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  