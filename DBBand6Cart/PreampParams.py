from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.PreampParam import PreampParam, COLUMNS
from datetime import datetime
from typing import List

class PreampParams():

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyPreamp:int, latestOnly:bool = True) -> List[PreampParam]:
        q = f"SELECT {','.join(COLUMNS)} FROM PreampParams WHERE fkPreamps = {keyPreamp} ORDER BY FreqLO ASC, TS DESC;"
        self.DB.execute(q)
        rows = self.DB.fetchall()
        if not rows:
            return []
        if latestOnly:
            keep = {}
            for row in rows:
                FreqLO = row[2]
                if FreqLO not in keep.keys():
                    keep[FreqLO] = row
            rows = [keep[FreqLO] for FreqLO in keep.keys()]            
        return [PreampParam(
            key = row[0],
            fkPreamps = row[1],
            FreqLO = row[2],
            timeStamp = makeTimeStamp(row[3]),
            VD1 = row[4] if row[4] else 0,
            VD2 = row[5] if row[5] else 0,
            VD3 = row[6] if row[6] else 0,
            ID1 = row[7] if row[7] else 0,
            ID2 = row[8] if row[8] else 0,
            ID3 = row[9] if row[9] else 0
        ) for row in rows]

    def create(self, fkPreamps:int, preampParams:List[PreampParam]) -> int:
        q = "INSERT INTO PreampParams (fkPreamps, FreqLO, VD1, VD2, VD3, ID1, ID2, ID3) VALUES "
        values = ""
        for row in preampParams:
            if row.FreqLO > 0:
                if values != "":
                    values += ","
                values += f"({row.fkPreamps}, {row.FreqLO}, {row.timeStamp.strftime(self.DB.TIMESTAMP_FORMAT)}, "
                values += f"{row.VD1}, {row.VD2}, {row.VD3}, {row.ID1}, {row.ID2}, {row.ID3})"
        
        if values == "":
            return 0
        
        q += values + ";"
        self.DB.execute(q, commit = True)
        
        # get the last value for keyPreampParams:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return 0
        else:
            return row[0]
