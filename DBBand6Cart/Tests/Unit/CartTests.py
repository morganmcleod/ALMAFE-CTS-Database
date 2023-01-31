import unittest
from DBBand6Cart.CartTests import CartTest, CartTests
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_CartTests(unittest.TestCase):
    '''
    TODO: this test uses real data from the database.
    It would be better to use synthetic data which is guaranteed to be reproducable.
    '''

    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = CartTests(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
    
    def test_create(self):
        testId = self.__create()
        self.assertTrue(testId > 0)
        self.assertTrue(self.obj.delete(testId))
    
    def test_read(self):
        records = self.obj.read(keyCartTest = 10839)
        self.assertTrue(len(records) == 1)
        rec = records[0]
        self.assertTrue(rec.key == 10839)
        self.assertTrue(rec.configId == 378)
        self.assertTrue(rec.fkSoftwareVersion == 1245)
        self.assertTrue(rec.fkTestType == 2)
        self.assertTrue(rec.description == 'Cart6.001 SWTEST')
        self.assertTrue(rec.operator == 'MM')
        
        records = self.obj.read(configId = 378)
        self.assertTrue(len(records) >= 100)
        rec = records[0]
        self.assertTrue(rec.key == 10926)

        records = self.obj.read(keyTestType = 1)
        self.assertTrue(len(records) >= 999)
    
        records = self.obj.read(serialNum = 20)
        self.assertTrue(len(records) >= 50)
    
    def test_update(self):
        pass    # not implemented
    
    def test_delete(self):
        testId = self.__create()
        self.obj.delete(testId)
        records = self.obj.read(keyCartTest = testId)
        self.assertFalse(records)
        
    def test_deleteMany(self):
        testId = self.__create()
        self.obj.deleteMany([testId])
        records = self.obj.read(keyCartTest = testId)
        self.assertFalse(records)
        
    def __create(self):
        cartTest = CartTest(
            configId = 2345,
            isSelection = False,
            fkTestType = 1,
            description = 'record created by test_CartTests',
            operator = 'robot'
        )
        return self.obj.create(cartTest)
