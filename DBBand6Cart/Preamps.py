from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.Preamp import Preamp, COLUMNS
from datetime import datetime
from typing import List

class Preamps():

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyPreamps:int = None, lna:int = None, keyMxrPreampAssys:int = None) -> List[Preamp]:
        if keyPreamps is not None:
            q = f"SELECT {','.join(COLUMNS)} FROM Preamps WHERE keyPreamps={keyPreamps};"
            self.DB.execute(q)
            rows = self.DB.fetchall()
            if not rows:
                return []
            return [Preamp(
                key = row[0],
                timeStamp = makeTimeStamp(row[1]),
                serialNum = row[2] if row[2] else '',
                notes = row[3] if row[3] else '',
                coldDataBy = row[4] if row[4] else '',
                coldDataTS = makeTimeStamp(row[5]) if row[5] else None
            ) for row in rows]

        elif lna is not None and keyMxrPreampAssys is not None:
            q = f"SELECT PA.keyPreamps, PA.TS, PA.SN, PA.Notes, PA.ColdData_By, PA.TS_ColdData "
            q += "FROM Preamps AS PA, PreampPairs AS PP, MxrPreampAssys AS MPA "
            q += f"WHERE PA.keyPreamps = PP.fkPreamp{lna} AND PP.keyPreampPairs = MPA.fkPreampPair "
            q += f"AND MPA.keyMxrPreampAssys={keyMxrPreampAssys};"
            self.DB.execute(q)
            rows = self.DB.fetchall()
            if not rows:
                return []
            return [Preamp(
                key = row[0],
                timeStamp = makeTimeStamp(row[1]),
                serialNum = row[2] if row[2] else '',
                notes = row[3] if row[3] else '',
                coldDataBy = row[4] if row[4] else '',
                coldDataTS = makeTimeStamp(row[5]) if row[5] else None
            ) for row in rows]
            
        else:
            q = "SELECT MAX(keyPreamps), TS, SN FROM Preamps GROUP BY SN ORDER BY SN DESC;"
            self.DB.execute(q)
            rows = self.DB.fetchall()
            if not rows:
                return []
            return [Preamp(
                key = row[0],
                timeStamp = makeTimeStamp(row[1]),
                serialNum = row[2],
            ) for row in rows]

    def create(self, serialNum:str, coldDataBy:str = None, notes:str = None, copyFromId:int = None) -> int:
        rec = None
        if copyFromId is not None:
            rec = self.readPreamps(keyPreamps = copyFromId)
        rec = rec[0] if rec else Preamp()
        if serialNum:
            rec.serialNum = serialNum
        if notes:
            rec.notes = notes
        if coldDataBy:
            rec.coldDataBy = coldDataBy
            rec.coldDataTS = datetime.now()
        notes = f"'{rec.notes}'" if rec.notes else "NULL"
        coldDataBy = f"'{rec.coldDataBy}'" if rec.coldDataBy else "NULL"
        coldDataTS = f"'{rec.coldDataTS.strftime(self.DB.TIMESTAMP_FORMAT)}'" if rec.coldDataTS else "NULL"
        q = "INSERT INTO Preamps (SN, Notes, ColdData_By, TS_ColdData) VALUES "
        q += f"({rec.serialNum}, {notes}, {coldDataBy}, {coldDataTS});"
        self.DB.execute(q, commit = True)
        
        # get the value for keyPreamps:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return 0
        else:
            return row[0]
