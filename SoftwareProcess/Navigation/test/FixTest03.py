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
        os.remove('log.txt') 
        
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
#             Sad path:
#             input is not string
#             no input
#             input doesn't match specification
#             
#             Happy path:
#             setSightingFile('stars.xml') True
#             setSightingFile('stars.xml') False

    def test200_010_ShouldSetValidSightingFile(self):
        theFix = F.Fix()
        result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
        self.assertEquals(result,os.path.abspath("CA02_200_ValidStarSightingFile.xml"))
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(os.path.abspath("CA02_200_ValidStarSightingFile.xml")))
        theLogFile.close()
        os.remove('log.txt') 


#  helper methods
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  