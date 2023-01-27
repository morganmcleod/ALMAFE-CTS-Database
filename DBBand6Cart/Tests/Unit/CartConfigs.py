import unittest
from Database.CartConfigs import CartConfig, CartConfigs
from app.LoadConfiguration import loadConfiguration
from datetime import datetime

class test_CartConfigs(unittest.TestCase):
    
    def setUp(self):
        self.obj = CartConfigs(loadConfiguration('dbBand6Cart'))
        
    def tearDown(self):
        self.obj = None
    
    def test_read(self):
        # get all latest configurations:
        configs = self.obj.read()
        
        # there should be more than 70 CCAs having latest configurations:
        self.assertTrue(len(configs) > 70)
        
        # test each one:
        for config in configs:
            # use subTest so loop will continue after first failure:
            with self.subTest(config = config):
                self.assertIsInstance(config, CartConfig)
                self.assertTrue(config.id > 0)
                self.assertTrue(len(config.serialNum) > 0)
                self.assertTrue(len(config.ESN0) == 16, msg = "key = {}: ESN0='{}'".format(config.id, config.ESN0))
                self.assertTrue(len(config.ESN1) == 16 or config.ESN1 is '')
                self.assertIsInstance(config.timeStamp, datetime)
        
        # retrieve and test a specific one:
        records = self.obj.read(configs[0].id)
        self.assertIsInstance(config, CartConfig)
        self.assertTrue(records[0].id > 0)
        self.assertTrue(len(records[0].serialNum) > 0)
        self.assertTrue(len(records[0].ESN0) == 16, msg = records[0].ESN0)
        self.assertTrue(len(records[0].ESN1) == 16 or config.ESN1 is '')
        self.assertIsInstance(records[0].timeStamp, datetime)
