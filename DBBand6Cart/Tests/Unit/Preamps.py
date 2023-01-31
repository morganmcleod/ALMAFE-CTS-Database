import unittest
from DBBand6Cart.schemas.Preamp import Preamp
from DBBand6Cart.schemas.PreampParam import PreampParam
from DBBand6Cart.Preamps import Preamps
from DBBand6Cart.PreampParams import PreampParams
from DBBand6Cart.LoadConfiguration import loadConfiguration
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime

class test_Preamps(unittest.TestCase):
    
    def setUp(self):
        self.driver = DriverMySQL(loadConfiguration('ALMAFE-CTS-Database.ini', 'dbBand6Cart'))
        self.obj = Preamps(driver = self.driver)
        
    def tearDown(self):
        self.obj = None
        self.driver.disconnect()

    def test_readPreamps(self):
        for key in (3329, 3323, 3278, 2594, 2540):
            with self.subTest(key = key):
                rows = self.obj.readPreamps(keyPreamps = key)
                self.assertEqual(len(rows), 1)
                row = rows[0]
                self.assertIsInstance(row, Preamp)
                self.assertEqual(row.key, key)
                self.assertIsInstance(row.timeStamp, datetime)
                if row.serialNum is not None:
                    self.assertNotEqual(row.serialNum, "")
                if row.coldDataTS is not None:
                    self.assertIsInstance(row.coldDataTS, datetime)
        for key in (1178, 945, 1196, 1148, 1095):
            rows = self.obj.readPreamps(lna = 0, keyMxrPreampAssys = key)
            for row in rows:
                with self.subTest(row = row):
                    self.assertIsInstance(row, Preamp)
                self.assertIsInstance(row.timeStamp, datetime)
                if row.serialNum is not None:
                    self.assertNotEqual(row.serialNum, "")
                if row.coldDataTS is not None:
                    self.assertIsInstance(row.coldDataTS, datetime)
        for key in (1197, 1096, 1195, 1117, 1933):
            rows = self.obj.readPreamps(lna = 1, keyMxrPreampAssys = key)
            for row in rows:
                with self.subTest(row = row):
                    self.assertIsInstance(row, Preamp)
                self.assertIsInstance(row.timeStamp, datetime)
                if row.serialNum is not None:
                    self.assertNotEqual(row.serialNum, "")
                if row.coldDataTS is not None:
                    self.assertIsInstance(row.coldDataTS, datetime)
                
    
    def test_createPreamp(self):
        # self.obj.createPreamp(serialNum:str, coldDataBy:str = None, notes:str = None, copyFromId:int = None) -> int:
        pass

    def test_readPreampParams(self):
        
        # self.obj.readPreampParams(keyPreamps:int, freqLO:float = None) -> Optional[List[PreampParam]]:
        pass

    def test_createPreampParams(self):
        # self.obj.createPreampParams(fkPreamps:int, preampParams:List[PreampParam]) -> int:
        pass