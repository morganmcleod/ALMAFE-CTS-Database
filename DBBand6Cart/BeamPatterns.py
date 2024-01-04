""" Create and read records in the DBBand6Cart.BeamPatterns table
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from datetime import datetime
from typing import List, Optional
from .schemas.BeamPattern import BeamPattern, COLUMNS
from .schemas.CombineTestsRecord import CombineTestsRecord
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

    def readCarrierFreqs(self, fkParentTest:int) -> List[CombineTestsRecord]:
        q = f"SELECT MIN(TimeStamp), FreqCarrier FROM BeamPatterns WHERE fkCartTest={fkParentTest} GROUP BY FreqCarrier;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return None
        else:
            return [CombineTestsRecord(
                key = row[1],
                fkParentTest = fkParentTest,
                fkDutType = 0,
                timeStamp = makeTimeStamp(row[0]),  # MIN(TimeStamp)
                path0_TestId = 0,
                path1 = str(row[1]),                # frequency
                text = f"{row[1]}"                  # frequency
            ) for row in rows]

    def readScans(self, fkParentTest: int = 0, freqCarrier: float = 0.0, keyBeamPattern: int = None) -> List[CombineTestsRecord]:
        q = f"SELECT {','.join(COLUMNS)} FROM BeamPatterns"
        where = ""

        if keyBeamPattern:
            where += f"keyBeamPattern = {keyBeamPattern}"
        else:
            where += f"fkCartTest = {fkParentTest} AND FreqCarrier = {freqCarrier}"
                
        q += " WHERE " + where + " ORDER BY keyBeamPattern ASC;"

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

            return [CombineTestsRecord(
                key = item.key,
                fkParentTest = fkParentTest,
                fkDutType = 0,
                timeStamp = item.timeStamp,
                path0_TestId = 0,
                path1 = str(item.FreqCarrier),
                path2 = str(item.key),
                description = item.getDescription(),    # pol copol
                text = f"{item.FreqCarrier}"            # frequency
            ) for item in items]
