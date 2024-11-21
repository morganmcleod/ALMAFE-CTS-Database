import unittest
from DBBand6Cart.schemas.CartConfig import CartConfig, CartKeys
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
                self.assertTrue(config.key > 0)
                self.assertTrue(len(config.serialNum) > 0)
                self.assertIsInstance(config.timeStamp, datetime)
        
        # retrieve and test a specific one:
        records = self.obj.read(configs[0].key)
        record = records[0]
        self.assertIsInstance(config, CartConfig)
        self.assertTrue(record.key > 0)
        self.assertTrue(len(record.serialNum) > 0)
        self.assertIsInstance(record.timeStamp, datetime)

        for config in configs:
            keys = self.obj.readKeys(config.key, 0)
            # use subTest so loop will continue after first failure:
            with self.subTest(keys = keys):
                if keys:           
                    self.assertIsInstance(keys, CartKeys)
                    self.assertTrue(keys.key > 0)
                    self.assertTrue(keys.keyMixer > 0)
                    self.assertTrue(keys.keyChip1 > 0)
                    self.assertTrue(keys.keyChip2 > 0)
                    self.assertTrue(keys.keyPreamp1 > 0)
                    self.assertTrue(keys.keyPreamp2 > 0)        
                    self.assertIsInstance(keys.timeStamp, datetime)
