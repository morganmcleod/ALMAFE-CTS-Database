import unittest
from Database.TestTypes import TestType, TestTypes
from app.LoadConfiguration import loadConfiguration

class test_TestTypes(unittest.TestCase):
    
    def setUp(self):
        self.obj = TestTypes(loadConfiguration('dbBand6Cart'))
        
    def tearDown(self):
        self.obj = None
    
    def test_read(self):
        # get all test types:
        testTypes = self.obj.read()
        
        # there should be at least 10:
        self.assertTrue(len(testTypes) >= 10)
        
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
