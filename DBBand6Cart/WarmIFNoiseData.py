from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pandas import DataFrame
from .schemas.WarmIFNoise import COLUMNS, WarmIFNoise
from .schemas.DUT_Type import DUT_Type
from .GetLastInsertId import getLastInsertId
from datetime import datetime
from typing import Dict, Union

class WarmIFNoiseData(object):
    """
    Create, Read, Update, Delete records in dbBand6Cart.WarmIF_Noise_Data
    We use pandas.DataFrame to convey records in and out.
    """    

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)
        
    def create(self, record: WarmIFNoise):
        """
        Create records in WarmIF_Noise_Data
        :param data: WarmIFNoise record
        """
        # make column list, skipping keyCartTest:
        q = f"INSERT INTO WarmIF_Noise_Data({','.join(COLUMNS[1:])}) VALUES ({record.getInsertVals()});"
        self.DB.execute(q, commit = True)
        record.key = getLastInsertId(self.DB)
        return record.key
    
    def read(self, fkCartTest:int, dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        """
        q = f"SELECT {','.join(COLUMNS)} FROM WarmIF_Noise_Data WHERE fkCartTest = {fkCartTest}"
        if dutType != DUT_Type.Unknown:
            q += f" AND fkDUT_Type = {dutType.value}"
        q += " ORDER BY keyWarmIF_Noise_Data;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = COLUMNS)
    
    def readCartTests(self, dutType:DUT_Type = DUT_Type.Unknown) -> Dict[int, Dict[str, Union[int, datetime]]]:
        """
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return dict: {cartTestId: {'numMeasurements': int, 'minTS': datetime, 'maxTS': datetime}
        """
        q = "SELECT fkCartTest, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS FROM WarmIF_Noise_Data"
        if dutType != DUT_Type.Unknown:
            q += f" WHERE fkDUT_Type = {dutType.value}"
        q += " GROUP BY fkCartTest ORDER BY fkCartTest;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return {row[0] : {
                'numMeasurements': row[1], 
                'minTS': makeTimeStamp(row[2]), 
                'maxTS': makeTimeStamp(row[3])
            } for row in rows}
    
    def isNewerData(self, timeStamp: datetime) -> bool:
        q = f"SELECT TS FROM WarmIF_Noise_Data WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False
