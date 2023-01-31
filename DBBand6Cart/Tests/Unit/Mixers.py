import unittest
from DBBand6Cart.schemas.MixerParam import MixerParam
from DBBand6Cart.MixerParams import MixerParams
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_Mixers(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = MixerParams(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()
   
    def test_readMixerParams(self):
        for key in (1178, 945, 1196, 1148, 1095, 1197, 1096, 1195, 1117, 1933): 
            rows = self.obj.readMixerParams(keyMxrPreampAssys = key, freqLO = None)
            for row in rows:
                with self.subTest(row = row):
                    self.assertIsInstance(row, MixerParam)
                    self.assertGreater(row.key, 0)
                    self.assertGreater(row.fkMixerChips, 0)
                    self.assertGreater(row.FreqLO, 0)
                    self.assertIsInstance(row.timeStamp, datetime)
                    self.assertGreater(row.VJ, 0)
                    self.assertGreater(row.IJ, 0)
                    self.assertGreater(row.IMAG, 0)
        for key in (1178, 945, 1196, 1148, 1095, 1197, 1096, 1195, 1117, 1933): 
            rows = self.obj.readMixerParams(keyMxrPreampAssys = key, freqLO = 221.0)
            for row in rows:
                with self.subTest(row = row):
                    self.assertIsInstance(row, MixerParam)
                    self.assertGreater(row.key, 0)
                    self.assertGreater(row.fkMixerChips, 0)
                    self.assertEqual(row.FreqLO, 221.0)
                    self.assertIsInstance(row.timeStamp, datetime)
                    self.assertGreater(row.VJ, 0)
                    self.assertGreater(row.IJ, 0)
                    self.assertGreater(row.IMAG, 0)

    def test_createMixerParams(self):
        # TODO
        pass