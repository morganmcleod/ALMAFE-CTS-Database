from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BPError import BPErrorLevel, BPError, COLUMNS

class BPErrors():
    """
    Beam pattern errors table in dbBand6Cart
    """

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BPError) -> bool:
        """ Insert one record

        :param record to insert. record.key will be updated with the new keyBP_Errors
        :return keyBP_Errors: int or None if error.
        """
        q = f"INSERT INTO BP_Errors({','.join(COLUMNS[1:])}) VALUES ({record.getInsertVals()});"
        return self.DB.execute(q, commit = True)

    def read(self, fkBeamPattern:int) -> List[BPError]:
        """ Read all records associated with a given scan

        TODO: Selecting based on time range is probably more valuable.  This will miss errors where fkBeamPattern is 0.
        :param int fkBeamPattern: the scan
        :return List[BPError]
        """
        q = f"SELECT {','.join(COLUMNS)} FROM BP_Errors where fkBeamPatterns = {fkBeamPattern} ORDER BY {COLUMNS[0]} ASC;"
        
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BPError(
            key = row[0],
            fkBeamPattern = row[1],
            Level = BPErrorLevel(row[2]),
            Message = row[3],
            System = row[4],
            Model = row[5],
            Source = row[6],
            timeStamp = makeTimeStamp(row[7]),
            FreqSrc = row[8],
            FreqRcvr = row[9]
        ) for row in rows]
