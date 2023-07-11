from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BPRawDatum import BPRawDatum, COLUMNS

class BPRawData():
    '''
    BP_Data table in dbBand6Cart
    '''

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, records: List[BPRawDatum]) -> int:
        q = f"INSERT INTO BP_Data({','.join(COLUMNS[1:])}) VALUES "

        values = ""
        for rec in records:
            if values:
                values += ","
            values += "(" + ','.join((
                str(rec.fkBeamPattern),
                str(rec.Pol),
                str(rec.Position_X),
                str(rec.Position_Y),
                str(rec.SourceAngle),
                str(rec.Power),
                str(rec.Phase),
                "'" + datetime.now().strftime(self.DB.TIMESTAMP_FORMAT) + "'"
            )) + ")"
        q += values + ";"
        if self.DB.execute(q, commit = True):
            return len(records)
        else:
            return 0
        
    def read(self, fkBeamPattern: int) -> List[BPRawDatum]:
        q = f"SELECT {','.join(COLUMNS)} FROM BP_Data WHERE fkBeamPattern = {fkBeamPattern} ORDER BY keyBP_Data ASC;"

        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        
        return [BPRawDatum(
            key = row[0],
            fkBeamPattern = row[1],
            Pol = row[2],
            Position_X = row[3],
            Position_Y = row[4],
            SourceAngle = row[5],
            Power = row[6],
            Phase = row[7],
            TimeStamp = makeTimeStamp(row[8])
        ) for row in rows]
