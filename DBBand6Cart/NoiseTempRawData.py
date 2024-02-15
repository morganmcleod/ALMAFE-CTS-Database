from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.CombineTestsRecord import CombineTestsRecord
from .schemas.DUT_Type import DUT_Type
from .schemas.NoiseTempRawDatum import COLUMNS, NoiseTempRawDatum
from .GetLastInsertId import getLastInsertId
from pandas import DataFrame
from typing import List
from datetime import datetime

class NoiseTempRawData(object):
    """
    Create, Read, Update, Delete records in dbBand6Cart.NT_Raw_Data
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
        
    def create(self, record: NoiseTempRawDatum):
        """
        Create records in WarmIF_Noise_Data
        :param record: NoiseTempRawDatum record
        """
        # make column list, skipping keyCartTest:
        q = f"INSERT INTO NT_Raw_Data({','.join(COLUMNS[1:])}) VALUES ({record.getInsertVals()});"
        self.DB.execute(q, commit = True)
        record.key = getLastInsertId(self.DB)
        return record.key
        
    def read(self, fkCartTest:int, dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read records referencing fkCartTest
        :param fkCartTest: selector
        :return pandas.DataFrame
        """
        q = f"SELECT {','.join(COLUMNS)} FROM NT_Raw_Data WHERE fkCartTest = {fkCartTest}"
        if dutType != DUT_Type.Unknown:
            q += f" AND fkDUT_Type = {dutType.value}"
        q += " ORDER BY keyNT_Raw_Data;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = COLUMNS)
    
    def readCartTests(self, dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read the distinct values of fkCartTest in the table.
        
        TODO: this query would benefit from an index on fkCartTest.
        :return dict { fkCartTest: (numMeas, minTS, maxTS) } 
        """
        q = "SELECT fkCartTest, COUNT(*) AS numMeas, MIN(TS) AS minTS, MAX(TS) AS maxTS FROM NT_Raw_Data"
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
        q = f"SELECT TS FROM NT_Raw_Data WHERE TS > '{timeStamp}' LIMIT 1;"
        self.DB.execute(q)
        row = self.DB.fetchone()
        return True if row else False
        
    def readLOFreqs(self, fkCartTest:int, dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read the available LO frequencies for a fkCartTest
        :param fkCartTest: fkCartTest or fkMxrTest
        :return list[CombineTestsRecord] or None if not found
        """
        q = f"SELECT MIN(TS), FreqLO FROM NT_Raw_Data WHERE fkCartTest={fkCartTest}"
        if dutType != DUT_Type.Unknown:
            q += f" WHERE fkDUT_Type = {dutType.value}"
        q += " GROUP BY FreqLO;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [CombineTestsRecord(
                key = 0,
                fkParentTest = fkCartTest,
                fkDutType = DUT_Type.Unknown.value,
                timeStamp = row[0],         # MIN(TS)
                path0_TestId = 0,
                path1 = str(row[1]),        # frequency
                text = str(row[1])          # frequency
            ) for row in rows]

    def readSelected(self, selection:List[CombineTestsRecord], dutType:DUT_Type = DUT_Type.Unknown):
        """
        Read noise temperature raw data specific cartTestIds and LO frequencies
        :param selection: list[CombineTestsRecord] to retrieve
        :return pandas DataFrame or None if not found
        """
        q = "SELECT {} FROM NT_Raw_Data".format(",".join(COLUMNS)) 
        
        where = ""
        for sel in selection:
            if where:
                where += " OR "
            where += f"(fkCartTest={sel.path0_TestId} AND FreqLO={float(sel.path1)})"
        if dutType != DUT_Type.Unknown:
            where = f" fkDUT_Type={dutType.value} AND (" + where + ")"
        q += " WHERE " + where + " ORDER BY keyNT_Raw_Data;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return DataFrame(rows, columns = COLUMNS)       
