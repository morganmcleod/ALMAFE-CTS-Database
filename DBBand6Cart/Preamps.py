""" Create, read records in DBBand6Cart.Preamps
"""
from ALMAFE.basic.ParseTimeStamp import makeTimeStamp
from ALMAFE.database.DriverMySQL import DriverMySQL
from .schemas.Preamp import Preamp, COLUMNS
from .GetLastInsertId import getLastInsertId
from datetime import datetime
from typing import List

class Preamps():
    """ Create, read records in DBBand6Cart.Preamps
    """
    def __init__(self, connectionInfo:dict = None, driver:DriverMySQL = None):
        """ Constructor
        :param connectionInfo: for initializing DriverMySQL if driver is not provided
        :param driver: initialized DriverMySQL to use or None
        """
        assert driver or connectionInfo
        self.DB = driver if driver else DriverMySQL(connectionInfo)

    def read(self, keyPreamps:int = None, lna:int = None, keyMxrPreampAssys:int = None) -> List[Preamp]:
        """ Read Preamps records

        :param int keyPreamps: ID of a single record to read, defaults to None
        :param int lna: optionally limit to preamp 0 or 1, defaults to None
        :param int keyMxrPreampAssys: Read preamps associated with a Mixer config, defaults to None
        :return List[Preamp]
        """
        if keyPreamps is not None:
            # read a single Preamp record:
            q = f"SELECT {','.join(COLUMNS)} FROM Preamps WHERE keyPreamps={keyPreamps} LIMIT 1;"
            self.DB.execute(q)
            row = self.DB.fetchone()
            if not row:
                return []
            return [Preamp(
                key = row[0],
                timeStamp = makeTimeStamp(row[1]),
                serialNum = row[2] if row[2] else '',
                notes = row[3] if row[3] else '',
                coldDataBy = row[4] if row[4] else '',
                coldDataTS = makeTimeStamp(row[5]) if row[5] else None
            )]

        elif lna is not None and keyMxrPreampAssys is not None:
            # read for a specific mixer config and LNA 1 or 2:
            q = f"SELECT PA.keyPreamps, PA.TS, PA.SN, PA.Notes, PA.ColdData_By, PA.TS_ColdData "
            q += "FROM Preamps AS PA, PreampPairs AS PP, MxrPreampAssys AS MPA "
            q += f"WHERE PA.keyPreamps = PP.fkPreamp{lna} AND PP.keyPreampPairs = MPA.fkPreampPair "
            q += f"AND MPA.keyMxrPreampAssys={keyMxrPreampAssys} LIMIT 1;"
            self.DB.execute(q)
            row = self.DB.fetchone()
            if not row:
                return []
            return [Preamp(
                key = row[0],
                timeStamp = makeTimeStamp(row[1]),
                serialNum = row[2] if row[2] else '',
                notes = row[3] if row[3] else '',
                coldDataBy = row[4] if row[4] else '',
                coldDataTS = makeTimeStamp(row[5]) if row[5] else None
            )]
            
        else:
            # read the most recent config for all preamps
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

    def create(self, preamp: Preamp, copyFromId:int = None) -> int:
        """ Create a Preamp record 

        :param Preamp preamp: record with fields to update
        :param int copyFromId: if provided, fields not in 'preamp' will be initialized from this ID, defaults to None
        :return int: new record keyPreamps
        """
        rec = Preamp()
        if copyFromId is not None:
            rec = self.readPreamps(keyPreamps = copyFromId)
            if rec:
                rec = rec[0]
        if preamp.serialNum:
            rec.serialNum = preamp.serialNum
        if preamp.notes:
            rec.notes = preamp.notes
        if preamp.coldDataBy:
            rec.coldDataBy = preamp.coldDataBy
        if preamp.coldDataTS:
            rec.coldDataTS = preamp.coldDataTS
        preamp = rec
        
        q = f"INSERT INTO Preamps (SN, Notes, ColdData_By, TS_ColdData) VALUES ({preamp.getInsertVals()})"
        self.DB.execute(q, commit = True)        
        preamp.key = getLastInsertId(self.DB)
        return preamp.key
