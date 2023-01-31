import unittest
from DBBand6Cart.schemas.CartConfig import CartConfig, CartConfig
from DBBand6Cart.CartConfigs import CartConfigs
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime


class test_CartConfigs(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = CartConfigs(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
    
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
                self.assertTrue(len(config.ESN1) == 16 or config.ESN1 == '')
                self.assertIsInstance(config.timeStamp, datetime)
        
        # retrieve and test a specific one:
        records = self.obj.read(configs[0].id)
        self.assertIsInstance(config, CartConfig)
        self.assertTrue(records[0].id > 0)
        self.assertTrue(len(records[0].serialNum) > 0)
        self.assertTrue(len(records[0].ESN0) == 16, msg = records[0].ESN0)
        self.assertTrue(len(records[0].ESN1) == 16 or config.ESN1 == '')
        self.assertIsInstance(records[0].timeStamp, datetime)
