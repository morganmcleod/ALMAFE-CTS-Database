from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from pydantic import BaseModel
from datetime import datetime
from typing import List
from .schemas.BeamPattern import BeamPattern, COLUMNS

class BeamPatterns():
    '''
    BeamPatterns table in dbBand6Cart
    '''

    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        '''
        Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        '''
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def create(self, record: BeamPattern):
        values = "{},{},{},{},{},{},{},{},{},{},{}".format(
            record.fkCartTest,
            record.FreqLO,
            record.FreqCarrier,
            record.Beam_Center_X,
            record.Beam_Center_Y,
            record.Scan_Angle,
            record.Scan_Port,
            record.Lvl_Angle,
            record.AutoLevel,
            record.Resolution,
            record.SourcePosition
        )
        q = f"INSERT INTO BeamPatterns({','.join(COLUMNS[1:-1])}) VALUES ({values});"
        self.DB.execute(q, commit = True)

        # get the value for keyBeamPattern:
        q = "SELECT LAST_INSERT_ID()"
        self.DB.execute(q)
        row = self.DB.fetchone()
        if not row:
            return None
        else:
            record.key = row[0]
            return row[0]
        
    def read(self, keyId: int = None, fkCartTest: int = None) -> List[BeamPattern]:
        q = f"SELECT {','.join(COLUMNS)} FROM BeamPatterns"
        where = ""

        if keyId:
            where += f"keyBeamPattern = {keyId}"
        if fkCartTest:
            if where:
                where += " AND "
            where += f"fkCartTest = {fkCartTest}"

        if where:
            q += " " + where
        
        q += " ORDER BY keyBeamPattern ASC;"
    
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
            TimeStamp = makeTimeStamp(row[12])
        ) for row in rows]
