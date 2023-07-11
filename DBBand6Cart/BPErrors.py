from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BPError import BPErrorLevel, BPError, COLUMNS

class BPErrors():
    '''
    Beam pattern errors table in dbBand6Cart
    '''

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BPError) -> bool:
        values = "{},{},'{}','{}','{}','{}','{}','{}',{},{}".format(
            record.fkBeamPattern,
            record.Level.value,
            record.Message,
            record.TS_First,
            record.System,
            record.Model,
            record.Source,
            datetime.now(),
            record.FreqSrc,
            record.FreqRcvr            
        )
        q = f"INSERT INTO BP_Errors({','.join(COLUMNS[1:])}) VALUES ({values});"
        return self.DB.execute(q, commit = True)

    def read(self, fkBeamPattern:int) -> List[BPError]:
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
            TS_First = makeTimeStamp(row[4]),
            System = row[5],
            Model = row[6],
            Source = row[7],
            TS = makeTimeStamp(row[8]),
            FreqSrc = row[9],
            FreqRcvr = row[10]
        ) for row in rows]
