""" Create and read records in the DBBand6Cart.BeamPatterns table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from DBBand6Cart.schemas.SelectTestsRecord import SelectTestsRecord
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .schemas.BeamPattern import BeamPattern, COLUMNS
from .GetLastInsertId import getLastInsertId

class BeamPatterns():
    """ Create and read records in the DBBand6Cart.BeamPatterns table
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor
        
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BeamPattern) -> Optional[int]:
        """ Insert one record

        :param record to insert. record.key will be updated with the new keyBeamPatterns
        :return keyBeampPattern: int or None if error.
        """
        q = f"INSERT INTO BeamPatterns({','.join(COLUMNS[1:-1])}) VALUES ({record.getInsertVals()});"
        self.DB.execute(q, commit = True)

        record.key = getLastInsertId(self.DB)
        return record.key
                    
    def read(self, keyId: int = None, fkCartTest: int = None) -> List[BeamPattern]:
        """ Read one or more records
        
        Either keyId or fkCartTest must be provided.
        :param int keyId: of a specific record to read, defaults to None
        :param int fkCartTest: read all associated records, defaults to None
        :return List[BeamPattern]
        """
        assert keyId or fkCartTest

        q = f"SELECT {','.join(COLUMNS)} FROM BeamPatterns"
        where = ""

        if keyId:
            where += f"keyBeamPattern = {keyId}"
        if fkCartTest:
            if where:
                where += " AND "
            where += f"fkCartTest = {fkCartTest}"

        if where:
            q += " WHERE " + where
        
        q += f" ORDER BY {COLUMNS[0]} ASC;"
    
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BeamPattern(
            key = row[0],
            fkCartTest = row[1],
            FreqLO = row[2],
            FreqCarrier = row[3],
            Beam_Center_X = row[4],
            Beam_Center_Y = row[5],
            Scan_Angle = row[6],
            Scan_Port = row[7],
            Lvl_Angle = row[8],
            AutoLevel = row[9],
            Resolution = row[10],
            SourcePosition = row[11],
            timeStamp = makeTimeStamp(row[12])
        ) for row in rows]

    def readCarrierFreqs(self, fkParentTest:int):
        q = f"SELECT MIN(TimeStamp), MIN(keyBeamPattern), FreqCarrier FROM BeamPatterns WHERE fkCartTest={fkParentTest} GROUP BY FreqCarrier;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [SelectTestsRecord(
                fkParentTest = fkParentTest,
                fkDutType = 0,
                fkChildTest = row[1],
                timeStamp = makeTimeStamp(row[0]),
                frequency = row[2],
                text = str(row[2])
            ) for row in rows]

    def readScans(self, fkParentTest:int, freqCarrier:float):
        q = f"SELECT {','.join(COLUMNS)} FROM BeamPatterns WHERE fkCartTest = {fkParentTest} AND FreqCarrier = {freqCarrier} ORDER BY keyBeamPattern ASC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            items = [BeamPattern(
                key = row[0],
                fkCartTest = row[1],
                FreqLO = row[2],
                FreqCarrier = row[3],
                Beam_Center_X = row[4],
                Beam_Center_Y = row[5],
                Scan_Angle = row[6],
                Scan_Port = row[7],
                Lvl_Angle = row[8],
                AutoLevel = row[9],
                Resolution = row[10],
                SourcePosition = row[11],
                timeStamp = makeTimeStamp(row[12])
            ) for row in rows]

            return [SelectTestsRecord(
                fkParentTest = fkParentTest,
                fkDutType = 0,
                fkChildTest = item.key,
                timeStamp = item.timeStamp,
                frequency = item.FreqCarrier,
                text = item.getDescription()
            ) for item in items]
