import unittest
from DBBand6Cart.schemas.MixerConfig import MixerConfig, MixerKeys
from DBBand6Cart.MixerConfigs import MixerConfigs
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_MixerConfigs(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = MixerConfigs(driver = self.driver)
        
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
                self.assertIsInstance(config, MixerConfig)
                self.assertTrue(config.id > 0)
                self.assertTrue(len(config.serialNum) > 0)
                self.assertIsInstance(config.timeStamp, datetime)
        
        # retrieve and test a specific one:
        records = self.obj.read(configs[0].id)
        record = records[0]
        self.assertIsInstance(config, MixerConfig)
        self.assertTrue(record.id > 0)
        self.assertTrue(len(record.serialNum) > 0)
        self.assertIsInstance(record.timeStamp, datetime)
        
        # retrieve keys:
        for config in configs:
            keys = self.obj.readKeys(config.id)
            # use subTest so loop will continue after first failure:
            with self.subTest(keys = keys):
                if keys:           
                    self.assertIsInstance(keys, MixerKeys)
                    self.assertTrue(len(keys.snMixer) > 0)
                    self.assertTrue(keys.id > 0)
                    self.assertTrue(keys.keyChip1 > 0)
                    self.assertTrue(keys.keyChip2 > 0)
                    self.assertTrue(keys.keyPreamp1 > 0)
                    self.assertTrue(keys.keyPreamp2 > 0)        
                    self.assertIsInstance(keys.timeStamp, datetime)