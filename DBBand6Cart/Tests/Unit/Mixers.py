import unittest
from DBBand6Cart.schemas.MixerParam import MixerParam
from DBBand6Cart.MixerConfigs import MixerConfigs
from DBBand6Cart.MixerParams import MixerParams
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_Mixers(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.mixerConfigs = MixerConfigs(driver = self.driver)
        self.mixerParams = MixerParams(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
   
    def test_readMixerParams(self):
        for id in (1178, 945, 1196, 1148, 1095, 1197, 1096, 1195, 1117, 1933):
            with self.subTest(id = id):
                 keys = self.mixerConfigs.readKeys(id)
                 if keys:
                    rows = self.mixerParams.read(keys.keyChip1)
                    row = rows[0]
                    self.assertIsInstance(row, MixerParam)
                    self.assertGreater(row.key, 0)
                    self.assertGreater(row.fkMixerChips, 0)
                    self.assertGreater(row.FreqLO, 0)
                    self.assertIsInstance(row.timeStamp, datetime)
                    self.assertGreater(abs(row.VJ), 0)
                    self.assertGreater(abs(row.IJ), 0)
                    self.assertGreater(row.IMAG, 0)

    def test_createMixerParams(self):
        # TODO
        pass