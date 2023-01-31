import unittest
from DBBand6Cart.MixerTests import MixerTest, MixerTests
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_MixerTests(unittest.TestCase):
    '''
    TODO: this test uses real data from the database.
    It would be better to use synthetic data which is guaranteed to be reproducable.
    '''
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = MixerTests(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
    
    def test_create(self):
        testId = self.__create()
        self.assertTrue(testId > 0)
        self.assertTrue(self.obj.delete(testId))
    
    def test_read(self):
        records = self.obj.read(keyMixerTest = 6778)
        self.assertTrue(len(records) == 1)
        rec = records[0]
        self.assertTrue(rec.key == 6778)
        self.assertTrue(rec.configId == 2100)
        self.assertTrue(rec.fkSoftwareVersion == 0)
        self.assertTrue(rec.fkTestType == 1)
        self.assertTrue(rec.description == 'SWTEST')
        self.assertTrue(rec.operator == 'MM')
        
        records = self.obj.read(configId = 2100)
        self.assertTrue(len(records) >= 5)
        rec = records[0]
        self.assertTrue(rec.key == 6779)
        
        records = self.obj.read(keyTestType = 1)
        self.assertTrue(len(records) >= 999)
    
    def test_update(self):
        pass    # not implemented
    
    def test_delete(self):
        testId = self.__create()
        self.obj.delete(testId)
        records = self.obj.read(keyMixerTest = testId)
        self.assertFalse(records)
        
    def test_deleteMany(self):
        testId = self.__create()
        self.obj.deleteMany([testId])
        records = self.obj.read(keyMixerTest = testId)
        self.assertFalse(records)
    
    def __create(self):
        mixerTest = MixerTest(
            configId = 1234,
            fkSoftwareVersion = 5678,
            fkTestType = 1,
            description = 'record created by test_MixerTests',
            operator = 'robot'
        )            
        return self.obj.create(mixerTest)
        