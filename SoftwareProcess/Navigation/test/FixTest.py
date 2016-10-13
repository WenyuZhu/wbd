'''
Created on Oct 9, 2016

@author: artha
'''
import unittest
import Navigation.prod.Fix as Fix
from copyreg import constructor
from wsgiref import validate
from fileinput import filename


class FixTest(unittest.TestCase):


    def setUp(self):
        self.className = 'Fix.'


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
#             add 'start of log' in file
#             create a file handler
#
#             Sad path:
#             input is not string
# 
#             Happy path:
#             create a logfile if it doesn't exist
#             or append to the file if it already exist
#             start with 'start of log'
            
#Sad path

    def test100_090_ShouldRaiseExceptionOnNonStringInput(self):
        expectedDiag = self.className + "_init_:"
        with self.assertRaises(ValueError) as context:
            fix=Fix.Fix(123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
          
#Happy path
    def test100_020_ShouldCreateAnInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
          
    def test100_030_ShouldCreateAnInstanceOfFix(self):
        self.assertIsInstance(Fix.Fix('logFile2'), Fix.Fix)
          
# Acceptance test:200
#         Analysis - setSightingFile
#             input f.xml:
#             a string as a filename
#             f-> str
#             .xml->Mandatory
#             output:
#             boolean value repersenting whether the file already exists
#             
#             state change:
#             write 'Start of sighting file f.xml' in to log file
#             where f.xml is actual file name
#             
#             Sad path:
#             input is not string
#             no input
#             input doesn't match specification
#             
#             Happy path:
#             setSightingFile('stars.xml') True
#             setSightingFile('stars.xml') False
  
#Sad path
    def test200_090_ShouldRaiseValueError(self):
        expectedDiag = self.className + "setSightingFile:"
        fix=Fix.Fix()
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile(432)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
              
    def test200_091_ShouldRaiseValueError(self):
        expectedDiag = self.className + "setSightingFile:"
        fix=Fix.Fix()
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
      
    def test200_092_ShouldRaiseValueError(self):
        expectedDiag = self.className + "setSightingFile:"
        fix=Fix.Fix()
        with self.assertRaises(ValueError) as context:
            fix.setSightingFile('a2gf.wsdx')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
         
#Happy path
    def test200_010_ShouldReturnTrue(self):
        fix=Fix.Fix()
        self.assertTrue(fix.setSightingFile('stars.xml'))
        
    def test200_020_ShouldReturnFalse(self):
        fix=Fix.Fix()
        self.assertTrue(fix.setSightingFile('stars.xml'))
        self.assertFalse(fix.setSightingFile('stars.xml'))
        
# Acceptance test:300
#    Analysis - getSightings
#        input:
#        None
#        output:
#        approximated Latitude and approximated Longitude
#        in this program those are '0d0.0'
#
#        state change:
#        getSightings() should produce a single log entry sighting in the "sightingFile"
#
#        Sad path:
#        no sightingFile in instance
#        there is no mandatory tag in xml file
#        there are invalid calculation
#        there are invalid tag in sightingFlie
#
#        Happy path:
#        getSightings() '0d0.0','0d0.0'
        
#        Sad path
    def test300_090_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])    
        
    def test300_091_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('mandatorymissstars.xml') #'mandatorymissstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_092_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('Wrongformatstars.xml') #'Wrongformatstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_093_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('lowboundrystar.xml') #'lowboundrystar.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_094_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('boundarylimitstars.xml') #'boundarylimitstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_095_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('testheightboundarystars.xml') #'boundarylimitstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_096_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('testtemtboundarystars.xml') #'boundarylimitstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_097_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('testpresboundarystars.xml') #'boundarylimitstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)]) 
        
    def test300_098_ShouldRaiseValueError(self):
        expectedDiag = self.className + "getSightings:"
        fix=Fix.Fix()
        fix.setSightingFile('testhorzboundarystars.xml') #'boundarylimitstars.xml is a xml file with no mandatory tag'
        with self.assertRaises(ValueError) as context:
            fix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])         
        
#        Happy path
    def test300_010_ShouldReturnLatitudeAndLongitude(self):
        fix=Fix.Fix()
        fix.setSightingFile('optionalmissstars.xml')
        self.assertEqual(fix.getSightings(), ('0d0.0','0d0.0'))
        
    def test300_011_ShouldReturnLatitudeAndLongitude(self):
        fix=Fix.Fix()
        fix.setSightingFile('stars.xml')
        self.assertEqual(fix.getSightings(), ('0d0.0','0d0.0'))

