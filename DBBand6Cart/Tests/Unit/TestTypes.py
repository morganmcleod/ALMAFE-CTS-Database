import unittest
from DBBand6Cart.TestTypes import TestType, TestTypes
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL

class test_TestTypes(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = TestTypes(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
    
    def test_read(self):
        # get all test types:
        testTypes = self.obj.read()
        
        # there should be at least 5:
        self.assertTrue(len(testTypes) >= 5)
        
        # test each one:
        for testType in testTypes:
            # use subTest so loop will continue after first failure:
            with self.subTest(testType = testType):
                self.assertIsInstance(testType, TestType)
                self.assertTrue(testType.id > 0)
                self.assertTrue(len(testType.name) > 0)
                self.assertTrue(len(testType.description) > 0)
            
        # retrieve and test a specific one: 
        testType = self.obj.read(testTypes[0].id)[0]
        self.assertIsInstance(testType, TestType)
        self.assertTrue(testType.id > 0)
        self.assertTrue(len(testType.name) > 0)
        self.assertTrue(len(testType.description) > 0)
